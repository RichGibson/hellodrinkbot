import { shuffleAnswers } from "../src/components/utils.js";

describe("shuffleAnswers Tests", () => {
  test("output array equals same length as input array", () => {
    let sampleArray = [1, 2, 3, 4, 5];
    let sampleArrayLength = sampleArray.length;
    let shuffledArray = shuffleAnswers(sampleArray);
    expect(shuffledArray).toHaveLength(sampleArrayLength);
  });
});