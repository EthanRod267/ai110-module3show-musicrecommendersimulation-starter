# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Think of the recommender as a judge handing out points. You tell it three things about your taste: your favorite **genre** (like pop), your favorite **mood** (like happy), and how much **energy** you want, on a scale from 0 (calm and quiet) to 1 (loud and intense). The judge then looks at every song in the catalog, one at a time, and gives it points for how well it fits you:

- **Same genre as your favorite: 2 points.** This is worth the most, because genre is usually the biggest part of someone's taste. A pop fan generally wants pop, whatever the mood.
- **Same mood as your favorite: 1 point.** Mood matters, but it changes with the moment, so it counts for half as much as genre.
- **Energy close to what you asked for: up to 1.5 points.** A song with exactly your energy level gets the full 1.5. The further away it is, the fewer points it gets, so a song that's a little off still gets most of them and a song at the opposite extreme gets almost none. It rewards being *close* to your target, not being louder or quieter.

A perfect song can earn 4.5 points. Once every song has a score, the judge sorts them from highest to lowest and shows you the top five, along with the reasons each one earned its points.

**Example:** for someone who likes happy pop with energy 0.8, *Sunrise City* scores 4.47. It's pop (+2), it's happy (+1), and its energy of 0.82 is almost exactly right (+1.47). *Gym Hero* comes second with 3.30: it's pop, but its mood is "intense," so it misses the mood point. *Rooftop Lights* is happy but "indie pop," which doesn't count as a genre match, so it ends up third with 2.44.

The song features the judge looks at are genre, mood and energy. The catalog also lists tempo, danceability, valence (how positive a song sounds) and acousticness, but these aren't scored. Tempo and danceability mostly rise and fall with energy in this catalog, so counting them too would reward the same thing several times.

**Changes from the starter:** the starter code didn't score anything; it just returned the first five songs in the file. This version reads the whole catalog, scores every song with the point system above, ranks them, and explains each pick.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
