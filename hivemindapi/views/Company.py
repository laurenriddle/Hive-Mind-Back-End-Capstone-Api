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
    
    This class houses functions for List, Retrieve, Destroy, and Create for industries

   
    '''

    def retrieve(self, request, pk=None):
        '''
        Handles GET requests for a single Interview 
        Returns:
            Response --- JSON serialized Interviews instance
        To access a single industry: 
        http://localhost:8000/industries/1

        NOTE: Replace the 1 with any ID you wish to retrieve 
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

        To access all industries: 
        http://localhost:8000/industries
        '''
        user = request.auth.user.applicant.id

        # list interview
        companies = Companies.objects.all()

        # take repsonse and covert to JSON
        serializer = IndustrySerializer(companies, many=True, context={'request': request})

        # return repsonse as JSON
        return Response(serializer.data)
