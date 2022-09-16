import { getDisplayValue } from "../src/components/utils.js";

describe("getDisplayValue Tests", () => {
  test("true returns True", () => {
    expect(getDisplayValue(true)).toBe("True");
  });
  test("false returns False", () => {
    expect(getDisplayValue(false)).toBe("False");
  });
  test("string returns string", () => {
    expect(getDisplayValue("test")).toBe("test");
  });
  test("number returns number", () => {
    expect(getDisplayValue(5)).toBe(5);
  });
  test("null returns null", () => {
    expect(getDisplayValue(null)).toBe(null);
  });
});