<template>
 <!-- lancement : node +  cd outil-gestion-interne + npm run serve
 sur navigateur :   - Local:   http://localhost:8080/ ou 
  - Network: http://192.168.1.18:8080/-->
    <div>
    <nav class="navbar bleu case m-3">
      <div class="container">
        <div class="row">
          <div class="col">
  
  <!-- Bouton avec sélection déroulante -->
            <div style="position: relative; display: inline-block;">
              <button class="bleu case style_input case_clair" @click="toggleDropdown">{{ buttonText }}</button>
              <div v-if="isDropdownOpen" class="dropdown case bleu p-2 g-2" style="position: absolute; top: 110%; right: 100; ;;">
                <ul>
                  <li @click="selectOption('La Raffinerie')">La Raffinerie</li>
                  <li @click="selectOption('couture')">couture</li>
                  <li @click="selectOption('inter-travaux')">inter-travaux</li>
                </ul>
              </div>
            </div>
            <div style="display: inline-block;" class="case p-2">
              <span v-if="selectedOption"> {{ selectedOption }}</span>
            </div>
          </div>
        </div>
      </div>
    </nav>
     <main>
  
       <div class="container-fluid">
        
         <!-- menu lateral -->
          <div class="row g-1 b-2">
            <div class=" col-md-1 case">
              <div class="container-fluid">
                <div class="row d-flex">
                  <nav class="p-0 vert sidebar case">
                    <div class="sidebar-sticky">
                      <ul class="nav flex-column">
                        <li class="nav-item">
                          <button class="btn m-2 rounded b-0 menu_lateral text-start">
                            <i class="bi bi-bar-chart-line"></i> Tableau de bord
                          </button>
                          <button class="btn m-2 rounded b-0 menu_lateral text-start">
                            <i class="bi bi-currency-euro"></i> Suivi budgétaire
                          </button>
                          <button class="btn m-2 rounded b-0 menu_lateral text-start">
                            <i class="bi bi-piggy-bank"></i> Plan de trésorerie
                          </button>
                          <button class="btn m-2 rounded b-0 menu_lateral text-start">
                            <i class="bi bi-cash-coin"></i> Suivi subventions
                          </button>
                          <button class="btn m-2 rounded b-0 menu_lateral text-start">
                            <i class="bi bi-file-music"></i> Suivi évenements
                          </button>
                          <button class="btn m-2 rounded b-0 menu_lateral text-start">
                            <i class="bi bi-people"></i> Suivi volontariat
                          </button>
                          <button class="btn m-2 rounded b-0 menu_lateral text-start">
                            <i class="bi bi-list-columns-reverse"></i> Répertoire Raffineur.euses
                          </button>
                          <button class="btn m-2 rounded b-0 menu_lateral text-start">
                            <i class="bi bi-clipboard-data"></i> tableau de bord perso
                          </button>
                          <button class="btn m-2 rounded b-0 menu_lateral text-start">
                            <i class="bi bi-book"></i> documentation
                          </button>
                        </li>
                      </ul>
                    </div>
                  </nav>
                </div>
              </div>
            </div>
  
  <!-- corp du tableau central -->
           <div class="col">
             <!-- membre + recap -->
              <section class="case">
                  <div class="row case_moyen">
                    <!-- membre du collectif -->
                    <div class="col-md-4">
                      <div class="rose p-2 pt-0 case h-100">
                        <div class="case titre">
                           <OuvrirFermer title="Membre du collectif">
                              <CreationTableau :titre="titre_membres" :rows="rows_membres" :columns="columns_membres"/>
                           </OuvrirFermer>
                        </div>
                      </div>                     
                    </div>
                    
                   <!-- recap budget -->
                    <div class="col-md-8">
                     <div class="orange p-2 pt-0 case h-100">
                      <OuvrirFermer title="Recap budgétaire" class="case titre">
                         <table class="container">
                            <tr>
                            <!-- dépense -->
                            <td class=" case ">  
                                  
                           <div><CreationTableau :titre="titre_recap_depenses" :rows="rows_recap_depenses" :columns="columns_recap_depenses" :showFooter="true"/></div>
                            </td>
                            <!-- recette -->
                            <td class=" case">                           
                              <div><CreationTableau :titre="titre_recap_recettes" :rows="rows_recap_recettes" :columns="columns_recap_recettes" :showFooter="true"/></div>
                            </td>
                            </tr>
                          </table> 
                        </OuvrirFermer>
                      </div> 
                    </div> 
                  </div>
                </section>

  <!-- depense / recette -->
                <div class="container-fluid">
                  <div class="row">
                    <div class="col">
                      <div class="jaune my-3 case">
                          <table class="container">
                            <tr>
                            <!-- dépense -->
                            <td class="case p-2 pt-0">
                               <OuvrirFermer title="Dépenses" class="case titre">
                               <div class="case case_clair p-2 pt-0">
                            
                              <table class="container ">
                                 <div class="case titre">Bienveillance</div>
                                 
                                 <table class=" case">
                                 <tr class=" case flex-container">                                   
                                  <!-- prévisionnel -->
                                  <td class="case h-100">
                                    <div><CreationTableau :titre="titre_prev_bienveillance" :rows="rows_prev_bienveillance" :columns="columns_prev_bienveillance" :showFooter="true"/></div>   
                                  </td>                          
                            
                                  <!-- réel -->
                                  <td class="case h-100">                                
                                    <div><CreationTableau :titre="titre_reel_bienveillance" :rows="rows_reel_bienveillance" :columns="columns_reel_bienveillance" :showFooter="true"/></div>
                                  </td>
                                 </tr>
                               </table>
                              </table> 
                               </div>  
                               </OuvrirFermer>                  
                             </td>                          
                            
                            <!-- recette -->
                            <td class=" p-2">
                              <div class="case titre">Recettes</div>
                               <div class="case case_clair p-2 ">
                                
                              </div>
                            </td>
                            </tr>
                          </table> 
                     </div>


                    </div>
                  </div>
                </div>
              
            </div>
          </div>
        </div>
      </main>
    </div>
  </template>
  
  <script>
import CreationTableau from "@/components/CreationTableau.vue";
import OuvrirFermer from "@/components/OuvrirFermer.vue";


  export default {
    
   components: {
    CreationTableau,
    OuvrirFermer,

  },
    data() {
      return {

      // État du tableau (true: étendu, false: replié)
      showTable: true,  

        //données bandeau
        buttonText: 'groupe / pôle / projet',
        isDropdownOpen: false,
        selectedOption: null,
  
        //données membre du collectif
        titre_membres : "",
        rows_membres: ['Paul', 'Jessica', 'Ben', 'Véronique'],
        columns_membres: [
          { name: 'à valider', styleClass: 'case', input: false }, // La colonne par défaut est sans input
          { name: 'à facturer', styleClass: 'case', input: false }, 
          { name: 'à payer', styleClass: 'case', input: false },
        ],

        //données recap depenses
        titre_recap_depenses : "Dépenses",
        rows_recap_depenses: ['bienveillance', 'presta int.', 'presta.ext / achats', 'dépenses int.'],
        columns_recap_depenses: [
          { name: 'prév', styleClass: 'case', input: false }, // La colonne par défaut est sans input
          { name: 'dépensé', styleClass: 'case', input: false },
          { name: 'reste à dépensé', styleClass: 'case', input: false },
        ],

        //données recap recettes
        titre_recap_recettes : "Recettes",
        rows_recap_recettes: ['suventions / app', 'prestations', 'ventes', 'recette int'],
        columns_recap_recettes: [
          { name: 'prév.', styleClass: 'case', input: false }, // La colonne par défaut est sans input
          { name: 'encaissé', styleClass: 'case', input: false },
          { name: 'reste à encaisser', styleClass: 'case', input: false },
        ],

        //données prévisionnel bienveillance
        titre_prev_bienveillance : "Prévisionnel",
        rows_prev_bienveillance: ['bienveillance'],
        columns_prev_bienveillance: [
          { name: 'Montant', styleClass: 'case', input: true }, // La colonne par défaut est sans input
        
        ],

        //données réel bienveillance
        titre_reel_bienveillance : "Réel",
        rows_reel_bienveillance: ['Paul', 'Jessica'],
        columns_reel_bienveillance: [
          { name: 'date.', styleClass: 'case', input: true }, // La colonne par défaut est sans input
          { name: 'propo.', styleClass: 'case', input: true },
          { name: 'validé', styleClass: 'case', input: true },
          { name: 'factu.', styleClass: 'case', input: true },
          { name: 'payé', styleClass: 'case', input: false },
        ],



      };
    },
  
    computed: {
      
    },
  
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
  
  <style >
  @import url('https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css');
  @import url('https://cdn.jsdelivr.net/npm/bootstrap-icons@1.5.0/font/bootstrap-icons.css');
  
  @import url('https://fonts.googleapis.com/css2?family=Itim&display=swap');
 
  .case.menu_lateral {
    font-family: 'Itim', cursive;
    color :white;
    font-size: larger; 
    border-radius: 20px;
    
  }
  
  .titre 
  {
    font-size: medium; 
  }
  
  .en-tete {
  font-size: 0.9em;
  text-align: center;
  white-space : nowrap;
  }
  
  .case {
    font-family: 'Itim', cursive;
    color :white;
    border-radius: 15px;
    border-collapse: separate;
    border-spacing: 2px;
    

        }

  .case_moyen {
    border-collapse: separate;
    border-spacing: 10px; 
         
    }
  
    .case.case_petite {
      width: 50px;
      height: 25px;
      border-radius: 8px;
      border-spacing: 10px; 
      width: 70px;
         
    }
  
    .case.case_fonce {
      background: rgba(0, 0, 0, .1);
      width: 50px;
    }
  
    .case.case_clair {
          background: rgba(255, 255, 255, .2);
    }

    .case.case_input {
          background: rgba(255, 255, 255, .7);
          border: 0px;
          width: 50px;
          color : rgba(0, 0, 0, .6);

    }

.sidebar {
    width: auto;
   
    
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