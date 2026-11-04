"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    # python -m src.main (from the project root)
    from src.recommender import load_songs, recommend_songs
except ModuleNotFoundError:
    # python src/main.py
    from recommender import load_songs, recommend_songs


# Taste profiles: the targets every song is compared against.
# Keys mirror the UserProfile dataclass, so UserProfile(**prefs) also works.
#   favorite_genre / favorite_mood: exact match earns the genre / mood points
#   target_energy: 0-1; songs closer to this score higher
#   likes_acoustic: True rewards acoustic songs, False rewards non-acoustic ones
PROFILES = {
    "High-Energy Pop": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.85,
        "likes_acoustic": False,
    },
    "Chill Lofi": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.35,
        "likes_acoustic": True,
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.9,
        "likes_acoustic": False,
    },
    "Sad Banger (conflict)": {
        "favorite_genre": "blues",
        "favorite_mood": "sad",
        "target_energy": 0.9,
        "likes_acoustic": False,
    },
    "Case Trap": {
        "favorite_genre": "Pop",
        "favorite_mood": "Happy",
        "target_energy": 0.85,
        "likes_acoustic": False,
    },
    "Acoustic Metalhead": {
        "favorite_genre": "metal",
        "favorite_mood": "angry",
        "target_energy": 0.97,
        "likes_acoustic": True,
    },
    "Out of Range": {
        "favorite_genre": "metal",
        "favorite_mood": "angry",
        "target_energy": 1.8,
        "likes_acoustic": False,
    },
    "Near-Miss Genre": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.76,
        "likes_acoustic": False,
    },
    "Genre Ghost": {
        "favorite_genre": "k-pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
        "likes_acoustic": False,
    },
    "Blank Slate": {
        "favorite_genre": "",
        "favorite_mood": "",
        "target_energy": 0.5,
        "likes_acoustic": False,
    },
}


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for name, user_prefs in PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print_recommendations(name, user_prefs, recommendations)


MAX_SCORE = 6.25  # genre 0.75 + mood 1.0 + energy 4.0 + acoustic 0.5
WIDTH = 60


def print_recommendations(name: str, user_prefs: dict, recommendations: list) -> None:
    """Prints the ranked songs as cards: title, score bar and one reason per line."""
    print()
    print("=" * WIDTH)
    print(f" TOP RECOMMENDATIONS: {name.upper()}".center(WIDTH))
    print(
        f" for: {user_prefs['favorite_genre']} | {user_prefs['favorite_mood']}"
        f" | energy {user_prefs['target_energy']}".center(WIDTH)
    )
    print("=" * WIDTH)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        # Bar of 20 blocks, filled in proportion to the max possible score
        filled = round(20 * score / MAX_SCORE)
        bar = "#" * filled + "." * (20 - filled)

        print()
        print(f" {rank}. {song['title']}  -  {song['artist']}")
        print(f"    {song['genre']} / {song['mood']}")
        print(f"    Score: {score:.2f} / {MAX_SCORE}  [{bar}]")
        print("    Why:")
        for reason in explanation.split("; "):
            print(f"      - {reason}")
        print("-" * WIDTH)


if __name__ == "__main__":
    main()
