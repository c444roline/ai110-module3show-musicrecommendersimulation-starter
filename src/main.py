"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from tabulate import tabulate
from recommender import load_songs, recommend_songs


PROFILES = {
    "Happy Pop Fan": {"genre": "pop", "mood": "happy", "energy": 0.8},
    "Chill Lofi Listener": {"genre": "lofi", "mood": "chill", "energy": 0.35, "valence": 0.6, "danceability": 0.55, "acousticness": 0.8, "tempo_bpm": 75},
    "Intense Rock Enthusiast": {"genre": "rock", "mood": "intense", "energy": 0.92, "valence": 0.45, "danceability": 0.7, "acousticness": 0.1, "tempo_bpm": 145},
    "Conflicted (High Energy + Sad Mood)": {"genre": "pop", "mood": "melancholic", "energy": 0.95, "valence": 0.2, "danceability": 0.85, "acousticness": 0.1, "tempo_bpm": 130},
    "All-Zeros Minimalist": {"genre": "ambient", "mood": "chill", "energy": 0.0, "valence": 0.0, "danceability": 0.0, "acousticness": 1.0, "tempo_bpm": 50},
    "Genre Not In Catalog (K-pop)": {"genre": "k-pop", "mood": "energetic", "energy": 0.85, "valence": 0.9, "danceability": 0.88, "acousticness": 0.15, "tempo_bpm": 125},
}


def run_profile(name, prefs, songs):
    recommendations = recommend_songs(prefs, songs, k=5)

    print(f"\n{'='*90}")
    pref_str = ", ".join(f"{k}={v}" for k, v in prefs.items())
    print(f"  Profile: {name}")
    print(f"  {pref_str}")
    print(f"{'='*90}")

    rows = []
    for rank, (song, score, explanation) in enumerate(recommendations, 1):
        rows.append([
            f"#{rank}",
            song["title"],
            song["artist"],
            f"{score:.2f}",
            explanation,
        ])

    print(tabulate(
        rows,
        headers=["Rank", "Title", "Artist", "Score", "Reasons"],
        tablefmt="grid",
        maxcolwidths=[None, None, None, None, 50],
    ))


def main() -> None:
    import os
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    songs = load_songs(os.path.join(base_dir, "data", "songs.csv"))
    for name, prefs in PROFILES.items():
        run_profile(name, prefs, songs)


if __name__ == "__main__":
    main()
