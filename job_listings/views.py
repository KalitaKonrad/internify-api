from django.shortcuts import render
from rest_framework import generics
from .models import Job, Company
from .serializers import JobSerializer, CompanySerializer
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly


class JobList(generics.ListCreateAPIView):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    queryset = Job.jobobjects.all()  # only published jobs
    serializer_class = JobSerializer


class JobDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    queryset = Job.jobobjects.all()  # only published jobssearch only published jobs
    serializer_class = JobSerializer


class CompanyList(generics.ListCreateAPIView):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class CompanyDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
