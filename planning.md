# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

UCI ACC Housing Options

I chose this domain because with off-campus housing, there are a lot of details outside of official channels that are still important for a student to consider. Details like cleanliness, thickness of walls so that you won't get disturbed by neighbors, and just general thoughts of a housing option would be very important for a student to know about before making their decisions.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

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

Summary: My domain will be of knowledge on UCI ACC Apartments. This knowledge is useful because a student would be living in these apartments for a year, and would want to know all the good and bad details about a choice before making a decision.

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** 1000

**Overlap:** 150

**Reasoning:** Usually, the reviews are split into paragraphs. A smaller review could be 1-3 sentences, while a larger review could be 4-6 paragraphs. To take into account these, I decided to have a larger chunk size, to either capture a good portion of a larger review or multiple reviews.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** all-MiniLM-L6-v2

**Top-k:** 5 chunks

**Production tradeoff reflection:** I'd choose a better model, like an OpenAI model. I'd also include more sources to draw information from.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| #   | Question                                                                                             | Expected answer                                                                                                 |
| --- | ---------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| 1   | What do students say about PV1's bus situation, and what is the downside of its bus stop location?   | PV 1 is very close to a bus stop. However, the bus may be full, since it is the last stop in the \_ track.      |
| 2   | What type of room arrangement does VDC typically offer, and how do students feel about the space?    | VDC offers usually single rooms, so comfortable.                                                                |
| 3   | What are the most common complaints students mention about Plaza Verde 2?                            | New construction, very clean, sometimes faulty wifi, expensive parking                                          |
| 4   | What amenities does Camino del Sol offer, and what is the approximate monthly rent range?            | Has pool and laundry, access to all other ACC amenities, pool/hot tub, don't have to sahre a room, $1,103-1,462 |
| 5   | What are the specific storage and furniture limitations students mention about Puerta del Sol rooms? | Free laundry, close walk, has to share closet with two people, no desks                                         |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. The reviews are mixed, and chunks will likely have information on different ACC apartments.

2. Reviews can range from less than an incomplete sentence to multiple paragraphs, meaning that information can get mixed up.

3. Some of the sources are in ranked formatting, meaning that there could be bias towards some apartments over others.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->
<img width="582" height="87" alt="image" src="https://github.com/user-attachments/assets/73532a53-9445-4e9a-bbff-c1045bbb612e" />

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

I plan on using Claude to help guide me through step by step to helping me complete this, so I can understand and learn by example. If needed, I'll also provide Claude the documents to recommend chunk sizes and k sizes.

With each specific function, I'll ask Claude the steps on how to implement it, write it out myself, and verify with Claude that it matches what I need.

**Milestone 3 — Ingestion and chunking:**
Returned 94 chunks

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
