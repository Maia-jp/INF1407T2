import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ProgLang(models.Model):
    name = models.CharField(primary_key=True, max_length=24)
    # helloWorld = models.CharField(max_length=1024)

class Snippet(models.Model):
    #Meta
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    #Actual Data 
    code = models.CharField(max_length=1024)
    title = models.CharField(max_length=36)
    lang = models.ForeignKey(ProgLang, on_delete=models.CASCADE)    