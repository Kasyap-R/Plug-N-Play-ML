<script>
    import {createEventDispatcher } from 'svelte'
    import { REGRESSION, CLASSIFICATION } from '../utils/constants'

    const dispatch = createEventDispatcher();
    let problemTypes = [CLASSIFICATION, REGRESSION]
    let selectedProblemType = null;
    let showcaseProblemSelector = false;

    function chooseProblemType() {
        showcaseProblemSelector = true;
    }

    function updateTempSelectedProblem(problemType) {
        if (problemType === selectedProblemType) {
            selectedProblemType = null;
            return;
        }
        selectedProblemType = problemType;
    }

    function updateSelectedProblem() {
        showcaseProblemSelector = false;
        dispatch("problemTypeSelected", selectedProblemType);
    }
    
</script>


<main>
    <div class="button-display-container">
        <button class="problem-type-selector" on:click={chooseProblemType}>Select Problem Type</button>
        {#if selectedProblemType}
            <div class="selected-problem-display">Problem Type: {selectedProblemType}</div>
        {/if}
    </div>
    {#if showcaseProblemSelector}
        <div class="overlay">
            <div class="problem-select">
                <h1>Please Choose the Type of Problem the Model Should Solve</h1>
                <div class="problem-types-container">
                    {#each problemTypes as problem}
                        <div 
                            class="problem-type-option {selectedProblemType === problem ? 'selected' : ''}" 
                            on:click={() => updateTempSelectedProblem(problem)}
                            on:keydown={e => e.key === 'Enter' && updateTempSelectedProblem(problem)}
                        >
                            {problem}
                        </div>
                    {/each}
                </div>
                <button class="confirm-button" on:click={updateSelectedProblem}>Confirm</button>
            </div>
        </div>
    {/if}
    
</main>

<style>
    .problem-type-selector {
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

    .problem-type-selector:hover {
        background-color: #0056b3;
    }

    .problem-type-selector:active {
        background-color: #004085;
    }

    .button-display-container {
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .selected-problem-display {
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

    .problem-select {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        width: 80%;
        max-width: 600px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }

    .problem-types-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 10px;
    }

    .problem-type-option {
        padding: 10px 20px;
        border: 1px solid #ccc;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.2s;
    }

    .problem-type-option:hover, .problem-type-option.selected {
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
