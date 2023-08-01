# Dashboard Raffinerie

Tableau de bord imaginé par Julien pour la Raffinerie.


## Document de travail :

https://codimd.communecter.org/yxDYGactSfmNg87kOV0FgA#


## Installation Frontend

```bash
cd front_vuejs
npm install
npm run serve
```


## Installation Backend

```bash
poetry install
poetry run python manage.py migrate
poetry run python manage.py createsuperuser
poetry run python manage.py runserver
```
