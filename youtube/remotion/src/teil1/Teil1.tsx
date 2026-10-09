import { Audio } from "@remotion/media";
import { AbsoluteFill, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Embers, FireLight, Vignette } from "../components/Atmosphere";
import { Captions, Page } from "../components/Captions";
import { EndCard, SeriesBadge, TitleCard } from "../components/Cards";
import { Focus, KenBurns } from "../components/KenBurns";
import data from "./captions.json";

// Odyssee, Teil 1 "Niemand". Timing comes from captions.json, which is built
// from the voice track (Whisper word timestamps aligned to the script).
const piece = (key: string) => {
  const p = data.pieces.find((x) => x.key === key);
  if (!p) throw new Error(`missing piece ${key}`);
  return p;
};
const pages = data.pages as Page[];
const wordStart = (text: string) => pages.flatMap((p) => p.words).find((w) => w.text === text)!.startMs / 1000;

const T = {
  n1: piece("n1").start,
  n2: piece("n2").start,
  n3: piece("n3").start,
  n5: piece("n5").start,
  nb: piece("nb").start,
  poly: piece("poly").start,
  n7: piece("n7").start,
  list: wordStart("Eine") - 0.15,
  end1: piece("end1").start,
  end2: piece("end2").start,
  total: data.totalMs / 1000,
  sfx1: 11.454, // boulder sound effects in the mix (see the audio recipe)
  sfx2: 37.776,
};
const XF = 10; // crossfade frames

const IMG = {
  auge: { src: "teil1/auge.jpg", w: 2752, h: 1536 },
  felsen: { src: "teil1/felsen.jpg", w: 2752, h: 1536 },
  wein: { src: "teil1/wein.jpg", w: 1536, h: 2752 },
  schatten: { src: "teil1/schatten.jpg", w: 1536, h: 2752 },
  nacht: { src: "teil1/nacht.jpg", w: 1536, h: 2752 },
};

// Camera shake in pixels: boulder impacts and Polyphem's roar.
const shakeAt = (t: number) => {
  const hit = (t0: number, amp: number, decay: number) => (t >= t0 ? amp * Math.exp(-(t - t0) * decay) : 0);
  return (
    hit(T.sfx1, 9, 3) + hit(T.sfx1 + 1.1, 5, 4) + hit(T.poly, 16, 3.2) + hit(T.sfx2, 5, 3) + hit(T.sfx2 + 1.1, 3, 4)
  );
};

const Shot: React.FC<{
  readonly from: number;
  readonly to: number;
  readonly first?: boolean;
  readonly children: React.ReactNode;
}> = ({ from, to, first = false, children }) => {
  const { fps } = useVideoConfig();
  const start = Math.round(from * fps) - (first ? 0 : XF);
  return (
    <Sequence from={Math.max(0, start)} durationInFrames={Math.round(to * fps) - Math.max(0, start)} premountFor={fps}>
      {children}
    </Sequence>
  );
};

const Still: React.FC<{ readonly img: (typeof IMG)["auge"]; readonly a: Focus; readonly b: Focus; readonly sway?: number }> = ({
  img,
  a,
  b,
  sway = 0,
}) => <KenBurns src={img.src} imgW={img.w} imgH={img.h} from={a} to={b} fadeIn={XF} shake={sway} />;

export const Teil1: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const s = shakeAt(t);
  const dx = s * Math.sin(frame * 2.1);
  const dy = s * Math.cos(frame * 2.7);

  return (
    <AbsoluteFill style={{ backgroundColor: "black" }}>
      <AbsoluteFill style={{ translate: `${dx}px ${dy}px`, scale: s > 0.5 ? "1.03" : "1" }}>
        <Shot from={0} to={T.n1} first>
          <TitleCard series="DIE ODYSSEE" part={1} keyword="NIEMAND" greek="Οὖτις" latin="Outis" />
        </Shot>
        <Shot from={T.n1} to={T.n2}>
          <Still img={IMG.auge} a={{ x: 0.62, y: 0.66, zoom: 2.0 }} b={{ x: 0.5, y: 0.5, zoom: 1.0 }} />
          <FireLight x={0.5} y={0.42} radius={0.5} strength={0.22} />
        </Shot>
        <Shot from={T.n2} to={T.n3}>
          <Still img={IMG.felsen} a={{ x: 0.72, y: 0.5, zoom: 1.0 }} b={{ x: 0.24, y: 0.5, zoom: 1.0 }} />
          <FireLight x={0.3} y={0.55} radius={0.7} strength={0.25} />
        </Shot>
        <Shot from={T.n3} to={T.n5}>
          <Still img={IMG.wein} a={{ x: 0.5, y: 0.5, zoom: 1.0 }} b={{ x: 0.5, y: 0.38, zoom: 1.3 }} />
          <FireLight x={0.55} y={0.98} radius={0.75} strength={0.3} />
          <Embers count={14} seed={3} opacity={0.5} />
        </Shot>
        <Shot from={T.n5} to={T.nb}>
          <Still img={IMG.schatten} a={{ x: 0.5, y: 0.5, zoom: 1.08 }} b={{ x: 0.5, y: 0.45, zoom: 1.18 }} sway={1} />
          <FireLight x={0.45} y={1.0} radius={0.8} strength={0.35} />
          <Embers count={14} seed={5} opacity={0.5} />
        </Shot>
        <Shot from={T.nb} to={T.poly}>
          <Still img={IMG.nacht} a={{ x: 0.5, y: 0.42, zoom: 1.35 }} b={{ x: 0.5, y: 0.45, zoom: 1.2 }} />
        </Shot>
        <Shot from={T.poly} to={T.n7}>
          <Still img={IMG.schatten} a={{ x: 0.5, y: 0.42, zoom: 1.25 }} b={{ x: 0.5, y: 0.4, zoom: 1.32 }} sway={1.5} />
          <FireLight x={0.45} y={1.0} radius={0.8} strength={0.4} />
        </Shot>
        <Shot from={T.n7} to={T.list}>
          <Still img={IMG.nacht} a={{ x: 0.5, y: 0.45, zoom: 1.2 }} b={{ x: 0.5, y: 0.5, zoom: 1.0 }} />
        </Shot>
        <Shot from={T.list} to={T.end1}>
          <TitleCard series="DIE ODYSSEE" part={1} keyword="NIEMAND" greek="Οὖτις" latin="Outis" fast />
        </Shot>
        <Shot from={T.end1} to={T.end2}>
          <Still img={IMG.nacht} a={{ x: 0.5, y: 0.8, zoom: 1.5 }} b={{ x: 0.5, y: 0.85, zoom: 1.75 }} />
          <FireLight x={0.5} y={0.78} radius={0.55} strength={0.3} />
        </Shot>
        <Shot from={T.end2} to={T.total}>
          <EndCard nextPart={2} subscribeAtFrame={Math.round(0.2 * fps)} />
        </Shot>
        <Vignette />
      </AbsoluteFill>

      <Sequence from={Math.round(T.n1 * fps)} durationInFrames={Math.round((T.end2 - T.n1) * fps)} premountFor={fps}>
        <SeriesBadge label="DIE ODYSSEE · TEIL 1" />
      </Sequence>
      <Sequence durationInFrames={Math.round(T.end2 * fps)}>
        <Captions pages={pages} />
      </Sequence>
      <Audio src={staticFile("teil1/ton.m4a")} />
    </AbsoluteFill>
  );
};

export const TEIL1_FRAMES = Math.ceil(T.total * 30);
