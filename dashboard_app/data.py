class data():
   
   #les paramètres sont de base en False, et mis en True si actifs
   #input : modifiable
   #list : liste déroulante
   #checkbox : case à cocher
   #total : fait le total en pied de page si "total" du tableau est en True

    membres_du_collectif = {
        "slug": "membres_du_collectif",
        "titre": "",
        "colonnes": [
            {'nom':'', 'list': True, }, # liste qui vient de l'organigramme
            {'nom':'A valider', 'total':True}, #total des colones A valider (bienveillance et presta interne) du suivi détaillé
            {'nom':'A facturer', 'total':True},  #total des colones A Facturer (bienveillance et presta interne) du suivi détaillé
            {'nom':'A Payer', 'total':True }, #total des colones A Payé (bienveillance et presta interne) du suivi détaillé
        ],
        "lignes": [
            ['Jacques', 10, 20, True],
            ['Camille', 10, 20, False],
            ['Jacqueline', 10, 20, True],
        ],
        "total": True,
        "editable": True,
    }

    recap_depenses = {
        "slug": "recap_depenses",
        "titre": "dépenses",
        "colonnes": [
            {'nom':''}, 
            {'nom':'prév'}, #somme du dépenses prévisionnel 
            {'nom':'dépensé'}, #somme des dépenses réel
            {'nom':'reste à dépenser'}, #somme des reste à dépenser
        ],
        "lignes": [
            ['bienveillance', 10, 20, True],
            ['presta int.', 10, 20, True],
            ['presta.ext / achats', 10, 20, True],
            ['dépenses int.', 10, 20, True],
        ],
        "total": True,
        "editable": False,
    }

    recap_recettes = {
        "slug": "recap_recettes",
        "titre": "recettes",
        "colonnes": [
            {'nom':'', 'input': True}, 
            {'nom':'prév', 'input': True},  #somme des recettes prévisionnel 
            {'nom':'encaissé', 'input': True}, #somme des recettes encaissées
            {'nom':'reste à encaisser', 'input': True}, #somme des recettes qui reste à encaisser
        ],
        "lignes": [
            ['animation ateliers', 10, 20, False],
            ['entretien matérie', 10, 20, False],
            ['ventes', 10, 20, False],
            ['recette int', 10, 20, False],
        ],
        "total": True,
        "editable": False,
    }
################## suivi budgétaire détaillé ################""
    ####  dépenses ###
    bienveillance_prev = {
        "slug": "recap_recettes",
        "titre": "recettes",
        "colonnes": [
            {'nom':'', 'input': True}, #les membres du collectif ayant le caractére bienveillant dans l'organigramme, peuvent ajouter des intulés 
            {'nom':'montant', 'input': True}, #les membres du collectif ayant le caractére bienveillant dans l'organigramme, peuvent ajouter des montants 
        ],
        "lignes": [
            ['garant du cadre', 100],
            ['ref budget', 100],
            ['ref communication', 100],
        ],
        "total": True,
        "editable": True,
    }

    bienveillance_reel = {
        "slug": "recap_recettes",
        "titre": "recettes",
        "colonnes": [
            {'nom':'', 'list': True}, #les bienveillants peuvent selectionné un nom 
            {'nom':'date', 'input': True}, #les bienveillants peuvent remplir une date
            {'nom':'propo.', 'input': True}, #les bienveillants peuvent remplir un un montant
            {'nom':'validé', 'checkbox': True}, #les bienveillants peuvent valider
            {'nom':'factu.', 'checkbox': True}, #les bienveillants peuvent valider
            {'nom':'payé', 'checkbox': True}, #si la facture est "payé" dans odoo, la checkbox est True, il y aura un peu de réflexion à avoir pour voir comment associé une proposition à une facture odoo
        ],
        "lignes": [
            ['Rémy', 100, True, False, False],
            ['Georgette', 200, True, True, False],
            ['hugues', 300, False, False, False],
            ['yvette', 500, True, True, False],
        ],
        "total": True,
        "editable": True,
    }

    presta_int_prev = {
        "slug": "recap_recettes",
        "titre": "recettes",
        "colonnes": [
            {'nom':'', 'input': True}, #les membres du collectif ayant le caractére bienveillant dans l'organigramme, peuvent ajouter des intulés 
            {'nom':'montant', 'input': True}, #les membres du collectif ayant le caractére bienveillant dans l'organigramme, peuvent ajouter des montants 
        ],
        "lignes": [
            ['animation ateliers', 530],
            ['entretien matérie', 200],
        ],
        "total": True,
        "editable": True,
    }

    presta_int_reel = {
        "slug": "recap_recettes",
        "titre": "recettes",
        "colonnes": [
            {'nom':'', 'liste': True}, #liste déroulante des presta interne de l'organigramme
            {'nom':'date', 'input': True}, #les presta int concerné peuvent remplir un une date
            {'nom':'propo.', 'input': True}, #les presta int concerné peuvent remplir un un montant
            {'nom':'validé', 'checkbox': True}, #les bienveillants peuvent valider
            {'nom':'factu.', 'checkbox': True}, #les presta int concerné peuvent valider
            {'nom':'payé', 'checkbox': True}, #si la facture est "payé" dans odoo, la checkbox est True 
        ],
        "lignes": [
            ['Rémy', 100, True, False, False],
            ['Georgette', 200, True, True, False],
        ],
        "total": True,
        "editable": True,
    }

    presta_ext_prev = {
        "slug": "recap_recettes",
        "titre": "recettes",
        "colonnes": [
            {'nom':'', 'input': True}, #les membres du collectif ayant le caractére bienveillant dans l'organigramme, peuvent ajouter des intulés 
            {'nom':'montant', 'input': True}, #les membres du collectif ayant le caractére bienveillant dans l'organigramme, peuvent ajouter des montants 
        ],
        "lignes": [
            ['matériel', 500],
            ['consomable', 400],
        ],
        "total": True,
        "editable": True,
    }

    presta_ext_reel = {
        "slug": "recap_recettes",
        "titre": "recettes",
        "colonnes": [
            {'nom':''},  #le nom des facture de tout les articles sauf co-rem et presta int
            {'nom':'intitulé'}, #l'intitulé des facture
            {'nom':'date'}, #date des factures
            {'nom':'validé',},#si la facture est "validé" dans odoo, la checkbox est True, c'est une checkbox non modifiable par l'utilisateur
            {'nom':'payé',}, #si la facture est "payé" dans odoo, la checkbox est True, c'est une checkbox non modifiable par l'utilisateur
        ],
        "lignes": [
            ['Ravate','course', '03/05/23', True, False],
            ['decathlon','matériel ', '09/08/23', True, True],
        ],
        "total": True,
        "editable": False,
    }

    depenses_int_prev = {
        "slug": "recap_recettes",
        "titre": "recettes",
        "colonnes": [
            {'nom':'', 'input': True}, #les membres du collectif ayant le caractére bienveillant dans l'organigramme, peuvent ajouter des intulés 
            {'nom':'montant', 'input': True}, #les membres du collectif ayant le caractére bienveillant dans l'organigramme, peuvent ajouter des montants 
        ],
        "lignes": [
            ['micro-recylerie','1000€'],
            ['Culture', '2000€'],
            ['commun', '2000€'],
        ],
        "total": True,
        "editable": True,
    }

    #le principe est que ce tableau est relié avec le tableau recette int des projets selectionné dans "nom"
    depenses_int_reel = { 
        "slug": "recap_recettes",
        "titre": "recettes",
        "colonnes": [
            {'nom':'', 'list': True}, #liste déroulante des projets
            {'nom':'date', 'input': True}, #date à rentrer par un bienveillant
            {'nom':'montant', 'input': True}, #montant à rentrer par un bienveillant
        ],
        "lignes": [
            ['micro-recylerie', '03/05/23','1000€'],
            ['Culture', '03/05/23', '2000€'],
        ],
        "total": True,
        "editable": False,
    }

    ####  recettes ###

    subvention_prev = {
        "slug": "recap_recettes",
        "titre": "recettes",
        "colonnes": [
            {'nom':'', 'input': True}, #les membres du collectif ayant le caractére bienveillant dans l'organigramme, peuvent ajouter des intulés 
            {'nom':'montant', 'input': True}, #les membres du collectif ayant le caractére bienveillant dans l'organigramme, peuvent ajouter des montants 
        ],
        "lignes": [
            ['micro-recylerie','1000€'],
            ['Culture', '2000€'],
            ['commun', '2000€'],
        ],
        "total": True,
        "editable": True,
    }

#ce tableau est relié à la page subventions
    subvention_reel = { 
        "slug": "recap_recettes",
        "titre": "recettes",
        "colonnes": [
                    {'nom':'',}, 
                    {'nom':'date', },
                    {'nom':'montant',},
        ],
        "lignes": [
            ['micro-recylerie', '03/05/23','1000€'],
            ['Culture', '03/05/23', '2000€'],
        ],
        "total": True,
        "editable": False,
    }

    presta_prev = {
        "slug": "recap_recettes",
        "titre": "recettes",
        "colonnes": [
            {'nom':'', 'input': True},  #les membres du collectif ayant le caractére bienveillant dans l'organigramme, peuvent ajouter des intulés 
            {'nom':'montant', 'input': True}, #les membres du collectif ayant le caractére bienveillant dans l'organigramme, peuvent ajouter des montants 
             
        ],
        "lignes": [
            ['micro-recylerie','1000€'],
            ['Culture', '2000€'],
            ['commun', '2000€'],
        ],
        "total": True,
        "editable": True,
    }

    presta_reel = { 
        "slug": "recap_recettes",
        "titre": "recettes",
        "colonnes": [
            {'nom':'',}, #factures client avec l'article presta ext via odoo
            {'nom':'date',}, # date des factures 
            {'nom':'montant',},# montant des factures
        ],
        "lignes": [
            ['micro-recylerie', '03/05/23','1000€'],
            ['Culture', '03/05/23', '2000€'],
        ],
        "total": True,
        "editable": False,
    }

    vente_prev = {
        "slug": "recap_recettes",
        "titre": "recettes",
        "colonnes": [
            {'nom':'', 'input': True}, #les membres du collectif ayant le caractére bienveillant dans l'organigramme, peuvent ajouter des intulés 
            {'nom':'montant', 'input': True}, #les membres du collectif ayant le caractére bienveillant dans l'organigramme, peuvent ajouter des montants 
        ],
        "lignes": [
            ['micro-recylerie','1000€'],
            ['Culture', '2000€'],
            ['commun', '2000€'],
        ],
        "total": True,
        "editable": True,
    }

    vente_reel = { 
        "slug": "recap_recettes",
        "titre": "recettes",
        "colonnes": [
            {'nom':'',}, #factures client avec l'article vente via odoo
            {'nom':'date',},  #date des factures 
            {'nom':'montant',},  #montant des factures 
        ],
        "lignes": [
            ['micro-recylerie', '03/05/23','1000€'],
            ['Culture', '03/05/23', '2000€'],
        ],
        "total": True,
        "editable": False,
    }

    recettes_int_prev = {
        "slug": "recap_recettes",
        "titre": "recettes",
        "colonnes": [
            {'nom':'', 'input': True}, #les membres du collectif ayant le caractére bienveillant dans l'organigramme, peuvent ajouter des intulés 
            {'nom':'montant', 'input': True}, #les membres du collectif ayant le caractére bienveillant dans l'organigramme, peuvent ajouter des montants 
        ],
        "lignes": [
            ['micro-recylerie','1000€'],
            ['Culture', '2000€'],
            ['commun', '2000€'],
        ],
        "total": True,
        "editable": True,
    }

#le principe est que ce tableau est relié avec le tableau dépense int des projets selectionné dans "nom"
    recettes_int_reel = { 
        "slug": "recap_recettes",
        "titre": "recettes",
        "colonnes": [
            {'nom': '', 'list': False}, 
            {'nom': 'date', 'input': True},
            {'nom': 'montant', 'input': True},
        ],
        "lignes": [
            ['micro-recylerie', '03/05/23','1000€'],
            ['Culture', '03/05/23', '2000€'],
        ],
        "total": True,
        "editable": False,
    }

############ Organigramme #################


    organigramme = { 
        "slug": "recap_recettes",
        "titre": "recettes",
        "colonnes": [
                    {'nom':'', 'list': True}, #liste déroulante des membres de odoo qui ont l'étiquette "Raffineur.euse"
                    {'nom':'presta interne', 'checkbox': True}, #peut être coché par les admins 
                    {'nom':'garant du cadre', 'checkbox': True}, #peut être coché par les admins
                    {'nom':'référent budgtet / subvention', 'checkbox': True}, #peut être coché par les admins
                    {'nom':'référent tâche planning', 'checkbox': True}, #peut être coché par les admins
        ],
        "lignes": [
            ['jessica', True, True, False, False ],
            ['Bob', True, False, True, False ],
            ['John', True, False, False, True ],
            ['Suzy', True, False, False, False ],
        ],
        "total": True,
        "editable": False,
    }

       


