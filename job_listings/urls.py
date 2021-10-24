from django.urls import path, include
from .views import JobList, JobDetail

# app_name = 'jobs'

urlpatterns = [
    path('<int:pk>/', JobDetail.as_view(), name='detailcreate'),
    path('', JobList.as_view(), name='listcreate'),
]
