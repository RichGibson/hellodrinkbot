import { getPercentage } from "../src/components/utils.js";

describe("getPercentage Tests", () => {
  test("10 out of 10 returns 100", () => {
    expect(getPercentage(10, 10)).toBe(100);
  });

  test("0 out of 10 returns 0", () => {
    expect(getPercentage(0, 10)).toBe(0);
  });

  test("4 out of 5 returns 80", () => {
    expect(getPercentage(4, 5)).toBe(80);
  });

  // TODO: Handle these scenarios
  test("NaN results in 0", () => {
    expect(getPercentage("5", "Five")).toBe(0);
  });

  test("null results in 0", () => {
    expect(getPercentage(null, null)).toBe(0);
  });
});