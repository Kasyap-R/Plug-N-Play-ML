<script>
    import { createEventDispatcher } from 'svelte';
    const dispatch = createEventDispatcher();

    let files = []
    let isDragging = false;

    function handleDragOver(event) {
        event.preventDefault();
    }

    function handleDrop(event) {
        event.preventDefault();
        isDragging = false;
        const newFiles = [...event.dataTransfer.files].map(file => ({file, id: Date.now() + Math.random()}))
        files = [...files, ...newFiles];
        dispatch('filesUploaded', files);
    }

    function handleFileChange(event) {
        const newFiles = [...event.target.files].map(file => ({ file, id: Date.now() + Math.random()}));
        files = [...files, ...newFiles];
        dispatch('filesUploaded', files);
    }

    function removeFile(id) {
        files = files.filter(file => file.id !== id);
    }

    function handleDragEnter() {
        isDragging = true;
    }

    function handleDragLeave() {
        isDragging = false;
    }

</script>


<main>
    <div
        class="upload-area"
        on:dragover={handleDragOver}
        on:drop={handleDrop}
        on:dragleave={handleDragLeave}
        on:dragenter={handleDragEnter}
        class:drag-over={isDragging}
    >
        Drag & Drop your files here or
        <label class="file-label">Browse<input type="file" bind:files on:change={handleFileChange} class="file-input"></label>
    </div>
    <ul class="file-list">
        {#each files as fileObj (fileObj.id)}
            <li class="file-item">
                <button class="remove-file" on:click={() => removeFile(fileObj.id)}>x</button>
                {fileObj.file.name}
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

    .file-input {
        display: none;
    }
    
    .file-item {
        list-style-type: none
    }

    .remove-file {
        color: red;
        background-color: white;
        border: 2px gray; 
        border-radius: 1rem;
    }

    .drag-over {
        background-color: #9e9696e5;
    }

</style>