Dependencies for this project are managed using `pipenv`: https://pipenv.readthedocs.io/en/latest/

* Install `pipenv` on your host.
* To install dependencies: `pipenv install`.
* To use the generated virtualenv: `pipenv shell`.
* Inside the virtualenv:
    * To generate the DB: `./manage.py migrate`
    * To create a test user: `./manage.py createsuperuser`
    * To run the development server: `./manage.py migrate`
    
The docker container for this service (running the Django development server) is `wesjordan/soundbin-admin:dev`