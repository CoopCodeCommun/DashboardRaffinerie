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

# Installer les librairies python :
poetry install

# Initialiser et/ou mettre à jour la structure de la base de donnée :
poetry run python manage.py migrate

# Créer un super utilisateur :
poetry run python manage.py createsuperuser

# Lancer le serveur de développement :
poetry run python manage.py runserver
```

Une fois le serveur de developpement lancé, vous pouvez accéder au site à l'adresse : http://localhost:8000

La page se recharge automatiquement si une modification est detectée dans les templates comme dans les controleurs.

#### Documentation technique

Work in progres ...