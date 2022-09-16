<script>
    import {
        maxNumberOfQuestions,
        numberOfQuestions,
        hasQuizBegun,
        quizTitle,
    } from "../data/store";
    import { fly } from "svelte/transition";

    const onSubmit = () => {
        hasQuizBegun.set(true);
    };
</script>

<style>
    h1 {
        font-size: 1.4em;
        margin-bottom: 1em 0 2em 0;
    }
    label {
        margin: 2em 0;
    }
    input {
        background: transparent;
        border: 0;
        border-bottom: 2px solid #fff;
        color: #fff;
        text-align: center;
        display: block;
        margin: 0 auto;
    }
</style>

<div
    in:fly={{ x: 200, duration: 500, delay: 500 }}
    out:fly={{ x: -200, duration: 500 }}>
    <h1>Welcome to {$quizTitle}!</h1>
    <form on:submit|preventDefault={onSubmit}>
        <label>
            How many questions would you like?
            <input
                type="number"
                bind:value={$numberOfQuestions}
                max={$maxNumberOfQuestions}
                min="1"
                required />
        </label>
        <button type="submit">Start</button>
    </form>
</div>
