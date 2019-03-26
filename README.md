Build Status: [![CircleCI](https://circleci.com/gh/cs-4284-capstone/soundbin-admin/tree/master.svg?style=svg)](https://circleci.com/gh/cs-4284-capstone/soundbin-admin/tree/master)

Dependencies for this project are managed using `pipenv`: https://pipenv.readthedocs.io/en/latest/

* Install `pipenv` on your host.
* To install dependencies: `pipenv install`.
* To use the generated virtualenv: `pipenv shell`.
* Inside the virtualenv:
    * To run `manage.py` you need to have the `SECRET_KEY` environment variable set. This variable is used to encrypt 
    administrator passwords, so it must be consistent between runs. 
    * To generate the DB: `./manage.py migrate`
    * To create a test user: `./manage.py createsuperuser`
    * To run the development server: `./manage.py runserver`
    
The production docker container for this service is `wesjordan/soundbin-admin:dev`.
