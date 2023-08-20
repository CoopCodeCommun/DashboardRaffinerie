<template>
  <!-- lancement : node +  cd outil-gestion-interne + npm run serve
  sur navigateur :   - Local:   http://localhost:8080/ ou
   - Network: http://192.168.1.18:8080/-->

  <div>

    <!-- barre de menu supérieur -->
    <nav class="navbar bleu case m-2">
      <div class="container-fluid">
        <div class="row">
          <div class="col">
            <!-- Bouton selection pôle avec sélection déroulante -->
            <div id="app">
              <BoutonMenu :options="dropdownOptions"/>
            </div>
          </div>
          <div class="col">
            <!-- Bouton se connecter -->
            <div id="app">
              <button class="bleu case style_input case_clair" @click="showLoginForm = true">Se connecter</button>
              <div class="login-form" v-if="showLoginForm">
                <form>
                  <label for="username">Identifiant :</label>
                  <input type="text" id="username" v-model="username">

                  <label for="password">Mot de passe :</label>
                  <input type="password" id="password" v-model="password">

                  <button type="submit">Valider</button>
                  <button type="button" @click="showLoginForm = false">Annuler</button>
                </form>
              </div>
            </div>

          </div>
        </div>
      </div>
    </nav>

    <main>
      <div class="container-fluid">
        <div class="row">
          <div class="col-md-2">
            <!-- menu lateral -->
            <MenuLateral :menuItems="menuItems"/>
          </div>

          <!-- suivi budgétaire -->
          <div class="col-md-10">
            <!-- membre + recap -->
            <section class="row">

              <!-- membre du collectif -->
              <section class="col-md-4">
                <div class="rose p-2 pt-0 case h-100">
                  <div>
                    <OuvrirFermer title="Membre du collectif">
                      <CreationTableau :titre="titre_membres" :rows="rows_membres" :columns="columns_membres"/>
                    </OuvrirFermer>
                  </div>
                </div>
              </section>

              <!-- recap budget -->
              <section class="col-md-8" style="display: flex;  align-items: stretch;">
                <div class="orange p-2 pt-0 case ">
                  <OuvrirFermer title="Recap budgétaire" class="case titre">
                    <section class="container-fluid">
                      <div class="row h-100">
                        <!-- dépense -->
                        <div class="col p-2 pt-0 case h-100">
                          <div>
                            <CreationTableau :titre="titre_recap_depenses" :rows="rows_recap_depenses"
                                             :columns="columns_recap_depenses" :showFooter="true"/>
                          </div>
                        </div>

                        <!-- recette -->
                        <div class="col p-2 pt-0 case h-100">
                          <div>
                            <CreationTableau :titre="titre_recap_recettes" :rows="rows_recap_recettes"
                                             :columns="columns_recap_recettes" :showFooter="true"/>
                          </div>
                        </div>
                      </div>
                    </section>
                  </OuvrirFermer>
                </div>
              </section>
            </section>

            <!-- depense / recette -->
            <div class="row">
              <section class="container-fluid">
                <div class="row">
                  <div class="col">
                    <div class="jaune my-3 case">

                      <section class="container">
                        <div class="row">

                          <!-- Dépense -->
                          <div class="col-7">
                            <OuvrirFermer title="Dépenses" class="case titre">
                              <div class="container case case_clair h-100 ">

                                <!-- Bienveillance -->
                                <OuvrirFermer title="Bienveillance" class="case titre">
                                  <div class="row d-flex align-items-stretch">
                                    <!-- prévisionnel -->
                                    <div class="col-4">
                                      <div>
                                        <CreationTableau :titre="titre_prev_bienveillance"
                                                         :rows="rows_prev_bienveillance"
                                                         :columns="columns_prev_bienveillance" :showFooter="true"/>
                                      </div>
                                    </div>
                                    <!-- réel -->
                                    <div class="col-8">
                                      <div>
                                        <CreationTableau :titre="titre_reel_bienveillance"
                                                         :rows="rows_reel_bienveillance"
                                                         :columns="columns_reel_bienveillance" :showFooter="true"/>
                                      </div>
                                    </div>
                                  </div>
                                </OuvrirFermer>

                                <!-- prestations internes -->
                                <OuvrirFermer title="prestation internes" class="case titre">
                                  <div class="row">
                                    <!-- prévisionnel -->
                                    <div class="col-4">
                                      <div>
                                        <CreationTableau :titre="titre_prev_prestations_internes"
                                                         :rows="rows_prev_prestations_internes"
                                                         :columns="columns_prev_prestations_internes"
                                                         :showFooter="true"/>
                                      </div>
                                    </div>
                                    <!-- réel -->
                                    <div class="col-8">
                                      <div>
                                        <CreationTableau :titre="titre_reel_prestations_internes"
                                                         :rows="rows_reel_prestations_internes"
                                                         :columns="columns_reel_prestations_internes"
                                                         :showFooter="true"/>
                                      </div>
                                    </div>
                                  </div>
                                </OuvrirFermer>

                                <!-- prestations externes / achats -->
                                <OuvrirFermer title="Prestations externes / achats" class="case titre">
                                  <div class="row">
                                    <!-- prévisionnel -->
                                    <div class="col-4">
                                      <div>
                                        <CreationTableau :titre="titre_prev_prestations_externes"
                                                         :rows="rows_prev_prestations_externes"
                                                         :columns="columns_prev_prestations_externes"
                                                         :showFooter="true"/>
                                      </div>
                                    </div>
                                    <!-- réel -->
                                    <div class="col-8">
                                      <div>
                                        <CreationTableau :titre="titre_reel_prestations_externes"
                                                         :rows="rows_reel_prestations_externes"
                                                         :columns="columns_reel_prestations_externes"
                                                         :showFooter="true"/>
                                      </div>
                                    </div>
                                  </div>
                                </OuvrirFermer>

                                <!-- dépenses internes -->
                                <OuvrirFermer title="Dépenses interne" class="case titre">
                                  <div class="row">
                                    <!-- prévisionnel -->
                                    <div class="col-4">
                                      <div>
                                        <CreationTableau :titre="titre_prev_dépenses_internes"
                                                         :rows="rows_prev_dépenses_internes"
                                                         :columns="columns_prev_dépenses_internes" :showFooter="true"/>
                                      </div>
                                    </div>
                                    <!-- réel -->
                                    <div class="col-8">
                                      <div>
                                        <CreationTableau :titre="titre_reel_dépenses_internes"
                                                         :rows="rows_reel_dépenses_internes"
                                                         :columns="columns_reel_dépenses_internes" :showFooter="true"/>
                                      </div>
                                    </div>
                                  </div>
                                </OuvrirFermer>


                              </div>
                            </OuvrirFermer>
                          </div>

                          <!-- recette -->
                          <div class="col p-2">
                            <OuvrirFermer title="Recettes" class="case titre">
                              <div class="case case_clair p-2 h-100">

                                <!-- Subventions -->
                                <OuvrirFermer title="Subvention / appel à projets" class="case titre">
                                  <div class="row">
                                    <!-- prévisionnel -->
                                    <div class="col-5">
                                      <div>
                                        <CreationTableau :titre="titre_prev_subvention" :rows="rows_prev_subvention"
                                                         :columns="columns_prev_subvention" :showFooter="true"/>
                                      </div>
                                    </div>
                                    <!-- réel -->
                                    <div class="col-7">
                                      <div>
                                        <CreationTableau :titre="titre_reel_subvention" :rows="rows_reel_subvention"
                                                         :columns="columns_reel_subvention" :showFooter="true"/>
                                      </div>
                                    </div>
                                  </div>
                                </OuvrirFermer>

                                <!-- Prestations -->
                                <OuvrirFermer title="Prestations" class="case titre">
                                  <div class="row">
                                    <!-- prévisionnel -->
                                    <div class="col-5">
                                      <div>
                                        <CreationTableau :titre="titre_prev_prestations" :rows="rows_prev_prestations"
                                                         :columns="columns_prev_prestations" :showFooter="true"/>
                                      </div>
                                    </div>
                                    <!-- réel -->
                                    <div class="col-7">
                                      <div>
                                        <CreationTableau :titre="titre_reel_prestations" :rows="rows_reel_prestations"
                                                         :columns="columns_reel_prestations" :showFooter="true"/>
                                      </div>
                                    </div>
                                  </div>
                                </OuvrirFermer>

                                <!-- ventes -->
                                <OuvrirFermer title="ventes" class="case titre">
                                  <div class="row">
                                    <!-- prévisionnel -->
                                    <div class="col-5">
                                      <div>
                                        <CreationTableau :titre="titre_prev_ventes" :rows="rows_prev_ventes"
                                                         :columns="columns_prev_ventes" :showFooter="true"/>
                                      </div>
                                    </div>
                                    <!-- réel -->
                                    <div class="col-7">
                                      <div>
                                        <CreationTableau :titre="titre_reel_ventes" :rows="rows_reel_ventes"
                                                         :columns="columns_reel_ventes" :showFooter="true"/>
                                      </div>
                                    </div>
                                  </div>
                                </OuvrirFermer>

                                <!-- Recettes internes -->
                                <OuvrirFermer title="Recettes internes" class="case titre">
                                  <div class="row">
                                    <!-- prévisionnel -->
                                    <div class="col-5">
                                      <div>
                                        <CreationTableau :titre="titre_prev_recettes_internes"
                                                         :rows="rows_prev_recettes_internes"
                                                         :columns="columns_prev_recettes_internes" :showFooter="true"/>
                                      </div>
                                    </div>
                                    <!-- réel -->
                                    <div class="col-7">
                                      <div>
                                        <CreationTableau :titre="titre_reel_recettes_internes"
                                                         :rows="rows_reel_recettes_internes"
                                                         :columns="columns_reel_recettes_internes" :showFooter="true"/>
                                      </div>
                                    </div>
                                  </div>
                                </OuvrirFermer>
                              </div>
                            </OuvrirFermer>
                          </div>
                        </div>
                      </section>
                    </div>


                  </div>
                </div>
              </section>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>


  <!-- modal pour le bouton se connecter -->

</template>

<script>
import CreationTableau from "@/components/CreationTableau.vue";
import OuvrirFermer from "@/components/OuvrirFermer.vue";
import BoutonMenu from "@/components/BoutonMenu.vue";
import MenuLateral from "@/components/MenuLateral.vue";
import {ref} from 'vue';


export default {

  setup() {
    const showLoginForm = ref(false)
    const username = ref('')
    const password = ref('')

    const submit = () => {
      console.log(`Username: ${username.value}, Password: ${password.value}`)
      // ici, vous pouvez ajouter le code pour envoyer les informations de connexion à votre serveur
    }

    return {
      showLoginForm,
      username,
      password,
      submit,
    }
  },

  components: {
    CreationTableau,
    OuvrirFermer,
    BoutonMenu,
    MenuLateral,

  },
  data() {
    return {

      // liste des pôles projet
      dropdownOptions: ['La Raffinerie', 'couture', 'inter-travaux', 'groupe culture'],

      // État du tableau (true: étendu, false: replié)
      showTable: true,

      // icone et text menu latéral

      menuItems: [
        {icon: 'bi bi-bar-chart-line', text: 'Tableau de bord'},
        {icon: 'bi bi-currency-euro', text: 'Suivi budgétaire'},
        {icon: 'bi bi-piggy-bank', text: 'Plan de trésorerie'},
        {icon: 'bi bi-cash-coin', text: 'Suivi subventions'},
        {icon: 'bi bi-file-music', text: 'Suivi évenements'},
        {icon: 'bi bi-list-ol', text: 'Suivi volontariat'},
        {icon: 'bi bi-people', text: 'Répertoire Raffineur.euses'},
        {icon: 'bi bi-clipboard-data', text: 'Tableau de bord perso'},
        {icon: 'bi bi-book', text: 'Documentation'},
      ],


      //données membre du collectif
      titre_membres: "",
      rows_membres: ['Paul', 'Jessica', 'Ben', 'Véronique'],
      columns_membres: [
        {name: 'à valider', styleClass: 'case', input: false, dropdown: false,}, // La colonne par défaut est sans input
        {name: 'à facturer', styleClass: 'case', input: false, dropdown: false,},
        {name: 'à payer', styleClass: 'case', input: false, dropdown: false,},
      ],

      //données recap depenses
      titre_recap_depenses: "Dépenses",
      rows_recap_depenses: ['bienveillance', 'presta int.', 'presta.ext / achats', 'dépenses int.'],
      columns_recap_depenses: [
        {name: 'prév', styleClass: 'case', input: false, dropdown: false,}, // La colonne par défaut est sans input
        {name: 'dépensé', styleClass: 'case', input: false, dropdown: false,},
        {name: 'reste à dépensé', styleClass: 'case', input: false, dropdown: false,},
      ],

      //données recap recettes
      titre_recap_recettes: "Recettes",
      rows_recap_recettes: ['suventions / app', 'prestations', 'ventes', 'recette int'],
      columns_recap_recettes: [
        {name: 'prév.', styleClass: 'case', input: false, dropdown: false,}, // La colonne par défaut est sans input
        {name: 'encaissé', styleClass: 'case', input: false, dropdown: false,},
        {name: 'reste à encaisser', styleClass: 'case', input: false, dropdown: false,},
      ],

      //données prévisionnel bienveillance
      titre_prev_bienveillance: "Prévisionnel",
      rows_prev_bienveillance: ['bienveillance'],
      columns_prev_bienveillance: [
        {name: 'Montant', styleClass: 'case', input: true, dropdown: false,}, // La colonne par défaut est sans input
      ],

      //données réel bienveillance
      titre_reel_bienveillance: "Réel",
      rows_reel_bienveillance: ['Paul', 'Jessica', 'kevin'],
      columns_reel_bienveillance: [
        {name: 'date', styleClass: 'case', input: true, dropdown: false,}, // La colonne par défaut est sans input
        {name: 'propo.', styleClass: 'case', input: true, dropdown: false,},
        {name: 'validé', styleClass: 'case', input: true, dropdown: false,},
        {name: 'factu.', styleClass: 'case', input: true, dropdown: false,},
        {name: 'payé', styleClass: 'case', input: false, dropdown: false,},
      ],

      //données prévisionnel prestations internes
      titre_prev_prestations_internes: "Prévisionnel",
      rows_prev_prestations_internes: ['bienveillance', 'animation ateliers', 'entretien matériel'],
      columns_prev_prestations_internes: [
        {name: 'Montant', styleClass: 'case', input: true, dropdown: false,}, // La colonne par défaut est sans input
      ],

      //données réel prestation interne
      titre_reel_prestations_internes: "Réel",
      rows_reel_prestations_internes: ['Jessica', 'kevin'],
      columns_reel_prestations_internes: [
        {name: 'date', styleClass: 'case', input: true, dropdown: false,}, // La colonne par défaut est sans input
        {name: 'propo.', styleClass: 'case', input: true, dropdown: false,},
        {name: 'validé', styleClass: 'case', input: true, dropdown: false,},
        {name: 'factu.', styleClass: 'case', input: true, dropdown: false,},
        {name: 'payé', styleClass: 'case', input: false, dropdown: false,},
      ],

      //données prévisionnel prestations externes
      titre_prev_prestations_externes: "Prévisionnel",
      rows_prev_prestations_externes: ['achat matériel', 'prestataires externes'],
      columns_prev_prestations_externes: [
        {name: 'Montant', styleClass: 'case', input: true, dropdown: false,}, // La colonne par défaut est sans input
      ],

      //données réel prestation externes
      titre_reel_prestations_externes: "Réel",
      rows_reel_prestations_externes: ['Ravate', 'run market', 'SARL Payet'],
      columns_reel_prestations_externes: [
        {name: 'intitulé', styleClass: 'case', input: false}, // La colonne par défaut est sans input
        {name: 'date', styleClass: 'case', input: false},
        {name: 'validé', styleClass: 'case', input: false, dropdown: false,},
        {name: 'payé', styleClass: 'case', input: false, dropdown: false,},
      ],

      //données prévisionnel dépenses interne
      titre_prev_dépenses_internes: "Prévisionnel",
      rows_prev_dépenses_internes: ['pôle culture', 'inter-formation', 'micro-recylerie'],
      columns_prev_dépenses_internes: [
        {name: 'Montant', styleClass: 'case', input: true, dropdown: false,}, // La colonne par défaut est sans input
      ],

      //données réel dépenses interne
      titre_reel_dépenses_internes: "Réel",
      rows_reel_dépenses_internes: ['Dépenses interne'],
      columns_reel_dépenses_internes: [
        {name: 'pôle', styleClass: 'case', input: false, dropdown: true, options: ['Option 1', 'Option 2', 'Option 3']},
        {name: 'date', styleClass: 'case', input: true, dropdown: false,},
        {name: 'montant', styleClass: 'case', input: true, dropdown: false,},
      ],

      //données prévisionnel subvention
      titre_prev_subvention: "Prévisionnel",
      rows_prev_subvention: ['subventions'],
      columns_prev_subvention: [
        {name: 'Montant', styleClass: 'case', input: true, dropdown: false,}, // La colonne par défaut est sans input
      ],

      //données réel subvention
      titre_reel_subvention: "Réel",
      rows_reel_subvention: ['Région', 'Mairie'],
      columns_reel_subvention: [
        {name: 'Date', styleClass: 'case', input: false, dropdown: false,},
        {name: 'Montant', styleClass: 'case', input: false, dropdown: false,},
      ],

      //données prévisionnel prestations
      titre_prev_prestations: "Prévisionnel",
      rows_prev_prestations: ['divers prestations'],
      columns_prev_prestations: [
        {name: 'Montant', styleClass: 'case', input: true, dropdown: false,}, // La colonne par défaut est sans input
      ],

      //données réel prestations
      titre_reel_prestations: "Réel",
      rows_reel_prestations: ['asso rvp', 'SARL dudu'],
      columns_reel_prestations: [
        {name: 'Date', styleClass: 'case', input: false, dropdown: false,},
        {name: 'Montant', styleClass: 'case', input: false, dropdown: false,},
      ],


      //données prévisionnel ventes
      titre_prev_ventes: "Prévisionnel",
      rows_prev_ventes: ['Ventes en direct'],
      columns_prev_ventes: [
        {name: 'Montant', styleClass: 'case', input: true, dropdown: false,}, // La colonne par défaut est sans input
      ],

      //données réel ventes
      titre_reel_ventes: "Réel",
      rows_reel_ventes: ['vente en direct', 'asso hoareau'],
      columns_reel_ventes: [
        {name: 'Date', styleClass: 'case', input: false, dropdown: false,},
        {name: 'Montant', styleClass: 'case', input: false, dropdown: false,},
      ],


      //données prévisionnel recettes internes
      titre_prev_recettes_internes: "Prévisionnel",
      rows_prev_recettes_internes: ['divers pôles'],
      columns_prev_recettes_internes: [
        {name: 'Montant', styleClass: 'case', input: true, dropdown: false,}, // La colonne par défaut est sans input
      ],

      //données réel subvention
      titre_reel_recettes_internes: "Réel",
      rows_reel_recettes_internes: ['pôle jardin', 'bar'],
      columns_reel_recettes_internes: [
        {name: 'Date', styleClass: 'case', input: false, dropdown: false,},
        {name: 'Montant', styleClass: 'case', input: false, dropdown: false,},
      ],


    };
  },

  computed: {},

  methods: {

    //bandeau déroulant
    toggleDropdown() {
      this.isDropdownOpen = !this.isDropdownOpen;
    },
    selectOption(option) {
      this.selectedOption = option;
      this.isDropdownOpen = false;
    },

    // Méthode pour basculer l'état du tableau (étendu ou replié) lors du clic sur le symbole "+"/"-"
    toggleTable() {
      this.$emit('toggle');
    }


  }
}

</script>

<style>
@import url('https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css');
@import url('https://cdn.jsdelivr.net/npm/bootstrap-icons@1.5.0/font/bootstrap-icons.css');
@import url('https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js');
@import url('https://fonts.googleapis.com/css2?family=Itim&display=swap');


.case.menu_lateral {
  font-family: 'Itim', cursive;
  color: white;
  font-size: larger;
  border-radius: 20px;

}

.titre {
  font-size: medium;
}

.en-tete {
  font-size: 0.9em;
  text-align: center;
  white-space: nowrap;
}

.case {
  font-family: 'Itim', cursive;
  color: white;
  border-radius: 15px;
  border-collapse: separate;
  border-spacing: 2px;
  width: auto;


}

.padding-class {
  padding: .375rem;
}

.case_moyen {
  border-collapse: separate;
  border-spacing: 10px;
  width: 100%;

}

.case.case_petite {
  height: 25px;
  border-radius: 8px;
  border-spacing: 10px;
  min-width: 40px;
  width: auto;
  line-height: 1em;


}

.case.case_fonce {
  background: rgba(0, 0, 0, .1);

}

.case.case_clair {
  background: rgba(255, 255, 255, .2);
  width: 100%;
  height: 100%;
}

.case.case_input {
  background: rgba(255, 255, 255, .7);
  border: 0px;
  width: 50px;
  color: rgba(0, 0, 0, .6);

}

.case.case_dropdown {
  background: rgba(255, 255, 255, .7);
  border: 0px;
  width: 50px;
  color: rgba(0, 0, 0, .6);

}

.sidebar {
  width: auto;
}


.case.h-100 {
  height: 100%;
  height: auto;
}


.table-container table {
  width: 100%; /* This will make the table fill its container */
  height: 100%;
}

.table-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}


.table-container .case.case_clair {
  flex-grow: 1;
}

.rose {
  background-color: #eb8cac;
}

.jaune {
  background-color: #bfa20f;
}

.orange {
  background-color: #de9e21;
}

.bleu {
  background-color: #4796b9;
}

.vert {
  background-color: #39b1ab;
}


</style>