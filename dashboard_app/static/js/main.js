// les différentes data
const appData = {
    //les différent pôles dans le menu supérieur
    menuOptions: ['vélo', 'Groupe Culture', 'Micro recyclerie', 'champignonnière'],
    // les différents menu dans la barre latéral
    sidebarOptions: [
    { icon: 'bi bi-bar-chart-line', text: 'Tableau de bord', link: 'dashboard_app/templates/tableau_de_bord.html'},
    { icon: 'bi bi-person-video2', text: 'organigramme des rôles' },
    { icon: 'bi bi-currency-euro', text: 'Suivi budgétaire', link: 'dashboard_app/templates/suivi_budgetaire.html' },
    { icon: 'bi bi-piggy-bank', text: 'Plan de trésorerie' },
    { icon: 'bi bi-cash-coin', text: 'Suivi subventions' },
    { icon: 'bi bi-file-music', text: 'Suivi évenements' },
    { icon: 'bi bi-list-ol', text: 'Suivi volontariat' },
    { icon: 'bi bi-people', text: 'Répertoire Raffineur.euses' },
    { icon: 'bi bi-clipboard-data', text: 'Tableau de bord perso' },
    { icon: 'bi bi-book', text: 'Documentation' },
    ],

    //suivi budgétaire
        //données membre du collectif
        titre_membres: "",
        total_membres: false,
        newline_membres: true,
        rows_membres: [{ name: 'Paul' },{ name: 'Jessica' },{ name: 'Bob' },{ name: 'Marcel' }],
        columns_membres: [
            { name: 'à valider', },
            { name: 'à facturer',  },
            { name: 'à payer',  },
        ],

        //données recap depenses
        titre_recap_depenses : "Dépenses",
        total_recap_depenses: false,
        newline_recap_depenses: false,
        rows_recap_depenses: [{ name:'bienveillance' },{ name: 'presta int.' },{ name: 'presta.ext / achats' },{ name: 'dépenses int.'}],
        columns_recap_depenses: [
            { name: 'prév', }, 
            { name: 'dépensé', },
            { name: 'reste à dépensé',},
        ],

        //données recap recettes
        titre_recap_recettes : "Recettes",
        total_recap_recettes: true,
        newline_recap_recettes: false,
        rows_recap_recettes: ['suventions / app', 'prestations', 'ventes', 'recette int'].map(name => ({ name })),
        columns_recap_recettes: [
            { name: 'prév.',}, 
            { name: 'encaissé',},
            { name: 'reste à encaisser',},
        ],

        //données prévisionnel bienveillance
    titre_prev_bienveillance : "Prévisionnel",
    total_prev_bienveillance: true,
    newline_prev_bienveillance: true,
    rows_prev_bienveillance: ['bienvei- llance'].map(name => ({ name })),
    columns_prev_bienveillance: [
      { name: 'Montant', input: true,},
    ],

    //données réel bienveillance
    titre_reel_bienveillance : "Réel",
    total_reel_bienveillance: true,
    newline_reel_bienveillance: true,
    rows_reel_bienveillance: ['Paul', 'Jessica', 'kevin'].map(name => ({ name })),
    columns_reel_bienveillance: [
      { name: 'date', input: true, shouldTotal: false  },
      { name: 'propo.', input: true, },
      { name: 'validé', input: true, },
      { name: 'factu.', input: true, },
      { name: 'payé', },
    ],

    //données prévisionnel prestations internes
    titre_prev_prestations_internes : "Prévisionnel",
    total_prev_prestations_internes: true,
    newline_prev_prestations_internes: true,
    rows_prev_prestations_internes: ['bienveillance', 'animation ateliers', 'entretien matériel'].map(name => ({ name })),
    columns_prev_prestations_internes: [
      { name: 'Montant', input: true, },
    ],

    //données réel prestation interne
    titre_reel_prestations_internes : "Réel",
    total_reel_prestations_internes: true,
    newline_reel_prestations_internes: true,
    rows_reel_prestations_internes: [ 'Jessica', 'kevin'].map(name => ({ name })),
    columns_reel_prestations_internes: [
      { name: 'date', input: true, shouldTotal: false}, 
      { name: 'propo.', input: true, },
      { name: 'validé', input: true, },
      { name: 'factu.', input: true, },
      { name: 'payé', input: false, },
    ],

    //données prévisionnel prestations externes
    titre_prev_prestations_externes : "Prévisionnel",
    total_prev_prestations_externes: true,
    newline_prev_prestations_externes: true,
    rows_prev_prestations_externes: ['achat matériel','prestataires externes'].map(name => ({ name })),
    columns_prev_prestations_externes: [
      { name: 'Montant', input: true, }, 
    ],

    //données réel prestation externes
    titre_reel_prestations_externes : "Réel",
    total_reel_prestations_externes: true,
    newline_reel_prestations_externes: false,
    rows_reel_prestations_externes: [ 'Ravate', 'run market', 'SARL Payet'].map(name => ({ name })),
    columns_reel_prestations_externes: [
      { name: 'intitulé', shouldTotal: false },
      { name: 'date', shouldTotal: false,},
      { name: 'validé',},
      { name: 'payé',},
    ],

    //données prévisionnel dépenses interne
    titre_prev_depenses_internes : "Prévisionnel",
    total_prev_depenses_internes: true,
    newline_prev_depenses_internes: true,
    rows_prev_depenses_internes: ['pôle culture','inter-formation', 'micro-recylerie'].map(name => ({ name })),
    columns_prev_depenses_internes: [
      { name: 'Montant', input: true, }, 
    ],

    //données réel dépenses interne
    titre_reel_depenses_internes : "Réel",
    total_reel_depenses_internes: true,
    newline_reel_depenses_internes: true,
    rows_reel_depenses_internes: [ 'Dépenses interne'].map(name => ({ name })),
    columns_reel_depenses_internes: [
      { name: 'pôle', dropdown: true,  options: ['Option 1', 'Option 2', 'Option 3'], shouldTotal: false, },
      { name: 'date', input: true, shouldTotal: false,},
      { name: 'montant', input: true,  },          
    ],

    //données suivi recap dépenses
    titre_suivi_recap_depenses : "Recap",
    total_suivi_recap_depenses: false,
    newline_suivi_recap_depenses: false,
    rows_suivi_recap_depenses: [ 'Recap'].map(name => ({ name })),
    columns_suivi_recap_depenses: [
      { name: 'prévisionnel', },
      { name: 'réel', },
      { name: 'rest à dépenser', },          
    ],

     //données prévisionnel subvention
    titre_prev_subvention : "Prévisionnel",
    total_prev_subvention: true,
    newline_prev_subvention: true,
    rows_prev_subvention: ['subventions'].map(name => ({ name })),
    columns_prev_subvention: [
      { name: 'Montant', input: true, }, // La colonne par défaut est sans input
    ],

     //données réel subvention
    titre_reel_subvention : "Réel",
    total_reel_subvention : true,
    newline_reel_subvention : false,
    rows_reel_subvention: [ 'Région', 'Mairie'].map(name => ({ name })),
    columns_reel_subvention: [
      { name: 'Date',  shouldTotal: false},
      { name: 'Montant', },          
    ],

    //données prévisionnel prestations
    titre_prev_prestations : "Prévisionnel",
    total_prev_prestations: true,
    newline_prev_prestations: true,
    rows_prev_prestations: ['divers prestations'].map(name => ({ name })),
    columns_prev_prestations: [
      { name: 'Montant', input: true,  }, 
    ],

     //données réel prestations
    titre_reel_prestations : "Réel",
    total_reel_prestations: true,
    newline_reel_prestations: false,
    rows_reel_prestations: [ 'asso rvp', 'SARL dudu'].map(name => ({ name })),
    columns_reel_prestations: [
      { name: 'Date', shouldTotal: false},
      { name: 'Montant', },          
    ],


     //données prévisionnel ventes
    titre_prev_ventes : "Prévisionnel",
    total_prev_ventes: true,
    newline_prev_ventes: true,
    rows_prev_ventes: ['Ventes en direct'].map(name => ({ name })),
    columns_prev_ventes: [
        { name: 'Montant', input: true,}, 
    ],

     //données réel ventes
    titre_reel_ventes : "Réel",
    total_reel_ventes: true,
    newline_reel_ventes: false,
    rows_reel_ventes: [ 'vente en direct', 'asso hoareau'].map(name => ({ name })),
    columns_reel_ventes: [
      { name: 'Date', shouldTotal: false},
      { name: 'Montant', },          
    ],


     //données prévisionnel recettes internes
    titre_prev_recettes_internes : "Prévisionnel",
    total_prev_recettes_internes: true,
    newline_prev_recettes_internes: true,
    rows_prev_recettes_internes: ['divers pôles'].map(name => ({ name })),
    columns_prev_recettes_internes: [
      { name: 'Montant', input: true, }, // La colonne par défaut est sans input
    ],

     //données réel dépenses internes
    titre_reel_recettes_internes : "Réel",
    total_reel_recettes_internes: true,
    newline_reel_recettes_internes: true,
    rows_reel_recettes_internes: [ ' ', ' '].map(name => ({ name })),
    columns_reel_recettes_internes: [
      { name: 'Pôles', dropdown: true, shouldTotal: false},
      { name: 'Date', input: true, shouldTotal: false},
      { name: 'Montant', input: true, },          
    ],

};

// menu 
function showLoginForm() {
    document.getElementById('loginForm').style.display = 'block';
}
function hideLoginForm() {
    document.getElementById('loginForm').style.display = 'none';
}
function updateButtonText(element) {
    const buttonText = element.textContent || element.innerText;
    document.getElementById('dropdownMenuButton').textContent = buttonText;
}

// Générer les options du menu déroulant
const dropdownMenu = document.getElementById('dropdownMenuOptions');
appData.menuOptions.forEach(option => {
    const optionElement = document.createElement('a');
    optionElement.className = 'dropdown-item';
    optionElement.href = '#';
    optionElement.textContent = option;
    optionElement.onclick = function() {
        updateButtonText(option);
    };
    dropdownMenu.appendChild(optionElement);
});
function updateButtonText(text) {
    document.getElementById('dropdownMenuButton').textContent = text;
}

    // Générer les éléments du menu latéral
const sidebarMenu = document.getElementById('sidebarMenu');

appData.sidebarOptions.forEach(menuItem => {
const li = document.createElement('li');
li.className = 'nav-item';

const button = document.createElement('button');
button.className = 'btn m-1 b-0';

// Gestionnaire d'événement pour ajouter le style 'case_clair' lors du clic
button.addEventListener('click', function() {
     // Retirer le style 'case_clair' de tous les autres boutons
    sidebarMenu.querySelectorAll('.btn').forEach(btn => {
        btn.classList.remove('case_clair');
});

// Ajouter le style 'case_clair' au bouton actuellement cliqué
    button.classList.add('case_clair');

  // Charger le contenu dans le bloc de contenu
  if (menuItem.link) {
$.ajax({
  url: 'chemin/vers/une/page.html', 
  success: function(data) { 
    console.log('Success:', data); 
    $('#content-block-id').html(data); 
  }, 
  error: function(error) { 
    console.error('Error:', error); 
  }
});
  }
});

const icon = document.createElement('i');
icon.className = menuItem.icon;
button.appendChild(icon);

const textNode = document.createTextNode(` ${menuItem.text}`);
const textSpan = document.createElement('span');
textSpan.className = 'font-weight-bold';
textSpan.appendChild(textNode);
button.appendChild(textSpan);

li.appendChild(button);
sidebarMenu.appendChild(li);
});

//ouvrir/fermer une section
function toggleContent(element) {
const contentDiv = element.nextElementSibling;
const toggleSign = element.querySelector("#toggleSign");

if (contentDiv.style.display === "none" || !contentDiv.style.display) {
    contentDiv.style.display = "block";
    toggleSign.textContent = "-";
} else {
    contentDiv.style.display = "none";
    toggleSign.textContent = "+";
}
}

//créer une section avec titre toggle
class CreateToggle extends HTMLElement {
connectedCallback() {
    this.style.cursor = "pointer";
    this.addEventListener('click', this.toggleContent);

    let content = this.nextElementSibling;
    content.style.display = "block";  // Assurez-vous que le contenu est affiché par défaut

    const span = document.createElement("span");
    span.textContent = "-";  // Initialisez avec - puisque le contenu est visible
    this.appendChild(span);
    this.appendChild(document.createTextNode(` ${this.getAttribute('title')}`));
}

toggleContent = () => {
    let content = this.nextElementSibling;
    const span = this.querySelector("span"); // Assurez-vous de sélectionner le bon span

    if (content.style.display === "none") {
        content.style.display = "block";
        span.textContent = "-";
    } else {
        content.style.display = "none";
        span.textContent = "+";
    }
}
}

customElements.define('create-toggle', CreateToggle);




// Creation tableau
function createTableComplete(titre, rows, columns, containerId, total, newline) {
const container = document.getElementById(containerId);

const tableDiv = document.createElement('div');
tableDiv.id = 'tableau_content';
tableDiv.classList.add('case_clair', 'h-100');
tableDiv.style.margin = '0px';

const titleElement = document.createElement('div');
titleElement.style.fontWeight = 'bold';
titleElement.style.marginTop = '0px';
titleElement.style.padding = '5px 0px 0px 10px';
titleElement.textContent = titre;
tableDiv.appendChild(titleElement);

const table = document.createElement('table');
table.className = "table no-border table-spacing";

const headerRow = document.createElement('tr');
const firstHeader = document.createElement('th');
headerRow.appendChild(firstHeader);

columns.forEach(column => {
    const th = document.createElement('th');
    th.textContent = column.name;
    headerRow.appendChild(th);
});
table.appendChild(headerRow);

rows.forEach(row => {
    const tr = document.createElement('tr');
    tr.className = "case_petite";

    const th = document.createElement('th');
    th.className = "case_petite";
    th.textContent = row.name;

    if (row.subRows && row.subRows.length > 0) {
        const toggleButton = document.createElement('button');
        toggleButton.textContent = "+";
        toggleButton.onclick = function () {
            const subRows = Array.from(table.querySelectorAll('.sub-row'));
            const relatedSubRows = subRows.filter(subRow => subRow.dataset.parentRow === row.name);
            relatedSubRows.forEach(subRow => {
                if (subRow.style.display === "none") {
                    subRow.style.display = "";
                    toggleButton.textContent = "-";
                } else {
                    subRow.style.display = "none";
                    toggleButton.textContent = "+";
                }
            });
        };
        th.appendChild(toggleButton);
    }

    tr.appendChild(th);

    columns.forEach((column, columnIndex) => {
    const td = document.createElement('td');
    td.className = "case_petite";

    if (column.input) {
        const input = document.createElement('input');
        input.type = 'text';
        input.className = "form-control case_clair case_petite";
            input.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    e.preventDefault(); // Empêcher le comportement par défaut (soumission du formulaire, etc.)
                    this.blur(); // Retirer le focus de l'élément input (cela "validera" la cellule en enlevant le curseur de texte)
                }
                });
            addEventListenerToCell(input, columnIndex, table, columns);
            td.appendChild(input);
    } else if (column.dropdown) {
        const select = document.createElement('select');
        select.className = "form-control case_clair case_petite";
           // Création des options et ajout à l'élément select
        column.options.forEach(option => {
            const optionElement = document.createElement('option');
            optionElement.value = option;
            optionElement.textContent = option;
            select.appendChild(optionElement);
        });

        addEventListenerToCell(select, columnIndex, table, columns);
        td.appendChild(select);
    } else {
            td.className += " case_fonce";
        }
        tr.appendChild(td);
    });

    table.appendChild(tr);

    if (row.subRows && row.subRows.length) {
        row.subRows.forEach(subRow => {
            const subTr = document.createElement('tr');
            subTr.className = "case_petite sub-row";
            subTr.style.display = "none";
            subTr.dataset.parentRow = row.name;

            const subTh = document.createElement('th');
            subTh.className = "case_petite";
            subTh.textContent = subRow.name;
            subTr.appendChild(subTh);

            columns.forEach(() => {
                const subTd = document.createElement('td');
                subTd.className = "case_petite case_fonce";
                subTr.appendChild(subTd);
            });

            table.appendChild(subTr);
        });
    }
});

if (newline) {
    const addButtonRow = document.createElement('tr');
    const addButtonCell = document.createElement('td');
    addButtonCell.colSpan = columns.length + 1;

    const addButton = document.createElement('button');
    addButton.textContent = "Ajouter ligne +";
    addButton.style.background = 'none';
    addButton.style.border = 'none';
    addButton.style.cursor = 'pointer';
    addButton.style.fontSize = '0.9em';
    addButton.style.outline = 'none';

    addButton.onclick = function () {
        if (addButton.textContent === "Ajouter ligne +") {
            addButton.textContent = "Valider";
            addRow(table, columns, total);
        } else if (addButton.textContent === "Valider") {
            addButton.textContent = "Ajouter ligne +";

            let newRow;
            if (total) {
                newRow = table.querySelector('tr:last-child').previousElementSibling.previousElementSibling;
            } else {
                newRow = table.querySelector('tr:last-child').previousElementSibling;
            }
            const titleInput = newRow.querySelector('th:first-child input');

            if (titleInput) {
                const titleText = titleInput.value;
                const newTh = document.createElement('th');
                newTh.className = "case_petite";
                newTh.textContent = titleText;
                newRow.replaceChild(newTh, newRow.querySelector('th:first-child'));
            }
        }
    };

    addButtonCell.appendChild(addButton);
    addButtonRow.appendChild(addButtonCell);
    table.appendChild(addButtonRow);
}

if (total) {
const totalRow = document.createElement('tr');
totalRow.className = "case_petite total-row";

const totalHeader = document.createElement('td');
totalHeader.style.textAlign = 'right';
totalHeader.style.verticalAlign = 'middle';  
totalHeader.style.fontWeight = 'bold';       
totalHeader.textContent = 'Total';
totalRow.appendChild(totalHeader);

columns.forEach((column, columnIndex) => {
    const td = document.createElement('td');
    td.style.textAlign = 'center';
    td.style.verticalAlign = 'middle';

    if (column.shouldTotal !== false) {
        let sum = 0;
        td.className = "case_petite case_fonce";

        for (let i = 0; i < rows.length; i++) {
            const cell = table.rows[i + 1].cells[columnIndex + 1];
            const inputElement = cell.querySelector('input');
            let cellValue;
            if (inputElement) {
                cellValue = parseFloat(inputElement.value || 0);
            } else {
                cellValue = parseFloat(cell.textContent || cell.innerText || 0);
            }
            if (!isNaN(cellValue)) {
                sum += cellValue;
            }
        }
        td.textContent = sum.toFixed(0);
    } else {
        td.textContent = '';
        td.className = "case_petite"; 
    }

    totalRow.appendChild(td);
});
table.appendChild(totalRow);
}

tableDiv.appendChild(table);
container.appendChild(tableDiv);
}

function addEventListenerToCell(element, columnIndex, table, columns) {
element.oninput = function () {
    updateTotals(table, columns);
};
}

function updateTotals(table, columns) {
const totalRow = table.querySelector('.total-row');
const rowsExceptTotalAndAdd = Array.from(table.querySelectorAll('tr:not(.total-row):not(:last-child)'));
const columnIndicesToTotal = columns.reduce((indices, column, index) => {
if (column.shouldTotal !== false) {
indices.push(index);
}
return indices;
}, []);

columnIndicesToTotal.forEach((columnIndex, arrayIndex) => {
    let total = 0;
rowsExceptTotalAndAdd.forEach(row => {
const cell = row.cells[columnIndex + 1];
if (cell) {
const input = cell.querySelector('input');
if (input) {
const value = parseFloat(input.value);
if (!isNaN(value)) {
total += value;
}
}
}
});
const totalCell = totalRow.cells[columnIndex + 1];
    if (totalCell) {
        totalCell.textContent = total.toFixed(2);
        totalCell.style.textAlign = 'center';  // Centrer le texte dans la cellule
        totalCell.style.verticalAlign = 'middle';  // Centrer le texte verticalement
    }
});
}

function addRow(table, columns, total) {
const tr = document.createElement('tr');
tr.className = "case_petite";

const th = document.createElement('th');
th.className = "case_petite";

const inputTitle = document.createElement('input');
inputTitle.type = 'text';
inputTitle.className = "form-control case_clair case_petite";  // Style d'input

th.appendChild(inputTitle);
tr.appendChild(th);

columns.forEach(column => {
    const td = document.createElement('td');
    td.className = "case_petite";

    if (column.dropdown) {
        const select = document.createElement('select');
        select.className = "form-control case_clair case_petite";
        td.appendChild(select);
    } else if (column.input) {
        const input = document.createElement('input');
        input.type = 'text';
        input.className = "form-control case_clair case_petite";
        td.appendChild(input);
    } else {
        td.className += " case_fonce";
    }
    tr.appendChild(td);
});

const addButtonRow = table.querySelector('.add-button-row');
if (total) {
    table.insertBefore(tr, table.lastChild.previousElementSibling);
    table.appendChild(addButtonRow);  // Déplacer la ligne du bouton d'ajout à la fin du tableau
} else {
    table.insertBefore(tr, table.lastChild);
    table.appendChild(addButtonRow);  // Déplacer la ligne du bouton d'ajout à la fin du tableau
}

if (total) {
updateTotals(table, columns);
}
}

// Appel des focntions de tableaux
createTableComplete(appData.titre_membres, appData.rows_membres, appData.columns_membres, 'tableau_membre_collectif', appData.total_membres, appData.newline_membres);
createTableComplete(appData.titre_recap_depenses, appData.rows_recap_depenses, appData.columns_recap_depenses, 'tableau_recap_depenses', appData.total_recap_depenses, appData.newline_recap_depenses);
createTableComplete(appData.titre_recap_recettes, appData.rows_recap_recettes, appData.columns_recap_recettes, 'tableau_recap_recettes', appData.total_recap_recettes, appData.newline_recap_recettes);

// suivi détaillé
createTableComplete(appData.titre_prev_bienveillance, appData.rows_prev_bienveillance, appData.columns_prev_bienveillance, 'tableau_prev_bienveillance', appData.total_prev_bienveillance, appData.newline_prev_bienveillance);
createTableComplete(appData.titre_reel_bienveillance, appData.rows_reel_bienveillance, appData.columns_reel_bienveillance, 'tableau_reel_bienveillance', appData.total_reel_bienveillance, appData.newline_reel_bienveillance);
createTableComplete(appData.titre_prev_prestations_internes, appData.rows_prev_prestations_internes, appData.columns_prev_prestations_internes, 'tableau_prev_prestations_internes', appData.total_prev_prestations_internes, appData.newline_prev_prestations_internes);
createTableComplete(appData.titre_reel_prestations_internes, appData.rows_reel_prestations_internes, appData.columns_reel_prestations_internes, 'tableau_reel_prestations_internes', appData.total_reel_prestations_internes, appData.newline_reel_prestations_internes);
createTableComplete(appData.titre_prev_prestations_externes, appData.rows_prev_prestations_externes, appData.columns_prev_prestations_externes, 'tableau_prev_prestations_externes', appData.total_prev_prestations_externes, appData.newline_prev_prestations_externes );
createTableComplete(appData.titre_reel_prestations_externes, appData.rows_reel_prestations_externes, appData.columns_reel_prestations_externes, 'tableau_reel_prestations_externes', appData.total_reel_prestations_externes, appData.newline_reel_prestations_externes);
createTableComplete(appData.titre_prev_depenses_internes, appData.rows_prev_depenses_internes, appData.columns_prev_depenses_internes, 'tableau_prev_depenses_internes', appData.total_prev_depenses_internes, appData.newline_prev_depenses_internes);
createTableComplete(appData.titre_reel_depenses_internes, appData.rows_reel_depenses_internes, appData.columns_reel_depenses_internes, 'tableau_reel_depenses_internes', appData.total_reel_depenses_internes, appData.newline_reel_depenses_internes);
createTableComplete(appData.titre_prev_subvention, appData.rows_prev_subvention, appData.columns_prev_subvention, 'tableau_prev_subvention', appData.total_prev_subvention, appData.newline_prev_subvention);
createTableComplete(appData.titre_reel_subvention, appData.rows_reel_subvention, appData.columns_reel_subvention, 'tableau_reel_subvention', appData.total_reel_subvention, appData.newline_reel_subvention);
createTableComplete(appData.titre_prev_prestations, appData.rows_prev_prestations, appData.columns_prev_prestations, 'tableau_prev_prestations', appData.total_prev_prestations, appData.newline_prev_prestations);
createTableComplete(appData.titre_reel_prestations, appData.rows_reel_prestations, appData.columns_reel_prestations, 'tableau_reel_prestations', appData.total_reel_prestations, appData.newline_reel_prestations);
createTableComplete(appData.titre_prev_ventes, appData.rows_prev_ventes, appData.columns_prev_ventes, 'tableau_prev_ventes', appData.total_prev_ventes, appData.newline_prev_ventes);
createTableComplete(appData.titre_reel_ventes, appData.rows_reel_ventes, appData.columns_reel_ventes, 'tableau_reel_ventes', appData.total_reel_ventes, appData.newline_reel_ventes);
createTableComplete(appData.titre_prev_recettes_internes, appData.rows_prev_recettes_internes, appData.columns_prev_recettes_internes, 'tableau_prev_recettes_internes', appData.total_prev_recettes_internes, appData.newline_prev_recettes_internes);
createTableComplete(appData.titre_reel_recettes_internes, appData.rows_reel_recettes_internes, appData.columns_reel_recettes_internes, 'tableau_reel_recettes_internes', appData.total_reel_recettes_internes, appData.newline_reel_recettes_internes);



//fonction ouvrir/fermer un tableau
function toggleSection(element) {
const content = element.nextElementSibling;
if (content.style.display === "none" || !content.style.display) {
    content.style.display = "block";
    element.querySelector(".toggleSign").textContent = "-";
} else {
    content.style.display = "none";
    element.querySelector(".toggleSign").textContent = "+";
}
}

 document.addEventListener("DOMContentLoaded", function() {
// Vos appels à createTableComplete vont ici
});

