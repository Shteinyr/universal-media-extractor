# Udemy Course Offline Export

Status: initial implementation complete.

This feature adds a local, best-effort Udemy course export path for courses the user can access in their own Udemy account.

## What Was Added

- `POST /udemy/analyze` inspects a Udemy course through `yt-dlp --dump-single-json --flat-playlist`.
- `POST /udemy/download` starts an in-memory job that downloads the course with `yt-dlp`.
- Static UI now has `Course mode` next to URL and Local file modes.
- Course mode accepts:
  - Udemy course or lecture URL;
  - default Chrome session auth;
  - advanced manual `cookies.txt` fallback;
  - output folder;
  - quality: Best, 1080p, 720p, 480p;
  - container: MP4, MKV, WEBM;
  - subtitles toggle.
- Downloads default to `~/Downloads/Universal Media Extractor/Udemy`.

## Safety Boundary

- The app does not store usernames or passwords.
- The app does not store cookies in output metadata.
- Chrome session mode uses `yt-dlp --cookies-from-browser chrome`.
- Manual cookies mode redacts the cookies path in the download log command.
- The app does not implement DRM bypass, decryption-key handling, CAPTCHA bypass, paywall bypass, or unauthorized access.
- If Udemy blocks a lecture because of DRM, expired cookies, or access restrictions, the app should return a clear error.

## Implementation Notes

- The first implementation is `yt-dlp` first because the project already uses `yt-dlp`, subprocess safety, job polling, cancellation, and output management.
- `Puyodead1/udemy-downloader` was studied as a reference, but was not vendored or shipped inside the app.
- That project includes DRM/decryption-key oriented behavior, which is outside this app's scope.
- Resource attachments are marked best-effort. The current `yt-dlp` path may not include every Udemy asset.

## Output Shape

Typical output:

```text
~/Downloads/Universal Media Extractor/Udemy/
  Course_Name/
    01 - Section/
      001 - Lecture.mp4
      001 - Lecture.srt
    .metadata/
      udemy_download_request.json
      udemy_download_result.json
    .logs/
      udemy_download.log
```

## How To Test Manually

1. Open Udemy in Chrome and make sure you are signed in.
2. Start the app:

```bash
.venv/bin/python scripts/run_api.py
```

3. Open `http://127.0.0.1:8000/`.
4. Choose `Course mode`.
5. Paste a Udemy URL. Prefer the URL from the opened course player, for example `/course/<slug>/learn/lecture/<id>`.
6. Keep `Login source` set to `Chrome session`.
7. Click `Analyze course`.
8. If analysis succeeds, choose quality/container and click `Download course`.

If Chrome session access is blocked by macOS or unavailable, switch `Login source` to `Manual cookies.txt` and provide a local cookies file.

Observed note: for some Udemy courses, the clean `/course/<slug>/` URL can fail in `yt-dlp` with `Unable to extract course id`, while the lecture/player URL for the same course works and returns the full course playlist. The UI no longer rewrites lecture URLs into clean course URLs.

Start with a small course or use a short test course first. Do not attempt DRM-protected or unauthorized courses.

## Automated Checks

Automated tests mock subprocess and do not contact Udemy:

```bash
.venv/bin/python -m pytest tests/test_udemy_course_service.py tests/test_api_app.py -q
```

## Remaining Limits

- Real Udemy proof requires a user-provided course URL and a valid Chrome Udemy session.
- Browser cookies can expire or be blocked by macOS permissions.
- Some clean course URLs may fail in `yt-dlp`; use the lecture/player URL from an opened course when that happens.
- Some courses or lectures may be DRM/protected.
- Udemy platform behavior can change.
- Attachments/resources are best-effort in this first implementation.
- Full distributable packaging is not part of this feature.
