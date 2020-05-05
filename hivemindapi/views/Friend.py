from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.models import User
from hivemindapi.models import Applicant, Friend
from rest_framework.decorators import action
from .Cohort import CohortSerializer
from .Applicant import ApplicantSerializer

class FriendSerializer(serializers.HyperlinkedModelSerializer):
    """
    JSON serializer for applicant
    Arguments:
        serializers
    """

    # serializes the applicant and friend
    # applicant = ApplicantSerializer()
    # friend = ApplicantSerializer()

    class Meta:
        model = Friend
        url = serializers.HyperlinkedIdentityField(
            view_name='friend',
            lookup_field='id'
        )
        depth = 2
        fields = ('id', 'applicant', 'friend')


class Friends(ViewSet):
    '''
    
    This class houses functions for List, Retrieve, and Update for friend

   
    '''
    def retrieve(self, request, pk=None):
        """
        Handle GET requests for single friend relationship
        Returns:
            Response -- JSON serialized user instance

        To retrieve a applicant, make a GET request to:
        http://localhost:8000/friends/1

        NOTE: Replace the 1 with the ID of the friend relationship that corresponds with the relationship you want to retrieve.
        """
        try:
            friend = Friend.objects.get(pk=pk)
            serializer = ApplicantSerializer(
                friend, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """
        Handle GET requests to applicants resource
        Returns:
            Response -- JSON serialized list of applicants

        To search users by FIRST NAME ONLY, make a GET request to:
        http://localhost:8000/applicants?user_first=John

        NOTE: Replace John with the name of the user that you wish to retrieve.
        
        """
        friends = Friend.objects.all()

        # # filters for the authenticated user
        # applicant = self.request.query_params.get('applicant', False)
        # if applicant is not False:
        #     applicants = applicants.filter(id=request.auth.user.applicant.id)

        # # name filter
        # user_first = self.request.query_params.get('user_first', None)
        # user_last = self.request.query_params.get('user_last', None)
        # # filter users by first and last name
        # if user_first is not None and user_last is not None:
        #     applicants = applicants.filter(user__first_name__contains=user_first, user__last_name__contains=user_last)
        
        # # filtes for user by first name
        # if user_first is not None and user_last is None:
        #      applicants = applicants.filter(user__first_name__contains=user_first)

        # # filters for user by last name
        # if user_last is not None and user_first is None:
        #      applicants = applicants.filter(user__last_name__contains=user_last)

        serializer = FriendSerializer(
            friends, many=True, context={'request': request})

        return Response(serializer.data)