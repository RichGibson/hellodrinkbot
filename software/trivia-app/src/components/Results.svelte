<script>
  import {
    quiz,
    detailedScore,
    reset,
    scorePercentage,
  } from "../data/store.js";
  import { getDisplayValue, getPercentageColor } from "./utils.js";
  import { fly } from "svelte/transition";
  import { onMount } from "svelte";

  let percentage = 0;

  onMount(async () => {
    percentage = $scorePercentage; // To give the live update CSS effect
  });
</script>

<style>
  a {
    color: #ffff99;
  }
  h1 {
    font-size: 1.0em;
    margin-bottom: 1em;
  }
  .final-score {
    padding-bottom: .5em;
    margin-bottom: 0;
  }
  .score-scale {
    background: rgba(220, 220, 220, 0.6);
    border: 3px solid #fff;
    display: block;
    margin-bottom: 40px;
    position: relative;
    height: 30px;
    width: 100%;
  }
  .score-bar {
    width: 0px;
    position: absolute;
    top: 0;
    left: 0;
    display: block;
    height: 30px;
    background: rgba(220, 220, 220);
    transition: width 1s;
    transition-delay: 1s;
  }
  .icon {
    border: 3px solid #fff;
    color: #efefef;
    height: 2em;
    width: 2em;
    display: block;
    text-align: center;
    line-height: 2em;
  }

  .correct {
    background: #008568;
  }
  .wrong {
    background: #6E7783;
  }
  ul {
    padding: 0;
  }
  li {
    display: flex;
    margin-bottom: 3em;
  }
  li > div:first-of-type {
    flex: 0 0 3em;
  }
  li > div {
    flex: 1 1 auto;
  }
  li p {
    margin: 0;
    margin-bottom: 1em;
    font-size: 0.8em;
    text-align: left;
  }
  li p:nth-child(2) {
    font-size: 100%;
    font-weight: bold;
    text-align: left;
  }

  .followup {
    font-style: italic;
    font-size: 0.6em;
  }
</style>

<div
  in:fly={{ y: 200, duration: 500, delay: 500 }}
  out:fly={{ y: -200, duration: 500 }}>
  <h1>Results</h1>

  <div>
    <p class="final-score">Final Score: {percentage}%</p>
    <div class="score-scale">
      <div
        class="score-bar"
        style="width:{percentage}%; background:{getPercentageColor(percentage)}" />
    </div>
  </div>

  <div>
    Now you have choices!
    <ul>
    <li><a href="http://127.0.0.1:8080/ws/drink/79?booze1=15&booze12=10&booze40=15">Pour me a White Ukranian/Caucasian</a></li>
    <li><a href="http://127.0.0.1:8080">Let me see all of my drink choices</a></li>
    </ul>
    <button type="button" on:click={reset}>Play Again</button>
  </div>

  {#if $detailedScore != undefined && $detailedScore.length != 0}
    <ul>
      {#each $quiz as question, index}
        <li>
          <div>
            {#if $detailedScore[index].correct}
              <span class="icon correct">+1</span>
            {:else}<span class="icon wrong">0</span>{/if}
          </div>
          <div>
            <p>{question.question}</p>
            <p>{getDisplayValue(question.correctAnswer)}</p>
            {#if !$detailedScore[index].correct}
              <p>
                Your Answer:
                {getDisplayValue($detailedScore[index].chosenAnswer)}
              </p>
            {/if}
            {#if question.followup}
              <p class="followup">{question.followup}</p>
            {/if}
          </div>
        </li>
      {/each}
    </ul>
  {/if}

  <button type="button" on:click={reset}>Play Again</button>
</div>
