import gradio as gr
import sys
import cv2

from scripts.td_abg import get_foreground
from scripts.convertor import pil2cv




class webui:
    def __init__(self):
        self.demo = gr.Blocks()

    def processing(self, input_image, td_abg_enabled, h_split, v_split, n_cluster, alpha, th_rate, cascadePSP_enabled, fast, psp_L):
        image = pil2cv(input_image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mask, image = get_foreground(image, td_abg_enabled, h_split, v_split, n_cluster, alpha, th_rate, cascadePSP_enabled, fast, psp_L)
        return image, mask

    def launch(self, share):
        with self.demo:
            with gr.Row():
                with gr.Column():
                    input_image = gr.Image(type="pil")
                    with gr.Accordion("tile division ABG", open=True):
                        with gr.Box():
                            td_abg_enabled = gr.Checkbox(label="enabled", show_label=True)
                            h_split = gr.Slider(1, 2048, value=256, step=4, label="horizontal split num", show_label=True)
                            v_split = gr.Slider(1, 2048, value=256, step=4, label="vertical split num", show_label=True)

                            n_cluster = gr.Slider(1, 1000, value=500, step=10, label="cluster num", show_label=True)
                            alpha = gr.Slider(1, 255, value=100, step=1, label="alpha threshold", show_label=True)
                            th_rate = gr.Slider(0, 1, value=0.1, step=0.01, label="mask content ratio", show_label=True)

                    with gr.Accordion("cascadePSP", open=True):
                        with gr.Box():
                            cascadePSP_enabled = gr.Checkbox(label="enabled", show_label=True)
                            fast = gr.Checkbox(label="fast", show_label=True)
                            psp_L = gr.Slider(1, 2048, value=900, step=1, label="Memory usage", show_label=True)

                    submit = gr.Button(value="Submit")
                with gr.Row():
                    with gr.Column():
                        with gr.Tab("output"):
                            output_img = gr.Image()
                        with gr.Tab("mask"):
                            output_mask = gr.Image()
            submit.click(
                self.processing,
                inputs=[input_image, td_abg_enabled, h_split, v_split, n_cluster, alpha, th_rate, cascadePSP_enabled, fast, psp_L],
                outputs=[output_img, output_mask]
            )

        self.demo.queue()
        self.demo.launch(share=share)


if __name__ == "__main__":
    ui = webui()
    if len(sys.argv) > 1:
        if sys.argv[1] == "share":
            ui.launch(share=True)
        else:
            ui.launch(share=False)
    else:
        ui.launch(share=False)
