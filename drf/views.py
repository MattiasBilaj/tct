from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
from rest_framework import viewsets

from core.models import Subject, StudySession
from .serializers import SubjectSerializer, StudySessionSerializer

from .pagination import StudySessionPagination

@api_view(["GET"])
def test2(request):
    return Response({"message":"test"})

@api_view(["GET", "POST"])
def all_subjects(request):
    if request.method == "GET":
        qs = Subject.objects.all()
        serializer = SubjectSerializer(qs, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
@api_view(["GET"])
def subject(request, numri):
        subject = Subject.objects.get(id=numri)
        serializer = SubjectSerializer(subject, many=False)
        return Response(serializer.data)

@api_view(["GET"])
def study_session(request, numri):
     study_session = StudySession.objects.get(id=numri)
     serializer = StudySessionSerializer(study_session)
     return Response(serializer.data)

@api_view(["GET"])
def study_session_list(request):
    if request.method == "GET":
        subject_id = request.GET.get("subject_id", None)
        # Do bejm check nese ekziston subject_id
        if subject_id:
            # Do kerkojm db per studySession me ate subject_id
            qs = StudySession.objects.filter(subject__id=subject_id)
            # Serialize the data
            serializer = StudySessionSerializer(qs, many=True)
            # return
            return Response(serializer.data)
        
        duration_minutes = request.GET.get("duration_minutes", None)
        if duration_minutes:
            qs = StudySession.objects.filter(duration_minutes__lte=duration_minutes)
            serializer = StudySessionSerializer(qs, many=True)
            return Response(serializer.data)
        # start_date, end_date do ta marresh si query parameter YYYY-MM-DD
        # do besh check nese ekzistojne
        # start = datetime.fromisoformat(start_date) 
        # end = datetime.fromisoformat(start_date) 
        # lte dhe gte per te gjetur range 
        # Do beni return qs

        # DSH Shtojini pagination
        # DSH 
        # Implementoni ordering (sipas dates) acending edhe descending
        ordering = request.GET.get("ordering", None)
        if ordering:
            if ordering.startswith("-"):
                try:
                    date_obj = datetime.fromisoformat(ordering[1:])
                except ValueError:
                    return Response({"error":"Invalid string"})
                qs = StudySession.objects.all().filter(datetime__lte=date_obj).order_by("-datetime")
                serializer = StudySessionSerializer(qs, many=True)
                return Response(serializer.data)
            else:
                try:
                    date_obj = datetime.fromisoformat(ordering)
                except ValueError:
                    return Response({"error":"Invalid string"})
                qs = StudySession.objects.all().filter(datetime__gte=date_obj).order_by("datetime")
                serializer = StudySessionSerializer(qs, many=True)
                return Response(serializer.data)
        # EXTRA:
        # Perpiquni ta beni me nje query parameter, maybe nje string=-YYYY-MM-DD
        # .startswith("-") string slicing


class SubjectViewSet(viewsets.ModelViewSet):
     queryset = Subject.objects.all()
     serializer_class = SubjectSerializer

     """
     GET drf/subjects/
     POST drf/subjects/

     GET drf/subjects/{id}/
     PUT drf/subjects/{id}/
     PATCH drf/subjects/{id}/
     DELETE drf/subjects/{id}/
     """