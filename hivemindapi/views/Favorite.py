from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from hivemindapi.models import Favorite
from .Interview import InterviewSerializer



class FavoriteSerializer(serializers.HyperlinkedModelSerializer):
    '''
    JSON serializer for favorites
    Arguments: serializers.HyperlinkedModelSerializer
    '''
    # serialize interview
    interview = InterviewSerializer()

    class Meta:
        model = Favorite
        url = serializers.HyperlinkedIdentityField(
            view_name='favorite',
            lookup_field='id'
        )
        fields = ('id', 'interview', 'applicant_id')
        depth = 2


class Favorites(ViewSet):
    '''

    This class houses functions for List, Retrieve, Destroy, and Create
    '''

    def retrieve(self, request, pk=None):
        '''
        Handles GET requests for a single favorite
        Returns:
            Response --- JSON serialized favorites instance

        To retrieve a single Favorite:
        http://localhost:8000/favorites/1

        NOTE: Replace the 1 with the ID number of the favorite you wish to retrieve.
        '''
        try:
            # get single favorite
            favorite = Favorite.objects.get(pk=pk)
            serializer = FavoriteSerializer(
                favorite, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        '''
        Handles POST operations
        Returns:
            Response --- JSON serialized Favorite instance

        To create an Favorite, make a POST to this URL:
        http://localhost:8000/favorites

        '''
        # create new favorite instance
        new_favorites = Favorite()
        new_favorites.interview_id = request.data['interview_id']
        new_favorites.applicant_id = request.auth.user.applicant.id

        # save favorite
        new_favorites.save()

        serializer = FavoriteSerializer(
            new_favorites, context={'request': request})

        return Response(serializer.data)

    def list(self, request):
        '''
        Handles the GET all requstes to the favorite resource
        Returns:
        Response -- JSON serialized list of favorites
        To get all favorites with no filtering:
        http://localhost:8000/favorites
        
        To filter by LOGGED IN APPLICANT and COMPANY:
        http://localhost:8000/favorites?applicant=true&&interview=1

        NOTE: Replace the 1 with whichever company ID number you need.

        To filter by LOGGED IN APPLICANT:
        http://localhost:8000/favorites?applicant=true

        To filter by COMPANY:
        http://localhost:8000/favorites?interview=1
        NOTE: Replace the 1 with whichever company ID number you need.


        '''
        # gets all favorites
        favorites = Favorite.objects.all()

        # defines the user ID
        applicant_id = request.auth.user.applicant.id

        # filter by logged in applicant ID
        is_logged_in_applicant = self.request.query_params.get('applicant', False)
        if is_logged_in_applicant == 'true':
            favorites = favorites.filter(applicant__id=applicant_id)
       

        # filter by company ID
        company_id = self.request.query_params.get('interview', None)
        if company_id is not None:
            favorites = favorites.filter(interview__company__id=company_id)
       

        # take repsonse and covert to JSON
        serializer = FavoriteSerializer(favorites, many=True, context={'request': request})

        # return repsonse as JSON
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        '''
        Handles DELETE request for a single favorite
        Returns:
            Response -- 200, 404, or 500 status code

        To DELETE a favorite, make a delete request to:
        http://localhost:8000/favorites/1

        NOTE: Replace the 1 with the ID of the favorite you wish to delete.
        '''

        try: 
            # delete single favorite
            favorite = Favorite.objects.get(pk=pk)
            favorite.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Favorite.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   
