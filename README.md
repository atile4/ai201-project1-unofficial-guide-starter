# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section _after_ you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

UCI ACC Housing Options

I chose this domain because with off-campus housing, there are a lot of details outside of official channels that are still important for a student to consider. Details like cleanliness, thickness of walls so that you won't get disturbed by neighbors, and just general thoughts of a housing option would be very important for a student to know about before making their decisions.

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| #   | Source         | Description                                   | URL or location                                                                                                  |
| --- | -------------- | --------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| 1   | Reddit         | General thoughts on ACC Apartments            | https://www.reddit.com/r/UCI/comments/1cd2ub3 whats_life_like_in_the_acc_apartments/                             |
| 2   | Reddit         | Housing Recommendations for 2nd year          | https://www.reddit.com/r/UCI/comments/1oa9vmh/housing_recs_for_second_yr/                                        |
| 3   | Reddit         | Opinions about PV 1                           | https://www.reddit.com/r/UCI/comments/x4b6hb/honest_opinions_about_living_in_plaza_verde/                        |
| 4   | Reddit         | Asking about which ACC apartment is the best  | https://www.reddit.com/r/UCI/comments/18iltqk/which_continuing_student_housing_is_best/                          |
| 5   | Reddit         | PV II Reviews                                 | https://www.reddit.com/r/UCI/comments/1l8k2b9/plaza_verde_ii_reviews/                                            |
| 6   | RateMyDorm     | Ranked dorms in UCI (included on-campus)      | https://www.ratemydorm.com/dorms-ranked/university-of-california-irvine                                          |
| 7   | Reddit         | Asking about favorite ACC                     | https://www.reddit.com/r/UCI/comments/1306oa1/whats_your_favorite_acc_apartment_community/                       |
| 8   | Wordpress Blog | Ranking UCI Undergraduate Housing Communities | https://campusobscura.wordpress.com/2024/06/13/uci-undergraduate-housing-communities-ranked-an-unfiltered-guide/ |
| 9   | RateMyDorm     | VDC Reviews                                   | https://www.ratemydorm.com/reviews/university-of-california-irvine/uc-irvine-vista-del-campo                     |
| 10  | Reddit         | Are ACC Apartments really that bad?           | https://www.reddit.com/r/UCI/comments/14wks9z/are_the_acc_apartments_really_that_bad/                            |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 1000

**Overlap:** 150

**Why these choices fit your documents:** Usually, the reviews are split into paragraphs. A smaller review could be 1-3 sentences, while a larger review could be 4-6 paragraphs. To take into account the wide range of revies, I decided to have a larger chunk size, to either capture a good portion of a larger review or multiple reviews.

**Final chunk count:** 94

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** all-MiniLM-L6-v2

**Production tradeoff reflection:** I'd choose a better model, like an OpenAI model. The model I use, all-MiniLM-L6-v2, has a 256-token limit and will remove anything longer than that. Although my chunk size should fit inside this limit, it's a factor that still needs be considered. I'd also include more sources to draw information from, as some of my sources are shorter, particularly the reddit forums, are pretty short, and there are a wide variety of opinions on UCI's ACC apartments.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**
Grounding is enforced through a system prompt that constrains the model to the retrieved context. The prompt instructs the LLM that it is answering questions about UCI ACC housing based only on the student reviews passed to it as context. The `SYSTEM_PROMPT` variable lays out hard rules: answer using only the provided context, do not use outside or general knowledge about housing or UCI, and to respond with "I don't have enough info" if context doesn't contain enough information.

I also set the model's temperature to 0.2 so it stays close to the source text instead of generating creative or speculative answers. Structurally, the retrieved chunks are formatted into a numbered context block where each chunk is labeled with its source document, so the model sees both the text and where it came from before answering.

**How source attribution is surfaced in the response:**
Source attribution is generated programmatically from retrieval metadata, not by the LLM. After retrieval, each returned chunk carries a source field (the original document filename) stored in ChromaDB. The system collects these filenames, de-duplicates them while preserving retrieval order (most relevant source first), and displays them alongside every answer.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| #   | Question                                                                                             | Expected answer                                                                                                 | System response (summarized)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Retrieval quality  | Response accuracy |
| --- | ---------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ | ----------------- |
| 1   | What do students say about PV1's bus situation, and what is the downside of its bus stop location?   | PV 1 is very close to a bus stop. However, the bus may be full, since it is the last stop in the M track.       | Getting a spot in the bus can be hard, especially when people are heading to class. Bus stop location is convenient, but busy during peak hours                                                                                                                                                                                                                                                                                                                                                                                                            | Relevant           | Accurate          |
| 2   | What type of room arrangement does VDC typically offer, and how do students feel about the space?    | VDC offers usually single rooms, so comfortable.                                                                | Large, comparitively large single rooms, decent price. Carpet floors can be "kinda gross", and that the space can feel smaller when sharing roommates                                                                                                                                                                                                                                                                                                                                                                                                      | Partially Relevant | Accurate          |
| 3   | What are the most common complaints students mention about Plaza Verde 2?                            | New construction, very clean, sometimes faulty wifi, expensive parking                                          | According to the provided context, the most common complaints students mention about Plaza Verde 2 are related to the contract length, being 36 pages long and super one-sided towards the Landlord, as well as potential bug issues. One student also mentions considering not living in Plaza Verde 2 due to hearing "horror stories" about bugs from friends. Additionally, another student mentions that the contract is a concern, but does not specify other complaints. However, it is also mentioned that Plaza Verde II has the newest amenities. | Off-target         | Accurate          |
| 4   | What amenities does Camino del Sol offer, and what is the approximate monthly rent range?            | Has pool and laundry, access to all other ACC amenities, pool/hot tub, don't have to sahre a room, $1,103-1,462 | According to the context, Camino del Sol offers the following amenities: pool, included laundry, access to all other ACC Amenities. The approximate monthly rent range for Camino del Sol is $1,103-$1,462.                                                                                                                                                                                                                                                                                                                                                | Relevant           | Accurate          |
| 5   | What are the specific storage and furniture limitations students mention about Puerta del Sol rooms? | Free laundry, close walk, has to share closet with two people, no desks                                         | Having to share a closet with two people, There are no desks in the rooms, so students have to bring their own, Barely any space in the room, making it difficult to fit a desk                                                                                                                                                                                                                                                                                                                                                                            | Relevant           | Accurate          |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

What are the most common complaints students mention about Plaza Verde 2?

**What the system returned:**

According to the provided context, the most common complaints students mention about Plaza Verde 2 are related to the contract length, being 36 pages long and super one-sided towards the Landlord, as well as potential bug issues. One student also mentions considering not living in Plaza Verde 2 due to hearing "horror stories" about bugs from friends. Additionally, another student mentions that the contract is a concern, but does not specify other complaints. However, it is also mentioned that Plaza Verde II has the newest amenities.

**Root cause (tied to a specific pipeline stage):**

Although the return reflected what I saw when I skimmed through the documents, it's pretty off-topic in the sense that it doesn't give much information about the actual room.

I believe that the most likely cause was from Ingestion. I very likely didn't provide enough relevancy towards the topic of PV 2 itself, and the model could only draw its information from so many sources, particularly some irrelevant ones.

**What you would change to fix it:**
I would include sources involving more specific details about PV II.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

`planning.md` helped me with coming up with chunk/overlap sizes, organizing my thoughts, and sorting/gathering documents. Drawing out an architecture in Canva also helped me to comprehend the problem and implementation.

**One way your implementation diverged from the spec, and why:**
Although my implementation mostly followed the spec, while I was chunking and retrieving samples, I noticed that there were some words that were getting cut off. This was small, and the general idea remained consistent even with the cutoff, and I would've fixed this by having a larger overlap than 150.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- _What I gave the AI:_ My Chunking Strategy section from planning.md (1000-char chunks, 150 overlap, reasoning about variable-length reviews) and asked it to implement the chunking function.
- _What it produced:_ A recursive splitter that breaks on paragraphs, then sentences, then words. When I ran it on my real documents it crashed with a RecursionError — one document had a long unbroken stretch of text with no separators.
- _What I changed or overrode:_ I looked through the actual error and worked with Claude to fix the bug. The fix added a hard character-cut base case so an oversized piece always terminates. I verified the fix by re-running on my full document set and confirming it produced 94 clean chunks.

**Instance 2**

- _What I gave the AI:_ My 10 documents, and asked it to create a function that could scrape and format all the raw text and store it in the directory documents/.
- _What it produced:_ Three web scrapers for the three different types of websites I used as sources, as well as ingest.py to clean the punctuation/whitespaces.
- _What I changed or overrode:_ The reddit web scraper failed to retrieve the text, likely because it has guards against bots or against what I was doing. Instead of trying to figure this out, I modified the function to take the raw JSON text in one-line and work with the document from there.
