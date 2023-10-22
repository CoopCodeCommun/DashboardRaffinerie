
//////////////////////////// menu //////////////////////////

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

// Générer les options du menu déroulant de la navbar
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


//////////////////////////////// Générer les éléments du menu latéral ////////////////////////

 
document.addEventListener("DOMContentLoaded", function() {

    const sidebarMenu = document.getElementById('sidebarMenu');
    if (!sidebarMenu) {
        console.error("L'élément avec l'ID 'sidebarMenu' n'a pas été trouvé.");
        return;
    }

    appData.sidebarOptions.forEach(option => {
        const li = document.createElement('li');
        li.className = 'nav-item';

        const button = document.createElement('button');
        button.className = 'btn m-1 b-0';

        if (option.link && window.location.href.includes(option.link)) {
            button.classList.add('case_clair');
        }

        button.addEventListener('click', () => {
            sidebarMenu.querySelectorAll('.btn').forEach(btn => btn.classList.remove('case_clair'));
            button.classList.add('case_clair');
            if (option.link) {
                window.location.href = option.link;
            }
        });

        if (option.icon) {
            const icon = document.createElement('i');
            icon.className = option.icon;
            button.appendChild(icon);
        }

        const textSpan = document.createElement('span');
        textSpan.className = 'font-weight-bold';
        textSpan.textContent = ` ${option.text}`;

        if (!option.link) {
            textSpan.style.textDecoration = 'line-through';
        }

        button.appendChild(textSpan);
        li.appendChild(button);
        sidebarMenu.appendChild(li);
    });
});

// création des tableaux avec les données de datas.js, vérifie quel page est affiché et charge les données des tableaux corespondants
let groupeTableaux;
if (window.location.href.includes('subventions')) {groupeTableaux = tableaux.subventions;} 
else if (window.location.href.includes('repertoire')) {groupeTableaux = tableaux.repertoire;} 
// else if (window.location.href.includes('organigramme')) {groupeTableaux = tableaux.organigramme;}
else if (window.location.href.includes('suivi_budgetaire')) {groupeTableaux = tableaux.suivi_budgetaire;}
else if (window.location.href.includes('objectifs_indicateurs')) {groupeTableaux = tableaux.objectifs_indicateurs;}  

for (let nom_tableau in groupeTableaux) {
    if (groupeTableaux.hasOwnProperty(nom_tableau)) {
        let tableauData = groupeTableaux[nom_tableau];
        let containerId = nom_tableau;
        createTableComplete(tableauData.titre, tableauData.rows, tableauData.columns, containerId, tableauData.total, tableauData.newline);
    }
}

///////////////////////////   ouvrir/fermer une section  /////////////:::

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

/////////////////////////////// créer une section avec titre qui se replie /////////////////////////
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


/////////////////////////// Creation tableau ////////////////////////////////

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


//option création de nouvelle ligne

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

//option création d'un pied de tableau qui fait les totaux des colonnes

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


// style de case en fonction du type de case

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


//////////////////////////// fonction ouvrir/fermer un tableau /////////////////////////////


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
    fetch('http://localhost:8000/api/comptes/')
    .then(response => response.json())
    .then(data => {
        // Suppose que l'API renvoie un tableau de noms de comptes
        menuOptions = data;
        
        // Après cette étape, vous pourrez utiliser `menuOptions` 
        // pour n'importe quelle autre opération nécessaire dans votre script.
    })
    .catch(error => console.error('Erreur de fetch:', error));
});

