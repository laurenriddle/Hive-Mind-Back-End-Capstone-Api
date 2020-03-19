from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from hivemindapi.models.Favorite import Favorite
from hivemindapi.models.Cohort import Cohort
from hivemindapi.models.Company import Company
from hivemindapi.models.Applicant import Applicant
from hivemindapi.models.Interview import Interview
from hivemindapi.models.Industry import Industry
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token



print("test file loaded------------------------")

class TestInterviews(TestCase):
    # used for user auth
    def setUp(self):
        self.username = 'Julz'
        self.password = 'foobar'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.token = Token.objects.create(user=self.user)
        self.cohort = Cohort.objects.create(
            cohort="Day Cohort 36"
        )
        self.applicant = Applicant.objects.create(user_id=1,
            linkedin_profile="https://www.linkedin.com/in/lauren-riddle/",
            cohort_id=1,
            is_employed=True,
            employer="Ingram",
            image="./testpath.png",
            aboutme="Software Developer"
            )

    def test_post_interview(self):
        # define an industry
        self.industry = Industry.objects.create(
            industry="Publishing"
        )

        # define a company
        self.company = Company.objects.create(
            name="Ingram Content Group",
            industry_id=1,
            city="Nashville",
        )
        # define a interview
        new_interview = {
            "company_id": 1,
            "offer":False,
            "position":"Software Developer I",
            "date":"2020-11-11",
            "review":"Went Well",
            "advice":"Know OOP Fundamentals",
            "interview_type":"First Interview",
            "in_person":True,
            "code_challege":True,
            "applicant_id":1
        
        }


        # use the client to send the request and store the response
        response = self.client.post(
            reverse('interview-list'), new_interview, HTTP_AUTHORIZATION='Token ' + str(self.token)
        )

         # returns 200 back if we have a success with the test
        self.assertEqual(response.status_code, 200)

        # queries the table to see how many companies are in it
        self.assertEqual(Interview.objects.count(), 1)

        # queries the table to make sure the object we just added is in there by checking one of the properties. In this case, merchant_name.
        self.assertEqual(Interview.objects.get().review, "Went Well")

    def test_delete_payment_type(self):
          # define an industry
        self.industry = Industry.objects.create(
            industry="Publishing"
        )

        # define a favorite
        self.company = Company.objects.create(
            name="Ingram Content Group",
            industry_id=1,
            city="Nashville",
        )
        # define a interview
        new_interview = Interview.objects.create(
            company_id= 1,
            offer=False,
            position="Software Developer I",
            date="2020-11-11",
            review="Went Well",
            advice="Know OOP Fundamentals",
            interview_type="First Interview",
            in_person=True,
            code_challege=True,
            applicant_id=1
        
            )
         
        # perform a delete on the object. Note: you have to reverse to interview-detail sinces you are only targeting one object and not the whole list
        response = self.client.delete(reverse('interview-detail', kwargs={'pk': 1}), HTTP_AUTHORIZATION='Token ' + str(self.token))
 
        # Check that the response is 204 OK.
        self.assertEqual(response.status_code, 204)

        # Now we can grab all the interviews from the db. In this case there should be 0
        response = self.client.get(reverse('interview-list'), HTTP_AUTHORIZATION='Token ' + str(self.token))

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # test that the length of the response is 0, which means the delete was successful
        self.assertEqual(len(response.data), 0)

    def test_get_favorites(self):
         # define an industry
        self.industry = Industry.objects.create(
            industry="Publishing"
        )

        # define a favorite
        self.company = Company.objects.create(
            name="Ingram Content Group",
            industry_id=1,
            city="Nashville",
        )
        # define a interview
        new_interview = Interview.objects.create(
            company_id= 1,
            offer=False,
            position="Software Developer I",
            date="2020-11-11",
            review="Went Well",
            advice="Know OOP Fundamentals",
            interview_type="First Interview",
            in_person=True,
            code_challege=True,
            applicant_id=1
        
            )

        

        # Now we can grab all the companies (meaning the one we just created) from the db
        response = self.client.get(reverse('interview-list'), HTTP_AUTHORIZATION='Token ' + str(self.token))

        # Check that the response is 200 OK.
        # This is checking for the GET request result, not the POST. We already checked that POST works in the previous test!
        self.assertEqual(response.status_code, 200)

        # response.data is the python serialised data used to render the JSON, while response.content is the JSON itself.
        # Are we responding with the data we asked for? There's just one payment type in our dummy db, so it should contain a list with one instance in it
        self.assertEqual(len(response.data), 1)

        # test the contents of the data before it's serialized into JSON
        self.assertEqual(response.data[0]["review"], "Went Well")

        # Finally, test the actual rendered content as the client would receive it.
        # .encode converts from unicode to utf-8. Don't get hung up on this. It's just how we can compare apples to apples
        self.assertIn(new_interview.review.encode(), response.content)


    def test_retrieve_interview(self):
        # define an industry
        self.industry = Industry.objects.create(
            industry="Publishing"
        )

        # define a favorite
        self.company = Company.objects.create(
            name="Ingram Content Group",
            industry_id=1,
            city="Nashville",
        )
        # define a interview
        new_interview1 = Interview.objects.create(
            company_id= 1,
            offer=False,
            position="Software Developer I",
            date="2020-11-11",
            review="Went Well",
            advice="Know OOP Fundamentals",
            interview_type="First Interview",
            in_person=True,
            code_challege=True,
            applicant_id=1
        
        )

        # # define a interview
        new_interview2 = Interview.objects.create(
            company_id= 1,
            offer=False,
            position="Software Developer II",
            date="2020-11-11",
            review="Went Okay",
            advice="Know OOP Fundamentals",
            interview_type="First Interview",
            in_person=True,
            code_challege=True,
            applicant_id=1
        
        )

       
        response = self.client.get(reverse('interview-detail', kwargs={'pk': 2}), HTTP_AUTHORIZATION='Token ' + str(self.token))
 

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # test the contents of the data before it's serialized into JSON
        self.assertEqual(response.data["review"], "Went Okay")

        # Finally, test the actual rendered content as the client would receive it.
        # .encode converts from unicode to utf-8. Don't get hung up on this. It's just how we can compare apples to apples
        self.assertIn(new_interview2.review.encode(), response.content)
    
    def test_edit_interview(self):
        """TEST for update method on interview view"""
        # define an industry
        self.industry = Industry.objects.create(
            industry="Publishing"
        )

        # define a company
        self.company = Company.objects.create(
            name="Ingram Content Group",
            industry_id=1,
            city="Nashville",
        )
        # define a interview
        new_interview1 = Interview.objects.create(
            company_id= 1,
            offer=False,
            position="Software Developer I",
            date="2020-11-11",
            review="Went Well",
            advice="Know OOP Fundamentals",
            interview_type="First Interview",
            in_person=True,
            code_challege=True,
            applicant_id=1
        
        )
        updated_interview = {
            "company_id": 1,
            "offer":False,
            "position":"Software Developer I",
            "date":"2020-11-11",
            "review":"Went Great!",
            "advice":"Know OOP Fundamentals",
            "interview_type":"First Interview",
            "in_person":True,
            "code_challege":True,
            "applicant_id":1
        
        }


        # Update new_product
        response = self.client.put(
            reverse('interview-detail', kwargs={'pk': 1}), 
            updated_interview,
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + str(self.token)
        )

        # Assert that the put returns the expected 204 status
        self.assertEqual(response.status_code, 204)

        # Get the order again, it should now be the updated order.
        response = self.client.get(
            reverse('interview-detail', kwargs={'pk': 1}), HTTP_AUTHORIZATION='Token ' + str(self.token)
        )
        
        # Assert that the product name is now self.payment_type_two.id
        self.assertEqual(response.data["review"], "Went Great!")



        

if __name__ == '__main__':
    unittest.main()