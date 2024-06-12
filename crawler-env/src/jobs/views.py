# jobs/views.py

from django.shortcuts import render
from django.http import JsonResponse
from .models import Job
from .crawler import scrape_and_save_jobs
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def crawl_jobs_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            ville = data.get("ville")
            jobtitre = data.get("jobtitre").replace(" ", "+")
            distance = data.get("distance")
            if ville and jobtitre and distance:
                # scrape_and_save_jobs(ville, jobtitre, distance)
                jobs = scrape_and_save_jobs(ville, jobtitre, distance)
                jobs_count = len(jobs['Titles'])
                # on itère sur les tuples et on assigne les valeurs à chaque variable
                for title, company, description, url in zip(jobs['Titles'], jobs['Companies'], jobs['Descriptions'], jobs['Links']):
                    job = Job(title=title, company=company, description=description, url=url)
                    job.save()
                #cree le retour 
                jobs_list = []
                for i in range(jobs_count):
                    job_object = {
                        'Job Title': jobs['Titles'][i],
                        'Job Company': jobs['Companies'][i],
                        'Job Description': jobs['Descriptions'][i],
                        'Job Link': jobs['Links'][i]
                    }
                    jobs_list.append(job_object)
                print("THE JSON", jobs_list)
                # safe= false pour retourner une liste sans erreur
                return JsonResponse( jobs_list,safe=False, status=200)
            else:
                return JsonResponse({'error': 'Invalid parameters'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
@csrf_exempt
def get_all_jobs(request):
    jobs = Job.objects.all()
    job_data = []
    for job in jobs:
        job_object = {
            'Title': job.title,
            'Company': job.company,
            'Description': job.description,
            'Link': job.url
        }
        job_data.append(job_object)
    
    return JsonResponse(job_data, safe=False, status=200)