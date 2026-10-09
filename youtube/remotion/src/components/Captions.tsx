import { AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { CAPTION_FONT, GOLD, MUTED, TITLE_FONT } from "../style";

export type Word = { text: string; startMs: number; endMs: number; key: boolean };
export type Page = { startMs: number; endMs: number; speaker: string | null; words: Word[] };

// Word-by-word captions: the whole line is visible, the spoken word lights up
// in gold and pops slightly; keywords ("Niemand") stay gold. Character lines
// carry the speaker's name above them.
export const Captions: React.FC<{ readonly pages: Page[]; readonly centerY?: number }> = ({ pages, centerY = 1250 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const ms = (frame / fps) * 1000;
  const page = pages.find((p) => ms >= p.startMs && ms < p.endMs);
  if (!page) return null;

  const since = ms - page.startMs;
  const enter = interpolate(since, [0, 180], [0, 1], { extrapolateRight: "clamp", easing: Easing.bezier(0.16, 1, 0.3, 1) });

  return (
    <AbsoluteFill>
      <div
        style={{
          position: "absolute",
          left: 90,
          right: 90,
          top: centerY,
          translate: `0px ${interpolate(enter, [0, 1], [18, 0])}px`,
          opacity: enter,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          transform: "translateY(-50%)",
        }}
      >
        {page.speaker ? (
          <div
            style={{
              fontFamily: TITLE_FONT,
              fontWeight: 700,
              fontSize: 34,
              letterSpacing: 6,
              color: MUTED,
              marginBottom: 10,
              textShadow: "0 2px 8px rgba(0,0,0,0.9)",
            }}
          >
            {page.speaker}
          </div>
        ) : null}
        <div style={{ display: "flex", flexWrap: "wrap", justifyContent: "center", columnGap: 26, rowGap: 4 }}>
          {page.words.map((w, i) => {
            const active = ms >= w.startMs && ms < w.endMs;
            const spoken = ms >= w.startMs;
            const pop = interpolate(ms - w.startMs, [0, 90, 220], [1, 1.09, 1.04], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
            });
            const gold = w.key || active;
            return (
              <span
                key={i}
                style={{
                  fontFamily: CAPTION_FONT,
                  fontWeight: 800,
                  fontSize: 64,
                  lineHeight: 1.18,
                  color: gold ? GOLD : "#FFFFFF",
                  opacity: spoken || w.key ? 1 : 0.55,
                  scale: active ? String(pop) : "1",
                  WebkitTextStroke: "10px rgba(0,0,0,0.92)",
                  paintOrder: "stroke fill",
                  textShadow: active || w.key ? "0 0 22px rgba(232,180,90,0.55), 0 4px 10px rgba(0,0,0,0.8)" : "0 4px 10px rgba(0,0,0,0.8)",
                }}
              >
                {w.text}
              </span>
            );
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};
