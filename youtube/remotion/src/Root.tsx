import { Composition } from "remotion";
import { fontsLoaded } from "./style";
import { Teil1, TEIL1_FRAMES } from "./teil1/Teil1";

// Keep a reference so the font loading promise is part of the bundle.
void fontsLoaded;

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition id="Odyssee-Teil1" component={Teil1} durationInFrames={TEIL1_FRAMES} fps={30} width={1080} height={1920} />
    </>
  );
};
