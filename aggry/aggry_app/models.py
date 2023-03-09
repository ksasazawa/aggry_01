from django.db import models

class Jobs(models.Model):
    title = models.CharField(max_length=255)
    job = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    mod_location = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    detail = models.TextField()
    agent = models.CharField(max_length=255)
    url = models.URLField(blank=True, null=True)
    label1 = models.IntegerField(blank=True, null=True)
    label2 = models.IntegerField(blank=True, null=True)
    data_added = models.DateTimeField(auto_now_add=True)
    
