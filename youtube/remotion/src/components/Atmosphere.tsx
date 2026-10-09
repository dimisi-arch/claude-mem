import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { rand } from "../style";

// Flickering firelight: a warm glow whose strength wobbles like a flame.
export const FireLight: React.FC<{ readonly x: number; readonly y: number; readonly radius?: number; readonly strength?: number }> = ({
  x,
  y,
  radius = 0.55,
  strength = 0.35,
}) => {
  const frame = useCurrentFrame();
  const flicker = 0.75 + 0.12 * Math.sin(frame * 0.53) + 0.08 * Math.sin(frame * 1.37 + 2) + 0.05 * Math.sin(frame * 3.1 + 5);
  return (
    <AbsoluteFill
      style={{
        mixBlendMode: "screen",
        opacity: strength * flicker,
        background: `radial-gradient(circle at ${x * 100}% ${y * 100}%, rgba(255,150,60,0.9) 0%, rgba(255,110,30,0.35) ${radius * 45}%, rgba(0,0,0,0) ${radius * 100}%)`,
      }}
    />
  );
};

// Glowing embers drifting upwards. Positions are seeded, so every render is identical.
export const Embers: React.FC<{ readonly count?: number; readonly seed?: number; readonly opacity?: number }> = ({
  count = 26,
  seed = 1,
  opacity = 0.85,
}) => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();
  return (
    <AbsoluteFill style={{ opacity, pointerEvents: "none" }}>
      {new Array(count).fill(0).map((_, i) => {
        const r1 = rand(seed * 100 + i);
        const r2 = rand(seed * 200 + i);
        const r3 = rand(seed * 300 + i);
        const speed = 40 + r2 * 90; // px per second
        const life = height * 0.75 + r3 * height * 0.4;
        const travelled = (r1 * life + (frame / fps) * speed) % life;
        const y = height + 20 - travelled;
        const x = r1 * width + Math.sin(frame / fps * (0.6 + r2) + i) * 26;
        const size = 3 + r3 * 5;
        const fade = Math.min(1, travelled / 120) * Math.max(0, 1 - travelled / life);
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: x,
              top: y,
              width: size,
              height: size,
              borderRadius: "50%",
              background: "rgba(255,190,110,1)",
              boxShadow: `0 0 ${size * 3}px ${size}px rgba(255,120,40,0.7)`,
              opacity: fade * (0.5 + 0.5 * Math.sin(frame * 0.3 + i * 1.7)),
            }}
          />
        );
      })}
    </AbsoluteFill>
  );
};

export const Vignette: React.FC = () => (
  <AbsoluteFill
    style={{
      background: "radial-gradient(ellipse 75% 62% at 50% 48%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.5) 88%, rgba(0,0,0,0.72) 100%)",
    }}
  />
);
