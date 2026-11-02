import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Reads the songs CSV into a list of dicts, converting numeric columns to int/float."""
    print(f"Loading songs from {csv_path}...")
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            # csv gives every value as a string; convert the numeric columns
            row["id"] = int(row["id"])
            for key in ("energy", "tempo_bpm", "valence", "danceability", "acousticness"):
                row[key] = float(row[key])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores one song against the user's genre, mood and energy, returning (score, reasons)."""
    # TODO: Implement scoring logic using your Algorithm Recipe from Phase 2.
    # Expected return format: (score, reasons)
    score = 0.0
    reasons = []

    # Weights: genre match = 2.0 points, mood match = 1.0 point,
    # energy closeness = up to 1.5 points (max total 4.5)
    GENRE_POINTS = 2.0
    MOOD_POINTS = 1.0
    ENERGY_POINTS = 1.5

    if song["genre"] == user_prefs.get("favorite_genre"):
        score += GENRE_POINTS
        reasons.append(f"Genre matches favorite (+{GENRE_POINTS})")
    if song["mood"] == user_prefs.get("favorite_mood"):
        score += MOOD_POINTS
        reasons.append(f"Mood matches favorite (+{MOOD_POINTS})")

    # Numerical feature: reward closeness to the target, not higher/lower values.
    # similarity = 1 - |difference| (features are on a 0-1 scale), scaled by weight.
    target_energy = user_prefs.get("target_energy")
    if target_energy is not None:
        similarity = max(0.0, 1.0 - abs(song["energy"] - target_energy))
        energy_score = ENERGY_POINTS * similarity
        score += energy_score
        reasons.append(f"Energy closeness (+{energy_score:.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Scores every song and returns the top k as (song, score, explanation), highest first."""
    # TODO: Implement scoring and ranking logic
    # Expected return format: (song_dict, score, explanation)
    # Pythonic: build the scored list with a comprehension, then use sorted().
    #
    # .sort()  -> method on a list; sorts IN PLACE, mutates that list, returns None.
    #             Use it when you own the list and don't need the original order.
    # sorted() -> built-in function; accepts any iterable, returns a NEW sorted
    #             list and leaves the original untouched.
    #
    # Here `songs` is the caller's data, so sorted() avoids mutating it
    # and lets us sort a generator directly without an intermediate list.
    scored = (
        (song, score, "; ".join(reasons))
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    )
    return sorted(scored, key=lambda item: item[1], reverse=True)[:k]
