# RoomNER — Custom Named Entity Recognition for Floor-Plan Descriptions

A custom spaCy NER pipeline that reads natural-language house-plan descriptions ("bedroom1 is adjacent to balcony1, washroom1...") and extracts structured information about rooms, their sizes, positions, and how they connect — then visualizes room adjacency as an undirected graph with NetworkX.

## What it extracts

The model is trained from scratch on five custom entity labels:

| Label        | Example                                             |
|--------------|-----------------------------------------------------|
| `ROOM`       | `bedroom1`, `kitchen1`, `washroom2`                 |
| `QUANT`      | `two` (bedrooms), `one` (kitchen)                   |
| `DIRECTION`  | `southwest`, `north`, `center`                      |
| `DIMENSION`  | `17 square meters`, `12 squares`                    |
| `CONNECTION` | `bedroom1 is adjacent to balcony1, washroom1`       |

`CONNECTION` entities are then parsed into room pairs, exported as CSV edge lists, and drawn as undirected graphs — turning a paragraph of text into a room-adjacency diagram. See `screenshots/` for example outputs.

## Pipeline

```
final.json  →  Convert.py  →  spaCy training data (pickle / TRAIN_DATA)
                    ↓
               Train.py     →  trained NER model (saved to disk)
                    ↓
               Test.py      →  runs model on plan50/ text files
                             →  writes room-pair CSVs to Table/
                    ↓
               Undirected.py →  reads Table/*.csv, draws adjacency graphs
```

## Repository contents

```
RoomNER/
├── Convert.py       # Converts JSON annotations (one doc per line) into spaCy training format
├── Train.py         # Trains a blank-'en' spaCy NER model on the 5 custom labels (TRAIN_DATA embedded)
├── Test.py          # Runs the trained model over plan50/ and extracts room connections to CSV
├── Undirected.py    # Visualizes each CSV edge list as an undirected graph (NetworkX + Matplotlib)
├── final.json       # Annotated source data: floor-plan descriptions with entity spans
├── Converted.txt    # final.json already converted to spaCy training format
├── plan50/          # 50 unannotated floor-plan descriptions used as test data
└── screenshots/     # Example extractions, DataFrames, and rendered graphs
```

## Setup

> **Important:** this project is written against the **spaCy 2.x** training API (`nlp.begin_training()`, `nlp.update(texts, annotations)`), which does not exist in spaCy 3.x. Use the pinned `requirements.txt` and Python 3.7–3.8 — a default `pip install spacy` today installs 3.x and will crash.

```bash
# 1. Clone
git clone https://github.com/vinayassrao/RoomNER.git
cd RoomNER

# 2. Create a virtual environment (Python 3.7 or 3.8 recommended)
python -m venv venv
source venv/bin/activate        # Windows: venv\\Scripts\\activate

# 3. Install pinned dependencies
pip install -r requirements.txt
```

## Usage

**1. Convert annotated JSON to spaCy training format** (optional — `Converted.txt` already contains the converted data):

```bash
python Convert.py -i final.json -o training_data.pickle
```

**2. Train the model.** The converted data lives in the `TRAIN_DATA` variable inside `Train.py`; new labels go in the `LABEL` list. Train a fresh model for 100 iterations and save it:

```bash
python Train.py -o saved_model -n 100
```

Or continue training from an existing model (default is 10 iterations if `-n` is omitted):

```bash
python Train.py -m saved_model -n 50
```

After training, the script sanity-checks the model on a sample sentence and prints any `CONNECTION` entities it finds.

**3. Run extraction on the test set.** This loads every text file in `plan50/`, extracts `ROOM` and `CONNECTION` entities, resolves them into room pairs, and writes one CSV edge list per plan into `Table/`:

```bash
python Test.py -m saved_model
```

**4. Visualize the adjacency graphs.** Reads the CSVs in `Table/` and renders each plan's room connections as an undirected graph (one Matplotlib window per plan):

```bash
python Undirected.py
```

## Adapting to your own data

Any domain works, not just floor plans. Provide annotations as line-delimited JSON (`{"document": "...", "annotation": [{"start": .., "end": .., "label": ".."}]}`), run `Convert.py`, paste the output into `TRAIN_DATA`, update `LABEL` with your entity names, and retrain.

## Known limitations

- Training data is embedded directly in `Train.py` rather than loaded from the pickle that `Convert.py` produces.
- `Test.py` writes CSVs for plans 1950–1999, but `Undirected.py` iterates 1950–1998 and skips the final plan.
- Connection extraction relies on keyword heuristics (`adjacent`, `next`) on top of the NER output, so unusual phrasings can be missed.
- Built on spaCy 2.x; porting to spaCy 3's config-based training (`Example` objects, `spacy train`) is the natural modernization step.
