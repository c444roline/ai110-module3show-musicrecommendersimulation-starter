import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

GENRE_CLUSTERS = {
    "synthwave": "electronic", "EDM": "electronic", "electronic": "electronic", "ambient": "electronic",
    "lofi": "chill", "jazz": "chill", "acoustic": "chill", "classical": "chill",
    "pop": "pop", "indie pop": "pop", "funk": "pop", "R&B": "pop", "k-pop": "pop",
    "rock": "hard", "metal": "hard", "punk": "hard",
    "hip-hop": "rhythmic", "reggae": "rhythmic", "Latin": "rhythmic",
}

MOOD_CLUSTERS = {
    "happy": "positive", "energetic": "positive", "romantic": "positive",
    "chill": "lowkey", "relaxed": "lowkey", "focused": "lowkey", "dreamy": "lowkey",
    "moody": "dark", "melancholic": "dark", "aggressive": "dark", "nostalgic": "dark",
    "intense": "high_intensity",
}

NUMERIC_FIELDS = ["energy", "tempo_bpm", "valence", "danceability", "acousticness",
                  "instrumentalness", "lyrical_depth", "popularity"]

WEIGHTS = {
    "energy": 0.20,
    "valence": 0.20,
    "danceability": 0.20,
    "genre": 0.05,
    "mood": 0.05,
    "acousticness": 0.075,
    "tempo_bpm": 0.075,
    "instrumentalness": 0.05,
    "lyrical_depth": 0.05,
    "popularity": 0.05,
}


@dataclass
class Song:
    """A song with its genre, mood, and numeric audio features."""
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
    """A user's taste profile: preferred genre, mood, energy, and acoustic preference."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """Scores and ranks songs against a UserProfile using vibe-based content filtering."""
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k songs ranked by weighted similarity to the user's preferences."""
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "valence": 0.8,
            "danceability": 0.7,
            "acousticness": 0.8 if user.likes_acoustic else 0.2,
            "tempo_bpm": 120,
        }
        scored = []
        for song in self.songs:
            song_dict = {
                "id": song.id, "title": song.title, "artist": song.artist,
                "genre": song.genre, "mood": song.mood, "energy": song.energy,
                "tempo_bpm": song.tempo_bpm, "valence": song.valence,
                "danceability": song.danceability, "acousticness": song.acousticness,
            }
            score, _ = score_song(user_prefs, song_dict)
            scored.append((song, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return [s for s, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation of why a song was recommended."""
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "valence": 0.8,
            "danceability": 0.7,
            "acousticness": 0.8 if user.likes_acoustic else 0.2,
            "tempo_bpm": 120,
        }
        song_dict = {
            "id": song.id, "title": song.title, "artist": song.artist,
            "genre": song.genre, "mood": song.mood, "energy": song.energy,
            "tempo_bpm": song.tempo_bpm, "valence": song.valence,
            "danceability": song.danceability, "acousticness": song.acousticness,
        }
        score, reasons = score_song(user_prefs, song_dict)
        return f"Score: {score:.2f} — " + "; ".join(reasons)


def _categorical_similarity(value: str, target: str, clusters: Dict[str, str]) -> float:
    """Return 1.0 for exact match, 0.5 for same cluster, 0.0 otherwise."""
    if value.lower() == target.lower():
        return 1.0
    if clusters.get(value) and clusters.get(target) and clusters[value] == clusters[target]:
        return 0.5
    return 0.0


def _normalize_tempo(tempo: float) -> float:
    """Scale a BPM value to the 0–1 range using min-max normalization (50–200 BPM)."""
    min_t, max_t = 50, 200
    return max(0.0, min(1.0, (tempo - min_t) / (max_t - min_t)))


def load_songs(csv_path: str) -> List[Dict]:
    """Read a CSV file and return a list of song dicts with numeric values converted to floats."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            song = {}
            for key, value in row.items():
                if key in NUMERIC_FIELDS:
                    song[key] = float(value)
                elif key == "id":
                    song[key] = int(value)
                else:
                    song[key] = value
            songs.append(song)
    print(f"Loaded songs: {len(songs)}")
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a song against user prefs using weighted inverse distance; return (score, reasons)."""
    total_score = 0.0
    reasons = []
    active_weights = {}

    for feature, weight in WEIGHTS.items():
        if feature in ("genre", "mood"):
            if feature in user_prefs and feature in song:
                active_weights[feature] = weight
        else:
            if feature in user_prefs and feature in song:
                active_weights[feature] = weight

    weight_sum = sum(active_weights.values())
    if weight_sum == 0:
        return 0.0, ["No matching features"]

    normalized_weights = {k: v / weight_sum for k, v in active_weights.items()}

    for feature, weight in normalized_weights.items():
        if feature == "genre":
            sim = _categorical_similarity(song["genre"], user_prefs["genre"], GENRE_CLUSTERS)
            contribution = sim * weight
            total_score += contribution
            if sim == 1.0:
                reasons.append(f"genre match (+{contribution:.2f})")
            elif sim == 0.5:
                reasons.append(f"similar genre (+{contribution:.2f})")
        elif feature == "mood":
            sim = _categorical_similarity(song["mood"], user_prefs["mood"], MOOD_CLUSTERS)
            contribution = sim * weight
            total_score += contribution
            if sim == 1.0:
                reasons.append(f"mood match (+{contribution:.2f})")
            elif sim == 0.5:
                reasons.append(f"similar mood (+{contribution:.2f})")
        else:
            user_val = user_prefs[feature]
            song_val = song[feature]
            if feature == "tempo_bpm":
                user_val = _normalize_tempo(user_val)
                song_val = _normalize_tempo(song_val)
            similarity = 1.0 - abs(user_val - song_val)
            contribution = similarity * weight
            total_score += contribution
            reasons.append(f"{feature} similarity {similarity:.0%} (+{contribution:.2f})")

    return round(total_score, 4), reasons


ARTIST_PENALTY = 0.15
GENRE_PENALTY = 0.10


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Rank songs with diversity penalties for repeated artists/genres in the top-k."""
    scored = sorted(
        ((song, *score_song(user_prefs, song)) for song in songs),
        key=lambda item: item[1],
        reverse=True,
    )

    selected = []
    seen_artists = {}
    seen_genres = {}

    for song, raw_score, reasons in scored:
        if len(selected) >= k:
            break

        penalty = 0.0
        penalty_reasons = []
        artist = song.get("artist", "")
        genre = song.get("genre", "")

        if artist in seen_artists:
            penalty += ARTIST_PENALTY * seen_artists[artist]
            penalty_reasons.append(f"repeat artist x{seen_artists[artist]} (-{ARTIST_PENALTY * seen_artists[artist]:.2f})")

        if genre in seen_genres:
            penalty += GENRE_PENALTY * seen_genres[genre]
            penalty_reasons.append(f"repeat genre x{seen_genres[genre]} (-{GENRE_PENALTY * seen_genres[genre]:.2f})")

        final_score = round(max(0.0, raw_score - penalty), 4)
        all_reasons = list(reasons) + penalty_reasons
        selected.append((song, final_score, "; ".join(all_reasons)))

        seen_artists[artist] = seen_artists.get(artist, 0) + 1
        seen_genres[genre] = seen_genres.get(genre, 0) + 1

    return selected
