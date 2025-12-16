from core.views import (
    index, 
    test_view, 
    subject_list, 
    subject, 
    study_session_list, 
    study_session
)

from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('', index, name='index'),  # Frontend home page
    path('admin/', admin.site.urls),
    path('test/', test_view),
    path('subject-list/', subject_list),
    path('subject/<int:numri>/', subject),
    path('study-session-list/', study_session_list),
    path('study-session/<int:numri>/', study_session),
]
