import { AbsoluteFill, Easing, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";

export type Focus = { x: number; y: number; zoom: number };

type Props = {
  readonly src: string;
  readonly imgW: number;
  readonly imgH: number;
  readonly from: Focus;
  readonly to: Focus;
  /** Extra fade-in frames at the start (crossfade from the previous shot). */
  readonly fadeIn?: number;
  readonly shake?: number;
};

// Slow zoom/pan over a still, framed for 9:16. The focus point (0..1 of the
// image) is kept centred where possible; the image always covers the frame.
export const KenBurns: React.FC<Props> = ({ src, imgW, imgH, from, to, fadeIn = 0, shake = 0 }) => {
  const frame = useCurrentFrame();
  const { width, height, durationInFrames } = useVideoConfig();
  const p = interpolate(frame, [0, durationInFrames - 1], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.45, 0, 0.55, 1),
  });
  const zoom = from.zoom + (to.zoom - from.zoom) * p;
  const fx = from.x + (to.x - from.x) * p;
  const fy = from.y + (to.y - from.y) * p;
  const scale = Math.max(width / imgW, height / imgH) * zoom;
  const w = imgW * scale;
  const h = imgH * scale;
  const sx = shake ? Math.sin(frame * 0.9) * 0.004 + Math.sin(frame * 2.3) * 0.002 : 0;
  const sy = shake ? Math.sin(frame * 0.7 + 1) * 0.003 : 0;
  const left = Math.min(0, Math.max(width - w, width / 2 - (fx + sx * shake) * w));
  const top = Math.min(0, Math.max(height - h, height / 2 - (fy + sy * shake) * h));
  const opacity = fadeIn > 0 ? interpolate(frame, [0, fadeIn], [0, 1], { extrapolateRight: "clamp" }) : 1;

  return (
    <AbsoluteFill style={{ opacity, overflow: "hidden" }}>
      <Img src={staticFile(src)} style={{ position: "absolute", left, top, width: w, height: h }} />
    </AbsoluteFill>
  );
};
