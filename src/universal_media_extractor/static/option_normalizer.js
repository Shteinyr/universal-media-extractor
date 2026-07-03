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
