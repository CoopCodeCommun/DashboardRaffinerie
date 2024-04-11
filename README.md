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

| Auteur | Date     | Durée     | Description                                                                                        | Etat |
|--------|----------|-----------|----------------------------------------------------------------------------------------------------|------|
| Jonas  | 01/02/23 | 5 jours   | Création TiQo : liaison et création Api Qonto et Api Odoo                                          | Payé |
| Jonas  | 01/08/23 | 1 jour    | Installation de l'environnement de developpement Django pour le dashboard                          |      |
| Jonas  | 24/09/23 | 0.5 jour  | Déploiement version de préprod                                                                     |      |
| Jonas  | 02/10/23 | 1 jour    | Ajout de la base de donnée Contact et fichier d'exemple htmx                                       |      |
| Jonas  | 03/10/23 | 1 jour    | Base de donnée Account et API Odoo                                                                 |      |
| Jonas  | 04/10/23 | 1 jour    | Api CRUD, exemple Ajax & exemple tableau mode édition & page d'administration de la base de donnée |      |
| Jonas  | 01/11/23 | 1.5 jours | Templates                                                                                          |      |


___

# Préparer le preprod du dashboard.

- Après avoir téléchargé le repos, vérifier si les fichiers de migrations sont effacé, sinon effacer toutes les fichiers de migrations (sauf __init__.py)
- Aussi dans l'application vérifier s'il n'y a pas une base de donnée `db.sqlite3` . si oui la supprimer.
- Poetry:
    - `poetry install`
    - `poetry init` (si poetry est déjà installé)
    - `poetry shell`
- Création d'admin
    - Dans la racine de l'app `./manage.py create superuser`
    - username -> admin
    - email -> admin@ad.fr
    - password -> 1234exemple
    - username -> 1234exemple
- Création d'un BD pour mieux voir les fonctionnalités du programme
    - Dans la racine de l'app
        -  `./manage.py popdb`
    -  Ajoutons les données des API dans la config
        -  A récupérer le fichier .env par des réseaux chiffrées, exemple signal
        -  Ajoutons le fichier .env dans la racine de l'app (dans le même niveau comme manage.py ou dasheboard_app)
        -  Récuperons par les mêmes réseaux chiffrées la clé chiffrée de l'API Qonto et l'identification.
        -  Ajoutons ces données dans la BD suivant les procédures suivantes:
            -  Dans le terminale cliquez `./manage.py shell_plus`
            -  On sera dans ipython qui ressemble à ça `In [1]:`
            -  Créons l'objet Configuration avec la commande suivante:
            -  id_qonto = 'idintifiant_donne_par_reseau_criptee'
            -  qo_api_key = 'clef_api_donne_en_criptee'
        -  `Configuration.objects.create(qonto_login=id_qonto, qonto_apikey=qo_api_key)`
