from django.db import models
from django.contrib.auth.models import User
from .validators import validate_file_size
from PIL import Image

# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='content/images/', validators=[validate_file_size])
    caption = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    title = models.CharField(max_length=100)
    

    def __str__(self):
        return f"{self.title} - {self.created_at}"


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        
        img = Image.open(self.image.path)

        
        max_size = (300, 300)  
        img.thumbnail(max_size)

       
        img.save(self.image.path)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


