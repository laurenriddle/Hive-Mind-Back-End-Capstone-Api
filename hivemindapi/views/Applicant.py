from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.models import User
from hivemindapi.models import Applicant
from rest_framework.decorators import action
from .Cohort import CohortSerializer


class UsersSerializer(serializers.HyperlinkedModelSerializer):
    """
    JSON serializer for users.
    This allows us to embed the user information into applicant.

    Arguments:
        serializers
    """
    class Meta:
        model = User
        url = serializers.HyperlinkedIdentityField(
            view_name='user',
            lookup_field='id'
        )
        fields = ('id', 'url', 'username', 'last_name', 'first_name', 'email')


class ApplicantSerializer(serializers.HyperlinkedModelSerializer):
    """
    JSON serializer for applicant
    Arguments:
        serializers
    """

    # serializes the user
    user = UsersSerializer()
    cohort = CohortSerializer()

    class Meta:
        model = Applicant
        url = serializers.HyperlinkedIdentityField(
            view_name='applicant',
            lookup_field='id'
        )
        depth = 2
        fields = ('id', 'linkedin_profile', 'user', 'cohort', 'is_employed', 'employer', 'image', 'aboutme', 'jobtitle', 'location')


class Users(ViewSet):
    '''
    
    This class houses functions to retrieve a user
   
    '''
    def retrieve(self, request, pk=None):
        """Handle GET requests for single user
        Returns:
            Response -- JSON serialized user instance
        To retrieve a user, make a GET request to:
        http://localhost:8000/applicants 
        or you can also make a GET request to 
        http://localhost:8000/applicants/1

        NOTE: Replace the 1 with the ID of the APPLICANT that corresponds with the user you want to retrieve.
        """
        try:
            user = User.objects.get(pk=pk)
            serializer = UsersSerializer(user, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


class Applicants(ViewSet):
    '''
    
    This class houses functions for List, Retrieve, and Update for applicants

   
    '''
    def retrieve(self, request, pk=None):
        """
        Handle GET requests for single user
        Returns:
            Response -- JSON serialized user instance

        To retrieve a applicant, make a GET request to:
        http://localhost:8000/applicants/1

        NOTE: Replace the 1 with the ID of the applicant that corresponds with the user you want to retrieve.
        """
        try:
            applicant = Applicant.objects.get(pk=pk)
            serializer = ApplicantSerializer(
                applicant, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """
        Handle GET requests to applicants resource
        Returns:
            Response -- JSON serialized list of applicants

        To retrieve all users, make a GET request to:
        http://localhost:8000/applicants 

        To retrieve the LOGGED IN USER, make a get request to:
        http://localhost:8000/applicants?applicant=True


        To search users by FIRST NAME ONLY, make a GET request to:
        http://localhost:8000/applicants?user_first=John

        NOTE: Replace John with the name of the user that you wish to retrieve.

        To search users by LAST NAME ONLY, make a GET request to:
        http://localhost:8000/applicants?user_last=Doe
        
        NOTE: Replace Doe with the name of the user that you wish to retrieve.

        To search users by FIRST AND LAST NAME, make a GET request to:
        http://localhost:8000/applicants?user_first=John&&user_last=Doe
        
        NOTE: Replace John and Doe with the name of the user that you wish to retrieve.

        
        """
        applicants = Applicant.objects.all()

        # filters for the authenticated user
        applicant = self.request.query_params.get('applicant', False)
        if applicant is not False:
            applicants = applicants.filter(id=request.auth.user.applicant.id)

        # name filter
        user_first = self.request.query_params.get('user_first', None)
        user_last = self.request.query_params.get('user_last', None)
        # filter users by first and last name
        if user_first is not None and user_last is not None:
            applicants = applicants.filter(user__first_name__contains=user_first, user__last_name__contains=user_last)
        
        # filters for user by first name
        if user_first is not None and user_last is None:
             applicants = applicants.filter(user__first_name__contains=user_first)

        # filters for user by last name
        if user_last is not None and user_first is None:
             applicants = applicants.filter(user__last_name__contains=user_last)

        serializer = ApplicantSerializer(
            applicants, many=True, context={'request': request})

        return Response(serializer.data)

    #Custom action to update user profile
    @action(methods=['put'], detail=False, url_name='profile_update')
    def profile_update(self, request):
        """
        Handle PUT requests for an applicant
        Returns:
            Response -- Empty body with 204 status code
            
        To update a user, make a PUT request to:
        http://localhost:8000/applicants/profile_update
        
        """
        

        applicant = Applicant.objects.get(pk=request.auth.user.applicant.id)
        applicant.linkedin_profile = request.data["linkedin_profile"]
        applicant.cohort_id = request.data["cohort_id"]
        applicant.is_employed = request.data["is_employed"]
        applicant.employer = request.data["employer"]
        applicant.image = request.data["image"]
        applicant.aboutme = request.data["aboutme"]
        applicant.location = request.data["location"]
        applicant.jobtitle = request.data["jobtitle"]

        applicant.save()


        user = User.objects.get(pk=applicant.user_id)
        user.last_name = request.data["last_name"]
        user.first_name = request.data["first_name"]
        user.email = request.data["email"]
        user.username = request.data["username"]
        user.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)