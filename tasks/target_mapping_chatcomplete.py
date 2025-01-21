import json
import time
import jsonlines
import openai
from utils.process_response import process_gpt_response
from settings import OPENAI_API_KEY
from utils.build_prompt import build_prompt

openai.api_key = OPENAI_API_KEY


def query_gpt(user_input, gpt_model, prompt, temperature, seed):
    response = openai.chat.completions.create(
        model=gpt_model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_input}],
        temperature=temperature,
        seed=seed)
    resp = response.choices[0].message.content

    return resp

def generate_response_one_step(user_input, gpt_model, prompt, temperature, seed):
    resp = query_gpt(user_input=user_input,
                     gpt_model=gpt_model,
                     prompt=prompt,
                     temperature=temperature,
                     seed=seed)
    mapping_res = process_gpt_response(resp)
    new_dict = {"descr": descr, "mapping": mapping_res}
    print('\n---------------')
    print('Description:')
    print(descr, '\n')
    print('Response:')
    print(resp)

    return new_dict


def generate_response_two_step(user_input, gpt_model, prompt_1, prompt_2, temperature, seed):
    resp_1 = query_gpt(user_input=user_input,
                     gpt_model=gpt_model,
                     prompt=prompt_1,
                     temperature=temperature,
                     seed=seed)
    print('\n---------------')
    print('Description:')
    print(descr, '\n')
    print('Response_1:')
    print(resp_1, '\n')

    mapping_res_1 = process_gpt_response(resp_1)
    #input_attributes = {"relevant organizations" : mapping_res_1["relevant organizations"],
    #                    "relevant products" : mapping_res_1["relevant products"]}
    input_attributes = {"description": user_input,
                        "relevant organizations" : mapping_res_1["relevant organizations"],
                        "relevant products" : mapping_res_1["relevant products"]}
    user_input_2 = str(input_attributes)
    resp = query_gpt(user_input=user_input_2,
                     gpt_model=gpt_model,
                     prompt=prompt_2,
                     temperature=temperature,
                     seed=seed)
    print('Response_2:')
    print(resp)

    mapping_res_2 = process_gpt_response(resp)
    new_dict = {"descr": descr, "attribute": mapping_res_1, "mapping": mapping_res_2}
    return new_dict

if __name__ == "__main__":

    input_file = './data/input.jsonl'
    output_file = './data/output.jsonl'
    prompt_version = {
        "mode": "two_step_mode",
        "mapping_level":"L3",
        "step_one_version":"V1",
        "step_two_version":"V3"}
    
    mode = prompt_version['mode']
    prompt_1, prompt_2 = build_prompt(prompt_version)

    line_id = 0
    docs_limit = 2
    with open(input_file, 'r') as fr:
        with open(output_file, 'a') as fw: 
            for line in fr:
                line_id += 1
                if line_id >= docs_limit:
                    continue
                print(f'\n### No. {line_id} ###')
                line_dict = json.loads(line)
                descr = line_dict["text"]
                org_id = line_dict["org_id"]
                tm_tag = line_dict["target_market"]
                
                user_input = '"""' + descr + '"""'
                gpt_model = "gpt-4o" # ["gpt-3.5-turbo", "gpt-4", "gpt-4-1106-preview"]
                temperature = 0
                seed = 123

                try:
                    if mode == "one_step_mode":
                        new_dict = generate_response_one_step(user_input, gpt_model, prompt_1, temperature, seed)
                    elif mode == "two_step_mode":
                        new_dict = generate_response_two_step(user_input, gpt_model, prompt_1, prompt_2, temperature, seed)

                except Exception as e:
                    print(line_id, ': ', e)
                    new_dict = {"descr":descr, "attribute": {}, "mapping":{}}
                
                json.dump({"org_id": org_id, "gpt4_info": new_dict}, fw)
                fw.write('\n')