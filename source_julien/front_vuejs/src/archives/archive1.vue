<template>
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
  
  <!-- menu lateral -->
        <div class="container-fluid">
          <div class="row g-1">
            <div class=" col-md-2 case">
              <div class="container-fluid">
                <div class="row">
                  <nav class="p-0 vert sidebar case">
                    <div class="sidebar-sticky">
                      <ul class="nav flex-column">
                        <li class="nav-item">
                          <button class="btn m-2 rounded b-0 menu_lateral text-start">
                            <i class="bi bi-clipboard-data"></i> Tableau de bord
                          </button>
                          <button class="btn m-2 rounded b-0 menu_lateral text-start">
                            <i class="bi bi-currency-euro"></i> Suivi budgétaire
                          </button>
                          <button class="btn m-2 rounded b-0 menu_lateral text-start">
                            <i class="bi bi-piggy-bank"></i> Plan de trésorerie
                          </button>
                          <button class="btn m-2 rounded b-0 menu_lateral text-start">
                            <i class="bi bi-cash-coin"></i> Suivi  subventions
                          </button>
                        </li>
                      </ul>
                    </div>
                  </nav>
                </div>
              </div>
            </div>
  
  <!-- corp du tableau -->
            <div class="col">
              <section>
                <div class="container-fluid ">
                  <div class="row g-3 ">
                  
              <!-- membre du collectif -->
                    <div class="col-md-5 ">
                      <div class="rose p-2 case ">
                        <div class="case titre">Membre du collectif</div>
                        <div class="case case_clair p-2 ">
  
                        <!-- création des intitulés -->
                            <div>
    <CreationTableau
      :buttonText="buttonText"
      :rows="rows"
      :columns="columns"
    />
  </div>
  
                          <div>Ajouter membre</div>
                        </div>                      
                      </div>
                    </div>
                    
  <!-- recap budget -->
                    <div class="col">
                      <div class="orange p-2 case" style="height: 100%;">
                        <div class="case titre">Recap budgétaire</div>
                          <table class="">
                            <tr>
                            <!-- dépense -->
                            <td class=" case case_clair p-4">
                                                      <div class="case titre">Membre du collectif</div>
                        <div class="case case_clair p-2 ">
  
                        <!-- création des intitulés -->
                          <table class="case en-tete">
                             <thead>
                               <tr> <th></th>
                                   <th v-for="(column, columnIndex) in columns" :key="columnIndex">{{ column.name }}</th></tr>
                              </thead>
                         <tbody>
                         <tr v-for="(row, rowIndex) in tableContent" :key="rowIndex">
                            <!-- création des lignes -->
                               <th>{{ row.name }}</th>
                            <!-- création des colonnes -->
                         <td
                            v-for="(cell, cellIndex) in row.data"
                            :key="cellIndex"
                            :class="getCellClass(cell)"
                             >
              <!-- Utiliser v-html pour afficher le contenu généré par la méthode 'getCellContent' -->
              <span v-html="getCellContent(cell)"></span>
            </td>
          </tr>
        </tbody>
       </table>
  
                          <div>Ajouter membre</div>
                        </div>                      
                      
                            </td>                          
                            
                            <!-- recette -->
                            <td class=" case case_clair p-4">
                            
                            </td>
                            </tr>
  
                         </table> 
                      </div>  
                    </div>
                  </div>
                </div>
                
  <!-- depense / recette -->
                <div class="container-fluid">
                  <div class="row">
                    <div class="col">
                      <div class="jaune py-5 my-3 case"></div>
                    </div>
                  </div>
                </div>
              </section>
            </div>
          </div>
        </div>
      </main>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        //données bandeau
        buttonText: 'groupe / pôle / projet',
        isDropdownOpen: false,
        selectedOption: null,
  
        //données membre du collectif
        rows: ['Paul', 'Jessica', 'Ben', 'Véronique'],
        columns: [
          { name: 'à valider', styleClass: 'case case_colonne_1', input: false }, // La colonne par défaut est sans input
          { name: 'à facturer', styleClass: 'case case_colonne_2', input: false }, // Vous pouvez choisir la colonne en input
          { name: 'à payer', styleClass: 'case case_colonne_3', input: false },
        ],
      };
    },
  
    computed: {
      tableContent() {
        return this.maFonction(this.rows, this.columns);
      },
    },
  
    methods: {
  
      //bandeau
      toggleDropdown() {
        this.isDropdownOpen = !this.isDropdownOpen;
      },
      selectOption(option) {
        this.selectedOption = option;
        this.isDropdownOpen = false;
      },
  
      //construction tableau
      maFonction(rows, columns) {
        return rows.map((name, rowIndex) => {
          return {
            name,
            data: columns.map((column, columnIndex) => {
              if (column.input) {
                return {
                  content: '', // Ne pas mettre de contenu par défaut pour les cellules de la colonne en input
                  styleClass: column.styleClass || 'case',
                  userInput: '' // Ajouter une propriété pour stocker les données saisies par l'utilisateur
                };
              } else {
                return {
                  content: `Data ${rowIndex + 1}-${columnIndex}`,
                  styleClass: column.styleClass || 'case'
                };
              }
            })
          };
        });
      },
      getCellContent(cell) {
        // Générer le contenu de chaque cellule en fonction de la logique définie dans la méthode
        if (cell.userInput !== undefined) {
          return `<input v-model="cell.userInput" class="form-control case case_petite " />`;
        } 
      },
      getCellClass(cell) {
        // Obtenir la classe de style pour la cellule en fonction de la propriété 'input'
        const nonInputClass = cell.userInput === undefined ? 'case_petite case case_fonce' : '';
        return `${cell.styleClass || 'case'} ${nonInputClass}`;
      },
    },
  };
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
    font-size: larger; 
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
  
    .case.case_petite {
      width: 100px;
      border-radius: 8px;
      border-spacing: 10px; 
      width: 70px;
         
    }
  
    .case.case_fonce {
      background: rgba(0, 0, 0, .1);
    }
  
    .case.case_clair {
          background: rgba(255, 255, 255, .2);
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