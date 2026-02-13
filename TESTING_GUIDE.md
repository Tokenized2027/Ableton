# Flyin' Colors MCP - Testing Guide

**Test these commands in Claude Desktop after setup is complete.**

---

## Prerequisites ✅

Before testing, verify:
- [ ] UV installed (`uv --version`)
- [ ] Ableton remote script installed
- [ ] AbletonMCP selected in Ableton Preferences
- [ ] Ableton is running
- [ ] Claude Desktop configured with MCP server
- [ ] Claude Desktop restarted

---

## Test 1: Connection Test (5 seconds)

**In Claude Desktop, say:**
```
What tracks are currently in my Ableton session?
```

**Expected Result:**
Claude responds with track information from your Ableton session.

**If it fails:**
- Check Ableton is running
- Check AbletonMCP is selected in Preferences
- Restart Ableton + Claude Desktop

---

## Test 2: Command 1 - create_flyin_colors_session (30 seconds)

**In Claude Desktop, say:**
```
Create a new Flyin' Colors session at 148 BPM in D minor called "FC_Test_01"
```

**Expected Result:**
In Ableton, you should see:
- ✅ 11 tracks created:
  1. FC_Kick (MIDI)
  2. FC_Hats (MIDI)
  3. FC_Perc (MIDI)
  4. FC_Sub (MIDI)
  5. FC_RollingBass (MIDI)
  6. FC_Lead (MIDI)
  7. FC_Pad (MIDI)
  8. FC_Arp (MIDI)
  9. FC_FX (Audio)
  10. FC_Vocal (Audio)
  11. FC_Reference (Audio, muted)

- ✅ 4 return tracks:
  - FC_Reverb_Short
  - FC_Reverb_Long
  - FC_Delay
  - FC_Distortion

- ✅ Tempo set to 148 BPM
- ✅ Locator at bar 1: "FC_Test_01 - Dm - 148BPM"

**If return tracks fail:**
This is expected if `create_return_track` isn't fully supported. Tracks and tempo should still work.

**Success criteria:** At minimum, 11 tracks created + tempo set to 148.

---

## Test 3: Command 2 - generate_rolling_bass (15 seconds)

**In Claude Desktop, say:**
```
Generate a rolling bass pattern on track 5 (FC_RollingBass):
- Key: D minor
- 4 bars
- Rolling 16th pattern
- Chord progression: i, bVI, bVII, i
```

**Expected Result:**
In Ableton:
- ✅ MIDI clip appears on track 5 (FC_RollingBass), slot 1
- ✅ Clip name: "FC_Bass_Dm_rolling_16th"
- ✅ Clip length: 4 bars
- ✅ 64 notes visible in MIDI editor (16 per bar)
- ✅ Notes change each bar (D → Bb → C → D)
- ✅ Velocity pattern visible (accent on 1st and 3rd 16ths)

**Open the MIDI clip and verify:**
- Bar 1: D2 (MIDI 38) repeating
- Bar 2: Bb1 (MIDI 34) repeating
- Bar 3: C2 (MIDI 36) repeating
- Bar 4: D2 (MIDI 38) repeating

**Success criteria:** 64 notes, 4 bars, correct pitches.

---

## Test 4: Pattern Types (1 minute)

Test each pattern type to verify variety:

**4a. Pulsing 8th (Nitzhonot style):**
```
Generate a pulsing 8th bass pattern on track 5, key Dm, 4 bars
```
- Expected: Alternating root and octave (D2, D3, D2, D3...)
- 32 notes total (8 per bar)

**4b. Syncopated (groovy):**
```
Generate a syncopated bass pattern on track 5, key Dm, 4 bars
```
- Expected: Accents on off-beats, gaps on downbeats
- ~48 notes (skips every 4th)

**4c. Gallop (nu-metal):**
```
Generate a gallop bass pattern on track 5, key Dm, 4 bars
```
- Expected: 16-16-8th rhythm, aggressive feel
- 48 notes total (3 per beat × 4 beats × 4 bars)

---

## Test 5: Chord Progressions (30 seconds)

**Test complex progression:**
```
Generate a rolling bass on track 5:
- Key: A minor
- 8 bars
- Chord progression: i, iv, bVI, V
- 2 bars per chord
```

**Expected Result:**
- 8-bar clip (128 notes)
- Bars 1-2: A minor (A2)
- Bars 3-4: D minor (D2)
- Bars 5-6: F major (F2)
- Bars 7-8: E major (E2)

**Verify by ear:** Chord changes every 2 bars.

---

## Test 6: Integration Test - Full Workflow (2 minutes)

**Complete production start:**

```
1. Create a Flyin' Colors session at 148 BPM in D minor
2. Generate a rolling bass on the FC_RollingBass track with progression i-bVI-bVII-i over 4 bars
3. What's the current session state?
```

**Expected Result:**
- 11 tracks created
- Rolling bass clip on track 5
- Claude reports back session info

**Play the session:**
- Press spacebar in Ableton
- Trigger the bass clip (click on it in session view)
- You should hear the rolling D minor bass pattern

**Success criteria:** Music plays, sounds like a Flyin' Colors rolling bass.

---

## Test 7: Different Keys and Scales (1 minute)

**Test Phrygian Dominant (Goa/Nitzhonot):**
```
Generate a rolling bass on track 5:
- Key: E
- Scale: phrygian_dominant
- 4 bars
- Rolling 16th pattern
```

**Expected Result:**
- E Phrygian Dominant scale notes (E, F, G#, A, B, C, D)
- Sounds exotic, Middle Eastern flavor

**Test Harmonic Minor:**
```
Generate a rolling bass on track 5:
- Key: D
- Scale: harmonic_minor
- 4 bars
```

**Expected Result:**
- D Harmonic Minor (D, E, F, G, A, Bb, C#)
- Darker, classical minor feel

---

## Test 8: Edge Cases (30 seconds)

**Test minimal:**
```
Create a Flyin' Colors session with section type "minimal"
```
- Expected: Only 4 tracks (kick, sub, rolling bass, lead)

**Test jam:**
```
Create a Flyin' Colors session with section type "jam"
```
- Expected: Only 3 tracks (kick, hats, rolling bass)

**Test long pattern:**
```
Generate a rolling bass on track 5, 16 bars, key Dm
```
- Expected: 256 notes (16 bars × 16 notes per bar)
- Might take a few seconds to generate

---

## Troubleshooting

### "Can't connect to Ableton"
- Is Ableton running?
- Is AbletonMCP selected in Preferences?
- Restart Ableton

### "Track index out of range"
- Run `create_flyin_colors_session` first to create tracks
- Or use a track index that exists (0 = first track)

### "Notes not appearing"
- Check you're looking at the right clip slot
- Check track isn't muted
- Try opening the MIDI clip (double-click)

### "Wrong pitches"
- Verify key parameter (case-sensitive: "D" not "d")
- Check chord progression spelling (lowercase "i", uppercase "V")
- Open MIDI editor and check actual note numbers

### "Pattern sounds weird"
- Try different pattern_type
- Check velocity_pattern isn't too extreme
- Verify scale is correct for the genre

---

## Success Metrics

### Minimum Viable (Commands Work)
- ✅ Connection test passes
- ✅ Command 1 creates tracks
- ✅ Command 2 generates bass notes

### Full Success (Production Ready)
- ✅ All pattern types work
- ✅ Return tracks created
- ✅ Locator created
- ✅ Multiple keys/scales work
- ✅ Chord progressions sound correct
- ✅ Can start producing immediately

---

## Next Commands to Test (When Implemented)

**Command 3:** set_section_markers
**Command 4:** export_session_state

*Update this guide as more commands are implemented.*

---

**Test completed? Celebrate!** 🎯

**Current automation:** ~5-10 min saved per session (Commands 1-2)
**Future potential:** 35-40 min saved per session (when Commands 3-12 are implemented)
