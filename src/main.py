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

    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print(f"\n{'='*60}")
    print(f"  Top {len(recommendations)} Recommendations for profile:")
    print(f"  genre={user_prefs['genre']}, mood={user_prefs['mood']}, energy={user_prefs['energy']}")
    print(f"{'='*60}\n")

    for rank, (song, score, explanation) in enumerate(recommendations, 1):
        print(f"  #{rank}  {song['title']} by {song['artist']}")
        print(f"       Score: {score:.2f}")
        print(f"       Why:   {explanation}")
        print()


if __name__ == "__main__":
    main()
