from django.urls import path, include
from .views import JobList, JobDetail, CompanyDetail, CompanyList

# app_name = 'jobs'

urlpatterns = [
    path('jobs/<slug:slug>/', JobDetail.as_view(), name='job_detail'),
    path('jobs/', JobList.as_view(), name='job_list'),
    path('companies/<slug:slug>/', CompanyDetail.as_view(), name='company_detail'),
    path('companies/', CompanyList.as_view(), name='company_list')
]
