<script>
    import * as XLSX from 'xlsx'
    import {createEventDispatcher } from 'svelte'
    // NOTE: CURRENTLY ONLY SINGLE FILE UPLOADS ARE SUPPORTED SO THIS SHOULD REALLY BE SINGULAR
    // ALSO THIS COMPONENT ASSUMES THE FILE IS AN EXCEL FILE FOR NOW
    // TODO: ADD OPTION FOR USERS TO SELECT WHICH FILE TYPE THEY WILL BE ADDING
    export let uploadedFiles; 
    const dispatch = createEventDispatcher();
    let columns = []
    let selectedColumn = null;
    let showcaseColumnSelector = false;

    function chooseTargetVector() {
        // Load data and display it
        const reader = new FileReader();
        reader.onload = function(e) {
            const data = e.target.result;
            const workbook = XLSX.read(data, {type: "binary"});
            const wsname = workbook.SheetNames[0]
            const ws = workbook.Sheets[wsname];
            const parsedData = XLSX.utils.sheet_to_json(ws, {header: 1});

            columns = parsedData[0];
            showcaseColumnSelector = true;
        }

        reader.readAsBinaryString(uploadedFiles[0].file);
    }

    function updateTempSelectedColumn(column_name) {
        if (column_name === selectedColumn) {
            selectedColumn = null;
            return;
        }
        selectedColumn = column_name;
    }

    function updateSelectedColumn() {
        showcaseColumnSelector = false;
        dispatch("columnSelected", selectedColumn);
    }
    
</script>


<main>
    <div class="button-display-container">
        <button class="target-selector" on:click={chooseTargetVector}>Select Target Vector</button>
        {#if selectedColumn}
            <div class="selected-column-display">Target Vector: {selectedColumn}</div>
        {/if}
    </div>
    {#if showcaseColumnSelector}
        <div class="overlay">
            <div class="column-select">
                <h1>Please Choose a Column as Your Target Vector</h1>
                <div class="columns-container">
                    {#each columns as column}
                        <div 
                            class="column-option {selectedColumn === column ? 'selected' : ''}" 
                            on:click={() => updateTempSelectedColumn(column)}
                            on:keydown={e => e.key === 'Enter' && updateTempSelectedColumn(column)}
                        >
                            {column}
                        </div>
                    {/each}
                </div>
                <button class="confirm-button" on:click={updateSelectedColumn}>Confirm</button>
            </div>
        </div>
    {/if}
    
</main>

<style>
    .target-selector {
        background-color: #007BFF;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        font-size: 16px;
        cursor: pointer;
        transition: background-color 0.3s;
        margin: 15px;
    }

    .target-selector:hover {
        background-color: #0056b3;
    }

    .target-selector:active {
        background-color: #004085;
    }

    .button-display-container {
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .selected-column-display {
        text-align: center;
        padding: 1rem;

    }

    .overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.7);
        z-index: 999;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .column-select {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        width: 80%;
        max-width: 600px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }

    .columns-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 10px;
    }

    .column-option {
        padding: 10px 20px;
        border: 1px solid #ccc;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.2s;
    }

    .column-option:hover, .column-option.selected {
        background-color: #007BFF;
        color: white;
    }

    .confirm-button {
        background-color: #007BFF;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        cursor: pointer;
        margin-top: 20px;
    }

    .confirm-button:hover {
        background-color: #0056b3;
    }

    .confirm-button:active {
        background-color: #004085;
    }
</style>
