Personal Meal Decision Engine
Product + System Design Specification (MVP)
1. Problem Statement

Working professionals often struggle with deciding what to cook or eat. The decision problem arises due to:

conflicting preferences

health considerations

cuisine cravings

lack of structured meal planning

too many options

Existing solutions (recipe apps, meal planners) focus on recipes, not decision-making.

This system focuses on:

Helping users decide what to eat by querying dishes using natural language and composing meals interactively.

2. Product Vision

A personal food decision engine that:

understands natural language queries

maps them to structured dish tags

searches a local dish database

ranks dishes based on relevance

allows users to build meals interactively

Example queries:

something light chinese starter
paneer dinner
alkaline meal for my parents
crispy snack but not spicy
3. Core Principles
1. Local-first architecture

Dish knowledge resides locally.

SQLite database

Benefits:

fast

private

offline-capable

2. LLM only for language understanding

LLM does:

intent parsing
tag extraction
spelling correction
synonym understanding

LLM does NOT:

store dish data
generate meals
decide dish list

The database remains the source of truth.

3. Tag-driven search

Dishes are discovered using tags.

Example:

Palak Paneer
tags:
north_indian
paneer
protein_rich
iron_rich
dinner
veg

Tags allow flexible queries.

4. Meal composition workflow

Instead of suggesting a full meal immediately, users:

choose dishes progressively

Example:

Crispy Corn
+
Veg Fried Rice
+
Tomato Soup

This forms a meal.

4. High-Level Architecture
User
 │
 ▼
UI Layer
 │
 ▼
Query Processor
 │
 ├── LLM Intent Parser
 │
 ├── Tag Validator
 │
 ▼
Dish Search Engine
 │
 ▼
SQLite Database
 │
 ▼
Ranking Engine
 │
 ▼
Grouped Results
 │
 ▼
Meal Builder
 │
 ▼
Meal History Storage
5. System Components
5.1 Dish Registry

Stores all dishes and metadata.

Responsibilities:

add new dishes

manage dish tags

store references (photos, videos)

5.2 Tag Engine

Responsible for:

tag validation

tag lookup

tag-based search

Tags are the core indexing mechanism.

5.3 Query Processor

Responsible for:

sending user query to LLM

receiving tag list

validating tags

calling search engine

5.4 Dish Search Engine

Handles:

tag matching
ranking
result grouping
5.5 Meal Builder

Handles:

add dish
remove dish
finalize meal
5.6 Meal History Engine

Stores past meals.

Enables future improvements like:

dish co-occurrence
recommendations
6. Database Design

SQLite is used for simplicity.

6.1 dishes
dish_id      INTEGER PRIMARY KEY
name         TEXT
description  TEXT

Example:

1 | Palak Paneer
2 | Veg Fried Rice
3 | Crispy Corn
6.2 tags
tag_id       INTEGER PRIMARY KEY
name         TEXT UNIQUE
description  TEXT

Example:

indo_chinese
starter
crispy
spicy
light
protein_rich
6.3 dish_tags

Many-to-many mapping.

dish_id
tag_id
PRIMARY KEY(dish_id, tag_id)

Example:

Crispy Corn
indo_chinese
starter
crispy
non_spicy
6.4 dish_metadata (optional)

Stores rich content.

dish_id
image_url
youtube_url
notes
recipe_reference

Not used for search.

6.5 meals

Stores finalized meals.

meal_id
created_at
notes
6.6 meal_items
meal_id
dish_id

Example:

Meal #100
Palak Paneer
Roti
Boondi Raita
7. Indexing Strategy

To ensure fast search:

INDEX dish_tags_tag_id
INDEX dish_tags_dish_id
INDEX tags_name

Performance:

2000 dishes
200 tags

Query time:

~2–5 ms
8. Tag System

Tags describe dish attributes.

Example categories:

Cuisine
north_indian
south_indian
indo_chinese
italian
street_food
Dish Role
starter
main
rice
bread
snack
soup
dessert
drink
Taste
spicy
sweet
tangy
crispy
creamy
Nutrition
protein_rich
iron_rich
fiber_rich
low_protein
light
heavy
Dietary Restrictions
veg
jain
no_onion_garlic
satvik
Cooking Method
fried
baked
steamed
grilled
quick
slow_cooked
9. LLM Integration

LLM performs intent parsing and tag extraction.

Example prompt:

You are a food query interpreter.

Allowed tags:
north_indian
south_indian
indo_chinese
starter
crispy
spicy
non_spicy
light
low_protein
fried
baked
steamed
dinner
breakfast
dessert

User query:
"chinese starter crispy less-fried also non-spicy"

Return matching tags.

Output JSON:
{
 "tags": []
}
10. Tag Validation

Backend validates LLM output.

Example:

valid_tags = set(db_tags)
filtered_tags = [t for t in llm_tags if t in valid_tags]

Prevents hallucinated tags.

11. Dish Search Algorithm

Given tags:

indo_chinese
starter
crispy
non_spicy
light

SQL concept:

SELECT dish_id, COUNT(*) as score
FROM dish_tags
WHERE tag_id IN (...)
GROUP BY dish_id
ORDER BY score DESC

Score = number of matched tags.

12. Ranking Strategy
Match Count	Category
4+	Top Matches
2–3	Good Matches
1	Related Options
13. UI Design

Minimalistic interface.

13.1 Home Screen
Kya Khaoge

[Start Meal]
[Meal History]
13.2 Meal Builder Screen

Two panels.

--------------------------------
| Dish Search | Meal Builder   |
--------------------------------
| Query box   | Current Meal   |
| Tag chips   | Dish list      |
| Results     | Remove dish    |
--------------------------------
13.3 Filters Display
indo_chinese • starter • crispy • non_spicy
13.4 Result Groups
Top Matches
Good Matches
Related Options
13.5 Dish Card

Example:

Crispy Corn
tags: indo_chinese • starter • crispy

[Add to Meal]
13.6 Meal Builder Panel
Current Meal
------------
Crispy Corn
Veg Fried Rice

[Remove]
[Finalize Meal]
14. Meal Builder Flow

Example:

User: chinese crispy starter

System:

Crispy Corn
Veg Spring Roll

User adds:

Crispy Corn

Meal becomes:

Current Meal
Crispy Corn

System suggests next dishes.

15. Performance

Dataset:

2000 dishes
200 tags

Performance:

Component	Time
LLM parsing	500 ms
DB search	5 ms
Ranking	1 ms

Total:

~600–800 ms
16. Storage Size

Approximate database size:

dishes table      ~200 KB
tags table        ~20 KB
dish_tags table   ~500 KB
metadata          ~1–2 MB

Total:

~2–3 MB
17. Technology Stack

Backend:

Python
FastAPI
SQLite

Frontend:

Streamlit

LLM:

Claude / OpenAI API
18. Future Enhancements

Possible improvements:

Tag synonym graph
chatpata → spicy
oily → fried
Dynamic tag prompts

Reduce LLM token usage.

Vector semantic search

Understand vague queries.

Meal pattern learning

Example:

palak paneer → roti
rajma → rice
pizza → garlic bread
Nutrition analysis

Calculate macros automatically.

19. MVP Scope

The MVP will include:

dish database
tag-based search
LLM intent parsing
meal builder
meal history
minimal UI

Excluded from MVP:

vector search
nutrition engine
synonym graph
dynamic tag selection
20. Final Summary

This system combines:

LLM for language understanding
+
SQLite for deterministic dish knowledge
+
Tag-based indexing for flexible search
+
Interactive meal builder

The architecture is:

simple
fast
maintainable
scalable

Suitable for a personal food decision engine MVP.