# Setup Instructions

IMPORTANT: your repo must be named EXACTLY: hkgupta005-sketch
(must match your GitHub username exactly, or your README will not show on your
profile page — this is the #1 reason it "doesn't work" for people).

STEP-BY-STEP (copy-paste method, no git needed):

1. Extract this zip on your computer.

2. Go to github.com -> create a New repository -> name it exactly hkgupta005-sketch
   -> leave it empty (no README/gitignore) -> Create repository.
   (If it already exists, open it instead.)

3. In the repo, click "Add file" -> "Upload files". Drag in ALL the extracted files
   AND folders (README.md, banner.svg, lanyard.svg, stats.svg, langs.svg, trophies.svg,
   profile-illustration.jpg, SETUP.md, the .github folder, the scripts folder).
   Click "Commit changes".

   NOTE: the .github folder starts with a dot and sometimes doesn't drag-drop
   properly. If it's missing after upload, manually create the path
   .github/workflows/ in the repo (use "Add file" -> "Create new file" and type
   the full path including the file name, e.g. .github/workflows/snake.yml) and
   paste each workflow file's content in.

4. Go to repo Settings -> Actions -> General -> scroll to "Workflow permissions"
   -> select "Read and write permissions" -> Save.

5. Go to the "Actions" tab and run BOTH workflows once manually:
   - "Generate Snake"  -> Run workflow
   - "Update Stats"    -> Run workflow

6. Visit github.com/hkgupta005-sketch — this is now your live profile page.

WHAT THIS VERSION LOOKS LIKE:
- banner.svg: large character illustration with the background removed, blended
  directly onto the banner (no box/frame), name in a violet-to-gold gradient,
  a floating code-editor mockup, tech pills, About Me box, status badges.
- lanyard.svg: animated swinging ID card with a close-up face crop.
- Two-tone color palette only: deep violet (#7C3AED) + warm gold (#F5B800) on
  near-black.
- Tech Arsenal is a 3-column horizontal layout (Languages | AI/Data | Web/Backend/Tools).
- Real LinkedIn + Gmail links already filled in under "Let's Connect".
- stats.svg has a rank ring (S/A/B/C/D, computed live from your real GitHub data).

NOTES:
- stats.svg / langs.svg / trophies.svg show 0s / rank D right now because the
  account has no public repos yet — accurate, not a bug. They refresh automatically
  once you have real activity and the daily Action runs (or you re-run it manually).
- profile-illustration.jpg is just a backup copy of your art — banner.svg and
  lanyard.svg already have the image embedded inside them, so you don't need to
  reference this file anywhere for things to work.
