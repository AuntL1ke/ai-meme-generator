import requests
from django.shortcuts import render
import base64
import os
from dotenv import load_dotenv
from .models import Meme

from django.core.paginator import Paginator

def history(request):
    memes_list = Meme.objects.all().order_by('-created_at')
    paginator = Paginator(memes_list, 5)  

    page_number = request.GET.get('page')
    memes = paginator.get_page(page_number)

    return render(request, 'memes/history.html', {'memes': memes})

load_dotenv()
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

def index(request):
    image_data = None
    prompt = None
    error_message = None

    if request.method == 'POST':
        prompt = request.POST.get('prompt', '')
        if prompt:
            api_url = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"
            headers = {
                "Authorization": f"Bearer {HUGGINGFACE_TOKEN}",
                "Content-Type": "application/json"
            }
            payload = {"inputs": prompt}

            try:
                response = requests.post(api_url, headers=headers, json=payload, timeout=60)

                if response.status_code == 200:
                    encoded = base64.b64encode(response.content).decode('utf-8')
                    image_data = encoded

                    
                    Meme.objects.create(prompt=prompt, image_base64=encoded)

                else:
                    error_message = f"Generation error (status code {response.status_code}). Please try again."

            except requests.exceptions.Timeout:
                error_message = "Request timed out. Please try again later."
            except Exception as e:
                error_message = f"An error occurred: {str(e)}"

    return render(request, 'memes/index.html', {
        'image_data': image_data,
        'prompt': prompt,
        'error_message': error_message
    })


