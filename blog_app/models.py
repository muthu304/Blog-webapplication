from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) :
        return self.name
class Post(models.Model):
    title = models.CharField(max_length=100)
    rating = models.CharField()
    content = models.TextField()
    img_url = models.ImageField(null=True, upload_to="posts/images")
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    is_published = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        
    
    @property
    def formatted_img_url(self):
        try:
            url = self.img_url if str(self.img_url).startswith(('http://', 'https://')) else self.img_url.url
        except ValueError:
            url = '/static/images/placeholder.png'  # Default image path
        return url
    
    def __str__(self):
        return self.title


class aboutus(models.Model):
    content = models.TextField()

    