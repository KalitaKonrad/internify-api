from django.shortcuts import render
from rest_framework import generics
from .models import Job
from .serializers import JobSerializer


class JobList(generics.ListCreateAPIView):
    queryset = Job.jobobjects.all()  # only published jobs
    serializer_class = JobSerializer


class JobDetail(generics.RetrieveDestroyAPIView):
    queryset = Job.jobobjects.all()  # only published jobssearch only published jobs
    serializer_class = JobSerializer
