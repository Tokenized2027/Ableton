#!/usr/bin/env python3
"""
Flyin' Colors — Semi-Automated Reference Track Analysis Pipeline

Extracts musical features from audio files using librosa and outputs
a pre-filled reference analysis markdown template.

Usage:
    python librosa_analysis_pipeline.py "path/to/track.wav"
    python librosa_analysis_pipeline.py "path/to/track.mp3" --bpm-hint 148
    python librosa_analysis_pipeline.py "path/to/track.wav" --output "docs/reference-analysis/artist-track.md"
    python librosa_analysis_pipeline.py --batch "path/to/reference-tracks/" --bpm-hint 148

Requirements:
    pip install -r requirements.txt

Example Output:
    ```markdown
    # Reference Analysis: Filteria — Birds Lingva Franca

    ## Source Info
    - BPM: 148.2 (librosa estimate — verify with Ableton warp)
    - Key: Dm (confidence: 0.847)
    - Scale: harmonic_minor (verify by ear)
    - Length: 8:42 (192 bars at 148 BPM)

    ## Structure Map (bar-by-bar)
    | Bar Range | Section | Elements Active | Energy % | Notes |
    |-----------|---------|-----------------|----------|-------|
    | 1-16      | [TODO]  | [TODO]          | 45%      | [TODO]|
    | 17-32     | [TODO]  | [TODO]          | 67%      | [TODO]|
    ...
    ```
"""

import argparse
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    import librosa
    import numpy as np
except ImportError:
    logger.error("Required packages not installed.")
    logger.error("Run: pip install -r requirements.txt")
    sys.exit(1)


def validate_audio_file(audio_path: str) -> bool:
    """Validate that the audio file exists and is a supported format."""
    supported_formats = ['.wav', '.mp3', '.flac', '.ogg', '.aiff', '.aif', '.m4a']

    if not os.path.exists(audio_path):
        logger.error(f"File not found: {audio_path}")
        return False

    file_ext = Path(audio_path).suffix.lower()
    if file_ext not in supported_formats:
        logger.error(f"Unsupported format {file_ext}. Supported: {', '.join(supported_formats)}")
        return False

    return True


def analyze_track(audio_path: str, bpm_hint: Optional[float] = None, sample_rate: int = 22050) -> Optional[Dict[str, Any]]:
    """Extract musical features from an audio file."""

    logger.info(f"Loading: {audio_path}")

    try:
        y, sr = librosa.load(audio_path, sr=sample_rate, mono=True)

        if len(y) == 0:
            logger.error(f"Audio file is empty or corrupt: {audio_path}")
            return None

    except Exception as e:
        logger.error(f"Failed to load audio file: {e}")
        return None

    duration_sec = librosa.get_duration(y=y, sr=sr)

    # Edge case: Very short files
    if duration_sec < 5.0:
        logger.warning(f"Track is very short ({duration_sec:.1f}s), analysis may be unreliable")
    duration_min = duration_sec / 60

    logger.info(f"Duration: {duration_sec:.1f}s ({duration_min:.1f} min)")
    logger.info("Analyzing...")

    results = {
        "duration_sec": duration_sec,
        "duration_str": f"{int(duration_min)}:{int(duration_sec % 60):02d}",
    }

    # --- BPM ---
    logger.info("  → Tempo estimation...")
    try:
        if bpm_hint:
            tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr, start_bpm=bpm_hint)
        else:
            tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

        # librosa may return an array; extract scalar
        if hasattr(tempo, "__len__"):
            tempo = float(tempo[0])
        else:
            tempo = float(tempo)

        results["bpm"] = round(tempo, 1)
        results["beat_frames"] = beat_frames
        logger.info(f"  → BPM: {results['bpm']}")
    except Exception as e:
        logger.warning(f"Tempo detection failed: {e}")
        if bpm_hint:
            logger.info(f"  → Using BPM hint: {bpm_hint}")
            results["bpm"] = bpm_hint
        else:
            logger.info("  → Defaulting to 140 BPM")
            results["bpm"] = 140.0
        results["beat_frames"] = []

    # --- Key Detection ---
    logger.info("  → Key detection (chroma analysis)...")
    try:
        chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
        chroma_mean = np.mean(chroma, axis=1)

        pitch_classes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        root_idx = int(np.argmax(chroma_mean))
        root_note = pitch_classes[root_idx]

        # Determine major vs minor by comparing major and minor profile correlations
        major_profile = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
        minor_profile = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])

        # Rotate profiles to match detected root
        major_corr = np.corrcoef(chroma_mean, np.roll(major_profile, root_idx))[0, 1]
        minor_corr = np.corrcoef(chroma_mean, np.roll(minor_profile, root_idx))[0, 1]

        if minor_corr > major_corr:
            key_str = f"{root_note}m"
            mode = "minor"
        else:
            key_str = f"{root_note}"
            mode = "major"

        results["key"] = key_str
        results["mode"] = mode

        # Detect likely scale based on chroma weight distribution
        chroma_normalized = chroma_mean / np.max(chroma_mean)
        rotated_chroma = np.roll(chroma_normalized, -root_idx)

        # Compare against scale templates (relative to root)
        # Template format: 12 semitones from root, 1 = note in scale, 0 = not in scale
        scale_templates = {
            "natural_minor": [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0],      # W-H-W-W-H-W-W
            "harmonic_minor": [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1],     # Raised 7th
            "phrygian": [1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0],           # b2 (flat 2nd)
            "phrygian_dominant": [1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0],  # Phrygian + major 3rd (Nitzhonot/Goa)
            "dorian": [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0],             # Natural minor + raised 6th
            "major": [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1],              # W-W-H-W-W-W-H
        }

        best_scale = "natural_minor"
        best_scale_corr = -1
        for scale_name, template in scale_templates.items():
            corr = np.corrcoef(rotated_chroma, template)[0, 1]
            if corr > best_scale_corr:
                best_scale_corr = corr
                best_scale = scale_name

        results["scale"] = best_scale
        results["scale_confidence"] = round(best_scale_corr, 3)
        logger.info(f"  → Key: {key_str} ({best_scale}, confidence: {results['scale_confidence']})")
    except Exception as e:
        logger.warning(f"Key detection failed: {e}")
        results["key"] = "Unknown"
        results["mode"] = "unknown"
        results["scale"] = "unknown"
        results["scale_confidence"] = 0.0

    # --- Energy Curve ---
    logger.info("  → Energy curve (RMS per section)...")
    try:
        rms = librosa.feature.rms(y=y)[0]

        # Calculate bars based on BPM
        if results["bpm"] > 0:
            bar_duration_sec = (60.0 / results["bpm"]) * 4  # 4 beats per bar
            total_bars = int(duration_sec / bar_duration_sec)
        else:
            bar_duration_sec = 4.0  # Default fallback
            total_bars = int(duration_sec / bar_duration_sec)

        results["total_bars"] = total_bars

        # Energy per 16-bar section
        frames_per_bar = int(len(rms) / max(total_bars, 1))
        section_size = 16  # bars per section for energy analysis
        energy_sections = []

        for i in range(0, total_bars, section_size):
            start_frame = i * frames_per_bar
            end_frame = min((i + section_size) * frames_per_bar, len(rms))
            if start_frame < len(rms):
                section_energy = float(np.mean(rms[start_frame:end_frame]))
                energy_sections.append({
                    "bar_start": i + 1,
                    "bar_end": min(i + section_size, total_bars),
                    "energy": section_energy,
                })

        # Normalize energy to 0-100%
        if energy_sections:
            max_energy = max(s["energy"] for s in energy_sections)
            if max_energy > 0:
                for s in energy_sections:
                    s["energy_pct"] = round((s["energy"] / max_energy) * 100)
            else:
                for s in energy_sections:
                    s["energy_pct"] = 0

        results["energy_sections"] = energy_sections
    except Exception as e:
        logger.warning(f"Energy analysis failed: {e}")
        results["total_bars"] = 0
        results["energy_sections"] = []

    # --- Spectral Centroid (brightness) ---
    logger.info("  → Spectral analysis (brightness tracking)...")
    try:
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        results["avg_brightness_hz"] = round(float(np.mean(spectral_centroid)))
        results["max_brightness_hz"] = round(float(np.max(spectral_centroid)))
        results["min_brightness_hz"] = round(float(np.min(spectral_centroid)))
    except Exception as e:
        logger.warning(f"Spectral analysis failed: {e}")
        results["avg_brightness_hz"] = 0
        results["max_brightness_hz"] = 0
        results["min_brightness_hz"] = 0

    # --- Onset Density (rhythmic activity) ---
    logger.info("  → Onset detection (rhythmic density)...")
    try:
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        onsets = librosa.onset.onset_detect(y=y, sr=sr, units="time")
        results["total_onsets"] = len(onsets)
        results["avg_onsets_per_bar"] = round(len(onsets) / max(results.get("total_bars", 1), 1), 1)
    except Exception as e:
        logger.warning(f"Onset detection failed: {e}")
        results["total_onsets"] = 0
        results["avg_onsets_per_bar"] = 0.0

    # --- Section Boundaries (structural segmentation) ---
    logger.info("  → Structural segmentation...")
    try:
        # Use spectral clustering for section detection
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        bound_frames = librosa.segment.agglomerative(mfcc, k=8)
        bound_times = librosa.frames_to_time(bound_frames, sr=sr)

        sections = []
        bar_duration_sec = (60.0 / results["bpm"]) * 4 if results["bpm"] > 0 else 4.0
        for i, bt in enumerate(bound_times):
            bar_num = int(bt / bar_duration_sec) + 1
            sections.append({
                "time_sec": round(float(bt), 1),
                "bar": min(bar_num, results.get("total_bars", 0)),
            })
        results["section_boundaries"] = sections
    except Exception:
        results["section_boundaries"] = []
        logger.info("  → (Section detection failed — will leave blank)")

    logger.info("Analysis complete.")
    return results


def generate_markdown(results: Dict[str, Any], audio_path: str, artist: str = "", track_name: str = "") -> str:
    """Generate a pre-filled reference analysis markdown template."""

    filename = Path(audio_path).stem
    if not artist:
        artist = "[ARTIST]"
    if not track_name:
        track_name = filename.replace("-", " ").replace("_", " ").title()

    # Build energy/structure map
    structure_rows = ""
    for s in results.get("energy_sections", []):
        structure_rows += (
            f"| {s['bar_start']}-{s['bar_end']} | [TODO: Section name] | "
            f"[TODO: Elements active] | {s['energy_pct']}% | [TODO: Notes] |\n"
        )

    # Build section boundaries note
    boundaries_note = ""
    if results.get("section_boundaries"):
        boundaries_note = "**Detected section boundaries (approximate):** "
        boundary_strs = [f"bar {s['bar']} ({s['time_sec']}s)" for s in results["section_boundaries"]]
        boundaries_note += ", ".join(boundary_strs)

    md = f"""# Reference Analysis: {artist} — {track_name}

> **Auto-generated by librosa_analysis_pipeline.py on {datetime.now().strftime('%Y-%m-%d %H:%M')}**
> Fields marked [TODO] need manual completion by ear.

## Source Info
- **BPM:** {results['bpm']} (librosa estimate — verify with Ableton warp)
- **Key:** {results['key']} (confidence: {results.get('scale_confidence', 'N/A')})
- **Scale:** {results['scale']} (verify by ear — librosa key detection is ~70-80% accurate)
- **Length:** {results['duration_str']} ({results['total_bars']} bars at {results['bpm']} BPM)
- **Year:** [TODO]
- **Subgenre:** [TODO: Goa / Nitzhonot / Psycore / Full-On / etc.]

## Structure Map (bar-by-bar)

{boundaries_note}

| Bar Range | Section | Elements Active | Energy % | Notes |
|-----------|---------|-----------------|----------|-------|
{structure_rows}
## Bassline DNA
- **Pattern type:** [TODO: rolling 16th / acid / walking / pulsing]
- **Root movement:** [TODO: static / follows chords / chromatic walk]
- **Velocity pattern:** [TODO: describe accent pattern]
- **Filter behavior:** [TODO: static / automated sweeps / LFO]
- **Distortion level:** [TODO: clean / warm / aggressive / destroyed]

## Melodic DNA
- **Lead timbre:** [TODO: supersaw / pluck / acid / FM]
- **Phrase length:** [TODO: 4/8/16 bars]
- **Melodic contour:** [TODO: ascending / descending / arch / valley]
- **Note density:** [TODO: sparse whole notes / busy 16ths]
- **Intervals used:** [TODO: stepwise / leaps / arpeggiated]
- **Call-response:** [TODO: yes/no, describe pattern]

## Harmonic DNA
- **Chord progression (main):** [TODO: roman numerals + chords]
- **Chord progression (breakdown):** [TODO: if different]
- **Mode/scale:** {results['key']} {results['scale']} (verify by ear)
- **Harmonic rhythm:** [TODO: how often chords change — every bar / every 2 / every 4]
- **Bass-harmony relationship:** [TODO: root only / root+5th / walking / independent]

## Arrangement DNA
- **Total length:** {results['total_bars']} bars / {results['duration_str']}
- **Number of drops:** [TODO: 1/2/3]
- **Breakdown character:** [TODO: minimal / emotional / atmospheric / aggressive]
- **Transition techniques:** [TODO: filter sweep / snare roll / silence / impact / reverse cymbal]
- **Element introduction style:** [TODO: gradual / sudden / grouped]

## Sound Design DNA
- **Kick character:** [TODO: punchy / sub-heavy / clicky / distorted]
- **Hi-hat style:** [TODO: tight 16ths / open offbeats / shuffled]
- **Pad role:** [TODO: background texture / harmonic foundation / emotional core]
- **FX usage:** [TODO: risers / downlifters / impacts / sweeps — where and how]

## Spectral Profile (Auto-Detected)
- **Average brightness:** {results['avg_brightness_hz']} Hz
- **Brightness range:** {results['min_brightness_hz']} Hz — {results['max_brightness_hz']} Hz
- **Rhythmic density:** ~{results['avg_onsets_per_bar']} onsets/bar average
- **Interpretation:** [TODO: Is this a dark track (low centroid)? Bright and airy (high centroid)?]

## What Makes This Track Special
[TODO: 2-3 sentences on what's unique about this track that Flyin' Colors should learn from]

## DNA to Extract for Flyin' Colors
- [TODO: Specific technique 1 to adapt]
- [TODO: Specific technique 2 to adapt]
- [TODO: Specific technique 3 to adapt]
"""
    return md


def process_single_file(audio_path: str, args: argparse.Namespace) -> bool:
    """Process a single audio file."""
    if not validate_audio_file(audio_path):
        return False

    # Analyze
    results = analyze_track(audio_path, bpm_hint=args.bpm_hint, sample_rate=args.sample_rate)

    if results is None:
        logger.error(f"Analysis failed for: {audio_path}")
        return False

    # Generate markdown
    md = generate_markdown(results, audio_path, artist=args.artist, track_name=args.track_name)

    # Write output
    if args.output:
        output_path = args.output
    else:
        stem = Path(audio_path).stem.lower().replace(" ", "-")
        output_path = f"reference-analysis-{stem}.md"

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md)
        logger.info(f"\n✓ Output written to: {output_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to write output file: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Flyin' Colors — Semi-Automated Reference Track Analysis"
    )
    parser.add_argument("audio_path", nargs='?', help="Path to audio file (WAV, MP3, FLAC, etc.)")
    parser.add_argument("--bpm-hint", type=float, default=None,
                        help="Hint BPM for more accurate tempo detection (e.g., 148)")
    parser.add_argument("--artist", type=str, default="",
                        help="Artist name for the output template")
    parser.add_argument("--track-name", type=str, default="",
                        help="Track name for the output template")
    parser.add_argument("--output", type=str, default=None,
                        help="Output markdown file path (default: auto-generated)")
    parser.add_argument("--sample-rate", type=int, default=22050,
                        help="Sample rate for analysis (default: 22050)")
    parser.add_argument("--batch", type=str, default=None,
                        help="Process all audio files in directory")

    args = parser.parse_args()

    # Batch mode
    if args.batch:
        batch_dir = Path(args.batch)
        if not batch_dir.is_dir():
            logger.error(f"Batch directory not found: {args.batch}")
            sys.exit(1)

        audio_files = []
        for ext in ['.wav', '.mp3', '.flac', '.ogg', '.aiff', '.aif']:
            audio_files.extend(batch_dir.glob(f"*{ext}"))

        if not audio_files:
            logger.error(f"No audio files found in: {args.batch}")
            sys.exit(1)

        logger.info(f"Found {len(audio_files)} audio files to process\n")

        success_count = 0
        for audio_file in audio_files:
            logger.info(f"\n{'='*60}")
            logger.info(f"Processing: {audio_file.name}")
            logger.info('='*60)

            if process_single_file(str(audio_file), args):
                success_count += 1

        logger.info(f"\n{'='*60}")
        logger.info(f"Batch complete: {success_count}/{len(audio_files)} files processed successfully")
        logger.info('='*60)

    # Single file mode
    else:
        if not args.audio_path:
            parser.print_help()
            sys.exit(1)

        if process_single_file(args.audio_path, args):
            logger.info("\nNext steps:")
            logger.info("  1. Verify BPM and key with Ableton (librosa is ~90% accurate on BPM, ~70-80% on key)")
            logger.info("  2. Fill in [TODO] fields by ear")
            logger.info("  3. Move to docs/reference-analysis/")
        else:
            sys.exit(1)


if __name__ == "__main__":
    main()
