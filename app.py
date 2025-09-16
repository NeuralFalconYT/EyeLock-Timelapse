import gradio as gr
import os
import shutil

from eye_lock import process_images_fixed_eyes, create_timelapse

def get_images_from_gradio(gradio_input):
    files = []
    if isinstance(gradio_input, list):
        for f in gradio_input:
            if f.lower().endswith((".jpg", ".jpeg", ".png")):
                files.append(f)
    return files


def gradio_timelapse(images_input,image_duraion=0.1):
    if not images_input:
        return None

    aligned_folder = "./aligned_fixed_eyes"
    output_folder = "./download"

    # Clean workspace
    if os.path.exists(aligned_folder):
        shutil.rmtree(aligned_folder)
    os.makedirs(aligned_folder, exist_ok=True)

    files = get_images_from_gradio(images_input)
    if not files:
        return None

    process_images_fixed_eyes(files, aligned_folder, canvas_size=1024)
    # for f in files:
    #     try:
    #         os.remove(f)
    #     except Exception as e:
    #         pass
    output_video = create_timelapse(aligned_folder, output_folder,fps_in=image_duraion*100)
    return output_video
def ui():
    custom_css = """.gradio-container { font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif; }"""
    with gr.Blocks(theme=gr.themes.Soft(),css=custom_css) as demo:
        gr.HTML("""
            <div style="text-align: center; margin: 20px auto; max-width: 800px;">
                <h1 style="font-size: 2.5em; margin-bottom: 5px;">👁️ EyeLock Timelapse Generator</h1>
            </div>""")
        with gr.Row():  
            with gr.Column():  
                images_input = gr.File(
                    type="filepath",
                    file_count="multiple",
                    label="Upload Multiple Images (.jpg, .jpeg, .png only)"
                )
                image_duration = gr.Slider(label="Image Duration (seconds)", minimum=0.01, maximum=1.0, value=0.1, step=0.01, info="Duration each image is shown in the timelapse")
                generate_btn = gr.Button("🚀 Generate Timelapse")

            with gr.Column(): 
                output_video = gr.Video(label="Final Timelapse")
        gr.Markdown("### Instructions:")
        gr.Markdown("1. Upload multiple images of the same person’s face, such as selfies.")
        gr.Markdown("2. Click 'Generate Timelapse'.")
        gr.Markdown("3. Download the resulting video.")
        gr.Markdown("4. Open any editing app and crop the video according to your use case.")
        generate_btn.click(
            fn=gradio_timelapse,
            inputs=[images_input,image_duration],
            outputs=output_video
        )

    return demo


import click
@click.command()
@click.option("--share", is_flag=True, default=False, help="Enable sharing of the interface.")
@click.option("--debug", is_flag=True, default=False, help="Enable debug mode.")
def main(share,debug): 
    demo = ui()
    print("🚀 Launching Gradio Demo...")
    demo.queue().launch(debug=debug, share=share)

if __name__ == "__main__":
    main()