<script>
    import { createEventDispatcher } from 'svelte';
    const dispatch = createEventDispatcher();
    let selectedModel = null;

    let models = [
        ["XGBoost", "Powerful Model for use with Tabular Data", "xgboost"],
    ]

    function handleModelSelection(modelIndex) {
        let modelIdIndex = 2;
        if (selectedModel === modelIndex) {
            selectedModel = null;
            return;
        }
        selectedModel = modelIndex;
        dispatch("modelSelected", models[modelIndex][modelIdIndex]);
    }

</script>

<main>
    <div class="models-container">
        {#each models as model, modelIndex}
            <div
                class="model-item {selectedModel === modelIndex ? 'selected' : ''}"
                on:click={() => handleModelSelection(modelIndex)}
                on:keydown={e => e.key === 'Enter' && handleModelSelection(modelIndex)} 
            >
                <h2>{model[0]}</h2>
                <p>{model[1]}</p>
            </div>
        {/each}
    </div>
    
</main>

<style>
    .model-item {
        padding: 10px;
        border: 1px solid #ddd;
        margin: 10px 0;
        cursor: pointer;
        transition: background-color 0.3s;
        width: 25%;
        margin: 0 10px;
    }

    .model-item:hover {
        background-color: #f0f8ff; 
    }

    .model-item.selected {
        background-color: #e0f0ff;
        border-color: black;
    }

    .models-container {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-wrap: wrap;
    }

</style>