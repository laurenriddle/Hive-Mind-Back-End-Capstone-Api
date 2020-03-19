from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from hivemindapi.models.Cohort import Cohort
from hivemindapi.models.Applicant import Applicant
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token



print("test file loaded------------------------")

class TestApplicants(TestCase):
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

    def test_get_applicants(self):
        

        # Now we can grab all the companies (meaning the one we just created) from the db
        response = self.client.get(reverse('applicant-list'), HTTP_AUTHORIZATION='Token ' + str(self.token))

        # Check that the response is 200 OK.
        # This is checking for the GET request result, not the POST. We already checked that POST works in the previous test!
        self.assertEqual(response.status_code, 200)

        # response.data is the python serialised data used to render the JSON, while response.content is the JSON itself.
        # Are we responding with the data we asked for? There's just one payment type in our dummy db, so it should contain a list with one instance in it
        self.assertEqual(len(response.data), 1)

        # test the contents of the data before it's serialized into JSON
        self.assertEqual(response.data[0]["linkedin_profile"], "https://www.linkedin.com/in/lauren-riddle/")

       


    def test_retrieve_applicant(self):
       
        response = self.client.get(reverse('applicant-detail', kwargs={'pk': 1}), HTTP_AUTHORIZATION='Token ' + str(self.token))
 

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # test the contents of the data before it's serialized into JSON
        self.assertEqual(response.data["linkedin_profile"], "https://www.linkedin.com/in/lauren-riddle/")

       

if __name__ == '__main__':
    unittest.main()