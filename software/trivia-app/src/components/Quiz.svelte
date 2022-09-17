<script>
    import {
        quiz,
        detailedScore,
        currentQuestionIndex,
        score,
        isQuizDone,
        hasQuizBegun,
    } from "../data/store.js";
    import { getDisplayValue } from "./utils.js";
    import { fly } from "svelte/transition";

    let selectedAnswer;

    const onSubmit = () => {
        let correctAnswer = $quiz[$currentQuestionIndex].correctAnswer;
        if (correctAnswer === selectedAnswer) {
            score.update((score) => score + 1);

            $detailedScore = [
                ...$detailedScore,
                { correct: true, chosenAnswer: selectedAnswer },
            ];
        } else {
            $detailedScore = [
                ...$detailedScore,
                { correct: false, chosenAnswer: selectedAnswer },
            ];
        }

        selectedAnswer = "";

        if ($currentQuestionIndex < $quiz.length - 1) {
            currentQuestionIndex.update(
                (currentQuestionIndex) => currentQuestionIndex + 1
            );
        } else {
            hasQuizBegun.set(false);
            isQuizDone.set(true);
        }
    };
</script>

<style>
    fieldset {
        border: 0;
        margin-top: .8em;
        padding: 0 .8em;
    }
    legend {
        margin-bottom: 1em;
    }
    label {
        color: #fff;
        cursor: pointer;
        position: relative;
        font-size: 0.9em;
        line-height: .9em;
        box-sizing: border-box;
        padding: 20px 20px 20px 64px;
        text-align: left;
        margin-bottom: .8em;
        width: 100%;
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
    }
    input {
        position: absolute;
        opacity: 0;
        cursor: pointer;
        height: 0;
        width: 0;
    }
    .radio {
        position: absolute;
        top: 16px;
        left: 16px;
        height: 16px;
        width: 16px;
        background-color: #fff;
        border-radius: 50%;
        transition: 0.25s all;
    }
    .radio:after {
        content: "";
        position: absolute;
        display: none;
    }

    input:checked ~ .radio:after {
        display: block;
    }
    @keyframes shrinkGrow {
        0% {
            transform: scale(1);
        }
        50% {
            transform: scale(0);
        }
        100% {
            transform: scale(1);
        }
    }
    input:checked ~ .radio {
        animation-name: shrinkGrow;
        animation-duration: 0.5s;
    }

    label:hover > .radio {
        transform: scale(1.1);
    }
    .radio:after {
        top: 4px;
        left: 4px;
        width: 16px;
        height: 16px;
        border-radius: 50%;
        background:  rgb(39,116,174)
    }

    @media only screen and (max-width: 600px) {
        .radio {
            top: 12px;
            left: 12px;
            height: 20px;
            width: 20px;
        }
        .radio:after {
            top: 4px;
            left: 4px;
            width: 12px;
            height: 12px;
        }
        label {
            padding: 14px 14px 14px 48px;
        }
    }
</style>

{#each $quiz as question, questionIndex}
    {#if $currentQuestionIndex === questionIndex}
        <table>
        <tr>
        <td>
        {#if question.img !== 'img/'}
        <img src="{question.img}" width="300" alt='a fucking thing'><br>
        {/if}
        {#if question.extratext !== undefined}
        {question.extratext}<hr>
        {/if}
        </td>
        <td>


        <form
            on:submit|preventDefault={onSubmit}
            in:fly={{ x: 200, duration: 500, delay: 500 }}
            out:fly={{ x: -200, duration: 500 }}>
            <fieldset>
                <legend>{question.question}</legend>
                {#each question.answers as answer, answerIndex}
                    <label for="answer{answerIndex}">
                        <input
                            required
                            type="radio"
                            id="answer{answerIndex}"
                            value={answer}
                            name="question{questionIndex}"
                            bind:group={selectedAnswer} />
                        {getDisplayValue(answer)}
                        <span class="radio" />
                    </label>
                {/each}
            </fieldset>

            {#if $currentQuestionIndex < $quiz.length - 1}
                <button type="submit">Next Question</button>
            {:else}
                <button type="submit">Submit Answers</button>
            {/if}
        </form>
        </td>
        </tr>
        </table>
    {/if}
{/each}
