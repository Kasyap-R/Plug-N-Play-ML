<script>
    import { createEventDispatcher } from 'svelte';
    import { ERROR_MESSAGES } from '../utils/error_messages'
    export let allowedFileExtensions;

    const dispatch = createEventDispatcher();

    let files = []
    let isDragging = false;

    function handleFileDrop(event) {
        event.preventDefault();
        isDragging = false;
        if (isFileUploaded()) {
            return;
        }
        const newFiles = retrieveValidFiles([...event.dataTransfer.files])
        files = [...files, ...newFiles];
        dispatch('filesUploaded', files);
    }

    function handleFileUpload(event) {
        if (isFileUploaded()) {
            return;
        }
        const newFiles = retrieveValidFiles([...event.target.files])
        files = [...files, ...newFiles];
        dispatch('filesUploaded', files);
    }

    function retrieveValidFiles(files) {
        let unsupportedTypes = [];
        const supportedFiles = files.filter(file => {
                const isValid = validateFile(file)
                if(!isValid) {
                    unsupportedTypes.push(file.type || 'unknown');
                }
                return isValid
            })
            .map(file => ({file, id: Date.now() + Math.random()}))
        // Alert the user if there were unsupported files
        if (unsupportedTypes.length > 0) {
            alert(`Error: Attempting to upload unsupported file types of type [${unsupportedTypes.join(', ')}]`);
        }

        return supportedFiles;
    }

    function isFileUploaded() {
        const exceedsFileLimit = (files.length >= 1);
        if (exceedsFileLimit) {
            alert(ERROR_MESSAGES.TOO_MANY_FILES)
        }
        return exceedsFileLimit;
    }

    function removeFile(id) {
        files = files.filter(file => file.id !== id);
        dispatch('filesRemoved', files);
    }

    function validateFile(file) {
        return allowedFileExtensions.exec(file.name) !== null;
    }

    function handleDragEnter() {
        isDragging = true;
    }

    function handleDragLeave() {
        isDragging = false;
    }

    function handleDragOver(event) {
        event.preventDefault();
    }

</script>


<main>
    <div
        class="upload-area"
        on:dragover={handleDragOver}
        on:drop={handleFileDrop}
        on:dragleave={handleDragLeave}
        on:dragenter={handleDragEnter}
        class:drag-over={isDragging}
    >
        Drag & Drop your files here or
        <label class="file-label">Browse<input type="file" on:change={handleFileUpload} class="file-input"></label>
    </div>
    <ul class="file-list">
        {#each files as fileObj (fileObj.id)}
            <li class="file-item">
                <button class="delete-button" on:click={() => removeFile(fileObj.id)}>x</button>
                <span class="file-name">{fileObj.file.name}</span>
            </li>
        {/each}
    </ul>
</main>


<style>
    .upload-area {
        border: 2px dashed gray;
        padding: 20px;
        text-align: center;
        transition: background-color 0.3s;
        margin: auto;
        width: 50%;
    }

    .file-label {
        display: inline-block;
        padding: 10px 20px;
        background-color: #4CAF50;
        color: white;
        cursor: pointer;
        margin-top: 10px;
        border-radius: 5px;
    }

    .file-list {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 80%;
        margin: auto;
        margin-bottom: 8px;
    }

    .file-input {
        display: none;
    }
    
    .file-item {
        list-style-type: none;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .file-name {
        text-align: center;
    }

    .delete-button {
        color: red;
        background-color: white;
        cursor: pointer;
        border: none;
    }

    .delete-button:hover {
        background-color: gray;
        transition: cubic-bezier(0.075, 0.82, 0.165, 1);
    }

    .drag-over {
        background-color: #9e9696e5;
    }

</style>