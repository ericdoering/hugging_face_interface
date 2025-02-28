import gradio
import requests
import io
from PIL import Image
from variables import API_KEY  

API_URL = "https://router.huggingface.co/hf-inference/v1"
headers = {"Authorization": f"{API_KEY}"} 