// export const getPercentageColor = (scorePercentage) => {
//     if (scorePercentage >= 90) {
//         return "#279638";
//     } else if (scorePercentage >= 80) {
//         return "#1664d1";
//     } else if (scorePercentage >= 70) {
//         return "#d17216"
//     } else {
//         return "#d11616";
//     }
// }

import { getPercentageColor } from "../src/components/utils.js";

const green = "#008568";
const blue = "#0074C8";
const orange = "#d17216";
const red = "#d11616";

describe("getPercentageColor Tests", () => {
  test("90 thru 100 returns Green", () => {
    for (let index = 90; index < 101; index++) {
      let color = getPercentageColor(index);
      expect(color).toBe(green);
    }
  });
  test("80 thru 89 returns Blue", () => {
    for (let index = 80; index < 90; index++) {
      let color = getPercentageColor(index);
      expect(color).toBe(blue);
    }
  });
  test("70 thru 79 returns Orange", () => {
    for (let index = 70; index < 80; index++) {
      let color = getPercentageColor(index);
      expect(color).toBe(orange);
    }
  });
  test("0 thru 69 returns Red", () => {
    for (let index = 0; index < 70; index++) {
      let color = getPercentageColor(index);
      expect(color).toBe(red);
    }
  });
});