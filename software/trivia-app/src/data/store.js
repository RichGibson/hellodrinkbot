import {readable, writable, derived, get} from 'svelte/store';
import { generateQuiz, getPercentage } from '../components/utils';
import {trivia} from './trivia';

// Settings
export const maxNumberOfQuestions = readable(trivia.questions.length);
export const numberOfQuestions = writable(5);

// App State
export const hasQuizBegun = writable(false);
export const currentQuestionIndex = writable(0);
export const isQuizDone = writable(false);

// Data
export const triviaQuestions = readable(trivia.questions);
export const quizTitle = readable(trivia.title);
export const quiz = derived(hasQuizBegun, ($hasQuizBegun, set) => {
    if ($hasQuizBegun) {
        set(generateQuiz(get(triviaQuestions), get(numberOfQuestions)));
    }
}, [])
export const score = writable(0);
export const scorePercentage = derived([score, quiz], ([$score, $quiz]) => {
    return getPercentage($score, $quiz.length);
}, 0);
export const detailedScore = writable([]);
export const reset = () => {
    score.set(0);
    hasQuizBegun.set(false);
    currentQuestionIndex.set(0);
    isQuizDone.set(false);
    detailedScore.set([]);
}


