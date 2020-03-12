from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from hivemindapi.models import Interview
from .Applicant import ApplicantSerializer



class InterviewSerializer(serializers.HyperlinkedModelSerializer):
    '''
    JSON serializer for payment types
    Arguments: serializers.HyperlinkedModelSerializer
    Author: Lauren Riddle
    '''
    applicant = ApplicantSerializer()

    class Meta:
        model = Interview
        url = serializers.HyperlinkedIdentityField(
            view_name='interview',
            lookup_field='id'
        )
        fields = ('id', 'offer', 'position',  'date', 'review', 'advice', 'interview_type', 'in_person', 'code_challege', 'applicant', 'company_id' )
        depth = 2

class Interviews(ViewSet):
    '''
    
    # This class houses functions for List, Retrieve, Destroy, and Create
    '''

    def retrieve(self, request, pk=None):
        '''
        Handles GET requests for a single Interview 
        Returns:
            Response --- JSON serialized Interviews instance
        '''
        try:
            interview = Interview.objects.get(pk=pk)
            serializer = InterviewSerializer(interview, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        '''
        Handles POST operations
        Returns: 
            Response --- JSON serialized Interview instance
        '''
        new_interview = Interview()
        new_interview.company_id = request.data['company_id']
        new_interview.offer = request.data['offer']
        new_interview.position = request.data['position']
        new_interview.date = request.data['date']
        new_interview.review = request.data['review']
        new_interview.advice = request.data['advice']
        new_interview.interview_type = request.data['interview_type']
        new_interview.in_person = request.data['in_person']
        new_interview.code_challege = request.data['code_challege']
        new_interview.applicant_id = request.auth.user.applicant.id

        new_interview.save()

        serializer = InterviewSerializer(new_interview, context ={'request': request})

        return Response(serializer.data)
    

    def list(self, request):
        '''
        Handles the GET all requstes to the payment types resource
        Returns: 
        Response -- JSON serialized list of Payment Types
        Author: Lauren Riddle
        '''
        user = request.auth.user.customer.id
        # list payment types
        types = PaymentType.objects.filter(customer_id=user)

        # take repsonse and covert to JSON
        serializer = PaymentTypeSerializer(types, many=True, context={'request': request})

        # return repsonse as JSON
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        '''
        Handles DELETE request for a single payment type
        Returns:
            Response -- 200, 404, or 500 status code
        Author: Lauren Riddle
        '''

        try: 
            type = PaymentType.objects.get(pk=pk)
            type.delete(force_policy=None)

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except PaymentType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    