from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from hivemindapi.models import Interview
from .Applicant import ApplicantSerializer
from .Company import CompanySerializer


class InterviewSerializer(serializers.HyperlinkedModelSerializer):
    '''
    JSON serializer for interviews
    Arguments: serializers.HyperlinkedModelSerializer
    '''
    # serialize applicant and company
    applicant = ApplicantSerializer()
    company = CompanySerializer()

    class Meta:
        model = Interview
        url = serializers.HyperlinkedIdentityField(
            view_name='interview',
            lookup_field='id'
        )
        fields = ('id', 'offer', 'position',  'date', 'review', 'advice',
                  'interview_type', 'in_person', 'code_challege', 'applicant', 'company')
        depth = 2


class Interviews(ViewSet):
    '''

    This class houses functions for List, Retrieve, Destroy, Update, and Create
    '''

    def retrieve(self, request, pk=None):
        '''
        Handles GET requests for a single Interview
        Returns:
            Response --- JSON serialized Interviews instance

        To retrieve a single Interview:
        http://localhost:8000/interviews/1

        NOTE: Replace the 1 with the ID number of the interview you wish to retrieve.
        '''
        try:
            # get single interview
            interview = Interview.objects.get(pk=pk)
            serializer = InterviewSerializer(
                interview, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        '''
        Handles POST operations
        Returns:
            Response --- JSON serialized Interview instance

        To create an Interview, make a POST to this URL:
        http://localhost:8000/interviews

        '''
        # create new interview instance
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

        # save interview
        new_interview.save()

        serializer = InterviewSerializer(
            new_interview, context={'request': request})

        return Response(serializer.data)

    def list(self, request):
        '''
        Handles the GET all requstes to the interview resource
        Returns:
        Response -- JSON serialized list of interview
        To get all interviews with no filtering:
        http://localhost:8000/interviews
        
        To filter by LOGGED IN APPLICANT and COMPANY:
        http://localhost:8000/interviews?applicant=true&&company=1

        NOTE: Replace the 1 with whichever company ID number you need.

        To filter by LOGGED IN APPLICANT:
        http://localhost:8000/interviews?applicant=true

        To filter by COMPANY:
        http://localhost:8000/interviews?company=1
        NOTE: Replace the 1 with whichever company ID number you need.

        To filter by ANY APPLICANT ID: 
        http://localhost:8000/interviews?review=1

        NOTE: Replace the 1 with whichever applicant ID number you need.
        
        To filter by LOGGED IN APPLICANT and FRIENDS:
        http://localhost:8000/interviews?friend=true

        '''
        # gets all interviews
        interviews = Interview.objects.all()

        # defines the user ID
        applicant_id = request.auth.user.applicant.id

        # filter by logged in applicant ID
        is_logged_in_applicant = self.request.query_params.get('applicant', False)
        if is_logged_in_applicant == 'true':
            interviews = interviews.filter(applicant__id=applicant_id)
        
        # gets all of the applicant's friend's interviews
        is_friend = self.request.query_params.get('friend', False)
        if is_friend == 'true':
            interviews = Interview.objects.raw('''
            SELECT i.id,
            i.offer, 
            i.position, 
            i.date, 
            i.review, 
            i.advice, 
            i.interview_type, 
            i.in_person, 
            i.code_challege, 
            i.company_id, 
            i.applicant_id
            FROM hivemindapi_interview i
            JOIN hivemindapi_friend f ON i.applicant_id = f.friend_id
            WHERE f.applicant_id = %s
            ORDER BY i.date DESC;
            ''', [applicant_id])
        

        # filter by applicant ID
        applicant = self.request.query_params.get('review', None)
        if applicant is not None:
            interviews = interviews.filter(applicant__id=applicant)
        
       

        # filter by company ID
        company_id = self.request.query_params.get('company', None)
        if company_id is not None:
            interviews = interviews.filter(company__id=company_id)
       

        # take repsonse and covert to JSON
        serializer = InterviewSerializer(interviews, many=True, context={'request': request})

        # return repsonse as JSON
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        '''
        Handles DELETE request for a single interview
        Returns:
            Response -- 200, 404, or 500 status code

        To DELETE an interview, make a delete request to:
        http://localhost:8000/interviews/1

        NOTE: Replace the 1 with the ID of the interview you wish to delete.
        '''

        try: 
            # delete single interview
            interview = Interview.objects.get(pk=pk)
            interview.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Interview.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   

    def update(self, request, pk=None):
        '''
        Handles PUT request for a single interview
        Returns:
            Response -- 200, 404, or 500 status code

        To UPDATE an interview, make a PUT request to:
        http://localhost:8000/interviews/1

        NOTE: Replace the 1 with the ID of the interview you wish to update.
        '''
        # edit single interview
        interview = Interview.objects.get(pk=pk)
        interview.company_id = request.data['company_id']
        interview.offer = request.data['offer']
        interview.position = request.data['position']
        interview.date = request.data['date']
        interview.review = request.data['review']
        interview.advice = request.data['advice']
        interview.interview_type = request.data['interview_type']
        interview.in_person = request.data['in_person']
        interview.code_challege = request.data['code_challege']
        interview.applicant_id = request.auth.user.applicant.id
        
        # save changes
        interview.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)
