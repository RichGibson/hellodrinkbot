import { getArrayOfRandomNumbers } from "../src/components/utils.js";

describe("getArrayOfRandomNumbers Tests", () => {
  test("Array length to be 5 if input is 5", () => {
    let arrayLength = 5;
    let array = getArrayOfRandomNumbers(arrayLength, 5);
    expect(array).toHaveLength(arrayLength);
  });

  test("Array does not contain number higher than max", () => {
    let max = 50;
    let array = getArrayOfRandomNumbers(49, max);
    array.forEach((element) => {
      expect(element).toBeLessThan(max);
    });
  });
});