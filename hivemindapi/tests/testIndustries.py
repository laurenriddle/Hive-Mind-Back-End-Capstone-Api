from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from hivemindapi.models.Industry import Industry



print("test file loaded------------------------")

class TestIndustries(TestCase):

    def test_get_industries(self):
        # define a industry
        new_industry = Industry.objects.create(
            industry="Publishing"
            )
       
         

        # Now we can grab all the industries (meaning the one we just created) from the db
        response = self.client.get(reverse('industry-list'))

        # Check that the response is 200 OK.
        # This is checking for the GET request result, not the POST. We already checked that POST works in the previous test!
        self.assertEqual(response.status_code, 200)

        # response.data is the python serialised data used to render the JSON, while response.content is the JSON itself.
        # Are we responding with the data we asked for? There's just one payment type in our dummy db, so it should contain a list with one instance in it
        self.assertEqual(len(response.data), 1)

        # test the contents of the data before it's serialized into JSON
        self.assertEqual(response.data[0]["industry"], "Publishing")

        # Finally, test the actual rendered content as the client would receive it.
        # .encode converts from unicode to utf-8. Don't get hung up on this. It's just how we can compare apples to apples
        self.assertIn(new_industry.industry.encode(), response.content)


    def test_retrieve_industry(self):
        # define a industry
        new_industry1 = Industry.objects.create(
            industry="Publishing"
            )
         
        new_industry2 = Industry.objects.create(
            industry="Consulting"
            )
         
         
       
        response = self.client.get(reverse('industry-detail', kwargs={'pk': 2}))
 

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # test the contents of the data before it's serialized into JSON
        self.assertEqual(response.data["industry"], "Consulting")

        # Finally, test the actual rendered content as the client would receive it.
        # .encode converts from unicode to utf-8. Don't get hung up on this. It's just how we can compare apples to apples
        self.assertIn(new_industry2.industry.encode(), response.content)

if __name__ == '__main__':
    unittest.main()