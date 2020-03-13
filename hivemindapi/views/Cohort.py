from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from hivemindapi.models import Cohort



class CohortSerializer(serializers.HyperlinkedModelSerializer):
    '''
    JSON serializer for cohorts
    Arguments: serializers.HyperlinkedModelSerializer
    Author: Lauren Riddle
    '''

    class Meta:
        model = Cohort
        url = serializers.HyperlinkedIdentityField(
            view_name='cohort',
            lookup_field='id'
        )
        fields = ('id', 'cohort')
        depth = 2

class Cohorts(ViewSet):
    '''
    
    This class houses functions for List and Retrieve for cohorts

   
    '''

    def retrieve(self, request, pk=None):
        '''
        Handles GET requests for a single cohort 
        Returns:
            Response --- JSON serialized cohort instance

        To access a single cohort: 
        http://localhost:8000/cohorts/1

        NOTE: Replace the 1 with any ID you wish to retrieve 
        '''
        try:
            cohort = Cohort.objects.get(pk=pk)
            serializer = CohortSerializer(cohort, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    

    def list(self, request):
        '''
        Handles the GET all requstes to the cohort resource
        Returns: 
        Response -- JSON serialized list of cohort

        To access all cohorts: 
        http://localhost:8000/cohorts
        '''

        # list cohort
        cohorts = Cohort.objects.all()

        # take repsonse and covert to JSON
        serializer = CohortSerializer(cohorts, many=True, context={'request': request})

        # return repsonse as JSON
        return Response(serializer.data)