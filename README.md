# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

This is a **content-based** recommender: it compares each song's attributes to a user's stated taste. It doesn't use other listeners' behavior.

```text
songs.csv ──► load songs ──► score each song ──► sort by score ──► top k + reasons
                                   ▲
                     user profile ─┘
```

### Song features

Each `Song` stores `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability` and `acousticness`. The score uses four of them:

| Feature | Type | How it's used |
| --- | --- | --- |
| `genre` | Category | Exact match with the user's favorite genre |
| `mood` | Category | Exact match with the user's favorite mood |
| `energy` | Number (0–1) | How close it is to the user's target energy |
| `acousticness` | Number (0–1) | Bonus if the user likes acoustic music |

`tempo_bpm` and `danceability` are left out on purpose. In this catalog they are very strongly correlated with energy (0.96 and 0.86), so scoring them too would count the same "calm vs. intense" signal several times. `valence` is not used in the score for now; adding it is a possible experiment.

### User profile

A `UserProfile` stores:

- `favorite_genre` (e.g. `"pop"`)
- `favorite_mood` (e.g. `"happy"`)
- `target_energy`, a number from 0 to 1 (e.g. `0.8`)
- `likes_acoustic`, true or false

### Scoring rule (one song)

Each song gets points for how well it matches the profile:

| Component | Points |
| --- | --- |
| Genre matches | +2.0 |
| Mood matches | +1.0 |
| Energy closeness | +1.0 × `exp(-(energy - target)² / (2 × 0.15²))` |
| Likes acoustic and `acousticness` > 0.6 | +0.5 |

The maximum score is 4.5. Energy closeness uses a bell curve, so it rewards songs **near** the target energy, not just songs with higher or lower energy. A song within about 0.05 of the target earns almost the full point, and a song 0.4 or more away earns close to nothing. Genre has the highest weight because it is the broadest signal of taste; mood and energy refine the choice within it.

Each component that adds points also adds a reason (e.g. "matches your favorite genre (pop)"), and these reasons become the explanation shown with the recommendation.

Implementation details:

- Genre and mood matches are exact, case-insensitive and ignore surrounding spaces (`"Pop "` matches `"pop"`). There is no partial credit, so `indie pop` does not match `pop`.
- The energy curve uses a width (σ) of 0.15. Energy always earns some points, so it is the only reason given for songs that match neither genre nor mood.
- The acoustic bonus needs `acousticness` strictly above 0.6, and only applies when `likes_acoustic` is true.
- Scores are rounded to 2 decimals only for display; ranking uses the unrounded score.

Why these weights hold up on this catalog:

- A genre-only match (2.0 + energy) always beats a mood-only match, even one with perfect energy (1.0 + 1.0). But a song outside the user's genre can still fill the list once same-genre songs run out, so genre is the strongest signal without acting as a hard filter.
- Energy can add at most 1.0, so it never outweighs a categorical match; it orders songs within the same match level.
- The acoustic bonus (0.5) is the smallest weight, so it nudges ties rather than overriding taste.

### Ranking rule (the list)

1. Score every song in the catalog.
2. Sort from highest score to lowest. Ties are broken by song title (A–Z) so the order is always the same.
3. Return the top `k` songs (5 by default), each with its score and explanation.

For example, for a user who likes pop, happy and energy 0.8, *Sunrise City* ranks first (pop + happy + energy 0.82, about 3.99 points), followed by *Gym Hero* (pop, but intense mood, about 2.69 points).

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

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

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



