from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.models import User
from hivemindapi.models import Friend
from rest_framework.decorators import action

class FriendSerializer(serializers.HyperlinkedModelSerializer):
    """
    JSON serializer for Friends
    Arguments:
        serializers
    """

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
            Response -- JSON serialized friend instance

        To retrieve a friend relationship, make a GET request to:
        http://localhost:8000/friends/1

        NOTE: Replace the 1 with the ID of the friend relationship that corresponds with the relationship you want to retrieve.
        """
        try:
            friend = Friend.objects.get(pk=pk)
            serializer = FriendSerializer(
                friend, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """
        Handle GET requests to friends resource
        Returns:
            Response -- JSON serialized list of friends

        To retrieve all friend relationships, make a GET request to:
        http://localhost:8000/friends 

        To retrieve friends for the LOGGED IN USER, make a get request to:
        http://localhost:8000/friends?applicant=True

        
        """
        friends = Friend.objects.all()

        # filters for friends by the authenticated user
        applicant = self.request.query_params.get('applicant', False)
        if applicant is not False:
            friends = friends.filter(applicant_id=request.auth.user.applicant.id)

        serializer = FriendSerializer(
            friends, many=True, context={'request': request})

        return Response(serializer.data)

    def create(self, request):
        '''
        Handles POST operations
        Returns:
            Response --- JSON serialized Interview instance

        To create an Friend relationship, make a POST to this URL:
        http://localhost:8000/friends

        '''
        # create new friend instance
        new_friend = Friend()
        new_friend.applicant_id = request.auth.user.applicant.id
        new_friend.friend_id = request.data['friend_id']

        # save friend
        new_friend.save()

        serializer = FriendSerializer(
            new_friend, context={'request': request})

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        '''
        Handles DELETE request for a single friend relationship
        Returns:
            Response -- 200, 404, or 500 status code

        To DELETE an friend, make a delete request to:
        http://localhost:8000/friends/1

        NOTE: Replace the 1 with the ID of the friend you wish to delete.
        '''

        try: 
            # delete single friend
            friend = Friend.objects.get(pk=pk)
            friend.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Friend.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   
