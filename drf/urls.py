from django.urls import path, include
from .views import (
<<<<<<< HEAD
    TotalTimeAllSubjectsAsync, 
    test2, 
    all_subjects, 
    subject, 
    study_session, 
    study_session_list,
    total_time_all_subjects,
    third_party_api,
=======
    test2, SubjectListAsync, subject, study_session, 
    study_session_list, TotalTimeAllSubjectsAsync, SubjectViewSet
>>>>>>> bfbf54085d23588c77527eb347b4d9ece4ecbdb5
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"subjects", SubjectViewSet, basename="subject")

urlpatterns = [
    path("test2/", test2),
    path("all-subjects/", SubjectListAsync.as_view(), name="all-subjects"),
    path("subject/<int:numri>", subject),
    path("study-session/<int:numri>", study_session, name="study-session"),
    path("study-session-list/", study_session_list),
    path("total-time-all-subjects/", TotalTimeAllSubjectsAsync.as_view(), name="total-time-all-subjects"),
    path("", include(router.urls)),
<<<<<<< HEAD
    path("total-time-all-subjects/",total_time_all_subjects, name="total-time-all-subjects"),
    path("total-time-all-subjects-async", TotalTimeAllSubjectsAsync.as_view(), name="total-time-all-subjects-async"),
    path("third-party-api/", third_party_api, name="third-party-api")
=======
>>>>>>> bfbf54085d23588c77527eb347b4d9ece4ecbdb5
]