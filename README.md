# Dashboard Raffinerie

Tableau de bord imaginé par Julien pour la Raffinerie.


## Document de travail :

https://codimd.communecter.org/yxDYGactSfmNg87kOV0FgA#

## Installation de l'environnement de developpement.

#### Prérequis :

- Python 3.10 :
  - https://www.python.org/downloads
- Poetry : 
  - https://python-poetry.org/docs/#installing-with-the-official-installer
- Git :
  - https://git-scm.com/downloads

#### Installation 

```bash
git clone https://github.com/CoopCodeCommun/DashboardRaffinerie
cd DashboardRaffinerie
poetry install
poetry run python manage.py migrate
poetry run python manage.py createsuperuser
poetry run python manage.py runserver
```
