Dependencies for this project are managed using `pipenv`: https://pipenv.readthedocs.io/en/latest/

* Install `pipenv` on your host.
* To install dependencies: `pipenv install`.
* To use the generated virtualenv: `pipenv shell`.
* Inside the virtualenv:
    * To generate the DB: `./manage.py migrate`
    * To run the development server: `./manage.py migrate`