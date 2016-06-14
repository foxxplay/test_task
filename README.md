How to get the code running.

1) Create and activate new virtual environment:
`pip install virtualenv`
`virtualenv task`
`source task/bin/activate`

2) Install MongoDB if does not exist.
`sudo apt-get install mongodb`

3) Configure MongoDB connection. Change file task/settings.py, replace this parameters if need:
`_MONGODB_HOST = 'localhost'`
`_MONGODB_PORT = 27017`
`_MONGODB_USER = ''`
`_MONGODB_PASSWD = ''`
`_MONGODB_NAME = 'task'`

4) Install python packages
`pip install -r requirements.pip`

5) Run local server:
`./manage.py runserver`

6) Check http://127.0.0.1:8000/ 