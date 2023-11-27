function calculateTotals() {
    var columns = document.querySelectorAll('thead th');
    var totalCells = document.querySelectorAll('.total-cell');
    var rows = document.querySelectorAll('tbody tr:not(.d-none)');

    totalCells.forEach((cell, index) => {
        if (index < columns.length - 1) { // Assurez-vous de ne pas inclure la colonne d'action si elle est présente
            let sum = 0;
            rows.forEach(row => {
                let value = row.cells[index + 1].textContent; // +1 pour compenser la cellule "+ Total"
                sum += parseFloat(value) || 0;
            });
            cell.textContent = sum.toFixed(2);
        }
    });
}

function ajouterLigne() {
    var tableau = document.getElementById('monTableau');
    var nouvelleLigne = tableau.insertRow(-1); // Insère une ligne à la fin du tableau

    // Supposons que vous ayez 4 colonnes
    for (let i = 0; i < 4; i++) {
        let nouvelleCellule = nouvelleLigne.insertCell(i);
        nouvelleCellule.innerHTML = "Nouvelle cellule " + (i + 1);
        // Vous pouvez ajuster le contenu de la cellule selon vos besoins
    }
}




// Exécuter calculateTotals lorsque la page est chargée et à chaque fois que le tableau est mis à jour
document.addEventListener("DOMContentLoaded", calculateTotals);



//////////ancien code plus actif ///////////

//////////////////////////// menu //////////////////////////

// Fonction pour remplir le menu déroulant compte analytique
function populateDropdown() {
    const dropdownMenu = document.getElementById('dropdownMenuOptions');
    const selectedPoleSpan = document.getElementById('selectedPole');

    // Vérifiez si groupe_analytique a des éléments avant de définir le pôle par défaut
    if (groupe_analytique.length > 0) {
        selectedPoleSpan.textContent = groupe_analytique[0].name;
    }

    groupe_analytique.forEach(item => {
        const a = document.createElement('a');
        a.href = "#";
        a.className = "dropdown-item";
        a.textContent = ` ${item.name} `;

        // Écouteur d'événement pour mettre à jour le bouton avec le pôle sélectionné
        a.addEventListener('click', function() {
            selectedPoleSpan.textContent = item.name;
        });

        dropdownMenu.appendChild(a);
    });
}

// Fonction pour remplir le menu déroulant année
function populateYearDropdown() {
    const yearDropdownMenu = document.getElementById('yearDropdownOptions');
    const selectedYearSpan = document.getElementById('selectedYear');

    // Définissez l'année par défaut
    selectedYearSpan.textContent = appData.annees[0];

    appData.annees.forEach(year => {
        const a = document.createElement('a');
        a.href = "#";
        a.className = "dropdown-item";
        a.textContent = year;

        // Écouteur d'événement pour mettre à jour le bouton avec l'année sélectionnée
        a.addEventListener('click', function() {
            selectedYearSpan.textContent = year;
        });

        yearDropdownMenu.appendChild(a);
    });
}

// Exécution des fonctions
fetchAnalyticGroup().then(populateDropdown);
document.addEventListener("DOMContentLoaded", function() {
    populateYearDropdown();
});

//////////////////////////////// Générer les éléments du menu latéral ////////////////////////


document.addEventListener("DOMContentLoaded", function() {

    const sidebarMenu = document.getElementById('sidebarMenu');
    if (!sidebarMenu) {
        console.error("L'élément avec l'ID 'sidebarMenu' n'a pas été trouvé.");
        return;
    }

    appData.sidebarOptions.forEach(option => {
        const li = document.createElement('li');
        li.className = 'nav-item menu-item'; // Ajout de la classe 'menu-item'

        const button = document.createElement('button');
        button.className = 'btn m-1 b-0';


        // lorsqu'on clique sur un menu
        button.addEventListener('click', () => {
            // Fermez tous les autres menus sauf celui-ci
            const allMenus = document.querySelectorAll('.menu-item');
            allMenus.forEach(menu => {
                if (menu !== li) {
                    menu.classList.remove('open');
                }
            });

            if (option.submenu) {
                li.classList.toggle('open');
            }

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

        button.appendChild(textSpan);

        li.appendChild(button);



    // Gestion des sous-menus
    if (option.submenu) {
        const subMenuUl = document.createElement('ul');
        subMenuUl.className = 'submenu';

        option.submenu.forEach(subOption => {
            const subLi = document.createElement('li');
            subLi.className = 'submenu-item';

            const subButton = document.createElement('button');
            subButton.className = 'btn m-1 b-0';

            if (subOption.icon) {
                const subIcon = document.createElement('i');
                subIcon.className = subOption.icon;
                subButton.appendChild(subIcon);
            }

            const subTextSpan = document.createElement('span');
            subTextSpan.className = 'font-weight-bold';
            subTextSpan.textContent = ` ${subOption.text}`;

            // Si le sous-menu n'a pas de lien, barrer le texte
            if (!subOption.link) {
                subTextSpan.classList.add('sousmenusanslien');
            }

            subButton.appendChild(subTextSpan);

            // Ajout de l'événement click pour le sous-menu
            subButton.addEventListener('click', () => {
                if (subOption.link) {
                    window.location.href = subOption.link;
                }
            });

            subLi.appendChild(subButton);
            subMenuUl.appendChild(subLi);
        });

        li.appendChild(subMenuUl);
    }
    sidebarMenu.appendChild(li);
    });
});

// création des tableaux avec les données de datas.js, vérifie quel page est affiché et charge les données des tableaux corespondants
let groupeTableaux;
if (window.location.href.includes('subventions')) {groupeTableaux = tableaux.subventions;} 
else if (window.location.href.includes('repertoire')) {groupeTableaux = tableaux.repertoire;} 
else if (window.location.href.includes('organigramme')) {groupeTableaux = tableaux.organigramme;}
else if (window.location.href.includes('tableau_de_bord_perso')) {groupeTableaux = tableaux.tableau_de_bord_perso;}
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

function getColumnIndicesToHide(columns) {
    return columns.reduce((indices, column, index) => {
        if (column.shouldTotal === false) {
            indices.push(index);
        }
        return indices;
    }, []);
}

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
    th.classList.add('header-text');
    headerRow.appendChild(th);
});
table.appendChild(headerRow);

rows.forEach(row => {
    const tr = document.createElement('tr');
    tr.className = "case_petite";

    const th = document.createElement('th');
    th.className = "case_petite";
    th.textContent = row.name;
    th.style.minWidth = '20px';
    th.classList.add('header-text');

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

    // Si un commentaire est présent pour cette ligne, ajoutez une fonction de basculement
    if (row.commentaire) {
        th.style.cursor = "pointer";  // Changez le curseur pour indiquer qu'il est cliquable
        th.textContent = "+" + row.name;  // Ajoute "+/-" avant le nom de la ligne
        th.onclick = function() {
            const commentRow = this.parentNode.nextElementSibling;
            if (commentRow.style.display === "none") {
                commentRow.style.display = "";
                this.textContent = "-" + row.name;  // Lorsque le commentaire est affiché, montrez uniquement "-"
            } else {
                commentRow.style.display = "none";
                this.textContent = "+" + row.name;  // Lorsque le commentaire est caché, montrez uniquement "+"
            }
        }
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

    if (row.commentaire) {
        const commentRow = document.createElement('tr');
        commentRow.style.display = "none"; // Initialement caché
        commentRow.classList.add('comment-row'); // Ajout de la classe "comment-row"
        const commentCell = document.createElement('td');
        commentCell.colSpan = columns.length + 1;
    
        const commentDiv = document.createElement('div');
        commentDiv.textContent = row.commentaire;
        commentDiv.contentEditable = true; 
        commentDiv.className = "case_clair editable-content";
        commentCell.appendChild(commentDiv);
        commentRow.appendChild(commentCell);
    
        table.appendChild(commentRow);
        
    }

    if (row.subRows && row.subRows.length) {
        row.subRows.forEach(subRow => {
            const subTr = document.createElement('tr');
            subTr.className = "case_petite sub-row";
            subTr.style.display = "none";
            subTr.dataset.parentRow = row.name;

            const subTh = document.createElement('th');
            subTh.className = "case_petite";
            subTh.textContent = subRow.name;
            subTh.classList.add('header-text');
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
    totalHeader.classList.add('header-text');        
    totalHeader.style.cursor = 'pointer'; // Assurez-vous que le curseur est une main lorsque vous survolez "Total" ou "+/-"
    totalHeader.style.minWidth = '50px'; // Ajustez la largeur minimale selon vos besoins
    totalHeader.style.whiteSpace = 'nowrap'; // Empêche le texte de passer à la ligne suivante
    totalHeader.style.overflow = 'visible'; // Gère le débordement du contenu

    totalHeader.textContent = '+ Total'; // Commencez avec "+ Total"

    //cacher les lignes et colonnes sans total quand on clique sur total
    totalHeader.onclick = function() {
        const isCollapsed = totalHeader.textContent.startsWith('+');
        const rowsToToggle = Array.from(table.querySelectorAll('tr:not(:first-child):not(.total-row)'));
        const columnIndicesToHide = getColumnIndicesToHide(columns);

        console.log(columnIndicesToHide);
        
        rowsToToggle.forEach(row => {
            row.style.display = isCollapsed ? '' : 'none';
        });
    
        columnIndicesToHide.forEach(columnIndex => {
            for (let row of table.rows) {
                const cell = row.cells[columnIndex + 1];
                if (cell) {
                    cell.style.display = isCollapsed ? '' : 'none';
                }
            }
        });
    
        totalHeader.textContent = isCollapsed ? '- Total' : '+ Total';

        //fermer les commentaires
        const commentRows = Array.from(table.querySelectorAll('tr.comment-row')); // supposez que chaque ligne de commentaire a la classe "comment-row"
        commentRows.forEach(commentRow => {
        commentRow.style.display = "none";
    });
}
    
    totalRow.appendChild(totalHeader);

    columns.forEach((column, columnIndex) => {
        const td = document.createElement('td');
        td.style.textAlign = 'center';
        td.style.verticalAlign = 'middle';

        if (column.shouldTotal !== false) {
            let sum = 0;
            td.className = "case_petite case_fonce";

            for (let i = 0; i < rows.length; i++) {
                const currentRow = table.rows[i + 1];
    
                // Vérifiez si c'est une rangée de commentaire, et si c'est le cas, passez à la prochaine itération
                if (currentRow.classList.contains('comment-row')) {
                    continue;
                }
                const cell = currentRow.cells[columnIndex + 1];
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

    // Cachez initialement toutes les rangées sauf la rangée totale
    const rowsToHide = Array.from(table.querySelectorAll('tr:not(:first-child):not(.total-row)'));
    rowsToHide.forEach(row => {
        row.style.display = 'none';
    });

    // Cachez initialement les colonnes dont shouldTotal est false
    const columnIndicesToHide = getColumnIndicesToHide(columns);
    columnIndicesToHide.forEach(columnIndex => {
        for (let row of table.rows) {
            const cell = row.cells[columnIndex + 1];
            if (cell) {
                cell.style.display = 'none';
            }
        }
    });
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
