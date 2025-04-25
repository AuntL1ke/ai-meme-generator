from django.db import models

class Meme(models.Model):
    prompt = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    image_base64 = models.TextField()
    
    def __str__(self):
        return f"Meme {self.id} - {self.prompt[:20]}..."