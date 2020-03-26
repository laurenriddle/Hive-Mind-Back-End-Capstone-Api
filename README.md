<div align="center"><img src="./readmeimg/Logo.png" alt="Logo" width="300" height="360" /></div>


## What is Hive Mind?
Hive Mind is a social media platform that allows Nashville Software School students and alumni to create and share interview "surveys" for interviews that they have had with specific companies. These surveys include information that can be used by students to prepare for their own interviews with specific companies. With Hive Mind, students are able to create their own interview surveys, search for other student's interview surveys by company, save other user's surveys to a favorites board, customize personal profile information, and view other's profiles. 

## Why was Hive Mind created?
As a student who is about to graduate, when the job search process began, one thing that I quickly realized is that it can be hard to know exactly how to prepare for interviews with different companies. Each company has a different way of interviewing, different questions that they ask, and different code challenges and trying to guess the best way to prepare for these interviews can be nerve wracking. This is why I decided to create Hive Mind - a solution to ease the stress that students face during their job search by helping them feel more prepared for the interview process.


## Want to use the Hive Mind API? Follow the steps below to set it up.

1. Create a new directory in your terminal by running `mkdir Hive-Mind-API` and then run `cd Hive-Mind-API`. Clone down this repository by clicking the "Clone or Download" button above, copying the SSH key, and running the following command in your terminal `git clone SSHKEYGOESHERE`.
2. After the clone is finished, run `cd Hive-Mind-Back-End-Capstone-API` in your terminal. 
3. Create your virtual environment by typing the following commands in your terminal:
    - For OSX: 
        - `python -m venv HiveMindEnv`
        - `source ./HiveMindEnv/bin/activate`

    - For Windows:
        - `python -m venv HiveMindEnv`
        - `source ./HiveMindEnv/Scripts/activate`

4. Install the app's dependencies:

	- `pip install -r requirements.txt`

5. Build your database from the existing models:

	- `python manage.py makemigrations hivemindapi`
	- `python manage.py migrate`

6. Create a superuser for your local version of the app:

	- `python manage.py createsuperuser`

7. Populate your database with initial data from fixtures files: (_NOTE: every time you run this it will remove existing data and repopulate the tables_)

	- `python manage.py loaddata */fixtures/*.json`

8. Fire up your dev server and get to work!

	- `python manage.py runserver`

### Front-End Client

9. This API is dependent upon a front-end client. To run the full app, you will need to install and run the front-end client as well. You can find it here with instructions for setup:
https://github.com/laurenriddle/Hive-Mind-Back-End-Capstone-Client



## Hive Mind Documentation 

### Using the Hive Mind API with its client
1. Follow the instructions above to download the API and run the client. 

### Using the Hive Mind API independently from its client
1. Follow steps 1-8 above to set up the API and perform all installations needed to run it. 
2. Download Postman (https://www.postman.com/) and then open the app.
3. You will need to register a new user in the database so that you will have an authentication token, which is required for you to communicate with this API. First, in Postman, select the "New" button in the top, left corner. Select type "request", set the request name to "Register" and under collections/folders, create a new folder called "Hive Mind" and select it. Save the request. 
4. Once you create the request, a tab will open up in Postman that allows you to make fetch requests to the database. The first request you need to make is a POST request to http://localhost:8000/register. To do this, you need to set a header, where the key is "Content-Type" and the value is "application/json" (see image #1 below). After you create the header, copy the object below, go to body, select the option for "raw", and paste this object into the body (see image #2 below). 

	- Register Object: 
	`{
		"username": "johnd",
		"first_name": "John",
		"last_name": "Doe",
		"email": "jdoe@gmail.com",
		"password": "123",
		"cohort_id": 1,
		"is_employed": true,
		"image": null,
		"employer": null,
		"aboutme": null,
		"jobtitle": "Software Developer",
		"location": "Nashville",
		"linkedin_profile": null
	}`

5. Once you have the body and header of the request set, make sure you have the URL set to http://localhost:8000/register and the request method is set to POST. When you have these configured, select send. If the register was successful, you will see a token returned in the response section (see image #2 below).



### #1
![ERD](./readmeimg/Headers.png)


### #2
![ERD](./readmeimg/RegisterBody.png)

6. Once you get a token, copy it and go to your headers settings. Add a new header with the key of "Authorization" and the value of "Token YOURTOKENGOESHERE" (see image #3 below).

### #3
![ERD](./readmeimg/AddToken.png)

7. Once you have your token, you will then have access to all of the fetch calls available for the API. If you want to make a fetch call, simply input into Postman the URL you would like to make the fetch call to, pass your token and content-type in the header, and (if you are making a POST or a PUT) pass the object that you would like to send to the database in the body of the request. 

8. A complete list of URLs to which you can send request is available in the documentation below. The properties for each table in the database are available in the ERD below as well. 

### Testing 
Hive Mind comes equiped with tests for all endpoints. To execute these tests, in your terminal run `python manage.py test hivemindapi`. If all tests have passed, you should recieve a status of OK in your terminal. 

### Fetch Requests
Below are the endpoints that are available through this API, as well as the types of requests you can make for each endpoint and the URLs that you need to send the requests to for each method. 
_NOTE: All fetch requests need to be made to http://localhost:8000/._

1. __Applicant (PUT, POST, GET, RETRIEVE)__

	- To retrieve a SINGLE applicant, make a GET request to: http://localhost:8000/applicants/1.
	_NOTE: Replace the 1 with the ID of the applicant that corresponds with the user you want to retrieve._
	
	- To retrieve ALL users, make a GET request to: http://localhost:8000/applicants 

	- To retrieve the current LOGGED IN USER, make a GET request to: http://localhost:8000/applicants?applicant=True

	- To filter users by FIRST NAME ONLY, make a GET request to: http://localhost:8000/applicants?user_first=John
	_NOTE: Replace John with the name of the user that you wish to retrieve._

	- To filter users by LAST NAME ONLY, make a GET request to: http://localhost:8000/applicants?user_last=Doe
	_NOTE: Replace Doe with the name of the user that you wish to retrieve._

	- To filter users by FIRST AND LAST NAME, make a GET request to: http://localhost:8000/applicants?user_first=John&&user_last=Doe
	_NOTE: Replace John and Doe with the name of the user that you wish to retrieve._

	- To update a user, make a PUT request to: http://localhost:8000/applicants/profile_update

2. __Interview (PUT, POST, GET, RETRIEVE, DELETE)__

	- To retrieve a SINGLE interview, make a GET request to: http://localhost:8000/interviews/1
	_NOTE: Replace the 1 with the ID number of the interview you wish to retrieve._

	-  To create an interview, make a POST request to:http://localhost:8000/interviews

	- To get ALL interviews, make a GET request to: http://localhost:8000/interviews
        
    - To filter interviews by LOGGED IN APPLICANT and COMPANY, make a GET request to:http://localhost:8000/interviews?applicant=true&&company=1
	_NOTE: Replace the 1 with whichever company ID number you need._

    - To filter interviews by LOGGED IN APPLICANT, make a GET request to:http://localhost:8000/interviews?applicant=true

    - To filter interviews by COMPANY, make a GET request to:http://localhost:8000/interviews?company=1
    _NOTE: Replace the 1 with whichever company ID number you need._

    - To filter interviews by ANY APPLICANT ID, make a GET request to: http://localhost:8000/interviews?review=1
	_NOTE: Replace the 1 with whichever applicant ID number you need._

	- To DELETE an interview, make a DELETE request to: http://localhost:8000/interviews/1
	_NOTE: Replace the 1 with the ID of the interview you wish to delete._
        
    - To UPDATE an interview, make a PUT request to: http://localhost:8000/interviews/1
	_NOTE: Replace the 1 with the ID of the interview you wish to update._
        
3. __Company (POST, GET, RETRIEVE)__

	- To access a SINGLE company, make a GET request to: http://localhost:8000/companies/1
	_NOTE: Replace the 1 with any company ID you wish to retrieve._ 

	- To access ALL companies, make a GET request to: http://localhost:8000/companies

    - To filter companies by NAME, make a GET request to: http://localhost:8000/companies?name=atiba
	_NOTE: Replace Atiba with any company name that you would like to find._

	-  To create a company, make a POST request to: http://localhost:8000/companies

4. __Favorite (POST, GET, RETRIEVE, DELETE)__

	- To retrieve a SINGLE Favorite, make a GET request to: http://localhost:8000/favorites/1
	_NOTE: Replace the 1 with the ID number of the favorite you wish to retrieve._

	- To create a new Favorite, make a POST request to: http://localhost:8000/favorites

	- To get ALL favorites, make a GET request to: http://localhost:8000/favorites
        
    - To filter favorites by LOGGED IN APPLICANT and INTERVIEW, make a GET request to: http://localhost:8000/favorites?applicant=true&&interview=1 
	_NOTE: Replace the 1 with whichever interview ID number you wish to retrieve._

    - To filter favorites by LOGGED IN APPLICANT and COMPANY, make a GET request to: http://localhost:8000/favorites?interview__company_id=1&&applicant=true
	_NOTE: Replace the 1 with whichever applicant ID number and company ID number you wish to retrieve._

    - To filter favorites by LOGGED IN APPLICANT, make a GET request to: http://localhost:8000/favorites?applicant=true

    - To filter favorites by COMPANY, make a GET request to: http://localhost:8000/favorites?interview__company_id=1
	_NOTE: Replace the 1 with whichever company ID number you wish to retrieve._

    - To filter favorites by INTERVIEW, make a GET request to: http://localhost:8000/favorites?interview=1
	_NOTE: Replace the 1 with whichever interview ID number you wish to retrieve._

	- To delete a favorite, make a DELETE request to: http://localhost:8000/favorites/1
	_NOTE: Replace the 1 with the ID of the favorite you wish to delete._

5. __Industry (GET, RETRIEVE)__

	- To retrieve a SINGLE industry, make a GET request to: http://localhost:8000/industries/1
	_NOTE: Replace the 1 with any ID you wish to retrieve._

	-  To get ALL industries, make a GET request to: http://localhost:8000/industries

6. __Cohort (GET, RETRIEVE)__
	
	-  To retrieve a SINGLE cohort, make a GET request to: http://localhost:8000/cohorts/1
	_NOTE: Replace the 1 with any ID you wish to retrieve._
    
    - To access ALL cohorts, make a GET request to: http://localhost:8000/cohorts   
        
### Entity Relationship Diagram
![ERD](./readmeimg/erd2.png)

### Client
The client documentation for this application can be found here: https://github.com/laurenriddle/Hive-Mind-Back-End-Capstone-Client

## Hive Mind Tech Stack 
<div align="center"><img src="./readmeimg/react.png" alt="React.js" width="75" height="75" />&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<img src="./readmeimg/django.png" alt="Django" width="125" height="75" />&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<img src="./readmeimg/python.png" alt="Python" width="75" height="75" />&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<img src="./readmeimg/javascriptyellow.png" alt="Javascript" width="75" height="75" />&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<img src="./readmeimg/cloudinary.png" alt="Cloudinary" width="75" height="75" />&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<img src="./readmeimg/css3.png" alt="CSS" width="75" height="100" /></div>


<div align="center"><img src="./readmeimg/reactBootstrap.svg" alt="React Bootstrap" width="75" height="75" />&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<img src="./readmeimg/github.png" alt="GitHub" width="75" height="75" />&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<img src="./readmeimg/git.png" alt="Git" width="75" height="75" />&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<img src="./readmeimg/tableplus.png" alt="TablePlus" width="75" height="75" />&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<img src="./readmeimg/postman.png" alt="Postman" width="90" height="75"/></div>

©2019 - Lauren Riddle

