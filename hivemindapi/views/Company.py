from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from hivemindapi.models import Company
from .Industry import IndustrySerializer


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    '''
    JSON serializer for interviews
    Arguments: serializers.HyperlinkedModelSerializer
    Author: Lauren Riddle
    '''
    industry = IndustrySerializer()

    class Meta:
        model = Company
        url = serializers.HyperlinkedIdentityField(
            view_name='company',
            lookup_field='id'
        )
        fields = ('id', 'name', 'city', 'industry')
        depth = 2

class Companies(ViewSet):
    '''
    
    This class houses functions for List, Create, and Retrieve companies

   
    '''

    def retrieve(self, request, pk=None):
        '''
        Handles GET requests for a single Interview 
        Returns:
            Response --- JSON serialized Interviews instance
        To access a single company: 
        http://localhost:8000/companies/1

        NOTE: Replace the 1 with any company ID you wish to retrieve 
        '''
        try:
            company = Company.objects.get(pk=pk)
            serializer = CompanySerializer(company, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    

    def list(self, request):
        '''
        Handles the GET all requstes to the interview resource
        Returns: 
        Response -- JSON serialized list of interview

        To access all companies: 
        http://localhost:8000/companies

        To access companies by NAME:
        http://localhost:8000/companies?name=atiba

        NOTE: Replace atiba with any company name that you would like to find

        '''
        user = request.auth.user.applicant.id

        # list interview
        companies = Company.objects.all()
         # filter by applicant ID
        name = self.request.query_params.get('name', None)
        if name is not None:
            companies = companies.filter(name__contains=name)

        # take repsonse and covert to JSON
        serializer = CompanySerializer(companies, many=True, context={'request': request})

        # return repsonse as JSON
        return Response(serializer.data)
