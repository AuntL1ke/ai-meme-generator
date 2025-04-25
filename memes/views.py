import requests
from django.shortcuts import render
import base64
import os


HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

def index(request):
    image_data = None
    prompt = None

    if request.method == 'POST':
        prompt = request.POST.get('prompt', '')
        if prompt:
            api_url = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"
            headers = {
                "Authorization": f"Bearer {HUGGINGFACE_TOKEN}",  
                "Content-Type": "application/json"
            }
            payload = {"inputs": prompt}
            response = requests.post(api_url, headers=headers, json=payload)

            if response.status_code == 200:
                
                encoded = base64.b64encode(response.content).decode('utf-8')
                image_data = encoded

    return render(request, 'memes/index.html', {'image_data': image_data, 'prompt': prompt})
