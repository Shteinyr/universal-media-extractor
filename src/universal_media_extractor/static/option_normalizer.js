(function attachOptionNormalizer(global) {
  "use strict";

  const MIN_VIDEO_QUALITY = 1080;

  function buildFormatPickerData(result) {
    const mediaOptions = result?.media_options || {};
    const audio = dedupeMediaOptions(
      toArray(mediaOptions.audio),
      audioDedupeKey,
      "audio",
    );
    const video = dedupeMediaOptions(
      [...toArray(mediaOptions.combined), ...toArray(mediaOptions.video)]
        .filter((option) => videoQualityNumber(option) >= MIN_VIDEO_QUALITY),
      videoDedupeKey,
      "video",
    );
    const subtitles = dedupeSubtitleOptions([
      ...normalizeSubtitleOptions(result?.subtitles, "manual"),
      ...normalizeSubtitleOptions(result?.automatic_captions, "automatic"),
    ]);

    return { audio, video, subtitles };
  }

  function buildPresetPickerData(result) {
    const source = buildFormatPickerData(result);
    const bestVideo = chooseBestVideo(source.video);
    const fullHdVideo = chooseVideoByQuality(source.video, 1080);
    const smallerVideo = chooseSmallerVideo(source.video);
    const audioM4a = chooseAudioForContainer(source.audio, "m4a") || chooseBestAudio(source.audio);
    const audioMp3 = chooseBestAudio(source.audio);
    const subtitles = chooseBestSubtitle(source.subtitles);

    return {
      presets: [
        videoPreset("best_video", "Best Video", "Highest quality available", bestVideo),
        videoPreset("video_1080p", "1080p", "Standard full HD video", fullHdVideo),
        videoPreset("smaller_video", "Smaller Video", "Smallest available video at 1080p or higher", smallerVideo),
        audioPreset("audio_m4a", "Audio M4A", "Good quality, Apple-friendly audio", audioM4a, "m4a"),
        audioPreset("audio_mp3", "Audio MP3", "Most compatible audio file", audioMp3, "mp3"),
        subtitlePreset("subtitles", "Subtitles", "Save available subtitles", subtitles),
        unavailablePreset("archive_pack", "Archive Pack", "Planned: media, subtitles, metadata, and transcript together."),
      ],
      source,
    };
  }

  function dedupeMediaOptions(options, keyBuilder, category) {
    const byKey = new Map();
    toArray(options).forEach((option) => {
      const key = keyBuilder(option);
      const current = byKey.get(key);
      byKey.set(key, chooseBetterOption(current, option, category));
    });
    return Array.from(byKey.values());
  }

  function dedupeSubtitleOptions(options) {
    const byKey = new Map();
    toArray(options).forEach((option) => {
      const key = subtitleDedupeKey(option);
      const current = byKey.get(key);
      byKey.set(key, mergeSubtitleOption(current, option));
    });
    return Array.from(byKey.values());
  }

  function videoPreset(id, label, description, option) {
    if (!option) {
      return unavailablePreset(id, label, "No suitable video option found.");
    }
    const outputFormat = preferredVideoOutputFormat(option, id === "best_video" ? "mkv" : "mp4");
    return {
      ...option,
      selection_id: `preset:${id}`,
      preset_id: id,
      preset_label: label,
      preset_description: description,
      preset_output_format: outputFormat,
      preset_available: true,
      preset_detail: compactMediaDetail(option),
    };
  }

  function audioPreset(id, label, description, option, outputFormat) {
    if (!option) {
      return unavailablePreset(id, label, "No audio option found.");
    }
    return {
      ...option,
      selection_id: `preset:${id}`,
      preset_id: id,
      preset_label: label,
      preset_description: description,
      preset_output_format: outputFormat,
      preset_available: true,
      preset_detail: compactMediaDetail(option),
      type: "audio",
    };
  }

  function subtitlePreset(id, label, description, option) {
    if (!option) {
      return unavailablePreset(id, label, "No subtitles found.");
    }
    return {
      ...option,
      selection_id: `preset:${id}`,
      preset_id: id,
      preset_label: label,
      preset_description: description,
      preset_output_format: "srt",
      preset_available: true,
      preset_detail: compactSubtitleDetail(option),
      type: "subtitles",
    };
  }

  function unavailablePreset(id, label, reason) {
    return {
      selection_id: `preset:${id}`,
      preset_id: id,
      preset_label: label,
      preset_description: reason,
      preset_available: false,
      type: id === "subtitles" ? "subtitles" : "unavailable",
    };
  }

  function chooseBestVideo(options) {
    return [...toArray(options)].sort((a, b) => {
      const qualityDiff = videoQualityNumber(b) - videoQualityNumber(a);
      if (qualityDiff !== 0) {
        return qualityDiff;
      }
      return compareOptionScore(a, b, "video");
    })[0] || null;
  }

  function chooseVideoByQuality(options, targetQuality) {
    return [...toArray(options)]
      .filter((option) => videoQualityNumber(option) === targetQuality)
      .sort((a, b) => videoPreferenceScore(b) - videoPreferenceScore(a))[0] || null;
  }

  function chooseSmallerVideo(options) {
    const candidates = toArray(options).filter((option) => videoQualityNumber(option) >= MIN_VIDEO_QUALITY);
    return candidates.sort((a, b) => {
      const aSize = Number(a.filesize || a.filesize_approx || Number.MAX_SAFE_INTEGER);
      const bSize = Number(b.filesize || b.filesize_approx || Number.MAX_SAFE_INTEGER);
      if (aSize !== bSize) {
        return aSize - bSize;
      }
      return videoQualityNumber(a) - videoQualityNumber(b);
    })[0] || null;
  }

  function chooseBestAudio(options) {
    return [...toArray(options)].sort((a, b) => compareOptionScore(a, b, "audio"))[0] || null;
  }

  function chooseAudioForContainer(options, container) {
    return [...toArray(options)]
      .filter((option) => normalizedContainer(option) === container)
      .sort((a, b) => compareOptionScore(a, b, "audio"))[0] || null;
  }

  function chooseBestSubtitle(options) {
    return [...toArray(options)].sort((a, b) => {
      const manualDiff = Number(b.subtitle_type === "manual") - Number(a.subtitle_type === "manual");
      if (manualDiff !== 0) {
        return manualDiff;
      }
      return String(a.language || "").localeCompare(String(b.language || ""));
    })[0] || null;
  }

  function compareOptionScore(a, b, category) {
    const aScore = optionScore(a, category);
    const bScore = optionScore(b, category);
    for (let index = 0; index < aScore.length; index += 1) {
      if (bScore[index] !== aScore[index]) {
        return bScore[index] - aScore[index];
      }
    }
    return 0;
  }

  function videoPreferenceScore(option) {
    return [
      normalizedContainer(option) === "mp4" ? 4 : 0,
      option.type === "combined" ? 2 : 0,
      hasKnownSize(option) ? 1 : 0,
      option.is_default_recommended ? 1 : 0,
    ].reduce((total, value) => total + value, 0);
  }

  function preferredVideoOutputFormat(option, fallback) {
    const container = normalizedContainer(option);
    if (["mp4", "webm"].includes(container)) {
      return container === "webm" && fallback === "mkv" ? "mkv" : container;
    }
    return fallback;
  }

  function compactMediaDetail(option) {
    return [
      normalizedContainer(option).toUpperCase(),
      videoQualityNumber(option) > 0 ? `${videoQualityNumber(option)}p` : "",
      readableSize(option.filesize || option.filesize_approx),
    ].filter(Boolean).join(" · ");
  }

  function compactSubtitleDetail(option) {
    return [
      String(option.language || "all").toUpperCase(),
      option.subtitle_type === "automatic" ? "Auto captions" : "Manual subtitles",
    ].filter(Boolean).join(" · ");
  }

  function readableSize(size) {
    const numericSize = Number(size || 0);
    if (!Number.isFinite(numericSize) || numericSize <= 0) {
      return "";
    }
    const mib = 1024 * 1024;
    const kib = 1024;
    if (numericSize >= mib) {
      return `${(numericSize / mib).toFixed(numericSize >= 10 * mib ? 0 : 2)} MB`;
    }
    return `${(numericSize / kib).toFixed(0)} KB`;
  }

  function normalizeSubtitleOptions(options, fallbackType) {
    return toArray(options).map((option) => {
      const language = normalizeLanguage(option.language || option.id || "all");
      const subtitleType = normalizeSubtitleType(option.type || option.subtitle_type || fallbackType);
      return {
        ...option,
        format_id: language,
        selection_id: `subtitles:${subtitleType}:${language}`,
        type: "subtitles",
        subtitle_type: subtitleType,
        language,
        formats: uniqueSorted(toArray(option.formats).map((format) => String(format).toLowerCase())),
        is_default_recommended: subtitleType === "manual",
      };
    });
  }

  function chooseBetterOption(current, candidate, category) {
    if (!current) {
      return candidate;
    }

    const currentScore = optionScore(current, category);
    const candidateScore = optionScore(candidate, category);
    for (let index = 0; index < currentScore.length; index += 1) {
      if (candidateScore[index] > currentScore[index]) {
        return candidate;
      }
      if (candidateScore[index] < currentScore[index]) {
        return current;
      }
    }
    return current;
  }

  function optionScore(option, category) {
    return [
      hasKnownSize(option) ? 1 : 0,
      option.is_default_recommended ? 1 : 0,
      category === "video" && option.type === "combined" ? 1 : 0,
      completenessScore(option),
      videoQualityNumber(option),
      Number(option.filesize || option.filesize_approx || 0),
    ];
  }

  function mergeSubtitleOption(current, candidate) {
    if (!current) {
      return candidate;
    }
    return {
      ...chooseBetterOption(current, candidate, "subtitles"),
      formats: uniqueSorted([...toArray(current.formats), ...toArray(candidate.formats)]),
      is_default_recommended: Boolean(current.is_default_recommended || candidate.is_default_recommended),
    };
  }

  function audioDedupeKey(option) {
    return [
      "audio",
      normalizedContainer(option),
      sizeBucket(option.filesize || option.filesize_approx),
    ].join("|");
  }

  function videoDedupeKey(option) {
    return [
      "video",
      normalizedContainer(option),
      `${videoQualityNumber(option)}p`,
    ].join("|");
  }

  function subtitleDedupeKey(option) {
    return [
      "subtitles",
      normalizeLanguage(option.language || option.format_id || "all"),
      normalizeSubtitleType(option.subtitle_type || option.type || "manual"),
    ].join("|");
  }

  function normalizedContainer(option) {
    return String(option?.ext || option?.container || "unknown").trim().toLowerCase();
  }

  function normalizeLanguage(language) {
    return String(language || "all").trim().toLowerCase();
  }

  function normalizeSubtitleType(type) {
    const normalized = String(type || "manual").trim().toLowerCase();
    return ["automatic", "auto"].includes(normalized) ? "automatic" : "manual";
  }

  function videoQualityNumber(option) {
    if (Number.isFinite(option?.height)) {
      return Number(option.height);
    }
    const resolution = String(option?.resolution || "");
    const resolutionMatch = resolution.match(/(\d{3,4})p?$/) || resolution.match(/\d+x(\d{3,4})/);
    if (resolutionMatch) {
      return Number(resolutionMatch[1]);
    }
    const label = String(option?.display_label || "");
    const labelMatch = label.match(/(\d{3,4})p/);
    return labelMatch ? Number(labelMatch[1]) : 0;
  }

  function hasKnownSize(option) {
    return Boolean(option?.filesize || option?.filesize_approx);
  }

  function sizeBucket(size) {
    const numericSize = Number(size || 0);
    if (!Number.isFinite(numericSize) || numericSize <= 0) {
      return "unknown";
    }
    const kib = 1024;
    const mib = kib * 1024;
    if (numericSize < mib) {
      return `${Math.round(numericSize / kib)}kb`;
    }
    return `${Math.round(numericSize / mib)}mb`;
  }

  function completenessScore(option) {
    return [
      option?.format_id,
      option?.ext,
      option?.container,
      option?.resolution,
      option?.height,
      option?.width,
      option?.audio_codec,
      option?.video_codec,
      option?.filesize || option?.filesize_approx,
      option?.display_label,
    ].filter(Boolean).length;
  }

  function uniqueSorted(values) {
    return Array.from(new Set(toArray(values).filter(Boolean))).sort();
  }

  function toArray(value) {
    return Array.isArray(value) ? value : [];
  }

  const api = {
    buildFormatPickerData,
    buildPresetPickerData,
    dedupeMediaOptions,
    dedupeSubtitleOptions,
    normalizeSubtitleOptions,
    videoQualityNumber,
  };

  global.UIOptionNormalizer = api;
  if (typeof module !== "undefined" && module.exports) {
    module.exports = api;
  }
})(typeof globalThis !== "undefined" ? globalThis : window);
