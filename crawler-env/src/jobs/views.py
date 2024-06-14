# jobs/views.py

from django.shortcuts import render
from django.http import JsonResponse
from .models import Job
from .crawler import scrape_and_save_jobs
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .models import UserJobs
from .serializers import UserJobSerializer
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserUpdateSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer




@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
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
                jobs_count = len(jobs['Title'])
                # on itère sur les tuples et on assigne les valeurs à chaque variable
                for title, company, description, url in zip(jobs['Title'], jobs['Company'], jobs['Description'], jobs['Link']):
                    job = Job(title=title, company=company, description=description, url=url)
                    job.save()
                #cree le retour 
                jobs_list = []
                for i in range(jobs_count):
                    job_object = {
                        'Title': jobs['Title'][i],
                        'Company': jobs['Company'][i],
                        'Description': jobs['Description'][i],
                        'Link': jobs['Link'][i]
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
@api_view(['GET'])
@permission_classes([IsAuthenticated])
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

@csrf_exempt
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_favorite_user_jobs(request):
    user_jobs = UserJobs.objects.all()
    serializer = UserJobSerializer(user_jobs, many=True)
    return Response(serializer.data)

@csrf_exempt
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def favorite_user_job(request):
    serializer = UserJobSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@permission_classes([IsAuthenticated])
@api_view(['PUT'])
def update_user(request):
    try:
        user = request.user  
        serializer = UserUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    except Exception as e:
        return Response({'error': str(e)}, status=500)