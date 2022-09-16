const getRandomNumber = (max) => {
  return Math.floor(Math.random() * max);
};

export const getArrayOfRandomNumbers = (desiredLength, max) => {
  let array = [];
  while (array.length < desiredLength) {
    let randomNumber = getRandomNumber(max);
    if (!array.includes(randomNumber)) {
      array.push(randomNumber);
    }
  }
  return array;
};

//Source: https://javascript.info/task/shuffle
export const shuffleAnswers = (array) => {
  for (let i = array.length - 1; i > 0; i--) {
    let j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }

  return array;
};

export const getDisplayValue = (value) => {
  if (typeof value === "boolean") {
    if (value === true) {
      return "True";
    } else if (value === false) {
      return "False";
    }
  }

  return value;
};

export const getPercentageColor = (value) => {
  if (value >= 90) {
    return "#008568";
  } else if (value >= 80) {
    return "#0074C8";
  } else if (value >= 70) {
    return "#d17216";
  } else {
    return "#d11616";
  }
};

export const getPercentage = (score, max) => {
  let percentage = 0;
  if (typeof score === "number" && typeof max === "number") {
    percentage = Math.round((score / max) * 100);
  }
  return percentage;
};

export const generateQuiz = (quizQuestions, desiredLength) => {
    let indexes = getArrayOfRandomNumbers(
      desiredLength,
      quizQuestions.length
    );
    let quiz = [];

    indexes.forEach((index) => {
      let question = {};
      question.question = quizQuestions[index].q;
      question.followup = quizQuestions[index].followup;
      question.img = quizQuestions[index].img;
      question.extratext = quizQuestions[index].extratext;
      let copiedAnswers = [...quizQuestions[index].a];
      question.correctAnswer = quizQuestions[index].a[0];
      question.answers = shuffleAnswers(copiedAnswers);

      quiz.push(question);
    });

    return quiz;
}
