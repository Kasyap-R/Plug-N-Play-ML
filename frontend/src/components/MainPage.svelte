<script>
	import DataUploader from "./DataUploader.svelte";
	import ModelSelector from "./ModelSelector.svelte";
	import ResultsDisplay from "./ResultsDisplay.svelte";
	import TrainingInitiator from "./TrainingInitiator.svelte";
    import TargetSelector from "./TargetSelector.svelte";
    import ProblemTypeSelector from "./ProblemTypeSelector.svelte";

    import {ERROR_MESSAGES} from '../utils/error_messages'
    import { trainModel } from '../utils/api'
    import {MODEL_NAME_KEY, TARGET_COLUMN_NAME_KEY, FILE_KEY, PROBLEM_TYPE_KEY} from '../utils/constants'

    let uploadedFiles = [];
    let selectedModel = null;
    let isTraining = false;
    let allowedFileExtensions = /(\.xlsx)$/i;
    let selectedColumn = null;
    let selectedProblemType = null;

    function handleFileChange(event) {
        uploadedFiles = event.detail;
    }

    function handleModelSelection(event) {
        selectedModel = event.detail;
    }

    function handleColumnSelection(event) {
        selectedColumn = event.detail;
    }

    function handleProblemTypeSelection(event) {
        selectedProblemType = event.detail;
    }

    function checkIfReadyForTraining() {
        if (uploadedFiles === null || selectedModel === null || selectedColumn === null){
            return false;
        }
        return true;
    }

    async function initializeModelTraining(){
        if (!checkIfReadyForTraining()) {
            alert(ERROR_MESSAGES.NOT_READY);
            return;
        }
        if (isTraining) {
            alert(ERROR_MESSAGES.ALREADY_TRAINING);
            return;
        }

        isTraining = true;

        const formData = new FormData();
        uploadedFiles.forEach(dataItem => {
            formData.append(FILE_KEY, dataItem.file);  
        });
        
        formData.append(MODEL_NAME_KEY, selectedModel)
        formData.append(TARGET_COLUMN_NAME_KEY, selectedColumn)
        formData.append(PROBLEM_TYPE_KEY, selectedProblemType)

        try {
            const response = await trainModel(formData);
            console.log(response);
            isTraining = false;
        } catch (e) {
            console.error("Error when sending files:", e);
        }
    }


</script>

<main>
	<DataUploader {allowedFileExtensions} on:filesUploaded={handleFileChange} on:filesRemoved={handleFileChange}/>
    {#if uploadedFiles.length >= 1}
        <TargetSelector {uploadedFiles} on:columnSelected={handleColumnSelection}/> 
        <ProblemTypeSelector on:problemTypeSelected={handleProblemTypeSelection}/>
    {/if}
	<ModelSelector on:modelSelected={handleModelSelection}/>
	<TrainingInitiator on:startTraining={initializeModelTraining}/>
	<ResultsDisplay/>
</main>