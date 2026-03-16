## Kya Khaoge – Personal Meal Decision Engine

A minimal Streamlit prototype that helps you decide **what to eat** by searching dishes via tags and building meals interactively.

### Tech

- **Backend**: Python, SQLite
- **UI**: Streamlit (single-page app style)

### Features

- Natural-language style query input (e.g. `light chinese starter`, `paneer dinner`, `healthy breakfast`)
- Mock LLM tag extraction (`services/tag_parser.py`)
- Tag-based dish search with simple scoring (`services/search_engine.py`)
- Two-panel layout:
  - **Left**: Dish search, tags, results with “Add to Meal”
  - **Right**: Current Meal with remove + finalize
- Meal history view backed by SQLite

### Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

The first start will create `kya_khaoge.db`, schema, and sample seed data automatically.

