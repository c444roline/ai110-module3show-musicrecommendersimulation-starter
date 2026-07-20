# 🎵 Music Recommender Simulation

## Project Summary

<!-- In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does. -->
Real world music streaming platforms work to recommend music to people by using a combination of collaborative and content based filtering in a function that combines the different features available and using different weights to calculate a score and the distance of a particular songs score relative to the users preferences and rank them- recommending the top scoring songs. 

I want to make a recommender that can introduce K-pop to people who do not listen to it already. There are many different features that are collected in musical data. I want my version of the music recommender system to prioritize vibes when recommending music. This is because K-pop is a vast genre with many different sounds and many different songs can appeal to one group of people and not to another. Thus, my version will use a combination of energy, valence, danceability, and mood to calculate a value for each song. These capture what I call a vibe. 

It will  average out values for each of those 4 aforementioned features using the user's preferred songs to get values of users preference. Then it will calculate the inverse distance of songs in the data base to the user's preference-- the closer to user preference, the higher the score. Then, the system will rank the songs by their score and recommend the top few songs. 
---

## How The System Works
Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

---

Each song in the system is described by categorical attributes (genre, mood) and numeric attributes on a 0–1 scale (energy, valence, danceability, acousticness, instrumentalness, lyrical_depth, popularity). Tempo is stored in BPM and normalized to 0–1 before scoring using min-max scaling.

The UserProfile stores a target value for every feature the recommender scores against: a favorite genre, a favorite mood, and numeric targets for each feature (e.g., energy: 0.8, valence: 0.8, danceability: 0.7). These values can be set directly or derived by averaging the features across a set of songs the user already likes.

The recommender uses vibe-based content filtering whch is the idea that if a user enjoys how certain songs feel, they will enjoy other songs that feel similar. First, it normalizes tempo and defines genre/mood similarity clusters so that related categories (e.g., lofi and jazz) receive partial credit rather than a binary match/no-match. Then it scores each song using weighted inverse distance (`1 - |user - song|` for numeric features; cluster-based similarity for categorical features). The vibe features (energy, valence, danceability) carry 60% of the total weight, categorical features (genre, mood) carry 10%, and supporting features (acousticness, tempo, instrumentalness, lyrical_depth, popularity) carry 30%. Finally, it ranks all songs by their total weighted score and recommends the top 5.

Genre similarity clusters: Electronic/Synth (synthwave, EDM, electronic, ambient), Chill/Acoustic (lofi, jazz, acoustic, classical), Pop/Upbeat (pop, indie pop, funk, R&B), Hard/Intense (rock, metal, punk), Rhythmic/Groovy (hip-hop, reggae, Latin). Mood similarity clusters: Positive (happy, energetic, romantic), Low-key (chill, relaxed, focused, dreamy), Dark (moody, melancholic, aggressive, nostalgic), High-intensity (intense, energetic).

Potential Biases: The vibe-heavy weighting (60%) may flatten genre diversity — two songs from completely different genres could score nearly identically if their energy/valence/danceability match. The user profile values cluster between 0.5–0.8, so songs at the extremes will always be penalized even if the user would enjoy them occasionally. The cluster definitions are subjective — which genres count as "similar" is a judgment call that reflects one perspective. Finally, the small catalog (~18 songs) amplifies any bias since a single scoring quirk can shift the entire top-5 list.


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
Loaded songs: 10

============================================================
  Top 5 Recommendations for profile:
  genre=pop, mood=happy, energy=0.8
============================================================

  #1  Sunrise City by Neon Echo
       Score: 0.99
       Why:   energy similarity 98% (+0.65); genre match (+0.17); mood match (+0.17)

  #2  Rooftop Lights by Indigo Parade
       Score: 0.89
       Why:   energy similarity 96% (+0.64); similar genre (+0.08); mood match (+0.17)

  #3  Gym Hero by Max Pulse
       Score: 0.75
       Why:   energy similarity 87% (+0.58); genre match (+0.17)

  #4  Night Drive Loop by Neon Echo
       Score: 0.63
       Why:   energy similarity 95% (+0.63)

  #5  Storm Runner by Voltline
       Score: 0.59
       Why:   energy similarity 89% (+0.59)
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



