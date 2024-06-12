from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=200, null=True)
    company = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)
    url= models.TextField(null=True)

    def __str__(self):
        return self.title
