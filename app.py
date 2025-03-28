import gradio as gr
import requests
import io
from PIL import Image, ImageEnhance
from variables import API_KEY  

API_URL = "https://api-inference.huggingface.co/models/sd-community/sdxl-flash"

headers = { "Authorization": f"Bearer {API_KEY}" } 

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}, Response: {response.text}")
        return None 
    
    try:
        if "image" not in response.headers["Content-Type"]:
            print("API did not return an image. Response:", response.text)
            return None
        
        return response.content
    except Exception as e:
        print("Error processing response:", e)
        return None

def generate_image(prompt, brightness, contrast):
    image_bytes = query({ "inputs": prompt })
    image = Image.open(io.BytesIO(image_bytes))

    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(brightness)
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(contrast)

    return image

demo = gr.Interface(
    fn=generate_image,
    inputs=["text", gr.Slider(0.5, 2.0, 1.0), gr.Slider(0.5, 2.0, 1.0)],
    outputs="image",
    live=True
)

demo.launch(share=True)