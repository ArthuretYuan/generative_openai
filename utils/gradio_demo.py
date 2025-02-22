import json

import gradio as gr


def load_doc(doc_id, test_output_file):
    with open(test_output_file, "r") as f:
        docs = [line for line in f]
    doc = docs[int(doc_id)]
    doc = json.loads(doc)
    output_description = doc["descr"]
    # output_labels = doc["mapping"]
    # output_labels = json.dumps(doc["mapping"], indent=4)

    ro = doc["mapping"]["relevant organizations"]
    rp = doc["mapping"]["relevant products"]


    iro = doc["mapping"].get("irrelevant organizations")
    if iro is None:
        iro = doc["attribute"].get("irrelevant organizations")
        
    irp = doc["mapping"].get("irrelevant products")
    if irp is None:
        irp = doc["attribute"].get("irrelevant products")
        
    
    output_labels = "- relevant organizations: \n"
    if not ro:
        output_labels += '\tN/A\n'
    else:
        for dict_ro in ro:
            for k, v, in dict_ro.items():
                output_labels += f'\t{k}\n\t\t{v[0]}: {v[1]}\n'
    
    output_labels = output_labels + "- relevant products: \n"
    if not rp:
        output_labels += '\tN/A\n'
    else:
        for dict_rp in rp:
            for k, v, in dict_rp.items():
                output_labels += f'\t{k}\n\t\t{v[0]}: {v[1]}\n'
        
        
    output_labels =  output_labels + "- irrelevant organizations: \n"
    if not iro:
        output_labels = output_labels + '\tN/A\n'
    else:
        for iro_item in iro:
            output_labels = output_labels + '\t' + str(iro_item) + '\n'
    
    output_labels =  output_labels + "- irrelevant products: \n"
    if not irp:
        output_labels = output_labels + '\tN/A\n'
    else:
        for irp_item in irp:
            output_labels = output_labels + '\t' + str(irp_item) + '\n'
        
    return output_description, output_labels


def result_display(doc_id):
    test_output_file_1 = './gpt_generation/target_market/results/test_output_two_step_3level_30012024_T1215.jl'
    test_output_file_2 = './gpt_generation/target_market/results/test_output_two_step_3level_context_30012024_T1600.jl'

    output_description, output_labels_1 = load_doc(doc_id, test_output_file_1)
    _, output_labels_2 = load_doc(doc_id, test_output_file_2)

    return output_description, output_labels_1, output_labels_2

def gradio_demo():
    with gr.Blocks() as demo:
        with gr.Row():
            input_doc_id = gr.Textbox(label='Input a doc ID')
            btn = gr.Button("Generate")
        with gr.Row():
            with gr.Column(scale=1, min_width=600):
                output_desc = gr.Textbox(label="Description")
        with gr.Row():
            with gr.Column(scale=1, min_width=600):
                output_1 = gr.Textbox(label="Output_1")
            with gr.Column(scale=1, min_width=600):
                output_2 = gr.Textbox(label="Output_2")

        btn.click(result_display, inputs=[input_doc_id], outputs=[output_desc, output_1, output_2])

    demo.launch(server_name = '192.168.61.11', server_port=7863)

if __name__ == '__main__':
    #gradio_demo()
    test_output_file_2 = './gpt_generation/target_market/results/test_output_two_step_3level_context_30012024_T1600.jl'
    with open('FCCS_target_market_samples_evaluation.txt', 'a') as f:
        for doc_id in range(200):
            f.write(f'***************************** doc_id: {doc_id+1} *****************************\n\n')
            descr, output_labels_2 = load_doc(doc_id, test_output_file_2)
            f.write(f'*** description ***:\n{descr}\n\n')
            f.write(f'*** reference generated by GPT4 ***:\n{output_labels_2}\n\n')

