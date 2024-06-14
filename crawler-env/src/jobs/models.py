from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=255, unique=False)
    company = models.CharField(max_length=255, unique=False)
    description = models.TextField()
    url = models.URLField(unique=False)


class UserJobs(models.Model):
    id_user = models.IntegerField()
    job_title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    link = models.URLField()
 
    def __str__(self):
        return self.job_title
    
    def __str__(self):
        return self.title

class UserJobs(models.Model):
    id_user = models.IntegerField()
    job_title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    link = models.URLField()

    def __str__(self):
        return self.job_title