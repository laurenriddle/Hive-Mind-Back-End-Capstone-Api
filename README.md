## Want to use the Hive Mind API? Follow the steps below to run the application

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

## Front-End Client

9. This API is dependent on a front-end client. To run the full app, you will need to install and run the front-end client as well. You can find it here with instructions for setup:
https://github.com/laurenriddle/Hive-Mind-Back-End-Capstone-Client
