import { AbsoluteFill, Easing, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { GOLD, GOLD_LIGHT, GREEK_FONT, MUTED, NIGHT, PARCHMENT, TITLE_FONT } from "../style";
import { Embers } from "./Atmosphere";

const Backdrop: React.FC = () => {
  const frame = useCurrentFrame();
  const glow = 0.8 + 0.08 * Math.sin(frame * 0.21) + 0.05 * Math.sin(frame * 0.77);
  return (
    <AbsoluteFill style={{ backgroundColor: NIGHT }}>
      <AbsoluteFill
        style={{
          opacity: glow,
          background: "radial-gradient(circle at 50% 50%, rgba(140,70,22,0.55) 0%, rgba(80,36,10,0.25) 32%, rgba(8,6,5,0) 62%)",
        }}
      />
    </AbsoluteFill>
  );
};

const goldText: React.CSSProperties = {
  backgroundImage: `linear-gradient(100deg, ${GOLD} 0%, ${GOLD} 38%, ${GOLD_LIGHT} 50%, ${GOLD} 62%, ${GOLD} 100%)`,
  backgroundSize: "300% 100%",
  WebkitBackgroundClip: "text",
  backgroundClip: "text",
  color: "transparent",
};

// Opening card: series line, the keyword letter by letter in gold, a Greek subline.
export const TitleCard: React.FC<{
  readonly series: string;
  readonly part: number;
  readonly keyword: string;
  readonly greek: string;
  readonly latin: string;
  readonly fast?: boolean;
}> = ({ series, part, keyword, greek, latin, fast = false }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const k = fast ? 0.6 : 1;
  const seriesIn = interpolate(frame, [0, 18 * k], [0, 1], { extrapolateRight: "clamp" });
  const shimmer = interpolate(frame, [20 * k, 70 * k], [100, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const subIn = interpolate(frame, [26 * k, 48 * k], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill>
      <Backdrop />
      <Embers count={30} seed={7} opacity={0.75} />
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", flexDirection: "column", translate: "0px -40px" }}>
        <div
          style={{
            fontFamily: TITLE_FONT,
            fontWeight: 400,
            fontSize: 40,
            color: MUTED,
            opacity: seriesIn,
            letterSpacing: interpolate(seriesIn, [0, 1], [20, 10]),
            marginBottom: 26,
          }}
        >
          {`${series}  ·  TEIL ${part}`}
        </div>
        <div style={{ display: "flex", fontFamily: TITLE_FONT, fontWeight: 900, fontSize: 150, letterSpacing: 6 }}>
          {keyword.split("").map((ch, i) => {
            const s = spring({ frame: frame - (6 + i * 3) * k, fps, config: { damping: 200 } });
            return (
              <span
                key={i}
                style={{
                  ...goldText,
                  backgroundPosition: `${shimmer}% 0%`,
                  opacity: s,
                  translate: `0px ${interpolate(s, [0, 1], [40, 0])}px`,
                  filter: `blur(${interpolate(s, [0, 1], [8, 0])}px) drop-shadow(0 0 24px rgba(232,180,90,0.45))`,
                }}
              >
                {ch}
              </span>
            );
          })}
        </div>
        <div style={{ marginTop: 18, opacity: subIn, fontSize: 64, color: PARCHMENT, display: "flex", gap: 22, alignItems: "baseline" }}>
          <span style={{ fontFamily: GREEK_FONT }}>{greek}</span>
          <span style={{ fontFamily: TITLE_FONT, color: MUTED, fontSize: 40 }}>·</span>
          <span style={{ fontFamily: TITLE_FONT, fontSize: 52, color: MUTED }}>{latin}</span>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// Closing card: next part, channel logo, name, slogan and a subscribe pill that
// pulses while the narrator says "Abonniere".
export const EndCard: React.FC<{ readonly nextPart: number; readonly subscribeAtFrame: number }> = ({ nextPart, subscribeAtFrame }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const head = spring({ frame, fps, config: { damping: 200 } });
  const logo = spring({ frame: frame - 6, fps, config: { damping: 14, mass: 0.8 } });
  const name = interpolate(frame, [12, 28], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const sub = spring({ frame: frame - subscribeAtFrame, fps, config: { damping: 12 } });
  const pulse = 1 + 0.04 * Math.max(0, Math.sin((frame - subscribeAtFrame) * 0.25)) * (frame > subscribeAtFrame ? 1 : 0);
  return (
    <AbsoluteFill>
      <Backdrop />
      <Embers count={22} seed={11} opacity={0.6} />
      <AbsoluteFill style={{ alignItems: "center", flexDirection: "column", paddingTop: 260 }}>
        <div
          style={{
            ...goldText,
            fontFamily: TITLE_FONT,
            fontWeight: 900,
            fontSize: 92,
            letterSpacing: 4,
            opacity: head,
            translate: `0px ${interpolate(head, [0, 1], [-30, 0])}px`,
            filter: "drop-shadow(0 0 20px rgba(232,180,90,0.45))",
          }}
        >
          {`TEIL ${nextPart} FOLGT`}
        </div>
        <div
          style={{
            marginTop: 60,
            width: 470,
            height: 470,
            borderRadius: "50%",
            overflow: "hidden",
            scale: String(interpolate(logo, [0, 1], [0.6, 1])),
            opacity: Math.min(1, logo * 1.4),
            boxShadow: `0 0 0 6px rgba(232,180,90,0.85), 0 0 ${50 + 20 * Math.sin(frame * 0.15)}px rgba(232,150,60,0.55)`,
          }}
        >
          <Img src={staticFile("shared/logo.jpg")} style={{ width: "100%", height: "100%" }} />
        </div>
        <div style={{ marginTop: 56, opacity: name, fontFamily: TITLE_FONT, fontWeight: 700, fontSize: 84, color: PARCHMENT }}>Age of Geschichte</div>
        <div style={{ marginTop: 8, opacity: name, fontFamily: TITLE_FONT, fontSize: 38, color: MUTED, letterSpacing: 1 }}>
          Mythen. Legenden. Was wirklich geschah.
        </div>
        <div
          style={{
            marginTop: 70,
            padding: "22px 56px",
            borderRadius: 60,
            background: "linear-gradient(180deg, #E0262B 0%, #B5161B 100%)",
            color: "white",
            fontFamily: "Montserrat",
            fontWeight: 800,
            fontSize: 46,
            letterSpacing: 3,
            opacity: sub,
            scale: String(interpolate(sub, [0, 1], [0.7, 1], { easing: Easing.out(Easing.quad) }) * pulse),
            boxShadow: "0 10px 30px rgba(0,0,0,0.5)",
          }}
        >
          ABONNIEREN
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// Small series badge at the top, so every part reads as a continuation.
export const SeriesBadge: React.FC<{ readonly label: string }> = ({ label }) => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{ alignItems: "center" }}>
      <div
        style={{
          marginTop: 150,
          padding: "10px 26px",
          borderRadius: 40,
          background: "rgba(8,6,5,0.45)",
          border: "1.5px solid rgba(232,180,90,0.45)",
          fontFamily: TITLE_FONT,
          fontWeight: 700,
          fontSize: 28,
          letterSpacing: 5,
          color: GOLD_LIGHT,
          opacity: interpolate(frame, [0, 15], [0, 0.9], { extrapolateRight: "clamp" }),
        }}
      >
        {label}
      </div>
    </AbsoluteFill>
  );
};
