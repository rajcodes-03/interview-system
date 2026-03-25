from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.start_interview, name='start_interview'),
    path('session/<int:session_id>/q/<int:q_order>/', views.interview_question, name='interview_question'),
    path('session/<int:session_id>/results/', views.interview_results, name='interview_results'),
]