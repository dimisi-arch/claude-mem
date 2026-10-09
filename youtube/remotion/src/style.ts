// Series look for "Age of Geschichte" (see the series bible in Notion).
import { loadFont } from "@remotion/fonts";
import { staticFile } from "remotion";

export const GOLD = "#E8B45A";
export const GOLD_LIGHT = "#F6DDA4";
export const PARCHMENT = "#F5EBD7";
export const MUTED = "#C8B496";
export const NIGHT = "#080605";

export const TITLE_FONT = "Cinzel";
export const CAPTION_FONT = "Montserrat";
export const GREEK_FONT = "GFS Didot";

export const fontsLoaded = Promise.all([
  loadFont({ family: TITLE_FONT, url: staticFile("fonts/cinzel-latin-400-normal.woff2"), weight: "400" }),
  loadFont({ family: TITLE_FONT, url: staticFile("fonts/cinzel-latin-700-normal.woff2"), weight: "700" }),
  loadFont({ family: TITLE_FONT, url: staticFile("fonts/cinzel-latin-900-normal.woff2"), weight: "900" }),
  loadFont({ family: CAPTION_FONT, url: staticFile("fonts/montserrat-latin-600-normal.woff2"), weight: "600" }),
  loadFont({ family: CAPTION_FONT, url: staticFile("fonts/montserrat-latin-800-normal.woff2"), weight: "800" }),
  loadFont({ family: GREEK_FONT, url: staticFile("fonts/gfs-didot-greek-400-normal.woff2"), weight: "400" }),
]);

// Deterministic pseudo-random numbers (renders must be identical frame by frame).
export const rand = (seed: number) => {
  const x = Math.sin(seed * 12.9898 + 78.233) * 43758.5453;
  return x - Math.floor(x);
};
