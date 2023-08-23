<script>
	import DataUploader from "./DataUploader.svelte";
	import ModelSelector from "./ModelSelector.svelte";
	import ResultsDisplay from "./ResultsDisplay.svelte";
	import TrainingInitiator from "./TrainingInitiator.svelte";

    let uploadedData = null;
    let selectedModel = null;
    let isTraining = false;

    function handleFileUpload(event) {
        uploadedData = event.detail;
    }

    function handleModelSelection(event) {
        selectedModel = event.detail;
    }

    function checkIfReadyForTraining() {
        if (uploadedData === null || selectedModel === null){
            return false;
        }
        return true;
    }

    async function handleIntializingTraining(event){
        if (!checkIfReadyForTraining()) {
            alert("Ensure you have uploaded data and selected a model.");
            return;
        }
        if (isTraining) {
            alert("You are already training a model, please wait until training is complete before sending another request.");
            return;
        }
        isTraining = true;

        const requestBody = {
            data: uploadedData,
            model: selectedModel
        };
    }


</script>

<main>
	<DataUploader on:filesUploaded={handleFileUpload}/>
	<ModelSelector on:modelSelected={handleModelSelection}/>
	<TrainingInitiator on:startTraining={handleIntializingTraining}/>
	<ResultsDisplay/>
</main>