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

To run this in multithreaded mode 

```shell
(env) $ python manage.py populate <sites.txt> --threaded
```

To clear any entries in the database
```shell
python manage.py clear
```