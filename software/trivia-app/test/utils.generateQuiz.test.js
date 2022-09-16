import { generateQuiz } from "../src/components/utils.js";
import {trivia} from '../src/data/trivia.js';

describe("generateQuiz Tests", () => {
  test("happy path", () => {
    let quizLength = 10;
    let quiz = generateQuiz(trivia.questions, quizLength);
    
    expect(quiz).toHaveLength(10);

    quiz.forEach(question => {
      expect(question).toHaveProperty('question');
      expect(question).toHaveProperty('answers');
      expect(question).toHaveProperty('correctAnswer');
    });
    
  });

  test("ensure generated quiz includes all available questions when quiz length equals available trivia", () => {
    let quizLength = 10;
    let triviaData = trivia.questions.slice(0,10);
    let availableQuestions = triviaData.map(question => question.q);
    let quiz = generateQuiz(triviaData, quizLength);
    
    quiz.forEach(question => {
      let questionText = question.question;
      expect(availableQuestions).toContain(questionText);
      
    });
    expect(quiz).toHaveLength(quizLength);
  });
});
