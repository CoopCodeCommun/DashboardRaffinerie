<template>
  <div>
    <h1>Mon Tableau</h1>
    <CreationTableau
      :buttonText="buttonText"
      :rows="rows"
      :columns="columns"
    />
  </div>

  <div>
    <h1>Mon Tableau</h1>
    <CreationTableau
      :buttonText="buttonText"
      :rows="rows"
      :columns="columns"
    />
  </div>
</template>

<script>
import CreationTableau from "@/components/CreationTableau.vue";

export default {
  components: {
    CreationTableau,
  },

  data() {
    return {
      buttonText: "Critères personnalisés",
        rows: ['Paul', 'Jessica', 'Ben', 'Véronique'],
        columns: [
          { name: 'à valider', styleClass: 'case case_colonne_1', input: false }, // La colonne par défaut est sans input
          { name: 'à facturer', styleClass: 'case case_colonne_2', input: false }, // Vous pouvez choisir la colonne en input
          { name: 'à payer', styleClass: 'case case_colonne_3', input: true },
        ],
    };
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
