from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from hivemindapi.models.Cohort import Cohort


print("test file loaded------------------------")

class TestCohorts(TestCase):

    def test_get_cohorts(self):
        # define a cohort to be POSTed to the DB
        new_cohort = Cohort.objects.create(
            cohort="Day Cohort 36"
        )
         

        # Now we can grab all the cohorts (meaning the one we just created) from the db
        response = self.client.get(reverse('cohort-list'))

        # Check that the response is 200 OK.
        # This is checking for the GET request result, not the POST. We already checked that POST works in the previous test!
        self.assertEqual(response.status_code, 200)

        # response.data is the python serialised data used to render the JSON, while response.content is the JSON itself.
        # Are we responding with the data we asked for? There's just one payment type in our dummy db, so it should contain a list with one instance in it
        self.assertEqual(len(response.data), 1)

        # test the contents of the data before it's serialized into JSON
        self.assertEqual(response.data[0]["cohort"], "Day Cohort 36")

        # Finally, test the actual rendered content as the client would receive it.
        # .encode converts from unicode to utf-8. Don't get hung up on this. It's just how we can compare apples to apples
        self.assertIn(new_cohort.cohort.encode(), response.content)


    def test_retrieve_cohort(self):
       
        # define a company to be POSTed to the DB
        new_cohort1 = Cohort.objects.create(
            cohort="Day Cohort 36"
        )
         
        new_cohort2 = Cohort.objects.create(
            cohort="Day Cohort 37"
        )
         
         
       
        response = self.client.get(reverse('cohort-detail', kwargs={'pk': 1}))
 

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # test the contents of the data before it's serialized into JSON
        self.assertEqual(response.data["cohort"], "Day Cohort 37")

        # Finally, test the actual rendered content as the client would receive it.
        # .encode converts from unicode to utf-8. Don't get hung up on this. It's just how we can compare apples to apples
        self.assertIn(new_cohort2.cohort.encode(), response.content)

if __name__ == '__main__':
    unittest.main()