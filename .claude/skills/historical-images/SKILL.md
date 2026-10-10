---
name: historical-images
description: Find free, public-domain historical images (paintings, vase paintings, engravings, maps, objects) for an episode of the YouTube channel "Age of Geschichte" from museum open-access collections, with source and license for each, and redraw them in the channel's friendly hand-drawn style. Use when the user wants pictures, visuals, Bilder or B-roll for a history topic or episode, or asks where to get images without paying for AI generation.
---

# Historical images for an episode

Museums publish millions of old artworks as public domain (CC0). For a history channel
they are better than AI images: authentic, free, and safe to use in a monetised video.
`scripts/find_images.py` searches three sources that need no API key and returns only
public-domain items: Art Institute of Chicago, The Metropolitan Museum of Art, and
Wikimedia Commons. Standard-library Python only.

## Workflow

1. **Topic.** Take the episode from the user, or read its work page in Notion
   (the "Geschichtskanal: Kanal-Zentrale" page lists them; see session notes).
2. **Search terms — in English.** Museum metadata is English. Search several terms per
   scene: the English, Greek and Latin names (Odysseus / Ulysses, Polyphemus / Cyclops),
   the scene ("blinding of Polyphemus"), and object types ("Greek vase Odysseus",
   "amphora", "engraving"). One person or scene per query works better than a sentence.
3. **Run** for each term:
   `python3 .claude/skills/historical-images/scripts/find_images.py "TERM" --limit 5`
   and, for the ones worth keeping,
   `... "TERM" --limit 5 --download <scratchpad>/bilder-<episode>`.
   Images go to the scratchpad, never into the repo.
4. **Choose.** Read titles and dates: keep what actually shows the scene, prefer ancient
   and old-master works, say when a work is a later re-imagining (e.g. 19th-century
   painting of an ancient myth) and drop duplicates and unrelated hits (the search is
   full-text, so "Cyclops" also finds an oil lamp). Aim for 5–10 strong images per episode.
5. **Restyle into the channel look.** The user does not want the museum images as they
   are (2026-10-10): they must look clearly *drawn* — friendly, less natural, not a photo,
   not a painting, not anime. Use the museum image as the composition reference and let an
   image model redraw it:
   - **Canva** (no credits needed, plan quota): upload the file with `create-upload-url`
     (POST the raw bytes), then `generate-image` with the media id in `imageReferences`,
     `aspectRatio: PORTRAIT_9_16` for Shorts, and the style prompt below plus one line on
     what the scene shows. Poll `get-generate-image-job`; the result is a Canva media id
     with an "Open generated image" link.
   - **Runway** `generate_image` with the museum image *and* the channel's style reference
     (Runway task 47abaccc, see the Notion series bible) as `referenceImages` — needs credits.
   - Style prompt (test 2, 2026-10-10 — the user approved the direction of test 1 and asked
     for "more drawn, friendlier"; update this line when they approve a newer test):
     `Redraw as a friendly hand-drawn illustration, same composition. Clearly hand-drawn and
     inked, clean confident line art with visible pen strokes, simplified slightly stylized
     shapes, expressive faces, soft cel shading with flat colour areas, warm storybook
     graphic-novel look like modern animated-film concept art, a light touch of
     anime-influenced linework but NOT anime, NOT photorealistic, NOT a painting, NOT 3D.
     Mediterranean palette: turquoise and Aegean blue sea, ochre and terracotta rocks,
     golden sunlight. Dynamic sense of motion. No text.`
   - Fixed rules from the series bible: the Cyclops has exactly one eye in the middle of
     his forehead; violence only as shadow or hint.
   - Later (user's wish): a light animation of the stills — a slow pan or zoom in the
     edit, or a short image-to-video clip once credits are available.
6. **Hand over** in German: a short list per image — what it shows, artist, date,
   museum, license, link — and send the downloaded files with SendUserFile. Offer to put
   the list on the episode's Notion page; write there only after a yes. A restyled image
   is a new, AI-made work based on a public-domain original: credit the original, and keep
   the YouTube "altered or synthetic content" box ticked as for all AI images.

## Credit line

CC0 needs no credit, but the channel names its sources. Suggest one line per image for
the video description, e.g. `Bild: Arnold Böcklin, Odysseus und Polyphem (1896), Wikimedia Commons, gemeinfrei`.

## Known limits (tested 2026-10-10 from a cloud container)

- The Art Institute's image server sits behind a Cloudflare bot check that blocks cloud
  addresses: its results are listed, but `--download` skips them with a note. The links
  open normally in the user's browser, and downloads work from the user's PC.
- The Met answers bursts with 403 and Commons with 429; the script waits once and
  retries. If a source still fails, the others are still returned.
- Wikimedia "public domain" depends on the uploader's tag. For a key image, open the
  source page and check the tag matches an old work (author dead more than 70 years).
- More museum APIs (Smithsonian, Rijksmuseum, Europeana; free key needed) are in the
  public-apis list — see the `free-resources` skill.
