<script>
	import Quiz from "./components/Quiz.svelte";
	import Setup from "./components/Setup.svelte";
	import Results from "./components/Results.svelte";
	import { hasQuizBegun, isQuizDone } from "./data/store.js";
</script>

<style>
	:global(body) {
		background: rgb(39,116,174);
    background: linear-gradient(-35deg, rgba(39,116,174,1) 0%, rgba(1,66,106,1) 100%) no-repeat center center fixed;
		background-size: cover;
		color: #FFFFFF;
		font-family: "Poppins", sans-serif;
	}
	:global(button) {
		box-sizing: border-box;
		margin: 1em 0;
		background: transparent;
		color: #fff;
		cursor: pointer;
		border: 3px solid #fff;
		padding: 1em 0;
		font-size: 0.9em;
		transition: 0.2s all;
		width: 100%;
	}
	:global(button:hover, button:focus) {
		background: #FFFFFF;
		color:  rgb(39,116,174);
		transform: scale(1.05);
	}
	:global(button:active) {
		background: #FFFFFF;
		color:  rgb(39,116,174);
		transform: scale(1);
	}
	main {
		font-size: 18px;
		margin: 0 auto;
		max-width: 600px;
		text-align: center;
	}
	@media only screen and (max-width: 600px) {
		main {
			font-size: 18px;
		}
	}
</style>

<main>
	{#if $hasQuizBegun}
		<Quiz />
	{:else if $isQuizDone}
		<Results />
	{:else}
		<Setup />
	{/if}
</main>
