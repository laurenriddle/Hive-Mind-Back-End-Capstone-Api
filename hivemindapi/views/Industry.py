from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from hivemindapi.models import Industry



class IndustrySerializer(serializers.HyperlinkedModelSerializer):
    '''
    JSON serializer for interviews
    Arguments: serializers.HyperlinkedModelSerializer
    Author: Lauren Riddle
    '''

    class Meta:
        model = Industry
        url = serializers.HyperlinkedIdentityField(
            view_name='industry',
            lookup_field='id'
        )
        fields = ('id', 'industry')
        depth = 2

class Industries(ViewSet):
    '''
    
    This class houses functions for List and Retrieve for industries

   
    '''

    def retrieve(self, request, pk=None):
        '''
        Handles GET requests for a single industry 
        Returns:
            Response --- JSON serialized industry instance

        To access a single industry: 
        http://localhost:8000/industries/1

        NOTE: Replace the 1 with any ID you wish to retrieve 
        '''
        try:
            industry = Industry.objects.get(pk=pk)
            serializer = IndustrySerializer(industry, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    

    def list(self, request):
        '''
        Handles the GET all requstes to the industry resource
        Returns: 
        Response -- JSON serialized list of industry

        To access all industries: 
        http://localhost:8000/industries
        '''

        # list industry
        industries = Industry.objects.all()

        # take repsonse and covert to JSON
        serializer = IndustrySerializer(industries, many=True, context={'request': request})

        # return repsonse as JSON
        return Response(serializer.data)
