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

#### Temps de travail

| Auteur | Date     | Durée    | Description                                                                                        | Etat |
|--------|----------|----------|----------------------------------------------------------------------------------------------------|------|
| Jonas  | 01/02/23 | 5 jours  | Création TiQo : liaison et création Api Qonto et Api Odoo                                          | Payé |
| Jonas  | 01/08/23 | 1 jour   | Installation de l'environnement de developpement Django pour le dashboard                          |      |
| Jonas  | 24/09/23 | 1/2 jour | Déploiement version de préprod                                                                     |      |
| Jonas  | 02/10/23 | 1 jour   | Ajout de la base de donnée Contact et fichier d'exemple htmx                                       |      |
| Jonas  | 03/10/23 | 1 jour   | Base de donnée Account et API Odoo                                                                 |      |
| Jonas  | 04/10/23 | 1 jour   | Api CRUD, exemple Ajax & exemple tableau mode édition & page d'administration de la base de donnée |      |
