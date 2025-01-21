import gradio as gr
from gpt_generation.core.target_market_mapping_assistant import assistant_api_target_markets

def assistant_api_generator(input_text):
    target_markets = assistant_api_target_markets(input_text)
    output_str = ""
  
    for tm in target_markets:
        for key, val in tm.items():
            output_str += f"\n* Sentence (explicit): {key}"
            for tm_codes in val:
                tm_code = list(tm_codes.keys())[0]
                content = tm_codes[tm_code]
                output_str += f"\n\t- {tm_code}: \n\t\tSupport text: {content[0]}\n\t\tCorresponding definition: {content[1]}"
    return output_str



def gradio_demo():
    with gr.Blocks() as demo:
        with gr.Row():
            input_text = gr.Textbox(label='Input a description of a company.')
            btn = gr.Button("Generate")
        with gr.Row():
            with gr.Column(scale=1, min_width=600):
                target_markets = gr.Textbox(label="Description")
                

        btn.click(assistant_api_generator, inputs=[input_text], outputs=[target_markets])

    demo.launch(server_name = '192.168.61.11', server_port=7865)
    

if __name__ == "__main__":
    gradio_demo()