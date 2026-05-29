# AI Executive Briefing Generator
### Turning raw HR data into board-ready narrative — automatically.

---

## Overview

The AI Executive Briefing Generator is a Python tool that ingests an HR analytics CSV and produces a fully formatted `.docx` executive briefing, written in formal prose and grounded in the specific numbers from the dataset. It uses a **two-call Gemini API architecture** — one call to let the model inspect the schema and recommend the briefing's structure, and a second call per section to generate the narrative from quantitative slices of the data. The result is a workforce briefing of the kind an HR Director or C-suite executive would expect to receive, generated end-to-end with no human in the loop.

---

## Business Impact

Writing a briefing like this manually takes an HR analyst 4 to 6 hours: pulling the data, computing the statistics, writing narrative across multiple sections, and compiling a formatted document. This tool produces the same output in under 90 seconds, with no manual steps after the script runs.

For HR teams that produce recurring workforce reports (monthly, quarterly, or after engagement surveys), this means analyst time shifts from document production to strategic interpretation. The briefing adapts automatically to any HR dataset with the same column structure, making it reusable across clients, business units, or reporting cycles.

---

## Architecture — Two-Call Gemini Flow

```
            ┌────────────────────────┐
            │   data/sample_input.csv │
            └────────────┬───────────┘
                         │
                  data_loader()
                         │
                         ▼
        ┌────────────────────────────────────┐
        │  CALL 1 — Schema Discovery          │
        │  Sends: columns + dtypes + 3 rows   │
        │  Returns: JSON only                 │
        │   {                                 │
        │     "available_dimensions": [...],  │
        │     "recommended_sections": [...]   │
        │   }                                 │
        │  Retries once if JSON is invalid.   │
        └────────────────┬───────────────────┘
                         │
              For each recommended section:
                         │
                         ▼
        ┌────────────────────────────────────┐
        │  CALL 2 — Narrative Generation      │
        │  Sends: section prompt + data slice │
        │   (e.g. attrition by department,    │
        │    satisfaction by job role)        │
        │  Returns: formal executive prose    │
        └────────────────┬───────────────────┘
                         │
                  build_document()
                         │
                         ▼
            ┌────────────────────────────┐
            │  output/sample_briefing.docx │
            └────────────────────────────┘
```

**Call 1** asks Gemini to act as a data analyst and return strict JSON describing what the dataset can support and which sections the briefing should contain. The response is parsed with `response_mime_type=application/json` and validated; an invalid response triggers exactly one retry before the pipeline fails loudly.

**Call 2** runs once per section. Python computes a deterministic data slice for each section (e.g. attrition rates by tenure bucket, satisfaction by department, top job roles by turnover), injects it into the matching prompt from `prompts.md`, and asks Gemini to produce 2–3 paragraphs of formal narrative referencing the exact figures.

---

## Tech Stack

| Layer              | Tool                       | Purpose                                                  |
| ------------------ | -------------------------- | -------------------------------------------------------- |
| Language           | Python 3.12                | Pipeline orchestration                                   |
| LLM                | Gemini 2.5 Flash           | Schema discovery + narrative generation                  |
| Data handling      | pandas                     | CSV loading, aggregation, group-by analytics             |
| Document output    | python-docx                | Styled `.docx` assembly (headings, fonts, colours)       |
| Configuration      | python-dotenv              | Loading API credentials from `.env`                      |
| Prompt management  | `prompts.md`               | All prompts externalised; never hardcoded in Python      |
| Spec               | `CLAUDE.md`                | Architecture rules and build constraints                 |

---

## What the Tool Produces

![Sample Briefing Output](assets/sample_briefing_preview.png)

A professional `.docx` executive briefing containing:

- **Title page header** — "Workforce Executive Briefing" with the generation date.
- **Executive Summary** — High-level workforce metrics: headcount, overall attrition, average tenure, satisfaction, and compensation.
- **Attrition Analysis** — Highest-risk attrition segments by department, overtime status, job role, and tenure bucket.
- **Satisfaction & Engagement** — Job, environment, and work-life-balance satisfaction patterns across departments, plus the attrition gap between satisfied and dissatisfied employees.
- **Department Performance** — Performance ratings, income, satisfaction, and attrition broken down by department.
- **Risks & Recommendations** — Three numbered, quantified, action-oriented recommendations for leadership.

Every paragraph references specific figures derived from the dataset; the narrative is grounded in real numbers, not generic language.

---

## Key Capabilities

- **One API call per section (deliberate design)** — Each briefing section is generated in a separate Gemini call with its own focused data slice. This is a conscious trade-off: more API calls in exchange for higher-quality, data-specific narrative. Combining all sections into one call would reduce cost but produce generic output. Quality of analysis takes priority over API efficiency.
- **Two-call architecture** — Schema discovery and narrative generation are separated, so the briefing structure adapts to whatever dataset is supplied without code changes.
- **Strict JSON contract with retry** — Call 1 must return parseable JSON; the pipeline retries once and fails clearly otherwise.
- **Prompt/code separation** — All prompts live in `prompts.md`. Editing the tone, structure, or section instructions requires no Python changes.
- **Deterministic data slices** — Each section is grounded in a reproducible aggregation computed by pandas, not in the model's recall.
- **Lenient section routing** — If Gemini renames a section (e.g. "Overall Attrition Overview" vs "Attrition Analysis"), keyword matching still routes the correct data slice to the correct prompt.
- **Credential hygiene** — API keys are loaded from `.env`; no secrets in source.
- **Professional document styling** — Calibri body, accented heading colour, centred title block, dated subtitle.

---

## How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure your API key

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your_api_key_here
```

A free key from [Google AI Studio](https://aistudio.google.com/app/apikey) is sufficient — the pipeline uses 7+ calls per run: one for schema discovery, one per section, and one for the Chief HR Officer strategic commentary.

### 3. Run the generator

```bash
python briefing_generator.py
```

Expected output:

```
[schema] dimensions: [...]
[schema] sections:   ['Executive Summary', 'Attrition Analysis', ...]
[generating] Executive Summary
[generating] Attrition Analysis
[generating] Satisfaction & Engagement
[generating] Department Performance
[generating] Risks & Recommendations
[done] wrote output/sample_briefing.docx
```

Open `output/sample_briefing.docx` to read the generated briefing.

### 4. Interactive Q&A Mode (`--qa`)

```bash
python briefing_generator.py --qa
```

After the `.docx` is written, the script drops into an interactive Q&A loop:

```
[done] wrote output/sample_briefing.docx
[Q&A] Briefing ready. Ask questions about this report (type 'exit' to quit):
> Which department has the highest attrition?
Sales, at 20.6% — the highest of the three departments...
> exit
```

This implements **context-grounded Q&A using the RAG (Retrieval-Augmented Generation) pattern**: the full assembled briefing — every section plus the Strategic Executive Commentary — is injected as context with each question, and Gemini is instructed (via `PROMPT_8` in `prompts.md`) to answer **only** from that context and to say so plainly when the briefing does not cover a question. Answers are therefore grounded in the report, not in the model's general knowledge. Omit `--qa` to skip Q&A and exit after the document is written (existing default behaviour). A browser-based interface with drag-and-drop CSV upload and integrated chat is planned for v1.3 via Streamlit.

### 5. Automated Mode

For hands-off operation, run the watcher and simply drop a CSV into `data/`:

```bash
python watcher.py
```

```
[watcher] Monitoring data/ folder — drop a CSV to generate a briefing
[watcher] Detected new file: new_input.csv — generating briefing...
[schema] dimensions: [...]
[generating] Executive Summary
...
[done] wrote output/sample_briefing.docx
[watcher] Done.
```

The watcher uses [watchdog](https://pypi.org/project/watchdog/) to monitor `data/`. Any new `.csv` file dropped in (e.g. from Finder, a download, or another script) automatically triggers `briefing_generator.py` end-to-end — no manual step required. Press `Ctrl+C` to stop the watcher. Non-CSV files are ignored.

---

## Repository Structure

```
ai-executive-briefing-generator/
├── .env                     # API key (not committed)
├── .gitignore
├── CLAUDE.md                # Project spec and architecture rules
├── README.md
├── briefing_generator.py    # Pipeline entry point
├── watcher.py               # Folder watcher for automated mode
├── prompts.md               # Prompt library (all prompts)
├── requirements.txt
├── assets/
│   └── sample_briefing_preview.png  # README preview image
├── data/
│   └── sample_input.csv     # IBM HR Analytics dataset (1,470 rows, 35 cols)
└── output/
    └── sample_briefing.docx # Generated briefing
```

---

## Skills Demonstrated

`Python` · `API Integration` · `Prompt Engineering` · `Multi-Persona AI Pipeline` · `Context-Grounded Q&A (RAG Pattern)` · `Process Automation` · `People Analytics` · `Error Handling` · `Document Generation`
