from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Subject, StudySession
from datetime import datetime
import json

def index(request):
    """Serve the frontend HTML page"""
    return render(request, 'core/index.html')

def test_view(request):
    return JsonResponse({"message":"view is working."})

def subject_list(request):
    if request.method == "GET":
        subject_qs = Subject.objects.all().values("id", "name", "description")
        subjects = list(subject_qs)
        return JsonResponse(subjects, safe=False)
    return JsonResponse({"Error":"Method not allowed."})

@csrf_exempt
def subject(request, numri):
    if request.method == "GET":
        subject = Subject.objects.get(id=numri)

        subject_dict = {
            "id": subject.id,
            "name": subject.name,
            "description": subject.description
        }

        return JsonResponse(subject_dict, safe=False)
    if request.method == "POST":
        # Duhen marre te dhenat nga requesti
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        
        name = data.get("name")
        description = data.get("description", "")

        # Duhet krijuar objekti ne db
        subject = Subject.objects.create(name=name, description=description)

        # Dergo mesazh suksesi
        return JsonResponse({"message":"Subject was created succesfully"})
    
    if request.method == "PATCH":
        # Marrim te dhenat nga requesti (id, name, description)
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        
        name = data.get("name")
        description = data.get("description", "")
        # Duhet marr objekti nga db me id
        subject = Subject.objects.get(id=numri)
        # Duhet ndryshuar name dhe description
        if name:
            subject.name = name
        if description:
            subject.description = description
        # Duhet ber save objekti ne db
        subject.save()

        # return successful message, Old dhe new
        JsonResponse({"message":"Object Updated succesfully"})

        if request.method == "DELETE":
            subject = Subject.objects.get(id=numri)
            if subject:
                subject.delete()
                return JsonResponse({"message": "Deleted succesfully"})
            return JsonResponse({"Error": "Subject not found"})

    return JsonResponse({"Error":"Method not allowed."})

def study_session_list(request):
    if request.method == "GET":
        ss_qs = StudySession.objects.all().values("id", 
                                                  "subject",
                                                  "datetime",
                                                  "duration_minutes",
                                                  "notes")
        ss_list = []
        # Optimize
        for ss in ss_qs:
            subject = Subject.objects.get(id=ss.get("subject"))
            ss["subject"] = subject.name
            ss_list.append(ss)
        return JsonResponse(ss_list, safe=False)
    return JsonResponse({"Error":"Method not allowed."})


@csrf_exempt
def study_session(request, numri):
    if request.method == "GET":
        ss = StudySession.objects.get(id=numri)

        ss_dict = {
            "Id": ss.id,
            "Subject name": ss.subject.name,
            "Date time": ss.datetime,
            "Duration minutes": ss.duration_minutes,
            "Notes": ss.notes
        }

        return JsonResponse(ss_dict, safe=False)
    
    if request.method == "POST":
        # Duhen marre te dhenat nga requesti
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        
        subject = data.get("subject")
        datetime = data.get("datetime", datetime.now())
        duration_minutes = data.get("duration_minutes", 60)
        notes = data.get("notes", "")

        # Duhet krijuar objekti ne db
        ss = StudySession.objects.create(subject=subject, 
                                         datetime=datetime,
                                         duration_minutes=duration_minutes,
                                         notes=notes)

        # Dergo mesazh suksesi
        return JsonResponse({"message":"Study Session was created succesfully"})
    
    if request.method == "PATCH":
        # Marrim te dhenat nga requesti (id, name, description)
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        
        subject = data.get("subject", None)
        datetime = data.get("datetime", None)
        duration_minutes = data.get("duration_minutes", None)
        notes = data.get("notes", None)

        # Duhet marr objekti nga db me id
        ss = StudySession.objects.get(id=numri)
        # Duhet ndryshuar name dhe description
        if subject:
            ss.subject = subject
        if datetime:
            ss.datetime = datetime
        if duration_minutes:
            ss.duration_minutes = duration_minutes
        if notes:
            ss.notes = notes
        # Duhet ber save objekti ne db
        ss.save()

        # return successful message, Old dhe new
        JsonResponse({"message":"Object Updated succesfully"})

        if request.method == "DELETE":
            ss = StudySession.objects.get(id=numri)
            if ss:
                ss.delete()
                return JsonResponse({"message": "Deleted succesfully"})
            return JsonResponse({"Error": "Subject not found"})

    return JsonResponse({"Error":"Method not allowed."})