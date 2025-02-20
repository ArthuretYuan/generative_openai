
import openai
from settings import OPENAI_API_KEY

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

    return resp



if __name__ == "__main__":

   
    prompt = "You are a resume analyser. You will receive a resume of a candidate and extract his/her skills, like 'python', 'mongodb', 'sql', 'azure', etc."
    user_input = "I’m a machine learning Engineer with almost 3 years working experience in a Fintech company. My main job is to deliver AI solutions to automate decision making and optimise service pipeline. I had experience on developing AI services with LLM (e.g., BERT, xmlroberta) and generative AI (e.g., GPT, Llama). I also specialise in full ML lifecycle, including data collection, data evaluation, model training, service deployment, and service maintenance. I also worked with multi-functional teams, like back/front-end, data engineer, and infrastructure engineer to guarantee the AI service can be smoothly delivered in Production."
    gpt_model = "gpt-4o" # ["gpt-3.5-turbo", "gpt-4", "gpt-4-1106-preview"]
    temperature = 0
    seed = 123

    res = generate_response_one_step(user_input, gpt_model, prompt, temperature, seed)

    print(res)