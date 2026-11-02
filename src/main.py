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


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Taste profile: the targets every song is compared against.
    # Keys mirror the UserProfile dataclass, so UserProfile(**user_prefs) also works.
    user_prefs = {
        "favorite_genre": "pop",    # exact match earns the genre points
        "favorite_mood": "happy",   # exact match earns the mood points
        "target_energy": 0.8,       # 0-1; songs closer to this score higher
        "likes_acoustic": False,    # True adds a bonus for acousticness > 0.6
        "target_valence": 0.7,       # 0-1; songs closer to this score higher
        "target_danceability": 0.7,  # 0-1; songs closer to this score higher
        "target_tempo_bpm": 120,     # target tempo in beats per minute, songs closer to this score higher
        "target_acousticness": 0.6,  # 0-1; songs closer to this score higher if likes_acoustic is True
        "target_loudness": -5.0,     # target loudness in dB, songs closer to this score higher
        "target_instrumentalness": 0.5, # 0-1; songs closer to this score higher
        "target_liveness": 0.3,       # 0-1; songs closer to this score higher  
        "target_speechiness": 0.1,    # 0-1; songs closer to this score higher
        "target_key": 0,               # 0-11; songs closer to this key score higher
        "target_mode": 1,              # 0 for minor, 1 for major; songs closer to this mode score higher
        "target_duration_ms": 180000,  # target duration in milliseconds, songs closer to this score higher
        "target_popularity": 50,       # 0-100; songs closer to this score higher
        "target_familiarity": 0.5,      # 0-1; songs closer to this score higher
        "target_energy": 0.8            # 0-1; songs closer to this score higher
        
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print_recommendations(user_prefs, recommendations)


MAX_SCORE = 4.5  # genre 2.0 + mood 1.0 + energy 1.5
WIDTH = 60


def print_recommendations(user_prefs: dict, recommendations: list) -> None:
    """Prints the ranked songs as cards: title, score bar and one reason per line."""
    print()
    print("=" * WIDTH)
    print(" TOP RECOMMENDATIONS".center(WIDTH))
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
