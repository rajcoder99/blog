from django.db import models

# Create your models here.

class Blog_post(models.Model):
    title = models.CharField(max_length=150)
    desc = models.TextField()

