<template>
  <div class="collapsible-panel">
    <div class="panel-header" ref="panelHeader">
      <div class="search-input-button">
        <input type="text" v-model="fullSearchQuery" @keyup.enter="searchStepOne"
          @input="fetchSpellCheckQuery(); fetchAutocompleteResults();"
          @focus="currentFocusedInput = 'fullSearchQuery'; isDropdownVisible = true; updateDropdownPosition($event)"
          @blur="hideDropdown; isDropdownVisible = false" placeholder="Enter the search query..."
          class="search-input" />
        <button @click="searchStepOne" class="search-button"></button>
      </div>
      <button @click="toggle" class="advanced-search-button">Advanced<br>Search</button>
    </div>
    <div class="autocomplete-container" v-show="isDropdownVisible" ref="autocompleteContainer">
      <ul v-if="isDropdownVisible && (spellCheckedQuery || autocompleteResults.length)" class="autocomplete-dropdown">
        <li v-if="spellCheckedQuery && spellCheckedQuery !== query">
          <a href="#" @click.prevent="updateQuery(spellCheckedQuery)">
            <em>Did you mean:</em> {{ spellCheckedQuery }}
          </a>
        </li>
        <li v-for="(item, index) in autocompleteResults" :key="index">
          <a href="#" @click.prevent="updateQuery(item)">
            {{ item }}
          </a>
        </li>
      </ul>
    </div>
    <transition :duration="550" name="nested">
      <div class="panel-body-outer" v-show="isOpen">
        <div class="panel-body-inner">
          <div class="form-group">
            <div class="form-group-child">
              <input class="form-group-child-input" type="text" v-model="firstQuery"
                placeholder="Input the first query..." required=""
                @focus="currentFocusedInput = 'firstQuery'; isDropdownVisible = true; updateDropdownPosition($event)"
                @blur="hideDropdown; isDropdownVisible = false">
              <span class="form-group-child-input-bordert"></span>
            </div>
            <template v-if="selectedRadio === 'radio1'">
              <div class="form-group-child">
                <select v-model="selectedOperator" class="form-group-child-input">
                  <option value="">Choose the operator</option>
                  <option value="AND">AND</option>
                  <option value="OR">OR</option>
                  <option value="AND NOT">AND NOT</option>
                  <option value="OR NOT">OR NOT</option>
                </select>
                <span class="form-group-child-input-bordert"></span>
              </div>
            </template>
            <template v-else>
              <div class="form-group-child">
                <input class="form-group-child-input" type="number" v-model="proximityDistance"
                  placeholder="Input the distance... (only numbers)" required="">
                <span class="form-group-child-input-bordert"></span>
              </div>
            </template>
            <div class="form-group-child">
              <input class="form-group-child-input" type="text" v-model="secondQuery"
                placeholder="Input the second query..." required=""
                @focus="currentFocusedInput = 'secondQuery'; isDropdownVisible = true; updateDropdownPosition($event)"
                @blur="hideDropdown; isDropdownVisible = false">
              <span class="form-group-child-input-bordert"></span>
            </div>
          </div>
          <div class="form-group">
            <label class="radio-label" :class="{ 'label-no-input': !firstQuery }">
              {{ /\b\w+\b\s+\b\w+\b/.test(firstQuery) ? 'The first query is a phrase' : 'The first query is a word' }}
            </label>
            <div class="radio-buttons-container">
              <div class="radio-button">
                <input v-model="selectedRadio" id="radio1" class="radio-button-input" type="radio" value="radio1">
                <label for="radio1" class="radio-button-label">
                  <span class="radio-button-custom"></span>
                  Boolean
                </label>
              </div>
              <div class="radio-button">
                <input v-model="selectedRadio" id="radio2" class="radio-button-input" type="radio" value="radio2">
                <label for="radio2" class="radio-button-label">
                  <span class="radio-button-custom"></span>
                  Proximity
                </label>
              </div>
            </div>
            <label class="radio-label" :class="{ 'label-no-input': !secondQuery }">
              {{ /\b\w+\b\s+\b\w+\b/.test(secondQuery) ? 'The second query is a phrase' : 'The second query is a word'
              }}
            </label>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  data() {
    return {
      fullSearchQuery: '',
      isOpen: false,
      selectedRadio: 'radio1',
      firstQuery: '',
      selectedOperator: '',
      proximityDistance: '',
      secondQuery: '',
      isAdvancedSearchActive: false,
      spellCheckedQuery: '',
      autocompleteResults: [],
      isDropdownVisible: false,
      currentFocusedInput: '',
      dropdownPosition: { top: 0, left: 0 },
    };
  },
  watch: {
    firstQuery() {
      this.updateFullSearchQuery();
      this.fetchSpellCheckQuery();
      this.fetchAutocompleteResults();
    },
    secondQuery() {
      this.updateFullSearchQuery();
      this.fetchSpellCheckQuery();
      this.fetchAutocompleteResults();
    },
    selectedOperator() {
      this.updateFullSearchQuery();
    },
    proximityDistance() {
      this.updateFullSearchQuery();
    },
    selectedRadio() {
      this.updateFullSearchQuery();
    },
    isAdvancedSearchActive() {
      this.updateFullSearchQuery();
    },

    fullSearchQuery(newVal) {
      if (!this.fullSearchQuery) {
        this.spellCheckedQuery = '';
        this.autocompleteResults = [];
        return;
      }
      this.fetchSpellCheckQuery();
      this.fetchAutocompleteResults();

      if (!this.isAdvancedSearchActive)
        return;

      const operatorRegex = /(AND|OR|AND NOT|OR NOT)/;
      const proximityRegex = /#(\d+)\(([^,]+), ([^)]+)\)/;

      if (operatorRegex.test(newVal)) {
        const parts = newVal.split(operatorRegex).map(part => part.trim());
        if (parts.length === 3) {
          this.firstQuery = parts[0].replace(/^"|"$/g, '');
          this.selectedOperator = parts[1];
          this.secondQuery = parts[2].replace(/^"|"$/g, '');
          this.selectedRadio = 'radio1';
        }
      } else if (proximityRegex.test(newVal)) {
        const matches = newVal.match(proximityRegex);
        if (matches && matches.length === 4) {
          this.proximityDistance = matches[1];
          this.firstQuery = matches[2].replace(/^"|"$/g, '');
          this.secondQuery = matches[3].replace(/^"|"$/g, '');
          this.selectedRadio = 'radio2';
        }
      }
    },
  },
  methods: {
    searchStepOne() {
      if (this.fullSearchQuery.trim() === '') {
        alert('The search query cannot be empty');
        return;
      }
      this.$router.push({
        name: 'ResultPage',
        query: {
          q: this.fullSearchQuery,
          advanced: this.isAdvancedSearchActive ? '1' : '0'
        }
      });
    },
    toggle() {
      this.isOpen = !this.isOpen;
      this.isAdvancedSearchActive = !this.isAdvancedSearchActive;
      if (!this.isOpen) {
        this.firstQuery = '';
        this.secondQuery = '';
        this.selectedOperator = '';
        this.proximityDistance = '';
        this.fullSearchQuery = '';
      }
    },
    updateFullSearchQuery() {
      if (!this.isAdvancedSearchActive) {
        return;
      }
      const isPhrase = (query) => /\b\w+\b\s+\b\w+\b/.test(query);
      const firstQueryFormatted = isPhrase(this.firstQuery) ? `"${this.firstQuery}"` : this.firstQuery;
      const secondQueryFormatted = isPhrase(this.secondQuery) ? `"${this.secondQuery}"` : this.secondQuery;

      if (this.selectedRadio === 'radio1') {
        this.fullSearchQuery = `${firstQueryFormatted} ${this.selectedOperator} ${secondQueryFormatted}`.trim();
      } else {
        this.fullSearchQuery = `#${this.proximityDistance}(${firstQueryFormatted}, ${secondQueryFormatted})`.trim();
      }
    },

    //新增拼写检查和自动完成 - 请求后端 - 勿删
    // async fetchSpellCheckQuery() {
    //   if (!this.fullSearchQuery) return;
    //   try {
    //     const response = await fetch(`YOUR_SPELLCHECK_BACKEND_URL?query=${this.fullSearchQuery}`);
    //     if (response.ok) {
    //       const text = await response.text();
    //       this.spellCheckedQuery = text;
    //     }
    //   } catch (error) {
    //     console.error('Spell check error:', error);
    //   }
    // },
    // async fetchAutocompleteResults() {
    //   if (!this.fullSearchQuery) return;
    //   try {
    //     const response = await fetch(`YOUR_AUTOCOMPLETE_BACKEND_URL?query=${this.fullSearchQuery}`);
    //     if (response.ok) {
    //       const suggestions = await response.json();
    //       this.autocompleteResults = suggestions;
    //     }
    //   } catch (error) {
    //     console.error('Autocomplete error:', error);
    //   }
    // },

    //伪数据
    fetchSpellCheckQuery() {
      // 假设这是从拼写检查API返回的数据
      if (this.fullSearchQuery.toLowerCase().includes('teh')) {
        this.spellCheckedQuery = this.fullSearchQuery.replace('teh', 'the');
      } else {
        this.spellCheckedQuery = ''; // 如果没有拼写错误，不显示建议
      }
    },
    //伪数据
    fetchAutocompleteResults() {
      // 假设这是从自动完成API返回的数据
      this.autocompleteResults = [
        `${this.fullSearchQuery} suggestion 1`,
        `${this.fullSearchQuery} suggestion 2`,
        `${this.fullSearchQuery} suggestion 3`,
      ];
    },

    updateQuery(newQuery) {
      switch (this.currentFocusedInput) {
        case 'fullSearchQuery':
          this.fullSearchQuery = newQuery;
          break;
        case 'firstQuery':
          this.firstQuery = newQuery;
          break;
        case 'secondQuery':
          this.secondQuery = newQuery;
          break;
        default:
          console.log("No input field is currently focused.");
      }
      this.isDropdownVisible = false;
    },
    // hideDropdown() {
    //   setTimeout(() => {
    //     this.isDropdownVisible = false;
    //   }, 200);
    // },
    updateDropdownPosition(event) {
      const inputElement = event.target; // 获取当前聚焦的输入元素
      const autocompleteContainer = this.$refs.autocompleteContainer; // 通过 ref 获取 autocomplete 容器

      // 获取 panel-header 元素，以便可以将 autocomplete 容器移动回此位置
      const panelHeader = this.$refs.panelHeader;

      if (this.currentFocusedInput === 'fullSearchQuery' && panelHeader && autocompleteContainer) {
        // 如果是 fullSearchQuery 输入，将 autocomplete 容器移动到 panel-header 元素之后
        panelHeader.insertAdjacentElement('afterend', autocompleteContainer);
      } else if (inputElement && autocompleteContainer) {
        // 对于 firstQuery 和 secondQuery 输入，将 autocomplete 容器移动到 input 元素之后
        inputElement.insertAdjacentElement('afterend', autocompleteContainer);
      }
    },
  },
};
</script>

<style>
.autocomplete-container {
  /* position: relative; */
  position: absolute;
  text-align: left;
  z-index: 1000;
  width: 300px;
}

.autocomplete-dropdown {
  position: absolute;
  width: 100%;
  border: 1px solid #ccc;
  background-color: white;
  list-style-type: none;
  margin: 0;
  padding: 0;
  z-index: 100;
}

.autocomplete-dropdown li a {
  display: block;
  padding: 8px;
  text-decoration: none;
  color: black;
}

.autocomplete-dropdown li a:hover {
  background-color: #f3f3f3;
}

.search-input {
  width: 325px;
  padding: 10px;
  border: 5px solid white;
  border-radius: 30px;
}

.search-button {
  background-image: url('../assets/search.png');
  background-color: white;
  background-size: cover;
  background-position: center;
  border: none;
  width: 30px;
  height: 30px;
  cursor: pointer;
}

.search-input-button {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  width: 450px;
  border: 3px solid #2c3e50;
  border-radius: 30px;
}

.advanced-search-button {
  padding: 10px 20px;
  background-color: #2c3e50;
  color: white;
  margin-left: 10px;
  height: 100%;
  border: none;
  border-radius: 30px;
  white-space: normal;
  cursor: pointer;
}

.form-group-child {
  --width-of-input: 270px;
  --border-height: 1px;
  --border-before-color: gray;
  --border-after-color: #2c3e50;
  --input-hovered-color: #eee;
  position: relative;
  width: var(--width-of-input);
}

.form-group-child-input {
  color: #2c3e50;
  font-size: 0.9rem;
  background-color: transparent;
  width: 100%;
  box-sizing: border-box;
  padding-inline: 0.5em;
  padding-block: 0.7em;
  border: none;
  border-bottom: var(--border-height) solid var(--border-before-color);
}

.form-group-child-input-border {
  position: absolute;
  background: var(--border-after-color);
  width: 0%;
  height: 2px;
  bottom: 0;
  left: 0;
  transition: 0.3s;
}

input:hover {
  background: var(--input-hovered-color);
}

input:focus {
  outline: none;
}

input:focus~.input-border {
  width: 100%;
}

.radio-label {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  color: gray;
}

.label-no-input {
  color: #eee;
}

.radio-buttons-container {
  display: flex;
  align-items: center;
  gap: 24px;
}

.radio-button {
  display: inline-block;
  position: relative;
  cursor: pointer;
}

.radio-button-input {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

.radio-button-label {
  display: inline-block;
  padding-left: 30px;
  position: relative;
  font-size: 16px;
  color: #2c3e50;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.23, 1, 0.320, 1);
}

.radio-button-custom {
  position: absolute;
  top: 50%;
  left: 0;
  transform: translateY(-50%);
  width: 12px;
  height: 12px;
  border-radius: 50%;
  border: 2px solid white;
  transition: all 0.3s cubic-bezier(0.23, 1, 0.320, 1);
}

.radio-button-input:checked+.radio-button-label .radio-button-custom {
  transform: translateY(-50%) scale(0.9);
  border: 5px solid #2c3e50;
  color: #2c3e50;
}

.radio-button-input:checked+.radio-button-label {
  color: #2c3e50;
}

.radio-button-label:hover .radio-button-custom {
  transform: translateY(-50%) scale(1.2);
  border-color: #2c3e50;
  box-shadow: 0 0 10px #2c3e50;
}

.collapsible-panel {
  position: relative;
}

.panel-header {
  margin-bottom: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.panel-body-outer {
  position: absolute;
  width: 100%;
  z-index: 100;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  box-sizing: border-box;
}

.panel-body-inner {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.form-group {
  display: grid;
  grid-template-rows: 1fr 1fr 1fr;
  gap: 20px;
}

.panel-body-outer,
.panel-body-inner {
  background: #eee;
  padding: 15px;
  min-height: 100px;
}

.panel-body-inner {
  background: #eee;
  padding-left: 5px;
}

.nested-enter-active,
.nested-leave-active {
  transition: all 0.3s ease-in-out;
}

.nested-leave-active {
  transition-delay: 0.25s;
}

.nested-enter-from,
.nested-leave-to {
  transform: translateY(30px);
  opacity: 0;
}

.nested-enter-active .panel-body-inner,
.nested-leave-active .panel-body-inner {
  transition: all 0.3s ease-in-out;
}

.nested-enter-active .panel-body-inner {
  transition-delay: 0.25s;
}

.nested-enter-from .panel-body-inner,
.nested-leave-to .panel-body-inner {
  transform: translateX(30px);
  opacity: 0.001;
}
</style>