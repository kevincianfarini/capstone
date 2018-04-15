# To set up the development environment

```shell
git clone <repo url> && cd capstone
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python manage.py migrate
```

## Running the Project

This project is separated into a Django backing API and a frontend to consume cached blog documents. All frontend logic can be found in `/frontend`. 

To populate the database with blog documents

```shell
(env) $ python manage.py populate <sites.txt>
```

To generate tags for the cached documents. This can only be run after populating the database

```shell
(env) $ python manage.py tag
```

To clear any entries in the database
```shell
(env) $ python manage.py clear
```

To run the project
```shell
(env) $ python manage.py runserver 0.0.0.0:8000
```
and visit localhost:8000 in your browser. 


## Development Documentation

The backend exposes several APIs that the front end can consume. They are:
```python
'/files/tags/?tag=<tag>'
'/files/content/<id>/'
'/files/?tags=<tag1>|<tag2>|<tag3>' # filters BlogPosts which have all tags
```