# Simple Svelte Quiz App - original code by Jason Lutterloh

This is a simple Svelte quiz application. Given a JSON trivia document of questions & answers, you can very easily create a quiz web application.

## Getting Started

1. Clone the repository.
2. Run `npm install`
3. Run `npm run dev`
4. View the application on `http://localhost:5000`

## Build & Deploy

1. Run `npm run build`
2. Deploy whatever is in the `/public` folder
    (If you use Firebase, this is already setup. Just configure with your project details and run `firebase deploy`.)

## Creating Your Quiz

The application relies a .js file at `/src/data/trivia.js`. Inside is a structure like the following:

```js
export const trivia = {
  title: "[YOUR QUIZ TITLE GOES HERE]",
  questions:
  [
    {
      // Question Text.
      q: "QUESTION 1",

      // The first answer will be treated as the correct answer. They will be displayed randomly, however.
      // For true/false, use booleans. ie. ([true, false])
      // For all other answer types, use strings
      a: ["ANSWER1", "ANSWER2", "ANSWER3"],

      // This will display underneath the answer on the results page. Useful for extra information, fun facts, or clarifications
      followup: "FOLLOW UP TEXT"
    },
    ...
  ]
}

There is no max length for the trivia. A sample trivia data has been included.

## Modifying the code

You can add fields to the quiz file:

    img: "img/file.jpg",
    extratext: "this is extra text"

Then modify the generateQuiz method in componensts/utils.js:

    question.img = quizQuestions[index].img;

And then modify src/components/Quize.svelte to add those fields.

    <a href=""><img src="{question.img}" width="400">image</a>
    {question.extratext}<hr>

