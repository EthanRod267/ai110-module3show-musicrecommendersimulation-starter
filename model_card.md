# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**TuneJudge 1.0**

It works like a judge. It hands out points to every song and picks the winners.

---

## 2. Goal and Intended Use  

### Goal / Task

TuneJudge suggests 5 songs for one listener. You tell it your favorite genre, your favorite mood, how much energy you want, and whether you like acoustic music. It scores every song and shows the 5 best fits. It also explains why each song was picked.

### Intended use

- Classroom practice for learning how recommenders work.
- Testing how scoring rules and weights change the results.
- Small, made-up listener profiles.

### Not intended for

- Real music apps or real users. The catalog has only 20 songs.
- Judging what music is "good." It only measures fit with your settings.
- Anyone whose taste can't be described by one genre, one mood, and one energy level.

---

## 3. How the Model Works  

TuneJudge looks at each song one at a time and gives it points:

- **Same genre as your favorite:** 0.75 points.
- **Same mood as your favorite:** 1 point.
- **Energy close to what you asked for:** up to 4 points. A perfect match gets all 4. Points drop fast as the gap grows, so a song far from your target gets almost nothing.
- **Acoustic fit:** up to 0.5 points. If you like acoustic music, more acoustic songs score higher. If you don't, less acoustic songs score higher.

A perfect song scores 6.25. TuneJudge sorts all songs from highest to lowest and shows the top 5.

**Example:** a happy pop fan who wants energy 0.85 gets *Sunrise City* first (5.92). It's pop, it's happy, its energy is 0.82, and it isn't acoustic.

Genre and mood must match exactly. "indie pop" does not count as "pop."

**How I got here:** the starter code just returned the first 5 songs in the file. My first version weighted genre at 2 and energy at 1.5. I then added acoustic scoring, made energy misses cost more, and shifted weight from genre to energy.

---

## 4. Data  

- **20 songs.** The starter had 10. I added 10 more.
- **17 genres and 16 moods.** Most appear only once. Lofi is the biggest genre, with 3 songs.
- **Features:** genre, mood, energy, tempo, valence (how positive it sounds), danceability, and acousticness.
- **Used in scoring:** genre, mood, energy, and acousticness. Tempo, valence, and danceability are ignored.

**Limits:**

- Mood is tied to energy. Every sad, chill, or melancholy song is quiet. Every intense, angry, or euphoric song is loud.
- There is no energetic sad song and no calm angry song.
- Almost every loud song is electric. Barn Burner is the only loud acoustic song.
- No lyrics, language, artist popularity, or release year.

---

## 5. Strengths  

- It works well for common tastes. High-Energy Pop, Chill Lofi, and Deep Intense Rock all get the obvious #1 song.
- Every pick comes with reasons, so you can see why it was chosen.
- It doesn't break on missing genres. Asking for "k-pop" still returns happy songs at the right energy.
- Opposite tastes get opposite lists. Pop and Lofi share no songs.

---

## 6. Limitations and Bias 

**Energy beats everything else.** Energy is worth up to 4 points. A perfect genre and mood match is worth only 1.75. So if your favorite genre's songs are more than about 0.25 away from your energy target, another genre wins.

For example, a classical/melancholy fan who wants energy 0.6 got a reggae song first. The only classical song dropped to #3.

**Some tastes can't be served.** The catalog ties mood to energy. A listener who wants energetic sad music gets loud songs with no sadness. The system drops the mood without saying so.

**Some songs get shown more than others.** I tested 5,000 random listeners. Quiet songs in the crowded 0.28–0.48 energy range showed up as much as 1.9× their fair share. Loud songs at the edges, like Iron Collapse, showed up less than half as often.

**Exact matching is fragile.** "Pop" and "pop" count as different words. "indie pop" gets no credit for "pop."

---

## 7. Evaluation  

### Profiles tested

I tested 10 listener profiles: three normal tastes (High-Energy Pop, Chill Lofi, Deep Intense Rock) and seven tricky ones (Sad Banger, Case Trap, Acoustic Metalhead, Out of Range, Near-Miss Genre, Genre Ghost, Blank Slate). For each, I checked whether the #1 song was something that person would actually want and whether the rest of the top 5 made sense or was just filler.

### What surprised me

Gym Hero made the top 5 for 6 of the 10 profiles, and the "sad but high energy" listener got zero sad songs because the only sad song in the catalog is slow. Typing "Pop" instead of "pop" also made the system ignore genre and mood entirely, since it compares words exactly.

### Comparing pairs of profiles

**High-Energy Pop vs. Chill Lofi:** These two share no songs: Pop gets bright, loud songs and Lofi gets quiet, acoustic study music. That makes sense, because they sit at opposite ends of both the energy scale and the acoustic setting.

**High-Energy Pop vs. Deep Intense Rock (why Gym Hero keeps showing up):** Gym Hero is a very loud pop song, so the system gives it points for "pop" or "intense" plus nearly full energy points, and it never takes points away for having the wrong mood. Since the catalog only has two happy songs, the next best pick for a happy pop fan is simply the loudest pop song.

**Deep Intense Rock vs. Sad Banger:** Both want energy 0.9, and their top 5 lists are identical because no song in the catalog is both sad and loud. Rock gets a real match, but the sad fan just gets the loudest songs, which is explainable but not a good result.

**High-Energy Pop vs. Case Trap:** The only difference is capital letters, yet Sunrise City's score dropped from 5.92 to 4.17 and Rooftop Lights fell off the list. The system sees "Pop" and "pop" as different words, so this is a bug, not a difference in taste.

**High-Energy Pop vs. Near-Miss Genre:** Lowering energy from 0.85 to 0.76 moved Rooftop Lights up to a close #2 and pushed the very loud Gym Hero out of the top 5. That makes sense, though Rooftop Lights still gets no genre credit because "indie pop" isn't exactly "pop."

**Near-Miss Genre vs. Genre Ghost:** Asking for "k-pop," which isn't in the catalog, returns nearly the same list as "pop," just with smaller scores. This is a sensible fallback: the system still finds happy songs at the right energy instead of breaking.

**Acoustic Metalhead vs. Out of Range:** Iron Collapse is #1 for both, but an impossible energy of 1.8 cut its score from 5.76 to 2.35 and dropped every other song below 0.6. The system doesn't check its inputs, so only the genre and mood matches kept the right song on top.

**Chill Lofi vs. Acoustic Metalhead:** Both say they like acoustic music, but Lofi gets all acoustic songs and the Metalhead gets almost none. The acoustic setting is worth only 0.5 points against energy's 4, and every high-energy song in the catalog is electric.

**Chill Lofi vs. Blank Slate:** Lofi gets a focused list of lofi and chill songs, while Blank Slate gets a mix of R&B, country, lofi and reggae. Without a genre or mood, energy near 0.5 is the only thing left to sort by.

### Other checks I ran

Changing the weights three times changed the #1 song for only one profile, and checking about 294,000 combinations showed every score stays between 0 and 6.25 and matches its "Why" explanation. A test with 5,000 random listeners showed quiet songs appearing up to 1.9× their fair share while loud songs at the edges appeared less than half as often, and `pytest` passes (2 tests).

---

## 8. Ideas for Improvement  

1. **Rebalance the weights.** Try genre 1.0, mood 1.0, and energy 2.5. This would let a strong genre and mood match beat a slightly better energy match.
2. **Add more varied songs.** Several songs per genre and mood would give real choices beyond #1. It also needs missing combos, like energetic sad songs and calm intense songs.
3. **Make matching smarter.** Ignore capital letters. Give partial credit for related genres, like "pop" and "indie pop." Add a "don't care" option for acoustic music.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
