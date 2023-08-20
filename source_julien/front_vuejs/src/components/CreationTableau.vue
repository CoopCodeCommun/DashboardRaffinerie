<template>
  <td class="case case_clair px-2">
    <div class="table-container">
      <table class="case">
        <thead class="en-tete" v-if="tableContent && tableContent.length > 0 && tableContent[0].data && tableContent[0].data.length > 1" >
          <tr>
            <th></th>
            <th v-for="(column, columnIndex) in columns" :key="columnIndex">{{ column.name }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, rowIndex) in tableContent" :key="rowIndex">
            <th>{{ row.name }}</th>
            <td v-for="(cell, cellIndex) in row.data" :key="cellIndex" :class="getCellClass(cell)">
              <!-- Default cell -->
              <div v-if="cell.dropdown === false && cell.userInput === false"  class="case_fonce">
                {{ cell.content }}
              </div>
              <!-- Text input cell -->
              <div v-else-if="cell.userInput !== undefined">
                <input v-model="cell.userInput" class="form-control case case_petite case_input" style="margin: 0;" />
              </div>
              <!-- Dropdown cell -->
              <div v-else-if="cell.dropdown">
                  <select v-bind:value="cell.userInput" @change="cell.userInput = $event.target.value" class="form-control case case_petite case_dropdown" style="margin: 0;">
      <option v-for="option in cell.options" :key="option">{{ option }}</option>
    </select>
              </div>
            </td>
          </tr>
        </tbody>
        <tfoot v-if="showFooter">
          <tr>
            <th style="text-align: end;">Total</th>
            <td style="text-align: center;"
              v-for="(total, totalIndex) in getFooterData()"
              :key="totalIndex"
            >
              {{ total }}
            </td>
          </tr>
        </tfoot>
      </table>
    </div>
  </td>
</template>


<script>
export default {
  props: {
    titre: {
      type: String,
      default: ""
    },
    rows: {
      type: Array,
      default: () => []
    },
    columns: {
      type: Array,
      default: () => []
    },
    showFooter: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      tableContent: this.generateTableContent(),
    };
  },
  methods: {
    generateTableContent() {
  return this.rows.map(row => ({
    name: row,
    data: this.columns.map(column => ({
      content: '',
      userInput: column.input ? '' : undefined, // Si input est false, userInput sera undefined
      dropdown: column.dropdown,
      options: column.options,
      selectedOption: column.dropdown ? column.options[0] : undefined // Ajout de selectedOption
    }))
  }));
},
 getCellClass(cell) {
  if (cell.dropdown) {
    return 'case case_petite'; 
  } else {
    const nonInputClass = cell.userInput === undefined ? 'case case_petite case_fonce padding-class' : '';
    return `${cell.styleClass || 'case'} ${nonInputClass}`;
  }
},

getFooterData() {
  const footerData = Array(this.columns.length).fill(0);

  for (const row of this.tableContent) {
    row.data.forEach((cell, columnIndex) => {
      const cellValue = cell.userInput !== undefined && cell.userInput !== '' ? cell.userInput : cell.content;
      if (!isNaN(parseFloat(cellValue))) {
        footerData[columnIndex] += parseFloat(cellValue);
      }
    });
  }

  return footerData;
},
  },
};
</script>

<style>
  .row-title {
    line-height: 1; /* Ajustez cette valeur pour augmenter ou diminuer l'interligne */
  }
  .table-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.table-container .case.case_clair {
  flex-grow: 1;
}

.case_clair {
  height: 100%;
}

</style>