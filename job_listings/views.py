from django.shortcuts import render
from rest_framework import generics, status, viewsets
from .models import Job, Company
from .serializers import JobSerializer, CompanySerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .permissions import IsJobOwner, IsCompanyOwner


class JobList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Job.jobobjects.all()  # only published jobs
    serializer_class = JobSerializer

    def perform_create(self, serializer):
        company = self.request.user.company
        serializer.save(company_id=company.id)

    def create(self, request, *args, **kwargs):
        if not self.request.user.company:
            return Response({'error': 'No company found'}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)


class JobDetail(generics.RetrieveUpdateDestroyAPIView):

    def get_permissions(self):
        method = self.request.method
        if method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticatedOrReadOnly(), IsJobOwner()]
        else:
            return [IsAuthenticatedOrReadOnly()]

    queryset = Job.jobobjects.all()  # only published jobssearch only published jobs
    serializer_class = JobSerializer
    lookup_field = 'slug'


class CompanyList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CompanyDetail(generics.RetrieveUpdateDestroyAPIView):

    def get_permissions(self):
        method = self.request.method
        if method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticatedOrReadOnly(), IsCompanyOwner()]
        else:
            return [IsAuthenticatedOrReadOnly()]

    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    lookup_field = 'slug'
