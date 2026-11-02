"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Taste profile: the targets every song is compared against.
    # Keys mirror the UserProfile dataclass, so UserProfile(**user_prefs) also works.
    user_prefs = {
        "favorite_genre": "pop",    # exact match earns the genre points
        "favorite_mood": "happy",   # exact match earns the mood points
        "target_energy": 0.8,       # 0-1; songs closer to this score higher
        "likes_acoustic": False,    # True adds a bonus for acousticness > 0.6
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for rec in recommendations:
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


if __name__ == "__main__":
    main()
