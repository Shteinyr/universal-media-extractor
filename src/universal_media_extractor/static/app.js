const API_BASE_URL = "";
const form = document.querySelector("#analyze-form");
const localFileForm = document.querySelector("#local-file-form");
const courseForm = document.querySelector("#course-form");
const batchForm = document.querySelector("#batch-form");
const urlModeButton = document.querySelector("#url-mode-button");
const localModeButton = document.querySelector("#local-mode-button");
const batchModeButton = document.querySelector("#batch-mode-button");
const courseModeButton = document.querySelector("#course-mode-button");
const urlInput = document.querySelector("#url-input");
const localFileInput = document.querySelector("#local-file-input");
const localFileName = document.querySelector("#local-file-name");
const localAnalyzeButton = document.querySelector("#local-analyze-button");
const batchUrlInput = document.querySelector("#batch-url-input");
const batchPasteButton = document.querySelector("#batch-paste-button");
const batchTextFileInput = document.querySelector("#batch-text-file-input");
const playlistAnalyzeButton = document.querySelector("#playlist-analyze-button");
const courseUrlInput = document.querySelector("#course-url-input");
const courseAuthSourceSelect = document.querySelector("#course-auth-source");
const courseCookiesPathInput = document.querySelector("#course-cookies-path");
const courseManualCookiesPanel = document.querySelector("#course-manual-cookies-panel");
const courseAnalyzeButton = document.querySelector("#course-analyze-button");
const analyzeButton = document.querySelector("#analyze-button");
const apiStatus = document.querySelector("#api-status");
const emptyState = document.querySelector("#empty-state");
const loadingState = document.querySelector("#loading-state");
const resultContent = document.querySelector("#result-content");
const thumbnail = document.querySelector("#thumbnail");
const thumbnailWrap = document.querySelector(".thumbnail-wrap");
const extractorPill = document.querySelector("#extractor-pill");
const duration = document.querySelector("#duration");
const mediaTitle = document.querySelector("#media-title");
const uploader = document.querySelector("#uploader");
const webpageLink = document.querySelector("#webpage-link");
const warningsPanel = document.querySelector("#warnings-panel");
const warningsList = document.querySelector("#warnings-list");
const errorsPanel = document.querySelector("#errors-panel");
const errorsList = document.querySelector("#errors-list");
const formatPicker = document.querySelector("#format-picker");
const formatPickerEmpty = document.querySelector("#format-picker-empty");
const presetList = document.querySelector("#preset-list");
const advancedFormatDetails = document.querySelector("#advanced-format-details");
const formatTabs = document.querySelectorAll(".format-tab");
const flowSteps = document.querySelectorAll("#flow-steps li");
const downloadPanel = document.querySelector("#download-panel");
const selectedFormatLabel = document.querySelector("#selected-format-label");
const selectedFormatSummary = document.querySelector("#selected-format-summary");
const rightsCheckbox = document.querySelector("#rights-checkbox");
const downloadOutputDirInput = document.querySelector("#download-output-dir");
const downloadOutputFormatSelect = document.querySelector("#download-output-format");
const downloadOutputTemplateInput = document.querySelector("#download-output-template");
const downloadDuplicatePolicySelect = document.querySelector("#download-duplicate-policy");
const downloadButton = document.querySelector("#download-button");
const cancelDownloadButton = document.querySelector("#cancel-download-button");
const downloadResult = document.querySelector("#download-result");
const transcriptPanel = document.querySelector("#transcript-panel");
const transcriptFileLabel = document.querySelector("#transcript-file-label");
const whisperModel = document.querySelector("#whisper-model");
const transcriptFormat = document.querySelector("#transcript-format");
const transcribeButton = document.querySelector("#transcribe-button");
const cancelTranscribeButton = document.querySelector("#cancel-transcribe-button");
const transcriptResult = document.querySelector("#transcript-result");
const filesPanel = document.querySelector("#files-panel");
const filesList = document.querySelector("#files-list");
const outputDirLabel = document.querySelector("#output-dir-label");
const copyTranscriptButton = document.querySelector("#copy-transcript-button");
const copySummaryButton = document.querySelector("#copy-summary-button");
const copyOutputButton = document.querySelector("#copy-output-button");
const revealOutputButton = document.querySelector("#reveal-output-button");
const transcriptPreviewCard = document.querySelector("#transcript-preview-card");
const transcriptPreview = document.querySelector("#transcript-preview");
const localFilePanel = document.querySelector("#local-file-panel");
const localMediaType = document.querySelector("#local-media-type");
const localMetadataList = document.querySelector("#local-metadata-list");
const localRightsCheckbox = document.querySelector("#local-rights-checkbox");
const localWhisperModel = document.querySelector("#local-whisper-model");
const localTranscriptFormat = document.querySelector("#local-transcript-format");
const localTranscribeButton = document.querySelector("#local-transcribe-button");
const cancelLocalTranscribeButton = document.querySelector("#cancel-local-transcribe-button");
const localTranscriptResult = document.querySelector("#local-transcript-result");
const batchPanel = document.querySelector("#batch-panel");
const batchCount = document.querySelector("#batch-count");
const batchImportSummary = document.querySelector("#batch-import-summary");
const batchList = document.querySelector("#batch-list");
const batchPresetSelect = document.querySelector("#batch-preset");
const batchConcurrencySelect = document.querySelector("#batch-concurrency");
const batchOutputDirInput = document.querySelector("#batch-output-dir");
const batchStartButton = document.querySelector("#batch-start-button");
const batchRetryButton = document.querySelector("#batch-retry-button");
const batchCancelButton = document.querySelector("#batch-cancel-button");
const batchResult = document.querySelector("#batch-result");
const coursePanel = document.querySelector("#course-panel");
const courseLectureCount = document.querySelector("#course-lecture-count");
const courseSummaryList = document.querySelector("#course-summary-list");
const courseOutputDirInput = document.querySelector("#course-output-dir");
const courseQualitySelect = document.querySelector("#course-quality");
const courseOutputFormatSelect = document.querySelector("#course-output-format");
const courseSubtitlesCheckbox = document.querySelector("#course-subtitles");
const courseDownloadButton = document.querySelector("#course-download-button");
const cancelCourseDownloadButton = document.querySelector("#cancel-course-download-button");
const courseDownloadResult = document.querySelector("#course-download-result");
const refreshOutputsButton = document.querySelector("#refresh-outputs-button");
const recentResultsList = document.querySelector("#recent-results-list");
const recentCard = document.querySelector(".recent-card");

let currentAnalyzeResult = null;
let currentLocalFileResult = null;
let currentCourseResult = null;
let currentBatchItems = [];
let activeBatchId = null;
let selectedFormat = null;
let downloadedFileForTranscript = null;
let latestDownloadResult = null;
let latestTranscriptResult = null;
let activeDownloadJobId = null;
let activeTranscribeJobId = null;
let activeLocalTranscribeJobId = null;
let activeCourseDownloadJobId = null;
let activeFormatCategory = null;
let appConfig = { course_mode_enabled: true, public_product_mode: false, session_token: "" };
let sessionToken = "";
let appConfigPromise = null;
const DEFAULT_DOWNLOAD_OUTPUT_DIR = "~/Downloads/Universal Media Extractor";
const DEFAULT_UDEMY_OUTPUT_DIR = "~/Downloads/Universal Media Extractor/Udemy";
const SECURITY_HEADER_NAME = "X-UME-Session-Token";
const BATCH_PRESET_LABELS = {
  best_video: "Best Video",
  video_1080p: "1080p Video",
  smaller_video: "Smaller Video",
  audio_m4a: "Audio M4A",
  audio_mp3: "Audio MP3",
  subtitles: "Subtitles",
  archive_pack: "Archive Pack",
};

const OUTPUT_FORMAT_CHOICES = {
  audio: [
    ["m4a", "M4A"],
    ["mp3", "MP3"],
    ["wav", "WAV"],
  ],
  video: [
    ["mp4", "MP4"],
    ["mkv", "MKV"],
    ["webm", "WEBM"],
  ],
  combined: [
    ["mp4", "MP4"],
    ["mkv", "MKV"],
    ["webm", "WEBM"],
  ],
  subtitles: [
    ["srt", "SRT"],
    ["vtt", "VTT"],
  ],
};

const groups = {
  audio: document.querySelector("#audio-group"),
  video: document.querySelector("#video-group"),
  combined: document.querySelector("#combined-group"),
  subtitles: document.querySelector("#subtitles-group"),
  captions: document.querySelector("#captions-group"),
};

formatTabs.forEach((tab) => {
  tab.addEventListener("click", () => showFormatCategory(tab.dataset.category));
});

courseAuthSourceSelect?.addEventListener("change", () => {
  const isManual = courseAuthSourceSelect.value === "manual_cookies";
  courseManualCookiesPanel?.classList.toggle("hidden", !isManual);
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const url = urlInput.value.trim();

  if (!url) {
    renderFatalError("URL required", "Paste a public http or https media URL to analyze.");
    urlInput.focus();
    return;
  }

  if (!isValidUrl(url)) {
    renderFatalError("Invalid URL", "Enter a valid http or https URL, for example https://youtu.be/...");
    urlInput.focus();
    return;
  }

  setLoading(true);

  try {
    const response = await apiFetch("/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        source_type: "url",
        url,
        user_confirmed_rights: false,
      }),
    });

    if (!response.ok) {
      const message = await readErrorMessage(response);
      renderFatalError(
        "API error",
        message || `The local API returned HTTP ${response.status}.`
      );
      return;
    }

    const data = await response.json();
    renderAnalyzeResponse(data);
  } catch (error) {
    renderFatalError(
      "API unavailable",
      normalizeNetworkError(error)
    );
  } finally {
    setLoading(false);
  }
});

urlModeButton.addEventListener("click", () => switchInputMode("url"));
localModeButton.addEventListener("click", () => switchInputMode("local"));
batchModeButton.addEventListener("click", () => switchInputMode("batch"));
courseModeButton.addEventListener("click", () => switchInputMode("course"));

localFileInput.addEventListener("change", () => {
  const file = localFileInput.files?.[0];
  localFileName.textContent = file ? `${file.name} · ${readableSize(file.size)}` : "No file selected.";
});

batchForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  await importBatchUrls(batchUrlInput.value, "textarea");
});

batchPasteButton?.addEventListener("click", async () => {
  try {
    const text = await navigator.clipboard.readText();
    batchUrlInput.value = text;
    await importBatchUrls(text, "clipboard");
  } catch (error) {
    renderFatalError("Clipboard unavailable", "Paste URLs into the box manually, then click Import URLs.");
  }
});

batchTextFileInput?.addEventListener("change", async () => {
  const file = batchTextFileInput.files?.[0];
  if (!file) {
    return;
  }
  const text = await file.text();
  batchUrlInput.value = text;
  await importBatchUrls(text, "text_file");
});

playlistAnalyzeButton?.addEventListener("click", async () => {
  const url = firstUrlFromText(batchUrlInput.value);
  if (!url) {
    renderFatalError("Playlist URL required", "Paste a playlist URL first.");
    return;
  }
  setBatchLoading(true, "Analyzing playlist...");
  try {
    const response = await apiFetch("/playlists/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ source_url: url }),
    });
    if (!response.ok) {
      renderFatalError("Playlist analysis failed", await readErrorMessage(response));
      return;
    }
    renderPlaylistAnalyzeResult(await response.json());
  } catch (error) {
    renderFatalError("API unavailable", normalizeNetworkError(error));
  } finally {
    setBatchLoading(false);
  }
});

batchStartButton?.addEventListener("click", startBatchQueue);
batchRetryButton?.addEventListener("click", retryFailedBatchItems);
batchCancelButton?.addEventListener("click", cancelActiveBatch);

localFileForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const file = localFileInput.files?.[0];
  if (!file) {
    renderFatalError("File required", "Choose a local audio or video file to analyze.");
    localFileInput.focus();
    return;
  }

  setLocalLoading(true);
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await apiFetch("/local/analyze", {
      method: "POST",
      body: formData,
    });
    if (!response.ok) {
      renderFatalError("API error", await readErrorMessage(response));
      return;
    }
    renderLocalAnalyzeResult(await response.json());
  } catch (error) {
    renderFatalError("API unavailable", normalizeNetworkError(error));
  } finally {
    setLocalLoading(false);
  }
});

courseForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const courseUrl = normalizeUdemyCourseUrl(courseUrlInput.value.trim());
  const authSource = courseAuthSourceSelect.value || "chrome";
  const cookiesPath = courseCookiesPathInput.value.trim();
  if (!courseUrl) {
    renderFatalError("Course URL required", "Paste a Udemy course URL to analyze.");
    courseUrlInput.focus();
    return;
  }
  if (!isValidUrl(courseUrl) || !new URL(courseUrl).hostname.includes("udemy.")) {
    renderFatalError("Invalid course URL", "Enter a valid Udemy course URL.");
    courseUrlInput.focus();
    return;
  }
  if (authSource === "manual_cookies" && !cookiesPath) {
    renderFatalError("Cookies required", "Choose a readable cookies.txt file, or switch Login source back to Chrome session.");
    courseCookiesPathInput.focus();
    return;
  }

  setCourseLoading(true);
  try {
    const response = await apiFetch("/udemy/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(buildCourseAuthPayload({ course_url: courseUrl })),
    });
    if (!response.ok) {
      renderFatalError("API error", await readErrorMessage(response));
      return;
    }
    renderCourseAnalyzeResponse(await response.json());
  } catch (error) {
    renderFatalError("API unavailable", normalizeNetworkError(error));
  } finally {
    setCourseLoading(false);
  }
});

downloadButton.addEventListener("click", async () => {
  if (!currentAnalyzeResult || !selectedFormat) {
    renderDownloadResult({
      status: "blocked",
      errors: [{ code: "no_format_selected", message: "Select a format first." }],
    });
    return;
  }

  setDownloadLoading(true);

  try {
    const response = await apiFetch("/download", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        source_url: currentAnalyzeResult.source_url,
        format_id: selectedFormat.format_id,
        mode: selectedFormat.type,
        user_confirmed_rights: true,
        output_base_dir: downloadOutputDirInput.value.trim() || DEFAULT_DOWNLOAD_OUTPUT_DIR,
        source_title: currentAnalyzeResult.title || mediaTitle.textContent || null,
        output_format: selectedFormat.preset_output_format || downloadOutputFormatSelect.value || null,
        output_template: downloadOutputTemplateInput?.value?.trim() || "{title}",
        duplicate_policy: downloadDuplicatePolicySelect?.value || "rename",
        channel_name: currentAnalyzeResult.uploader?.channel_name || currentAnalyzeResult.uploader?.name || null,
      }),
    });

    if (!response.ok) {
      renderDownloadResult({
        status: "failed",
        errors: [{ code: "api_error", message: await readErrorMessage(response) }],
      });
      return;
    }

    const job = await response.json();
    activeDownloadJobId = job.job_id;
    renderJobStatus(downloadResult, job, "Download");
    toggleCancelButton(cancelDownloadButton, job);
    const finalJob = await pollJob(job.job_id, (updatedJob) => {
      renderJobStatus(downloadResult, updatedJob, "Download");
      toggleCancelButton(cancelDownloadButton, updatedJob);
    });
    cancelDownloadButton.classList.add("hidden");
    if (finalJob.status === "succeeded" && finalJob.result) {
      renderDownloadResult(finalJob.result);
    } else {
      renderJobStatus(downloadResult, finalJob, "Download");
    }
  } catch (error) {
    renderDownloadResult({
      status: "failed",
      errors: [{ code: "api_unavailable", message: normalizeNetworkError(error) }],
    });
  } finally {
    setDownloadLoading(false);
  }
});

cancelDownloadButton.addEventListener("click", async () => {
  if (activeDownloadJobId) {
    const job = await cancelJob(activeDownloadJobId, downloadResult, "Download");
    if (job) {
      toggleCancelButton(cancelDownloadButton, job);
    }
  }
});

transcribeButton.addEventListener("click", async () => {
  if (!downloadedFileForTranscript) {
    renderTranscriptResult({
      status: "blocked",
      errors: [{ code: "invalid_input_file", message: "Download a media file first." }],
    });
    return;
  }

  setTranscribeLoading(true);

  try {
    const response = await apiFetch("/transcribe", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        input_file_path: downloadedFileForTranscript,
        user_confirmed_rights: true,
        model: whisperModel.value,
        transcript_format: transcriptFormat.value,
        source_kind: selectedFormat?.type === "video" || selectedFormat?.type === "combined" ? "video" : "audio",
      }),
    });

    if (!response.ok) {
      renderTranscriptResult({
        status: "failed",
        errors: [{ code: "api_error", message: await readErrorMessage(response) }],
      });
      return;
    }

    const job = await response.json();
    activeTranscribeJobId = job.job_id;
    renderJobStatus(transcriptResult, job, "Transcription");
    toggleCancelButton(cancelTranscribeButton, job);
    const finalJob = await pollJob(job.job_id, (updatedJob) => {
      renderJobStatus(transcriptResult, updatedJob, "Transcription");
      toggleCancelButton(cancelTranscribeButton, updatedJob);
    });
    cancelTranscribeButton.classList.add("hidden");
    if (finalJob.status === "succeeded" && finalJob.result) {
      renderTranscriptResult(finalJob.result);
    } else {
      renderJobStatus(transcriptResult, finalJob, "Transcription");
    }
  } catch (error) {
    renderTranscriptResult({
      status: "failed",
      errors: [{ code: "api_unavailable", message: normalizeNetworkError(error) }],
    });
  } finally {
    setTranscribeLoading(false);
  }
});

cancelTranscribeButton.addEventListener("click", async () => {
  if (activeTranscribeJobId) {
    const job = await cancelJob(activeTranscribeJobId, transcriptResult, "Transcription");
    if (job) {
      toggleCancelButton(cancelTranscribeButton, job);
    }
  }
});

localTranscribeButton.addEventListener("click", async () => {
  if (!currentLocalFileResult?.saved_path) {
    renderTranscriptResult({
      status: "blocked",
      errors: [{ code: "invalid_input_file", message: "Analyze a local file first." }],
    }, localTranscriptResult);
    return;
  }
  setLocalTranscribeLoading(true);
  downloadedFileForTranscript = currentLocalFileResult.saved_path;

  try {
    const response = await apiFetch("/local/transcribe", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        saved_file_path: currentLocalFileResult.saved_path,
        output_dir: currentLocalFileResult.output_dir,
        user_confirmed_rights: true,
        model: localWhisperModel.value,
        transcript_format: localTranscriptFormat.value,
        source_kind: currentLocalFileResult.media_type || "unknown",
      }),
    });
    if (!response.ok) {
      renderTranscriptResult({
        status: "failed",
        errors: [{ code: "api_error", message: await readErrorMessage(response) }],
      }, localTranscriptResult);
      return;
    }

    const job = await response.json();
    activeLocalTranscribeJobId = job.job_id;
    renderJobStatus(localTranscriptResult, job, "Local transcription");
    toggleCancelButton(cancelLocalTranscribeButton, job);
    const finalJob = await pollJob(job.job_id, (updatedJob) => {
      renderJobStatus(localTranscriptResult, updatedJob, "Local transcription");
      toggleCancelButton(cancelLocalTranscribeButton, updatedJob);
    });
    cancelLocalTranscribeButton.classList.add("hidden");
    if (finalJob.status === "succeeded" && finalJob.result) {
      renderTranscriptResult(finalJob.result, localTranscriptResult);
    } else {
      renderJobStatus(localTranscriptResult, finalJob, "Local transcription");
    }
  } catch (error) {
    renderTranscriptResult({
      status: "failed",
      errors: [{ code: "api_unavailable", message: normalizeNetworkError(error) }],
    }, localTranscriptResult);
  } finally {
    setLocalTranscribeLoading(false);
  }
});

cancelLocalTranscribeButton.addEventListener("click", async () => {
  if (activeLocalTranscribeJobId) {
    const job = await cancelJob(activeLocalTranscribeJobId, localTranscriptResult, "Local transcription");
    if (job) {
      toggleCancelButton(cancelLocalTranscribeButton, job);
    }
  }
});

courseDownloadButton.addEventListener("click", async () => {
  if (!currentCourseResult?.course_url) {
    renderCourseDownloadResult({
      status: "blocked",
      errors: [{ code: "invalid_input_file", message: "Analyze a Udemy course first." }],
    });
    return;
  }

  setCourseDownloadLoading(true);
  try {
    const response = await apiFetch("/udemy/download", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        course_url: currentCourseResult.course_url,
        ...buildCourseAuthPayload({}),
        user_confirmed_rights: true,
        output_base_dir: courseOutputDirInput.value.trim() || DEFAULT_UDEMY_OUTPUT_DIR,
        course_title: currentCourseResult.course_title || null,
        quality: courseQualitySelect.value,
        output_format: courseOutputFormatSelect.value,
        include_subtitles: courseSubtitlesCheckbox.checked,
      }),
    });
    if (!response.ok) {
      renderCourseDownloadResult({
        status: "failed",
        errors: [{ code: "api_error", message: await readErrorMessage(response) }],
      });
      return;
    }

    const job = await response.json();
    activeCourseDownloadJobId = job.job_id;
    renderJobStatus(courseDownloadResult, job, "Course download");
    toggleCancelButton(cancelCourseDownloadButton, job);
    const finalJob = await pollJob(job.job_id, (updatedJob) => {
      renderJobStatus(courseDownloadResult, updatedJob, "Course download");
      toggleCancelButton(cancelCourseDownloadButton, updatedJob);
    });
    cancelCourseDownloadButton.classList.add("hidden");
    if (finalJob.status === "succeeded" && finalJob.result) {
      renderCourseDownloadResult(finalJob.result);
    } else {
      renderJobStatus(courseDownloadResult, finalJob, "Course download");
    }
  } catch (error) {
    renderCourseDownloadResult({
      status: "failed",
      errors: [{ code: "api_unavailable", message: normalizeNetworkError(error) }],
    });
  } finally {
    setCourseDownloadLoading(false);
  }
});

cancelCourseDownloadButton.addEventListener("click", async () => {
  if (activeCourseDownloadJobId) {
    const job = await cancelJob(activeCourseDownloadJobId, courseDownloadResult, "Course download");
    if (job) {
      toggleCancelButton(cancelCourseDownloadButton, job);
    }
  }
});

refreshOutputsButton?.addEventListener("click", () => {
  loadRecentOutputs();
});

copyTranscriptButton.addEventListener("click", () => {
  copyText(latestTranscriptResult?.transcript_text || "", "Transcript copied.");
});

copySummaryButton.addEventListener("click", () => {
  copyText(latestTranscriptResult?.summary_prompt_text || "", "Summary prompt copied.");
});

copyOutputButton.addEventListener("click", () => {
  copyText(latestTranscriptResult?.output_dir || latestDownloadResult?.output_dir || "", "Output path copied.");
});

revealOutputButton?.addEventListener("click", () => {
  revealOutputPath(latestTranscriptResult?.output_dir || latestDownloadResult?.output_dir || "");
});

appConfigPromise = initializeAppConfig();

if (recentCard && !recentCard.classList.contains("hidden")) {
  loadRecentOutputs();
}

async function initializeAppConfig() {
  try {
    const response = await fetch(`${API_BASE_URL}/config`, { cache: "no-store" });
    if (response.ok) {
      appConfig = await response.json();
      sessionToken = appConfig.session_token || "";
    }
  } catch {
    appConfig = { course_mode_enabled: true, public_product_mode: false, session_token: "" };
    sessionToken = "";
  }
  applyFeatureConfig();
}

async function ensureAppConfigLoaded() {
  if (!sessionToken && appConfigPromise) {
    await appConfigPromise;
  }
}

async function apiFetch(path, options = {}) {
  await ensureAppConfigLoaded();
  const headers = new Headers(options.headers || {});
  if (sessionToken) {
    headers.set(SECURITY_HEADER_NAME, sessionToken);
  }
  return fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers,
  });
}

function applyFeatureConfig() {
  const courseEnabled = appConfig.course_mode_enabled !== false;
  courseModeButton?.classList.toggle("hidden", !courseEnabled);
  courseModeButton?.setAttribute("aria-hidden", String(!courseEnabled));
  if (!courseEnabled) {
    courseForm?.classList.add("hidden");
    coursePanel?.classList.add("hidden");
    if (courseModeButton?.classList.contains("is-active")) {
      switchInputMode("url");
    }
  }
}

function isValidUrl(value) {
  try {
    const url = new URL(value);
    return url.protocol === "http:" || url.protocol === "https:";
  } catch {
    return false;
  }
}

function normalizeUdemyCourseUrl(value) {
  if (!value || !isValidUrl(value)) {
    return value;
  }
  const url = new URL(value);
  url.hash = "";
  return url.toString();
}

function buildCourseAuthPayload(base = {}) {
  const authSource = courseAuthSourceSelect.value || "chrome";
  const payload = {
    ...base,
    auth_source: authSource,
  };
  if (authSource === "manual_cookies") {
    payload.cookies_path = courseCookiesPathInput.value.trim();
  }
  return payload;
}

function switchInputMode(mode) {
  const isLocal = mode === "local";
  const isBatch = mode === "batch";
  const isCourse = mode === "course";
  urlModeButton.classList.toggle("is-active", !isLocal && !isBatch && !isCourse);
  localModeButton.classList.toggle("is-active", isLocal);
  batchModeButton.classList.toggle("is-active", isBatch);
  courseModeButton.classList.toggle("is-active", isCourse);
  urlModeButton.setAttribute("aria-pressed", String(!isLocal && !isBatch && !isCourse));
  localModeButton.setAttribute("aria-pressed", String(isLocal));
  batchModeButton.setAttribute("aria-pressed", String(isBatch));
  courseModeButton.setAttribute("aria-pressed", String(isCourse));
  form.classList.toggle("hidden", isLocal || isBatch || isCourse);
  localFileForm.classList.toggle("hidden", !isLocal);
  batchForm.classList.toggle("hidden", !isBatch);
  courseForm.classList.toggle("hidden", !isCourse);
  resetDownloadSelection();
  resetLocalState();
  resetBatchState(!isBatch);
  resetCourseState();
  emptyState.classList.remove("hidden");
  resultContent.classList.add("hidden");
  if (isLocal) {
    apiStatus.textContent = "Local file mode. Files stay on this machine.";
  } else if (isBatch) {
    apiStatus.textContent = "Batch mode. Import URLs, choose a preset, then start the queue.";
  } else if (isCourse) {
    apiStatus.textContent = "Course mode. Open Udemy in Chrome and sign in first.";
  } else {
    apiStatus.textContent = "Using local API at http://127.0.0.1:8000";
  }
}

async function readErrorMessage(response) {
  try {
    const data = await response.json();
    if (typeof data.detail === "string") {
      return data.detail;
    }
    if (Array.isArray(data.detail)) {
      return data.detail
        .map((item) => item.msg || item.message || "Invalid request.")
        .join(" ");
    }
    return "The local API rejected the request.";
  } catch {
    return response.statusText;
  }
}

function normalizeNetworkError(error) {
  if (error instanceof TypeError) {
    return "The local API is not reachable. Start the backend on 127.0.0.1:8000 and try again.";
  }
  if (error instanceof Error && error.message) {
    return error.message;
  }
  return "The local API did not respond.";
}

function setLoading(isLoading) {
  analyzeButton.disabled = isLoading;
  analyzeButton.textContent = isLoading ? "Analyzing..." : "Analyze";
  form.setAttribute("aria-busy", String(isLoading));
  emptyState.classList.toggle("hidden", true);
  loadingState.classList.toggle("hidden", !isLoading);
  if (isLoading) {
    resultContent.classList.add("hidden");
    resetDownloadSelection();
    updateFlowStep("analyze");
  }
}

function setLocalLoading(isLoading) {
  localAnalyzeButton.disabled = isLoading;
  localAnalyzeButton.textContent = isLoading ? "Analyzing..." : "Analyze local file";
  localFileForm.setAttribute("aria-busy", String(isLoading));
  emptyState.classList.toggle("hidden", true);
  loadingState.classList.toggle("hidden", !isLoading);
  if (isLoading) {
    resultContent.classList.add("hidden");
    resetDownloadSelection();
    resetLocalState();
    updateFlowStep("analyze");
  }
}

function setCourseLoading(isLoading) {
  courseAnalyzeButton.disabled = isLoading;
  courseAnalyzeButton.textContent = isLoading ? "Analyzing..." : "Analyze course";
  courseForm.setAttribute("aria-busy", String(isLoading));
  emptyState.classList.toggle("hidden", true);
  loadingState.classList.toggle("hidden", !isLoading);
  if (isLoading) {
    resultContent.classList.add("hidden");
    resetDownloadSelection();
    resetLocalState();
    resetCourseState();
    updateFlowStep("analyze");
  }
}

async function importBatchUrls(text, source) {
  if (!text.trim()) {
    renderFatalError("URLs required", "Paste one or more URLs first.");
    batchUrlInput.focus();
    return;
  }
  setBatchLoading(true, "Importing URLs...");
  try {
    const response = await apiFetch("/batch/import", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text, source }),
    });
    if (!response.ok) {
      renderFatalError("Import failed", await readErrorMessage(response));
      return;
    }
    renderBatchImportResult(await response.json());
  } catch (error) {
    renderFatalError("API unavailable", normalizeNetworkError(error));
  } finally {
    setBatchLoading(false);
  }
}

function renderBatchImportResult(result) {
  currentBatchItems = (result.urls || []).map((url, index) => ({
    source_url: url,
    source_title: "",
    playlist_index: index + 1,
    selected: true,
  }));
  showBatchPanel();
  batchImportSummary.textContent = [
    `${currentBatchItems.length} URL${currentBatchItems.length === 1 ? "" : "s"} imported`,
    result.duplicate_count ? `${result.duplicate_count} duplicate${result.duplicate_count === 1 ? "" : "s"} skipped` : "",
    (result.invalid_lines || []).length ? `${result.invalid_lines.length} invalid line${result.invalid_lines.length === 1 ? "" : "s"}` : "",
  ].filter(Boolean).join(" · ");
  renderBatchList();
}

function renderPlaylistAnalyzeResult(result) {
  if ((result.errors || []).length > 0) {
    showBatchPanel();
    renderErrors(result.errors || [], null);
    return;
  }
  currentBatchItems = (result.items || [])
    .filter((item) => item.url)
    .map((item) => ({
      source_url: item.url,
      source_title: item.title || "",
      playlist_index: item.playlist_index,
      selected: item.selected !== false,
    }));
  showBatchPanel();
  batchImportSummary.textContent = `${currentBatchItems.length} playlist item${currentBatchItems.length === 1 ? "" : "s"} found${result.title ? ` · ${result.title}` : ""}`;
  renderBatchList();
}

function showBatchPanel() {
  loadingState.classList.add("hidden");
  emptyState.classList.add("hidden");
  resultContent.classList.remove("hidden");
  renderSourceSummary({ title: "Batch downloads", source_type: "url", extractor: "local" });
  formatPicker.classList.add("hidden");
  downloadPanel.classList.add("hidden");
  transcriptPanel.classList.add("hidden");
  localFilePanel.classList.add("hidden");
  coursePanel.classList.add("hidden");
  warningsPanel.classList.add("hidden");
  errorsPanel.classList.add("hidden");
  batchPanel.classList.remove("hidden");
  updateBatchControls();
}

function renderBatchList(batch) {
  const items = batch?.items || currentBatchItems;
  batchList.innerHTML = "";
  batchCount.textContent = `${items.length} item${items.length === 1 ? "" : "s"}`;
  if (!items.length) {
    batchList.appendChild(emptyLine("No URLs imported."));
    updateBatchControls();
    return;
  }
  items.forEach((item, index) => {
    const row = document.createElement("label");
    row.className = "batch-row";
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = item.selected !== false;
    checkbox.disabled = Boolean(batch);
    checkbox.addEventListener("change", () => {
      currentBatchItems[index].selected = checkbox.checked;
      updateBatchControls();
    });
    const main = document.createElement("div");
    main.className = "batch-main";
    const title = document.createElement("strong");
    title.textContent = item.source_title || item.title || compactUrl(item.source_url);
    const meta = document.createElement("span");
    meta.textContent = batch ? humanBatchItemMeta(item) : compactUrl(item.source_url);
    meta.title = item.source_url || "";
    main.append(title, meta);
    row.append(checkbox, main);
    batchList.appendChild(row);
  });
}

async function startBatchQueue() {
  const selectedItems = currentBatchItems.filter((item) => item.selected !== false);
  if (!selectedItems.length) {
    renderBatchStatus({ status: "failed", errors: [{ code: "invalid_input_file", message: "Select at least one URL." }] });
    return;
  }
  setBatchRunning(true);
  try {
    const response = await apiFetch("/batch", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        items: selectedItems,
        preset: batchPresetSelect.value,
        user_confirmed_rights: true,
        output_base_dir: batchOutputDirInput.value.trim() || DEFAULT_DOWNLOAD_OUTPUT_DIR,
        output_template: "{title}",
        duplicate_policy: "rename",
        concurrency: Number(batchConcurrencySelect.value || 1),
      }),
    });
    if (!response.ok) {
      renderBatchStatus({ status: "failed", errors: [{ code: "unknown_error", message: await readErrorMessage(response) }] });
      return;
    }
    const batch = await response.json();
    activeBatchId = batch.batch_id;
    renderBatchStatus(batch);
    const finalBatch = await pollBatch(batch.batch_id, renderBatchStatus);
    renderBatchStatus(finalBatch);
  } catch (error) {
    renderBatchStatus({ status: "failed", errors: [{ code: "network_error", message: normalizeNetworkError(error) }] });
  } finally {
    setBatchRunning(false);
  }
}

async function pollBatch(batchId, onUpdate) {
  while (true) {
    await delay(1000);
    const response = await apiFetch(`/batch/${encodeURIComponent(batchId)}`);
    if (!response.ok) {
      throw new Error(await readErrorMessage(response));
    }
    const batch = await response.json();
    onUpdate(batch);
    if (["succeeded", "failed", "cancelled"].includes(batch.status)) {
      return batch;
    }
  }
}

async function retryFailedBatchItems() {
  if (!activeBatchId) {
    return;
  }
  setBatchRunning(true);
  try {
    const response = await apiFetch(`/batch/${encodeURIComponent(activeBatchId)}/retry-failed`, { method: "POST" });
    if (!response.ok) {
      renderBatchStatus({ status: "failed", errors: [{ code: "unknown_error", message: await readErrorMessage(response) }] });
      return;
    }
    const batch = await response.json();
    renderBatchStatus(batch);
    renderBatchStatus(await pollBatch(batch.batch_id, renderBatchStatus));
  } catch (error) {
    renderBatchStatus({ status: "failed", errors: [{ code: "network_error", message: normalizeNetworkError(error) }] });
  } finally {
    setBatchRunning(false);
  }
}

async function cancelActiveBatch() {
  if (!activeBatchId) {
    return;
  }
  const response = await apiFetch(`/batch/${encodeURIComponent(activeBatchId)}/cancel`, { method: "POST" });
  if (response.ok) {
    renderBatchStatus(await response.json());
  }
}


function renderBatchStatus(batch) {
  batchPanel.classList.remove("hidden");
  batchResult.classList.remove("hidden");
  batchResult.innerHTML = "";
  const status = batch.status || "unknown";
  batchResult.appendChild(statusHeading(`Queue ${humanStatusLabel(status).toLowerCase()}`, status));

  const summary = document.createElement("p");
  summary.className = "muted";
  summary.textContent = [
    `${batch.succeeded_count || 0} saved`,
    batch.failed_count ? `${batch.failed_count} failed` : "",
    batch.running_count ? `${batch.running_count} running` : "",
    batch.queued_count ? `${batch.queued_count} waiting` : "",
    BATCH_PRESET_LABELS[batch.preset] || batch.preset,
  ].filter(Boolean).join(" · ");
  batchResult.appendChild(summary);

  renderBatchList(batch);
  appendNoticeLines(batchResult, [...(batch.errors || []), ...(batch.warnings || [])]);
  batchRetryButton.classList.toggle("hidden", !(batch.failed_count > 0));
  batchCancelButton.classList.toggle("hidden", !["queued", "running"].includes(batch.status));
  if (["succeeded", "failed", "cancelled"].includes(batch.status)) {
    loadRecentOutputs();
  }
}

function setBatchLoading(isLoading, label = "Working...") {
  if (isLoading) {
    emptyState.classList.add("hidden");
    resultContent.classList.add("hidden");
    loadingState.classList.remove("hidden");
    loadingState.querySelector("h2").textContent = label;
  } else {
    loadingState.querySelector("h2").textContent = "Analyzing...";
  }
}

function setBatchRunning(isRunning) {
  batchStartButton.disabled = isRunning || currentBatchItems.filter((item) => item.selected !== false).length === 0;
  batchPresetSelect.disabled = isRunning;
  batchConcurrencySelect.disabled = isRunning;
  batchOutputDirInput.disabled = isRunning;
  batchStartButton.textContent = isRunning ? "Running queue..." : "Start queue";
}

function updateBatchControls() {
  batchStartButton.disabled = currentBatchItems.filter((item) => item.selected !== false).length === 0;
}

function resetBatchState(hidePanel = true) {
  activeBatchId = null;
  currentBatchItems = [];
  batchUrlInput.value = "";
  batchOutputDirInput.value = DEFAULT_DOWNLOAD_OUTPUT_DIR;
  batchPresetSelect.value = "best_video";
  batchConcurrencySelect.value = "1";
  batchCount.textContent = "No URLs";
  batchImportSummary.textContent = "";
  batchList.innerHTML = "";
  batchResult.classList.add("hidden");
  batchResult.innerHTML = "";
  batchRetryButton.classList.add("hidden");
  batchCancelButton.classList.add("hidden");
  batchStartButton.textContent = "Start queue";
  batchStartButton.disabled = true;
  batchPresetSelect.disabled = false;
  batchConcurrencySelect.disabled = false;
  batchOutputDirInput.disabled = false;
  if (hidePanel) {
    batchPanel.classList.add("hidden");
  }
}

function firstUrlFromText(text) {
  const match = String(text || "").match(/https?:\/\/[^\s<>"']+/);
  return match ? match[0].replace(/[.,);\]]+$/, "") : "";
}

function compactUrl(url) {
  try {
    const parsed = new URL(url);
    return `${parsed.hostname}${parsed.pathname}`.slice(0, 90);
  } catch {
    return String(url || "").slice(0, 90);
  }
}

function renderLocalAnalyzeResult(result) {
  currentLocalFileResult = result;
  loadingState.classList.add("hidden");
  emptyState.classList.add("hidden");
  resultContent.classList.remove("hidden");
  apiStatus.textContent = result.errors?.length
    ? "Local file needs attention."
    : "Local file analyzed.";

  renderSourceSummary({
    title: result.filename,
    duration_seconds: result.duration_seconds,
    extractor: "ffprobe",
    uploader: null,
    webpage_url: "",
    thumbnail_url: "",
  });
  formatPicker.classList.add("hidden");
  renderWarnings(result.warnings || []);
  renderErrors(result.errors || [], null);
  downloadPanel.classList.add("hidden");
  transcriptPanel.classList.add("hidden");
  coursePanel.classList.add("hidden");
  batchPanel.classList.add("hidden");
  localFilePanel.classList.toggle("hidden", (result.errors || []).length > 0);
  renderLocalMetadata(result);
  updateLocalTranscribeButtonState();
  updateFlowStep((result.errors || []).length > 0 ? "analyze" : "transcribe");
}

function renderCourseAnalyzeResponse(data) {
  const result = data.result || data;
  currentCourseResult = result;
  loadingState.classList.add("hidden");
  emptyState.classList.add("hidden");
  resultContent.classList.remove("hidden");
  apiStatus.textContent = result.errors?.length
    ? "Course analysis needs attention."
    : "Course analyzed.";

  renderSourceSummary({
    title: result.course_title || "Udemy course",
    duration_seconds: null,
    extractor: result.extractor || "udemy",
    uploader: null,
    webpage_url: result.course_url,
    thumbnail_url: "",
  });
  formatPicker.classList.add("hidden");
  downloadPanel.classList.add("hidden");
  transcriptPanel.classList.add("hidden");
  localFilePanel.classList.add("hidden");
  batchPanel.classList.add("hidden");
  renderWarnings(result.warnings || []);
  renderErrors(result.errors || [], null);
  renderCourseSummary(result);
  coursePanel.classList.toggle("hidden", (result.errors || []).length > 0);
  courseDownloadButton.disabled = (result.errors || []).length > 0;
  updateFlowStep((result.errors || []).length > 0 ? "analyze" : "download");
}

function renderCourseSummary(result) {
  const lectureCount = result.lecture_count || 0;
  courseLectureCount.textContent = `${lectureCount} lecture${lectureCount === 1 ? "" : "s"}`;
  courseSummaryList.innerHTML = "";
  [
    ["Course", result.course_title],
    ["Lectures", lectureCount ? String(lectureCount) : "Unknown"],
    ["Login", courseAuthSourceSelect.value === "manual_cookies" ? "Manual cookies.txt" : "Chrome session"],
  ].forEach(([label, value]) => {
    if (!value) {
      return;
    }
    const row = document.createElement("div");
    row.className = "file-row";
    const name = document.createElement("strong");
    name.textContent = label;
    const text = document.createElement("span");
    text.textContent = value;
    row.append(name, text);
    courseSummaryList.appendChild(row);
  });

  const sections = result.sections || [];
  sections.slice(0, 6).forEach((section) => {
    const row = document.createElement("div");
    row.className = "file-row";
    const name = document.createElement("strong");
    name.textContent = section.title || "Section";
    const text = document.createElement("span");
    text.textContent = `${(section.lectures || []).length} lecture${(section.lectures || []).length === 1 ? "" : "s"}`;
    row.append(name, text);
    courseSummaryList.appendChild(row);
  });
}

function renderLocalMetadata(result) {
  localMediaType.textContent = result.media_type || "unknown";
  localMetadataList.innerHTML = "";
  [
    ["Saved file", result.saved_path],
    ["Output directory", result.output_dir],
    ["Media type", result.media_type],
    ["Duration", formatDuration(result.duration_seconds)],
    ["Size", readableSize(result.size_bytes)],
    ["Format", result.format_long_name || result.format_name],
  ].forEach(([label, value]) => {
    if (!value) {
      return;
    }
    const row = document.createElement("div");
    row.className = "file-row";
    const name = document.createElement("strong");
    name.textContent = label;
    const text = document.createElement("span");
    text.textContent = value;
    row.append(name, text);
    localMetadataList.appendChild(row);
  });

  const streams = result.streams || [];
  streams.forEach((stream) => {
    const row = document.createElement("div");
    row.className = "file-row";
    const name = document.createElement("strong");
    name.textContent = `Stream ${stream.index ?? ""}`;
    const text = document.createElement("span");
    text.textContent = [
      stream.codec_type,
      stream.codec_name,
      stream.width && stream.height ? `${stream.width}x${stream.height}` : "",
      stream.sample_rate ? `${stream.sample_rate} Hz` : "",
      stream.channels ? `${stream.channels} ch` : "",
    ].filter(Boolean).join(" · ");
    row.append(name, text);
    localMetadataList.appendChild(row);
  });
}

function renderAnalyzeResponse(data) {
  const result = data.result;
  const resultErrors = result.errors || [];
  resetDownloadSelection();
  currentAnalyzeResult = result;
  loadingState.classList.add("hidden");
  emptyState.classList.add("hidden");
  resultContent.classList.remove("hidden");
  apiStatus.textContent = resultErrors.length > 0 ? "Analysis needs attention." : "Analysis complete.";

  renderSourceSummary(result);
  renderFormatPicker(result);
  renderWarnings(result.warnings || []);
  renderErrors(resultErrors, data.job.error);
  coursePanel.classList.add("hidden");
  batchPanel.classList.add("hidden");
  localFilePanel.classList.add("hidden");
  downloadPanel.classList.toggle("hidden", resultErrors.length > 0);
  updateFlowStep(resultErrors.length > 0 ? "analyze" : "select");
}

function renderSourceSummary(result) {
  const hasThumbnail = Boolean(result.thumbnail_url);
  thumbnailWrap.classList.toggle("is-empty", !hasThumbnail);
  thumbnail.src = hasThumbnail ? result.thumbnail_url : "";
  thumbnail.alt = hasThumbnail && result.title ? `${result.title} thumbnail` : "";
  extractorPill.textContent = result.extractor || result.source_type || "source";
  duration.textContent = result.duration_label || formatDuration(result.duration_seconds) || "duration unknown";
  mediaTitle.textContent = result.title || "Untitled source";

  const uploaderInfo = result.uploader;
  const uploaderName = uploaderInfo?.name || uploaderInfo?.channel_name;
  uploader.textContent = uploaderName ? `Uploader: ${uploaderName}` : "Uploader unavailable";

  if (result.webpage_url) {
    webpageLink.href = result.webpage_url;
    webpageLink.classList.remove("hidden");
  } else {
    webpageLink.classList.add("hidden");
  }
}

function renderFormatPicker(data) {
  const presetData = buildPresetPickerData(data);
  formatPicker.classList.remove("hidden");
  renderPresetPicker(presetData.presets || []);
  renderAdvancedFormatDetails(presetData.source || { audio: [], video: [], subtitles: [] });
}

function renderPresetPicker(presets) {
  presetList.innerHTML = "";
  const list = Array.isArray(presets) ? presets : [];
  formatPickerEmpty.classList.toggle("hidden", list.length > 0);
  if (list.length === 0) {
    formatPickerEmpty.textContent = "No presets available.";
    return;
  }
  list.forEach((preset) => presetList.appendChild(presetRow(preset)));
}

function presetRow(preset) {
  const row = document.createElement("button");
  row.type = "button";
  row.className = "preset-row format-row";
  row.dataset.selectionId = selectionKeyForOption(preset);
  row.disabled = !preset.preset_available;
  if (preset.preset_available) {
    row.addEventListener("click", () => selectFormat(preset));
  }

  const main = document.createElement("div");
  main.className = "preset-main";

  const label = document.createElement("strong");
  label.textContent = preset.preset_label || simpleFormatLabel(preset, categoryForOption(preset));
  main.appendChild(label);

  const meta = document.createElement("span");
  meta.className = "preset-meta";
  meta.textContent = preset.preset_detail || preset.preset_description || "";
  main.appendChild(meta);

  const badgeText = preset.preset_available ? presetBadge(preset) : "Unavailable";
  if (badgeText) {
    const badge = document.createElement("span");
    badge.className = preset.preset_available ? "badge recommended" : "badge muted-badge";
    badge.textContent = badgeText;
    main.appendChild(badge);
  }

  const description = document.createElement("div");
  description.className = "simple-format-helper";
  description.textContent = preset.preset_description || "";

  row.append(main, description);
  return row;
}

function presetBadge(preset) {
  if (preset.preset_id === "best_video" || preset.preset_id === "audio_m4a") {
    return "Recommended";
  }
  if (preset.preset_output_format) {
    return String(preset.preset_output_format).toUpperCase();
  }
  return "";
}

function renderAdvancedFormatDetails(data) {
  renderFormatGroup(groups.audio, "Audio streams", data.audio || [], "audio", "No audio streams.");
  renderFormatGroup(groups.video, "Video streams", data.video || [], "video", "No video streams at 1080p or higher.");
  renderFormatGroup(groups.subtitles, "Subtitle tracks", data.subtitles || [], "subtitles", "No subtitle tracks.");
  groups.audio?.classList.remove("hidden");
  groups.video?.classList.remove("hidden");
  groups.subtitles?.classList.remove("hidden");
  groups.combined?.classList.add("hidden");
  groups.captions?.classList.add("hidden");
  advancedFormatDetails?.classList.remove("hidden");
}

function defaultFormatCategory(data) {
  if ((data.audio || []).length > 0) {
    return "audio";
  }
  if ((data.video || []).length > 0) {
    return "video";
  }
  return "subtitles";
}

function buildPresetPickerData(result) {
  return window.UIOptionNormalizer.buildPresetPickerData(result);
}

function showFormatCategory(category) {
  activeFormatCategory = category;
  Object.entries(groups).forEach(([key, group]) => {
    if (!group) {
      return;
    }
    group.classList.toggle("hidden", key !== category);
  });
  formatPickerEmpty.classList.add("hidden");
  updateFormatTabs();
}

function updateFormatTabs() {
  formatTabs.forEach((tab) => {
    const isActive = tab.dataset.category === activeFormatCategory;
    tab.classList.toggle("is-active", isActive);
    tab.setAttribute("aria-pressed", String(isActive));
  });
}

function renderFormatGroup(container, title, options, category, emptyText) {
  const list = Array.isArray(options) ? [...options] : [];
  list.sort((a, b) => Number(b.is_default_recommended) - Number(a.is_default_recommended));

  container.innerHTML = "";
  container.classList.toggle("is-primary", list.length > 0);
  container.appendChild(groupHeader(title, list.length));

  if (list.length === 0) {
    container.appendChild(emptyLine(emptyText));
    return;
  }

  if (category === "subtitles") {
    renderSubtitleSelect(container, list);
    return;
  }

  const listNode = document.createElement("div");
  listNode.className = "format-list";
  list.forEach((option) => listNode.appendChild(formatRow(option, category)));
  container.appendChild(listNode);
}

function renderSubtitleSelect(container, options) {
  const field = document.createElement("label");
  field.className = "subtitle-select-field";
  field.htmlFor = "subtitle-option-select";

  const label = document.createElement("span");
  label.textContent = "Subtitle language";

  const select = document.createElement("select");
  select.id = "subtitle-option-select";
  select.className = "subtitle-select";

  const placeholder = document.createElement("option");
  placeholder.value = "";
  placeholder.textContent = "Choose subtitles...";
  select.appendChild(placeholder);

  options.forEach((option) => {
    const item = document.createElement("option");
    item.value = selectionKeyForOption(option);
    item.textContent = simpleFormatLabel(option, "subtitles");
    select.appendChild(item);
  });

  if (selectedFormat && selectedFormat.type === "subtitles") {
    select.value = selectionKeyForOption(selectedFormat);
  }

  select.addEventListener("change", () => {
    const option = options.find((item) => selectionKeyForOption(item) === select.value);
    if (option) {
      selectFormat(option);
    }
  });

  field.append(label, select);
  container.appendChild(field);

  const helper = document.createElement("p");
  helper.className = "simple-format-helper";
  helper.textContent = `${options.length} subtitle option${options.length === 1 ? "" : "s"} available.`;
  container.appendChild(helper);
}

function groupHeader(title, count) {
  const header = document.createElement("div");
  header.className = "group-header";

  const heading = document.createElement("h3");
  heading.textContent = title;

  const countNode = document.createElement("span");
  countNode.className = "count";
  countNode.textContent = `${count} found`;

  header.append(heading, countNode);
  return header;
}

function formatRow(option, category) {
  const row = document.createElement("button");
  row.type = "button";
  row.className = `format-row simple-format-row ${category}-option`;
  row.dataset.selectionId = selectionKeyForOption(option);
  row.addEventListener("click", () => selectFormat(option));

  const main = document.createElement("div");
  main.className = "format-main";
  main.appendChild(textBlock(simpleFormatLabel(option, category)));

  if (option.is_default_recommended) {
    const badge = document.createElement("span");
    badge.className = "badge recommended";
    badge.textContent = "Recommended";
    main.appendChild(badge);
  }

  row.appendChild(main);
  const helper = simpleFormatHelper(option, category);
  if (helper) {
    const note = document.createElement("div");
    note.className = "simple-format-helper";
    note.textContent = helper;
    row.appendChild(note);
  }

  return row;
}

function selectFormat(option) {
  selectedFormat = option;
  latestDownloadResult = null;
  latestTranscriptResult = null;
  downloadedFileForTranscript = null;
  document.querySelectorAll(".format-row.is-selected").forEach((row) => {
    row.classList.remove("is-selected");
  });
  document.querySelectorAll(`.format-row[data-selection-id="${cssEscape(selectionKeyForOption(option))}"]`).forEach((row) => {
    row.classList.add("is-selected");
  });
  selectedFormatLabel.textContent = selectedPresetLabel(option);
  selectedFormatSummary.textContent = formatSelectionSummary(option);
  renderOutputFormatChoices(option);
  downloadResult.classList.add("hidden");
  transcriptPanel.classList.add("hidden");
  filesPanel.classList.add("hidden");
  updateDownloadButtonState();
  updateFlowStep("download");
}

function resetDownloadSelection() {
  currentAnalyzeResult = null;
  selectedFormat = null;
  downloadedFileForTranscript = null;
  latestDownloadResult = null;
  latestTranscriptResult = null;
  rightsCheckbox.checked = true;
  downloadOutputDirInput.value = DEFAULT_DOWNLOAD_OUTPUT_DIR;
  downloadOutputFormatSelect.innerHTML = "";
  if (downloadOutputTemplateInput) {
    downloadOutputTemplateInput.value = "{title}";
  }
  if (downloadDuplicatePolicySelect) {
    downloadDuplicatePolicySelect.value = "rename";
  }
  selectedFormatLabel.textContent = "No format selected";
  selectedFormatSummary.textContent = "Choose a preset to continue.";
  downloadButton.disabled = true;
  downloadButton.textContent = "Download selected";
  cancelDownloadButton.classList.add("hidden");
  downloadPanel.classList.add("hidden");
  downloadResult.classList.add("hidden");
  downloadResult.innerHTML = "";
  transcriptPanel.classList.add("hidden");
  transcriptFileLabel.textContent = "No file selected";
  transcriptResult.classList.add("hidden");
  transcriptResult.innerHTML = "";
  whisperModel.value = "tiny";
  transcriptFormat.value = "txt";
  transcribeButton.textContent = "Transcribe";
  cancelTranscribeButton.classList.add("hidden");
  filesPanel.classList.add("hidden");
  filesList.innerHTML = "";
  outputDirLabel.textContent = "No output yet";
  transcriptPreview.textContent = "";
  transcriptPreviewCard.classList.add("hidden");
  copyTranscriptButton.disabled = true;
  copySummaryButton.disabled = true;
  copySummaryButton.classList.add("hidden");
  copyOutputButton.disabled = true;
  if (revealOutputButton) {
    revealOutputButton.disabled = true;
  }
  activeDownloadJobId = null;
  activeTranscribeJobId = null;
  activeFormatCategory = null;
  formatPicker.classList.add("hidden");
  formatPickerEmpty.classList.remove("hidden");
  presetList.innerHTML = "";
  advancedFormatDetails?.classList.add("hidden");
  Object.values(groups).forEach((group) => group?.classList.add("hidden"));
  updateFormatTabs();
}

function renderOutputFormatChoices(option) {
  const presetFormat = option.preset_output_format;
  const choices = presetFormat
    ? [[presetFormat, String(presetFormat).toUpperCase()]]
    : OUTPUT_FORMAT_CHOICES[option.type] || OUTPUT_FORMAT_CHOICES[categoryForOption(option)] || [];
  downloadOutputFormatSelect.innerHTML = "";
  choices.forEach(([value, label], index) => {
    const item = document.createElement("option");
    item.value = value;
    item.textContent = label;
    if (index === 0) {
      item.selected = true;
    }
    downloadOutputFormatSelect.appendChild(item);
  });
}

function resetLocalState() {
  currentLocalFileResult = null;
  activeLocalTranscribeJobId = null;
  localRightsCheckbox.checked = true;
  localWhisperModel.value = "tiny";
  localTranscriptFormat.value = "txt";
  localTranscribeButton.disabled = true;
  localTranscribeButton.textContent = "Transcribe local file";
  cancelLocalTranscribeButton.classList.add("hidden");
  localFilePanel.classList.add("hidden");
  localTranscriptResult.classList.add("hidden");
  localTranscriptResult.innerHTML = "";
  localMetadataList.innerHTML = "";
  localMediaType.textContent = "unknown";
}

function resetCourseState() {
  currentCourseResult = null;
  activeCourseDownloadJobId = null;
  courseOutputDirInput.value = DEFAULT_UDEMY_OUTPUT_DIR;
  courseAuthSourceSelect.value = "chrome";
  courseManualCookiesPanel.classList.add("hidden");
  courseCookiesPathInput.value = "";
  courseQualitySelect.value = "best";
  courseOutputFormatSelect.value = "mp4";
  courseSubtitlesCheckbox.checked = true;
  courseLectureCount.textContent = "No lectures loaded";
  courseSummaryList.innerHTML = "";
  courseDownloadButton.disabled = true;
  courseDownloadButton.textContent = "Download course";
  cancelCourseDownloadButton.classList.add("hidden");
  courseDownloadResult.classList.add("hidden");
  courseDownloadResult.innerHTML = "";
  coursePanel.classList.add("hidden");
}

function updateDownloadButtonState() {
  downloadButton.disabled = !selectedFormat;
}

function setDownloadLoading(isLoading) {
  downloadButton.disabled = isLoading || !selectedFormat;
  downloadButton.textContent = isLoading ? "Downloading..." : "Download selected";
}

function setCourseDownloadLoading(isLoading) {
  courseDownloadButton.disabled = isLoading || !currentCourseResult?.course_url;
  courseQualitySelect.disabled = isLoading;
  courseOutputFormatSelect.disabled = isLoading;
  courseSubtitlesCheckbox.disabled = isLoading;
  courseDownloadButton.textContent = isLoading ? "Downloading..." : "Download course";
  if (isLoading) {
    updateFlowStep("download");
  }
}

function canTranscribeSelectedFormat() {
  return ["audio", "video", "combined"].includes(selectedFormat?.type);
}

function nonTranscribableDownloadMessage() {
  if (selectedFormat?.type === "subtitles") {
    return "Subtitles were downloaded. Transcription is only available for audio or video with audio.";
  }
  return "This output cannot be transcribed.";
}

function statusClass(status) {
  if (status === "succeeded") {
    return "success";
  }
  if (["failed", "cancelled", "blocked"].includes(status)) {
    return "failed";
  }
  return "running";
}

function humanStatusLabel(status) {
  const labels = {
    queued: "Queued",
    running: "Working",
    succeeded: "Saved",
    failed: "Needs attention",
    cancelled: "Cancelled",
    blocked: "Blocked",
  };
  return labels[status] || "Working";
}

function humanStepLabel(step) {
  const value = String(step || "queued")
    .replace(/_/g, " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
  return value || "Queued";
}

function statusHeading(text, status) {
  const title = document.createElement("strong");
  title.className = `status-title ${statusClass(status)}`;
  title.textContent = text;
  return title;
}

function compactPathLine(label, value, { useFileName = false } = {}) {
  const line = document.createElement("p");
  const text = document.createElement("span");
  text.className = "result-path";
  text.textContent = useFileName ? fileName(value) : value;
  text.title = value;
  line.append(`${label}: `, text);
  return line;
}

function appendNoticeLines(container, notices) {
  notices.forEach((notice) => {
    const item = document.createElement("p");
    item.className = "muted";
    item.textContent = notice.message || notice.suggested_user_action || humanNoticeTitle(notice.code);
    if (notice.technical_details) {
      item.title = notice.technical_details;
    }
    container.appendChild(item);
  });
}

function humanNoticeTitle(code) {
  const titles = {
    unsupported_source: "Unsupported source",
    login_required: "Sign-in required",
    cookies_required: "Chrome session unavailable",
    network_error: "Connection issue",
    timeout: "Timed out",
    ytdlp_not_found: "Media engine missing",
    extractor_failed: "Source failed",
    invalid_output: "Invalid analyzer output",
    api_error: "Local API error",
    api_unavailable: "Local API unavailable",
    no_format_selected: "Choose an output first",
    invalid_input_file: "Missing media file",
    unknown_error: "Something went wrong",
  };
  return titles[code] || String(code || "Notice").replace(/_/g, " ");
}

function humanBatchItemMeta(item) {
  const parts = [humanStatusLabel(item.status)];
  if (item.error?.message) {
    parts.push(item.error.message);
  }
  return parts.filter(Boolean).join(" · ");
}


function renderDownloadResult(result) {
  latestDownloadResult = result;
  downloadResult.classList.remove("hidden");
  downloadResult.innerHTML = "";

  const status = result.status || "unknown";
  downloadResult.appendChild(statusHeading(status === "succeeded" ? "Download saved" : `Download ${humanStatusLabel(status).toLowerCase()}`, status));

  if (result.output_dir) {
    downloadResult.appendChild(compactPathLine("Folder", result.output_dir, { useFileName: true }));
    copyOutputButton.disabled = false;
    if (revealOutputButton) {
      revealOutputButton.disabled = false;
    }
  }

  const files = result.downloaded_files || [];
  if (files.length > 0) {
    const list = document.createElement("ul");
    files.forEach((file) => {
      const item = document.createElement("li");
      item.textContent = fileName(file);
      item.title = file;
      list.appendChild(item);
    });
    downloadResult.appendChild(list);
    if (canTranscribeSelectedFormat()) {
      downloadedFileForTranscript = files[0];
      transcriptFileLabel.textContent = fileName(files[0]);
      transcriptPanel.classList.remove("hidden");
      updateFlowStep("transcribe");
    } else {
      downloadedFileForTranscript = null;
      transcriptFileLabel.textContent = "No file selected";
      transcriptPanel.classList.add("hidden");
      const hint = document.createElement("p");
      hint.className = "download-hint";
      hint.textContent = nonTranscribableDownloadMessage();
      downloadResult.appendChild(hint);
      updateFlowStep("download");
    }
  }

  appendNoticeLines(downloadResult, [...(result.errors || []), ...(result.warnings || [])]);

  if ((result.errors || []).length > 0) {
    updateFlowStep("download");
  }
}


function renderCourseDownloadResult(result) {
  latestDownloadResult = result;
  courseDownloadResult.classList.remove("hidden");
  courseDownloadResult.innerHTML = "";

  const status = result.status || "unknown";
  courseDownloadResult.appendChild(statusHeading(status === "succeeded" ? "Course saved" : `Course ${humanStatusLabel(status).toLowerCase()}`, status));

  if (result.output_dir) {
    courseDownloadResult.appendChild(compactPathLine("Folder", result.output_dir, { useFileName: true }));
    copyOutputButton.disabled = false;
    if (revealOutputButton) {
      revealOutputButton.disabled = false;
    }
  }

  const files = result.downloaded_files || [];
  if (files.length > 0) {
    const summary = document.createElement("p");
    summary.className = "muted";
    summary.textContent = `${files.length} file${files.length === 1 ? "" : "s"} saved.`;
    courseDownloadResult.appendChild(summary);

    const list = document.createElement("ul");
    files.slice(0, 8).forEach((file) => {
      const item = document.createElement("li");
      item.textContent = fileName(file);
      item.title = file;
      list.appendChild(item);
    });
    courseDownloadResult.appendChild(list);
  }

  appendNoticeLines(courseDownloadResult, [...(result.errors || []), ...(result.warnings || [])]);

  if ((result.errors || []).length === 0 && result.status === "succeeded") {
    updateFlowStep("result");
    loadRecentOutputs();
  }
}


function renderJobStatus(container, job, label) {
  container.classList.remove("hidden");
  container.innerHTML = "";

  const status = job.status || "queued";
  container.appendChild(statusHeading(`${label}: ${humanStatusLabel(status)}`, status));

  const step = document.createElement("p");
  step.className = "job-detail";
  step.textContent = humanStepLabel(job.current_step || status);
  container.appendChild(step);

  if (Number.isFinite(job.progress_percent)) {
    const track = document.createElement("div");
    track.className = "progress-track";
    const fill = document.createElement("div");
    fill.className = "progress-fill";
    fill.style.width = `${Math.max(0, Math.min(100, Math.round(job.progress_percent)))}%`;
    track.appendChild(fill);
    container.appendChild(track);
  }

  if (job.cancel_requested) {
    const cancel = document.createElement("p");
    cancel.className = "muted";
    cancel.textContent = "Cancel requested. Stopping when possible.";
    container.appendChild(cancel);
  }

  if (job.error) {
    appendNoticeLines(container, [job.error]);
  }

  if (["failed", "cancelled"].includes(status) && job.job_id) {
    appendDiagnosticsButton(container, job.job_id);
  }
}

async function pollJob(jobId, onUpdate) {
  while (true) {
    await delay(900);
    const response = await apiFetch(`/jobs/${encodeURIComponent(jobId)}`);
    if (!response.ok) {
      throw new Error(await readErrorMessage(response));
    }
    const job = await response.json();
    onUpdate(job);
    if (["succeeded", "failed", "cancelled"].includes(job.status)) {
      return job;
    }
  }
}

async function cancelJob(jobId, container, label) {
  const response = await apiFetch(`/jobs/${encodeURIComponent(jobId)}/cancel`, {
    method: "POST",
  });
  if (!response.ok) {
    renderJobStatus(container, {
      status: "failed",
      current_step: "cancel failed",
      error: { code: "api_error", message: await readErrorMessage(response) },
    }, label);
    return;
  }
  const job = await response.json();
  renderJobStatus(container, job, label);
  return job;
}

function appendDiagnosticsButton(container, jobId) {
  const actions = document.createElement("div");
  actions.className = "actions-row diagnostics-actions";
  const button = document.createElement("button");
  button.type = "button";
  button.className = "secondary-button";
  button.textContent = "Copy diagnostics";
  button.addEventListener("click", async () => {
    await copyDiagnosticsBundle(jobId);
  });
  actions.appendChild(button);
  container.appendChild(actions);
}

async function copyDiagnosticsBundle(jobId) {
  try {
    const response = await apiFetch(`/diagnostics/jobs/${encodeURIComponent(jobId)}`);
    if (!response.ok) {
      apiStatus.textContent = await readErrorMessage(response);
      return;
    }
    const bundle = await response.json();
    await copyText(JSON.stringify(bundle, null, 2), "Diagnostics copied.");
  } catch (error) {
    apiStatus.textContent = normalizeNetworkError(error);
  }
}

function delay(ms) {
  return new Promise((resolve) => window.setTimeout(resolve, ms));
}

function toggleCancelButton(button, job) {
  button.classList.toggle("hidden", !["queued", "running"].includes(job.status));
}

function setTranscribeLoading(isLoading) {
  transcribeButton.disabled = isLoading;
  whisperModel.disabled = isLoading;
  transcriptFormat.disabled = isLoading;
  transcribeButton.textContent = isLoading ? "Transcribing..." : "Transcribe";
  if (isLoading) {
    updateFlowStep("transcribe");
  }
}

function updateLocalTranscribeButtonState() {
  localTranscribeButton.disabled = !currentLocalFileResult?.saved_path;
}

function setLocalTranscribeLoading(isLoading) {
  localTranscribeButton.disabled = isLoading || !currentLocalFileResult?.saved_path;
  localWhisperModel.disabled = isLoading;
  localTranscriptFormat.disabled = isLoading;
  localTranscribeButton.textContent = isLoading ? "Transcribing..." : "Transcribe local file";
  if (isLoading) {
    updateFlowStep("transcribe");
  }
}


function renderTranscriptResult(result, container = transcriptResult) {
  latestTranscriptResult = result;
  container.classList.remove("hidden");
  container.innerHTML = "";

  const status = result.status || "unknown";
  container.appendChild(statusHeading(status === "succeeded" ? "Transcript saved" : `Transcript ${humanStatusLabel(status).toLowerCase()}`, status));

  const transcriptPath = selectedTranscriptPath(result);
  if (transcriptPath) {
    container.appendChild(compactPathLine("File", transcriptPath, { useFileName: true }));
  }

  appendNoticeLines(container, [...(result.errors || []), ...(result.warnings || [])]);

  if ((result.errors || []).length === 0 && result.status === "succeeded") {
    renderFilesResult(result);
    updateFlowStep("result");
    loadRecentOutputs();
  }
}

function renderFilesResult(result) {
  filesPanel.classList.remove("hidden");
  filesList.innerHTML = "";
  outputDirLabel.textContent = result.output_dir ? fileName(result.output_dir) : "Output path unavailable";
  const transcriptPath = selectedTranscriptPath(result);

  [
    ["Folder", result.output_dir],
    ["Media file", downloadedFileForTranscript],
    ["Transcript", transcriptPath],
  ].forEach(([label, value]) => {
    if (!value) {
      return;
    }
    const row = document.createElement("div");
    row.className = "file-row";
    const name = document.createElement("strong");
    name.textContent = label;
    const path = document.createElement("span");
    path.textContent = fileName(value);
    path.title = value;
    row.append(name, path);
    filesList.appendChild(row);
  });

  const previewText = result.transcript_text || "";
  transcriptPreview.textContent = previewText.slice(0, 1200) || "Transcript text is empty.";
  transcriptPreviewCard.classList.remove("hidden");
  copyTranscriptButton.disabled = !result.transcript_text;
  copySummaryButton.disabled = !result.summary_prompt_text;
  copySummaryButton.classList.toggle("hidden", !result.summary_prompt_text);
  copyOutputButton.disabled = !(result.output_dir || latestDownloadResult?.output_dir);
  if (revealOutputButton) {
    revealOutputButton.disabled = !(result.output_dir || latestDownloadResult?.output_dir);
  }
}

function selectedTranscriptPath(result) {
  return result.transcript_txt_path || result.transcript_md_path || result.transcript_json_path || "";
}

async function loadRecentOutputs() {
  try {
    const response = await apiFetch("/outputs");
    if (!response.ok) {
      recentResultsList.innerHTML = "";
      recentResultsList.appendChild(emptyLine("Recent results are unavailable."));
      return;
    }
    renderRecentOutputs((await response.json()).outputs || []);
  } catch {
    recentResultsList.innerHTML = "";
    recentResultsList.appendChild(emptyLine("Recent results are unavailable."));
  }
}

function renderRecentOutputs(outputs) {
  recentResultsList.innerHTML = "";
  if (outputs.length === 0) {
    recentResultsList.appendChild(emptyLine("No user outputs yet."));
    return;
  }

  outputs.slice(0, 8).forEach((output) => {
    const row = document.createElement("div");
    row.className = "recent-output-row";

    const title = document.createElement("div");
    title.className = "recent-output-title";
    title.textContent = output.title_or_filename || output.output_id;

    const meta = metaLine([
      output.source_type,
      formatDate(output.created_at),
      readableSize(output.total_size_bytes),
      `${output.files_count || 0} files`,
    ]);

    const badges = metaLine([
      output.has_media && "media",
      output.has_transcript && "transcript",
      output.has_summary_prompt && "prompt",
    ]);

    const actions = document.createElement("div");
    actions.className = "recent-output-actions";
    const copyButton = document.createElement("button");
    copyButton.type = "button";
    copyButton.className = "small-button";
    copyButton.textContent = "Copy path";
    copyButton.addEventListener("click", () => {
      copyText(output.output_dir, "Output path copied.");
    });
    const revealButton = document.createElement("button");
    revealButton.type = "button";
    revealButton.className = "small-button";
    revealButton.textContent = "Reveal";
    revealButton.addEventListener("click", () => revealOutputPath(output.output_dir));
    const deleteButton = document.createElement("button");
    deleteButton.type = "button";
    deleteButton.className = "danger-button";
    deleteButton.textContent = "Delete";
    deleteButton.addEventListener("click", () => deleteRecentOutput(output.output_id));
    actions.append(copyButton, revealButton, deleteButton);

    row.append(title, meta, badges, actions);
    recentResultsList.appendChild(row);
  });
}

async function revealOutputPath(outputDir) {
  if (!outputDir) {
    apiStatus.textContent = "Output path unavailable.";
    return;
  }
  const outputId = fileName(outputDir);
  try {
    const response = await apiFetch("/outputs/" + encodeURIComponent(outputId) + "/reveal", {
      method: "POST",
    });
    if (!response.ok) {
      apiStatus.textContent = await readErrorMessage(response);
      return;
    }
    const result = await response.json();
    apiStatus.textContent = result.message || "Reveal requested.";
  } catch (error) {
    apiStatus.textContent = normalizeNetworkError(error);
  }
}

async function deleteRecentOutput(outputId) {
  try {
    const response = await apiFetch(`/outputs/${encodeURIComponent(outputId)}`, {
      method: "DELETE",
    });
    if (!response.ok) {
      apiStatus.textContent = await readErrorMessage(response);
      return;
    }
    const result = await response.json();
    apiStatus.textContent = result.message || "Output deleted.";
    loadRecentOutputs();
  } catch (error) {
    apiStatus.textContent = normalizeNetworkError(error);
  }
}

function updateFlowStep(activeStep) {
  const order = ["analyze", "select", "download", "transcribe", "result"];
  const activeIndex = Math.max(order.indexOf(activeStep), 0);
  flowSteps.forEach((step) => {
    const stepIndex = order.indexOf(step.dataset.step);
    step.classList.toggle("is-active", stepIndex === activeIndex);
    step.classList.toggle("is-done", stepIndex >= 0 && stepIndex < activeIndex);
  });
}

function selectedPresetLabel(option) {
  return option.preset_label || simpleFormatLabel(option, categoryForOption(option));
}

function simpleFormatLabel(option, category) {
  if (category === "subtitles") {
    return [
      option.language?.toUpperCase(),
      option.subtitle_type === "automatic" ? "Auto captions" : "Manual subtitles",
    ].filter(Boolean).join(" · ") || "Subtitles";
  }

  if (category === "video" || option.type === "video" || option.type === "combined") {
    return [
      displayContainer(option),
      displayResolution(option),
      readableSizeShort(option.filesize || option.filesize_approx),
    ].filter(Boolean).join(" · ");
  }

  return [
    displayContainer(option),
    readableSizeShort(option.filesize || option.filesize_approx),
  ].filter(Boolean).join(" · ") || "Audio";
}

function simpleFormatHelper(option, category) {
  if (category === "subtitles") {
    const formats = Array.isArray(option.formats) && option.formats.length > 0
      ? option.formats.slice(0, 3).join(", ")
      : "";
    return formats ? `Formats: ${formats}` : "";
  }
  if (category === "video" && option.type === "video") {
    return "";
  }
  return "";
}

function displayContainer(option) {
  return String(option.ext || option.container || option.format_id || "").toUpperCase();
}

function displayResolution(option) {
  const quality = videoQualityNumber(option);
  if (quality > 0) {
    return `${quality}p`;
  }
  return option.resolution || "";
}

function videoQualityNumber(option) {
  if (Number.isFinite(option.height)) {
    return Number(option.height);
  }
  const resolution = String(option.resolution || "");
  const match = resolution.match(/(\d{3,4})p?$/) || resolution.match(/\d+x(\d{3,4})/);
  if (match) {
    return Number(match[1]);
  }
  const label = String(option.display_label || "");
  const labelMatch = label.match(/(\d{3,4})p/);
  return labelMatch ? Number(labelMatch[1]) : 0;
}

function formatSelectionSummary(option) {
  return simpleFormatLabel(option, categoryForOption(option));
}

function selectionKeyForOption(option) {
  return option.selection_id || option.format_id;
}

function categoryForOption(option) {
  if (option.type === "subtitles") {
    return "subtitles";
  }
  if (option.type === "video" || option.type === "combined") {
    return "video";
  }
  return "audio";
}

async function copyText(text, successMessage) {
  if (!text) {
    apiStatus.textContent = "Nothing to copy.";
    return;
  }
  try {
    await navigator.clipboard.writeText(text);
  } catch {
    const textarea = document.createElement("textarea");
    textarea.value = text;
    textarea.setAttribute("readonly", "");
    textarea.style.position = "fixed";
    textarea.style.opacity = "0";
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand("copy");
    textarea.remove();
  }
  apiStatus.textContent = successMessage;
}

function textBlock(text) {
  const block = document.createElement("div");
  block.className = "format-label";
  block.textContent = text;
  return block;
}

function metaLine(items) {
  const meta = document.createElement("div");
  meta.className = "format-meta";
  items.filter(Boolean).forEach((item) => {
    const span = document.createElement("span");
    span.textContent = item;
    meta.appendChild(span);
  });
  return meta;
}

function renderWarnings(warnings) {
  const simpleWarnings = simplifyWarnings(warnings);
  renderCompactNoticePanel(warningsPanel, warningsList, simpleWarnings);
  warningsPanel.classList.toggle("warning", simpleWarnings.length > 0);
}

function renderErrors(errors, jobError) {
  const allErrors = [...errors];
  if (jobError && !allErrors.some((error) => error.code === jobError.code)) {
    allErrors.push(jobError);
  }
  renderNoticePanel(errorsPanel, errorsList, allErrors.map(describeError));
}

function describeError(error) {
  const knownMessages = {
    unsupported_source: "This source is not supported by the current analyzer.",
    login_required: "Udemy did not allow access with the current session.",
    cookies_required: "Chrome session is unavailable or Udemy rejected it.",
    network_error: "The analyzer could not access the source. Check the URL and network access, then retry.",
    timeout: "Analysis timed out. Try again later or use a shorter/public source.",
    ytdlp_not_found: "yt-dlp was not found. Check the local environment and PATH.",
    extractor_failed: "The source extractor failed. Source support is best-effort and may change.",
    invalid_output: "The analyzer returned invalid output. Retry or inspect the source.",
  };

  return {
    ...error,
    message: error.message || knownMessages[error.code] || "Analysis failed.",
    suggested_user_action:
      error.suggested_user_action || suggestedActionForCode(error.code),
  };
}

function suggestedActionForCode(code) {
  const actions = {
    unsupported_source: "Try a different public URL or wait for local-file support in a future block.",
    login_required: "Open Udemy in Chrome, make sure you are signed in, then try again.",
    cookies_required: "Open Chrome, sign in to Udemy, then retry. If it still fails, use Advanced manual cookies.txt.",
    network_error: "Check connectivity and retry.",
    timeout: "Retry later.",
  };
  return actions[code] || "";
}


function renderNoticePanel(panel, list, notices) {
  list.innerHTML = "";
  panel.classList.toggle("hidden", notices.length === 0);

  notices.forEach((notice) => {
    const item = document.createElement("div");
    item.className = "notice-item";

    const title = document.createElement("span");
    title.className = "notice-code";
    title.textContent = humanNoticeTitle(notice.code || notice.severity);

    const message = document.createElement("div");
    message.textContent = notice.message || notice.suggested_user_action || "No details.";

    item.append(title, message);
    if (notice.suggested_user_action) {
      const action = document.createElement("p");
      action.className = "muted";
      action.textContent = notice.suggested_user_action;
      item.appendChild(action);
    }
    if (notice.technical_details) {
      const details = document.createElement("details");
      details.className = "technical-details";
      const summary = document.createElement("summary");
      summary.textContent = "Technical details";
      const pre = document.createElement("pre");
      pre.textContent = notice.technical_details;
      details.append(summary, pre);
      item.appendChild(details);
    }
    list.appendChild(item);
  });
}

function renderCompactNoticePanel(panel, list, notices) {
  list.innerHTML = "";
  panel.classList.toggle("hidden", notices.length === 0);
  notices.forEach((notice) => {
    const item = document.createElement("div");
    item.className = "notice-item compact-notice";
    item.textContent = notice.message || "Note";
    list.appendChild(item);
  });
}

function simplifyWarnings(warnings) {
  const byCode = new Map();
  (warnings || []).forEach((warning) => {
    if (["no_subtitles", "no_automatic_captions", "format_size_unknown", "analysis_only_not_download_tested"].includes(warning.code)) {
      return;
    }
    if (warning.code === "platform_terms_warning") {
      byCode.set("platform_terms_warning", {
        message: "Only download or process media you have rights to use.",
      });
      return;
    }
    if (warning.code === "best_effort_extractor") {
      byCode.set("best_effort_extractor", {
        message: "Source support is best-effort and may change.",
      });
      return;
    }
    byCode.set(warning.code || warning.message, {
      message: warning.message || "Review this source before continuing.",
    });
  });
  return [...byCode.values()];
}

function renderFatalError(title, message) {
  loadingState.classList.add("hidden");
  emptyState.classList.add("hidden");
  resultContent.classList.remove("hidden");
  apiStatus.textContent = title;

  renderSourceSummary({
    title,
    duration_label: "",
    extractor: "local api",
    uploader: null,
    webpage_url: "",
    thumbnail_url: "",
  });
  renderFormatPicker({
    audio: [],
    video: [],
    subtitles: [],
  });
  renderWarnings([]);
  renderErrors([{ code: errorCodeFromTitle(title), message }], null);
  coursePanel.classList.add("hidden");
  batchPanel.classList.add("hidden");
  localFilePanel.classList.add("hidden");
  resetDownloadSelection();
}

function errorCodeFromTitle(title) {
  return title.toLowerCase().replaceAll(" ", "_").replace(/[^a-z0-9_]/g, "");
}

function emptyLine(text) {
  const line = document.createElement("p");
  line.className = "empty-line";
  line.textContent = text;
  return line;
}

function formatDuration(seconds) {
  if (!Number.isFinite(seconds)) {
    return "duration unknown";
  }
  const total = Math.round(seconds);
  const minutes = Math.floor(total / 60);
  const remainder = String(total % 60).padStart(2, "0");
  return `${minutes}:${remainder}`;
}

function formatDate(value) {
  if (!value) {
    return "";
  }
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return "";
  }
  return date.toLocaleString();
}

function readableSize(bytes) {
  if (!Number.isFinite(bytes) || bytes <= 0) {
    return "";
  }
  const units = ["B", "KiB", "MiB", "GiB"];
  let value = bytes;
  let unitIndex = 0;
  while (value >= 1024 && unitIndex < units.length - 1) {
    value /= 1024;
    unitIndex += 1;
  }
  return unitIndex === 0
    ? `${Math.round(value)} ${units[unitIndex]}`
    : `${value.toFixed(2)} ${units[unitIndex]}`;
}

function readableSizeShort(bytes) {
  const value = readableSize(bytes);
  return value
    .replace("KiB", "KB")
    .replace("MiB", "MB")
    .replace("GiB", "GB");
}

function fileName(path) {
  return String(path).split("/").pop() || path;
}

function cssEscape(value) {
  if (window.CSS && typeof window.CSS.escape === "function") {
    return window.CSS.escape(value);
  }
  return String(value).replace(/["\\]/g, "\\$&");
}
