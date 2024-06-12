# jobs/views.py

from django.shortcuts import render
from django.http import JsonResponse
from .models import Job
from .crawler import scrape_and_save_jobs
import json
# def job_list(request):
#     sector = request.GET.get('sector', '')
#     location = request.GET.get('location', '')
#     title = request.GET.get('title', '')

#     # Filtrer les jobs en fonction des critères de recherche
#     jobs = Job.objects.all()
#     if sector:
#         jobs = jobs.filter(sector__icontains=sector)
#     if location:
#         jobs = jobs.filter(location__icontains=location)
#     if title:
#         jobs = jobs.filter(title__icontains=title)

#     return render(request, 'job_list.html', {'jobs': jobs})


def crawl_jobs_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            ville = data.get('ville')
            jobtitre = data.get('jobtitre').replace(" ", "+")
            distance = data.get('distance')
            if ville and jobtitre and distance:
                jobs = scrape_and_save_jobs(ville, jobtitre, distance)
                return JsonResponse({'jobs': jobs}, status=200)
            else:
                return JsonResponse({'error': 'Invalid parameters'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


def trigger_crawler(request):
    # Appeler la fonction de scraping et sauvegarder les jobs
    scrape_and_save_jobs()
    return JsonResponse({'status': 'Crawler triggered successfully'})
