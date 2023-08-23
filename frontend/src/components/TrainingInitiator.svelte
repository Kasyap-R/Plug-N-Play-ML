<script>
    import {createEventDispatcher} from 'svelte'
    const dispatch = createEventDispatcher()

    function initializeTraining() {
        dispatch("startTraining")
    }

</script>

<main>
    <button class="training-button" on:click={initializeTraining}>Start Training</button>
</main>

<style>
    .training-button {
        background-color: #007BFF; /* Blue color */
        color: #FFF; /* White text color */
        padding: 10px 20px; /* Padding for top/bottom and left/right */
        border: none; /* Removes default border */
        border-radius: 5px; /* Rounded corners */
        font-size: 16px; /* Bigger font */
        cursor: pointer; /* Changes cursor to hand when hovering */
        transition: background-color 0.3s; /* Smooth transition effect for hover */
        margin-top: 50px;
    }

    .training-button:hover {
        background-color: #0056b3;
    }

    .training-button:active {
        background-color: #004085;
    }

</style>