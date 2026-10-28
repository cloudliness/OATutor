# Deploy this fork on Vercel

This branch is a standalone copy of OATutor for personal study. A Vercel
build does not need Firebase, LTI, Canvas, or any API keys. Mastery stays
in the browser (IndexedDB via localForage, plus the course-unlock flag in
`localStorage`).

## Import settings

| Setting | Value |
| --- | --- |
| Framework preset | Create React App |
| Root directory | `./` (repository root) |
| Install command | `npm ci` |
| Build command | `npm run build` |
| Output directory | `build` |
| Node.js version | 20.x or 22.x is fine. The build script sets `NODE_OPTIONS=--openssl-legacy-provider` so webpack 4 still runs on current Node. |

`vercel.json` already sets the framework, install command, build command,
output directory, and a rewrite so any path serves `index.html`. The app
uses hash routes (`/#/courses/0`), so refreshes work even without that
rewrite. The rewrite covers a direct visit to a non-hash path.

## Environment variables

None. Leave the env section empty.

These are intentionally unused in this fork:

- `REACT_APP_FIREBASE_CONFIG` — logging is off (`ENABLE_FIREBASE` and `DO_LOG_DATA` are false).
- `REACT_APP_AI_AGENT_URL` — the chat tutor is not configured. Lessons that are only a chat window will not have a model. Ordinary problem lessons do not need it.
- `REACT_APP_TTS_AWS_ENDPOINT` — text-to-speech playback is skipped when this is unset.
- `AI_HINT_GENERATION_AWS_ENDPOINT` — generated hints are off.

Do not paste the upstream project's Firebase or AWS secrets into the Hobby project.

## What the build pulls in

`npm run build` runs `scripts/ensure-content.js`, which checks out the public
submodule [CAHLR/OATutor-Content](https://github.com/CAHLR/OATutor-Content)
at commit `1925decc91567faf6203bdb41b9d52b14891426f` (the commit recorded in
this repo). If submodule checkout fails, the script clones that repository
over HTTPS. No deploy key is required.

Pre-Algebra is original content in this repo (`src/local-content/prealgebra`),
merged into the problem pool at build time. It is not part of the upstream
content submodule.

The processed pool is written to `public/static/content/oatutor.json` and
fetched at runtime, instead of being compiled into the JavaScript bundle.
Figures from the content repo are copied into the build as static images.

## Phone install

`public/manifest.json` plus `public/icons/icon-192.png` and
`public/icons/icon-512.png` make the site installable. On iOS, use Share →
Add to Home Screen. A service worker is registered in production so the app
shell can open again after the first visit. The lesson JSON and figures are
large, so a fully offline library is not cached.

## Course unlock

Pre-Algebra and OpenStax Elementary Algebra are open immediately. Every
other course shows “Pass the Algebra Check to unlock” until this browser
stores a pass. The flag is `localStorage` key `oatutor-advanced-unlock`.
The course list has a **Reset course unlock** button for testing. Resetting
lesson progress does not clear that flag, and clearing the flag does not
erase mastery.
