# 🎵 Music Recommender Simulation

## Project Summary

**TuneJudge 1.0** is a small command-line music recommender. You give it a taste profile: a favorite genre, a favorite mood, a target energy level, and whether you like acoustic music. It scores all 20 songs in the catalog, ranks them, and prints the top 5, with the reasons each song earned its points.

I tested it with 10 listener profiles, including 7 tricky ones built to break it. I tried three different sets of weights and measured which songs get shown most often. The results showed that the scoring works well for common tastes. They also showed that it leans heavily on energy, and that the small catalog limits what it can recommend. The details are in the [model card](model_card.md).

---

## How The System Works

This is a **content-based** recommender: it compares each song's attributes to a user's stated taste. It doesn't use other listeners' behavior.

```text
songs.csv ──► load songs ──► score each song ──► sort by score ──► top k + reasons
                                   ▲
                     user profile ─┘
```

### Song features

Each song has `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability` and `acousticness`. The score uses four of them:

| Feature | Type | How it's used |
| --- | --- | --- |
| `genre` | Category | Exact match with the user's favorite genre |
| `mood` | Category | Exact match with the user's favorite mood |
| `energy` | Number (0–1) | How close it is to the user's target energy |
| `acousticness` | Number (0–1) | How well it fits the user's acoustic preference |

`tempo_bpm` and `danceability` are left out on purpose. In this catalog they rise and fall with energy (correlations of 0.88 and 0.68), so scoring them would count the same "calm vs. intense" signal more than once. `valence` isn't used yet.

### User profile

A profile is a dictionary with:

- `favorite_genre` (e.g. `"pop"`)
- `favorite_mood` (e.g. `"happy"`)
- `target_energy`, a number from 0 to 1 (e.g. `0.8`)
- `likes_acoustic`, `True` or `False`

### Scoring rule (one song)

| Component | Points |
| --- | --- |
| Genre matches | +0.75 |
| Mood matches | +1.0 |
| Energy closeness | +4.0 × (1 − \|energy − target\|)² |
| Acoustic fit | +0.5 × `acousticness` if `likes_acoustic`, else +0.5 × (1 − `acousticness`) |

The maximum score is **6.25**.

- **Energy rewards closeness:** songs are scored on how near they are to the target, not on being louder or quieter. Squaring the closeness makes big misses cost much more than small ones. A song 0.1 away earns 3.24 points, while a song 0.5 away earns only 1.0.
- **Matching is exact:** genre and mood must be the same text. Matching is case-sensitive, and there is no partial credit, so `"Pop"` doesn't match `"pop"` and `indie pop` doesn't match `pop`.
- **Explanations:** every component that adds points also adds a reason, such as "Genre matches favorite (+0.75)". The CLI prints these under each song.

### Ranking rule (the list)

1. Score every song in the catalog.
2. Sort from highest score to lowest. Python's `sorted()` is stable, so ties keep their order from the CSV.
3. Return the top `k` songs (5 by default), each with its score and explanation.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   python -m src.main
   ```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Output of `python -m src.main` (top 5 per profile, current weights).

### High-Energy Pop

```text
============================================================
            TOP RECOMMENDATIONS: HIGH-ENERGY POP
               for: pop | happy | energy 0.85
============================================================

 1. Sunrise City  -  Neon Echo
    pop / happy
    Score: 5.92 / 6.25  [###################.]
    Why:
      - Genre matches favorite (+0.75)
      - Mood matches favorite (+1.0)
      - Energy closeness (+3.76)
      - Acoustic fit (+0.41)
------------------------------------------------------------

 2. Rooftop Lights  -  Indigo Parade
    indie pop / happy
    Score: 4.64 / 6.25  [###############.....]
    Why:
      - Mood matches favorite (+1.0)
      - Energy closeness (+3.31)
      - Acoustic fit (+0.33)
------------------------------------------------------------

 3. Gym Hero  -  Max Pulse
    pop / intense
    Score: 4.61 / 6.25  [###############.....]
    Why:
      - Genre matches favorite (+0.75)
      - Energy closeness (+3.39)
      - Acoustic fit (+0.47)
------------------------------------------------------------

 4. Storm Runner  -  Voltline
    rock / intense
    Score: 3.98 / 6.25  [#############.......]
    Why:
      - Energy closeness (+3.53)
      - Acoustic fit (+0.45)
------------------------------------------------------------

 5. Barn Burner  -  The Hollow Pines
    folk / energetic
    Score: 3.98 / 6.25  [#############.......]
    Why:
      - Energy closeness (+3.92)
      - Acoustic fit (+0.06)
------------------------------------------------------------
```

### Chill Lofi

```text
============================================================
               TOP RECOMMENDATIONS: CHILL LOFI
               for: lofi | chill | energy 0.35
============================================================

 1. Library Rain  -  Paper Lanterns
    lofi / chill
    Score: 6.18 / 6.25  [####################]
    Why:
      - Genre matches favorite (+0.75)
      - Mood matches favorite (+1.0)
      - Energy closeness (+4.00)
      - Acoustic fit (+0.43)
------------------------------------------------------------

 2. Midnight Coding  -  LoRoom
    lofi / chill
    Score: 5.56 / 6.25  [##################..]
    Why:
      - Genre matches favorite (+0.75)
      - Mood matches favorite (+1.0)
      - Energy closeness (+3.46)
      - Acoustic fit (+0.35)
------------------------------------------------------------

 3. Spacewalk Thoughts  -  Orbit Bloom
    ambient / chill
    Score: 4.92 / 6.25  [################....]
    Why:
      - Mood matches favorite (+1.0)
      - Energy closeness (+3.46)
      - Acoustic fit (+0.46)
------------------------------------------------------------

 4. Focus Flow  -  LoRoom
    lofi / focused
    Score: 4.75 / 6.25  [###############.....]
    Why:
      - Genre matches favorite (+0.75)
      - Energy closeness (+3.61)
      - Acoustic fit (+0.39)
------------------------------------------------------------

 5. Coffee Shop Stories  -  Slow Stereo
    jazz / relaxed
    Score: 4.29 / 6.25  [##############......]
    Why:
      - Energy closeness (+3.84)
      - Acoustic fit (+0.45)
------------------------------------------------------------
```

### Deep Intense Rock

```text
============================================================
           TOP RECOMMENDATIONS: DEEP INTENSE ROCK
              for: rock | intense | energy 0.9
============================================================

 1. Storm Runner  -  Voltline
    rock / intense
    Score: 6.12 / 6.25  [####################]
    Why:
      - Genre matches favorite (+0.75)
      - Mood matches favorite (+1.0)
      - Energy closeness (+3.92)
      - Acoustic fit (+0.45)
------------------------------------------------------------

 2. Gym Hero  -  Max Pulse
    pop / intense
    Score: 5.24 / 6.25  [#################...]
    Why:
      - Mood matches favorite (+1.0)
      - Energy closeness (+3.76)
      - Acoustic fit (+0.47)
------------------------------------------------------------

 3. Bassline Fever  -  Kilowatt Kids
    edm / euphoric
    Score: 4.10 / 6.25  [#############.......]
    Why:
      - Energy closeness (+3.61)
      - Acoustic fit (+0.49)
------------------------------------------------------------

 4. Iron Collapse  -  Grave Engine
    metal / angry
    Score: 3.94 / 6.25  [#############.......]
    Why:
      - Energy closeness (+3.46)
      - Acoustic fit (+0.48)
------------------------------------------------------------

 5. Sunrise City  -  Neon Echo
    pop / happy
    Score: 3.80 / 6.25  [############........]
    Why:
      - Energy closeness (+3.39)
      - Acoustic fit (+0.41)
------------------------------------------------------------
```

### Sad Banger (conflict)

```text
============================================================
         TOP RECOMMENDATIONS: SAD BANGER (CONFLICT)
                for: blues | sad | energy 0.9
============================================================

 1. Storm Runner  -  Voltline
    rock / intense
    Score: 4.37 / 6.25  [##############......]
    Why:
      - Energy closeness (+3.92)
      - Acoustic fit (+0.45)
------------------------------------------------------------

 2. Gym Hero  -  Max Pulse
    pop / intense
    Score: 4.24 / 6.25  [##############......]
    Why:
      - Energy closeness (+3.76)
      - Acoustic fit (+0.47)
------------------------------------------------------------

 3. Bassline Fever  -  Kilowatt Kids
    edm / euphoric
    Score: 4.10 / 6.25  [#############.......]
    Why:
      - Energy closeness (+3.61)
      - Acoustic fit (+0.49)
------------------------------------------------------------

 4. Iron Collapse  -  Grave Engine
    metal / angry
    Score: 3.94 / 6.25  [#############.......]
    Why:
      - Energy closeness (+3.46)
      - Acoustic fit (+0.48)
------------------------------------------------------------

 5. Sunrise City  -  Neon Echo
    pop / happy
    Score: 3.80 / 6.25  [############........]
    Why:
      - Energy closeness (+3.39)
      - Acoustic fit (+0.41)
------------------------------------------------------------
```

### Case Trap

```text
============================================================
               TOP RECOMMENDATIONS: CASE TRAP
               for: Pop | Happy | energy 0.85
============================================================

 1. Sunrise City  -  Neon Echo
    pop / happy
    Score: 4.17 / 6.25  [#############.......]
    Why:
      - Energy closeness (+3.76)
      - Acoustic fit (+0.41)
------------------------------------------------------------

 2. Storm Runner  -  Voltline
    rock / intense
    Score: 3.98 / 6.25  [#############.......]
    Why:
      - Energy closeness (+3.53)
      - Acoustic fit (+0.45)
------------------------------------------------------------

 3. Barn Burner  -  The Hollow Pines
    folk / energetic
    Score: 3.98 / 6.25  [#############.......]
    Why:
      - Energy closeness (+3.92)
      - Acoustic fit (+0.06)
------------------------------------------------------------

 4. Concrete Verses  -  Block Theory
    hip-hop / confident
    Score: 3.90 / 6.25  [############........]
    Why:
      - Energy closeness (+3.46)
      - Acoustic fit (+0.44)
------------------------------------------------------------

 5. Gym Hero  -  Max Pulse
    pop / intense
    Score: 3.86 / 6.25  [############........]
    Why:
      - Energy closeness (+3.39)
      - Acoustic fit (+0.47)
------------------------------------------------------------
```

### Acoustic Metalhead

```text
============================================================
           TOP RECOMMENDATIONS: ACOUSTIC METALHEAD
              for: metal | angry | energy 0.97
============================================================

 1. Iron Collapse  -  Grave Engine
    metal / angry
    Score: 5.76 / 6.25  [##################..]
    Why:
      - Genre matches favorite (+0.75)
      - Mood matches favorite (+1.0)
      - Energy closeness (+4.00)
      - Acoustic fit (+0.01)
------------------------------------------------------------

 2. Bassline Fever  -  Kilowatt Kids
    edm / euphoric
    Score: 3.85 / 6.25  [############........]
    Why:
      - Energy closeness (+3.84)
      - Acoustic fit (+0.01)
------------------------------------------------------------

 3. Gym Hero  -  Max Pulse
    pop / intense
    Score: 3.71 / 6.25  [############........]
    Why:
      - Energy closeness (+3.69)
      - Acoustic fit (+0.03)
------------------------------------------------------------

 4. Storm Runner  -  Voltline
    rock / intense
    Score: 3.58 / 6.25  [###########.........]
    Why:
      - Energy closeness (+3.53)
      - Acoustic fit (+0.05)
------------------------------------------------------------

 5. Barn Burner  -  The Hollow Pines
    folk / energetic
    Score: 3.47 / 6.25  [###########.........]
    Why:
      - Energy closeness (+3.03)
      - Acoustic fit (+0.44)
------------------------------------------------------------
```

### Out of Range

```text
============================================================
              TOP RECOMMENDATIONS: OUT OF RANGE
               for: metal | angry | energy 1.8
============================================================

 1. Iron Collapse  -  Grave Engine
    metal / angry
    Score: 2.35 / 6.25  [########............]
    Why:
      - Genre matches favorite (+0.75)
      - Mood matches favorite (+1.0)
      - Energy closeness (+0.12)
      - Acoustic fit (+0.48)
------------------------------------------------------------

 2. Bassline Fever  -  Kilowatt Kids
    edm / euphoric
    Score: 0.58 / 6.25  [##..................]
    Why:
      - Energy closeness (+0.09)
      - Acoustic fit (+0.49)
------------------------------------------------------------

 3. Gym Hero  -  Max Pulse
    pop / intense
    Score: 0.54 / 6.25  [##..................]
    Why:
      - Energy closeness (+0.07)
      - Acoustic fit (+0.47)
------------------------------------------------------------

 4. Storm Runner  -  Voltline
    rock / intense
    Score: 0.50 / 6.25  [##..................]
    Why:
      - Energy closeness (+0.05)
      - Acoustic fit (+0.45)
------------------------------------------------------------

 5. Concrete Verses  -  Block Theory
    hip-hop / confident
    Score: 0.44 / 6.25  [#...................]
    Why:
      - Energy closeness (+0.00)
      - Acoustic fit (+0.44)
------------------------------------------------------------
```

### Near-Miss Genre

```text
============================================================
            TOP RECOMMENDATIONS: NEAR-MISS GENRE
               for: pop | happy | energy 0.76
============================================================

 1. Sunrise City  -  Neon Echo
    pop / happy
    Score: 5.69 / 6.25  [##################..]
    Why:
      - Genre matches favorite (+0.75)
      - Mood matches favorite (+1.0)
      - Energy closeness (+3.53)
      - Acoustic fit (+0.41)
------------------------------------------------------------

 2. Rooftop Lights  -  Indigo Parade
    indie pop / happy
    Score: 5.33 / 6.25  [#################...]
    Why:
      - Mood matches favorite (+1.0)
      - Energy closeness (+4.00)
      - Acoustic fit (+0.33)
------------------------------------------------------------

 3. Night Drive Loop  -  Neon Echo
    synthwave / moody
    Score: 4.31 / 6.25  [##############......]
    Why:
      - Energy closeness (+3.92)
      - Acoustic fit (+0.39)
------------------------------------------------------------

 4. Concrete Verses  -  Block Theory
    hip-hop / confident
    Score: 4.28 / 6.25  [##############......]
    Why:
      - Energy closeness (+3.84)
      - Acoustic fit (+0.44)
------------------------------------------------------------

 5. Fuego Lento  -  Sol y Sombra
    reggaeton / playful
    Score: 4.11 / 6.25  [#############.......]
    Why:
      - Energy closeness (+3.69)
      - Acoustic fit (+0.42)
------------------------------------------------------------
```

### Genre Ghost

```text
============================================================
              TOP RECOMMENDATIONS: GENRE GHOST
               for: k-pop | happy | energy 0.8
============================================================

 1. Sunrise City  -  Neon Echo
    pop / happy
    Score: 5.25 / 6.25  [#################...]
    Why:
      - Mood matches favorite (+1.0)
      - Energy closeness (+3.84)
      - Acoustic fit (+0.41)
------------------------------------------------------------

 2. Rooftop Lights  -  Indigo Parade
    indie pop / happy
    Score: 5.01 / 6.25  [################....]
    Why:
      - Mood matches favorite (+1.0)
      - Energy closeness (+3.69)
      - Acoustic fit (+0.33)
------------------------------------------------------------

 3. Concrete Verses  -  Block Theory
    hip-hop / confident
    Score: 4.28 / 6.25  [##############......]
    Why:
      - Energy closeness (+3.84)
      - Acoustic fit (+0.44)
------------------------------------------------------------

 4. Night Drive Loop  -  Neon Echo
    synthwave / moody
    Score: 4.00 / 6.25  [#############.......]
    Why:
      - Energy closeness (+3.61)
      - Acoustic fit (+0.39)
------------------------------------------------------------

 5. Fuego Lento  -  Sol y Sombra
    reggaeton / playful
    Score: 3.81 / 6.25  [############........]
    Why:
      - Energy closeness (+3.39)
      - Acoustic fit (+0.42)
------------------------------------------------------------
```

### Blank Slate

```text
============================================================
              TOP RECOMMENDATIONS: BLANK SLATE
                    for:  |  | energy 0.5
============================================================

 1. Velvet Hours  -  Amara Lane
    r&b / romantic
    Score: 4.15 / 6.25  [#############.......]
    Why:
      - Energy closeness (+3.84)
      - Acoustic fit (+0.31)
------------------------------------------------------------

 2. Dusty Backroads  -  Willow Creek
    country / nostalgic
    Score: 3.74 / 6.25  [############........]
    Why:
      - Energy closeness (+3.61)
      - Acoustic fit (+0.13)
------------------------------------------------------------

 3. Midnight Coding  -  LoRoom
    lofi / chill
    Score: 3.53 / 6.25  [###########.........]
    Why:
      - Energy closeness (+3.39)
      - Acoustic fit (+0.15)
------------------------------------------------------------

 4. Harbor Sunshine  -  Roots Harbor
    reggae / uplifting
    Score: 3.52 / 6.25  [###########.........]
    Why:
      - Energy closeness (+3.24)
      - Acoustic fit (+0.28)
------------------------------------------------------------

 5. Focus Flow  -  LoRoom
    lofi / focused
    Score: 3.35 / 6.25  [###########.........]
    Why:
      - Energy closeness (+3.24)
      - Acoustic fit (+0.11)
------------------------------------------------------------
```

---

## Experiments You Tried

### 1. Edge-case profiles

I added 7 tricky profiles to `src/main.py` to see if the scoring could be fooled:

| Profile | What it tests | What happened |
| --- | --- | --- |
| Sad Banger | Sad mood but energy 0.9 | No song is both sad and loud. The list is all loud songs, and the mood is dropped |
| Case Trap | `"Pop"` / `"Happy"` with capitals | Genre and mood points vanish, because matching is case-sensitive |
| Acoustic Metalhead | Metal, but likes acoustic | Iron Collapse still wins. Every loud song is electric, so the acoustic setting barely matters |
| Out of Range | Energy 1.8 (the scale ends at 1) | Not caught. Energy points drop to near 0 for every song |
| Near-Miss Genre | Does "indie pop" count as "pop"? | No. Rooftop Lights gets no genre credit |
| Genre Ghost | `"k-pop"`, which isn't in the catalog | Falls back sensibly to happy songs at the right energy |
| Blank Slate | No genre or mood | Ranks purely by energy closeness |

### 2. Weight changes

I ran all 10 profiles under three weight settings:

| Version | Genre | Mood | Energy | Acoustic | Max |
| --- | --- | --- | --- | --- | --- |
| v1 (first working version) | 2.0 | 1.0 | 1.5 × closeness | none | 4.5 |
| v2 | 1.5 | 1.0 | 2.0 × closeness² | 0.5 | 5.0 |
| v3 (current) | 0.75 | 1.0 | 4.0 × closeness² | 0.5 | 6.25 |

- **v1:** genre and mood decided almost everything. Energy barely separated songs, since every song in a top 5 earned 1.36–1.5 of its 1.5 points. Barn Burner, an acoustic folk song, showed up in 7 top-5 lists, including rock and pop.
- **Lowering genre from 2.0 to 0.5 in v1** didn't change the #1 song for any profile. Only ranks 2–3 moved. The #1 song is usually the only song matching both genre and mood, so it wins at any weight.
- **v2:** acoustic scoring removed Barn Burner from the rock and pop lists. Squaring the energy closeness spread the scores out, so energy actually ranked songs.
- **v3:** doubling energy and halving genre helped a little. Rooftop Lights (happy, exact energy) now beats Gym Hero (pop, wrong mood). It also made some results worse. Sad Banger's #1 flipped from the one sad song to a loud rock song, and Barn Burner came back into the Case Trap list.

**Verdict:** the v3 change made the lists mostly *different*, not clearly *more accurate*. The real gains came from v2.

### 3. Exposure test

I scored 5,000 random listeners and counted how often each song appeared in a top 5. If every song were shown equally, each would appear about 1,250 times. Library Rain, a quiet song in the crowded 0.28–0.48 energy range, appeared 2,330 times. Iron Collapse, at the loud edge of the scale, appeared only 559 times.

---

## Limitations and Risks

- **Tiny catalog:** there are only 20 songs, and most genres and moods appear once. After the one best match, the rest of the list is often filler picked by energy.
- **Energy dominates:** energy is worth up to 4 points, but a perfect genre and mood match is worth only 1.75. Once your genre's songs are more than about 0.25 away from your energy target, an unrelated genre wins.
- **Mood is tied to energy in the data:** every sad or chill song is quiet, and every intense or angry song is loud. Listeners with mixed tastes, like energetic sad music, can't be served.
- **Uneven exposure:** quiet songs in the crowded energy range get shown about twice as often as loud songs at the edges.
- **Fragile matching:** matching is case-sensitive, there's no partial credit for related genres, and inputs aren't validated.
- **No real understanding of music:** it doesn't know about lyrics, language, artists, or what the listener has played before.

More detail is in the [model card](model_card.md).

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Building this showed me that a recommender is just a set of choices about what counts. The "prediction" is only adding up points, so the weights *are* the system's opinion about what matters. Changing one number reshuffled the lists. But it didn't change the top pick, because that was decided by which songs existed in the catalog. A list can look confident and come with clear reasons, yet still be filler when there's nothing good to recommend.

Bias showed up in places I didn't expect. Nobody wrote "prefer quiet songs," but quiet songs were shown about twice as often, because more of them are bunched together at similar energy levels. The data also tied mood to energy, so a listener who wanted something outside those patterns was quietly ignored. In a real app with millions of songs, the same effects could decide which artists get heard. They could also push users into a filter bubble without anyone choosing that on purpose.
