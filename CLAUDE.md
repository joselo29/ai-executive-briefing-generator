# Project: AI Executive Briefing Generator

## Goal
Build a Python tool that takes an HR analytics CSV as input, uses a two-call Gemini API architecture to analyse the data and generate narrative, and outputs a professionally formatted .docx executive briefing document automatically. No human in the loop after the script is triggered.

## Architecture — Two-Call Gemini API

### Call 1 — Schema Discovery (JSON output required)
Send column names, data types, and 3 sample rows to Gemini.
Gemini must return structured JSON only — no prose, no markdown, no explanation.

Expected JSON format:
{
  "available_dimensions": ["attrition", "satisfaction", "department", "tenure"],
  "recommended_sections": ["Executive Summary", "Attrition Analysis", "Department Performance", "Satisfaction & Engagement", "Risks & Recommendations"]
}

Python parses this JSON to configure which analysis modules run.
If Gemini returns anything other than valid JSON, raise an error and retry once.

### Call 2 — Narrative Generation (one call per section)
For each section, send the raw data slice relevant to that section to Gemini along with the section-specific prompt from prompts.md.
Gemini analyses the data and writes the narrative paragraph explaining what it found.
Gemini handles both analysis and narrative writing.

## Rules
- Read all prompts from prompts.md only. Never hardcode prompts in Python.
- Load API key from .env only. Never hardcode credentials anywhere.
- Call 1 must return valid JSON. Build in a retry mechanism if it does not.
- Output must be a real .docx file saved to the output/ folder.
- Use Gemini 2.5 Flash model (free tier sufficient). Model name: gemini-2.5-flash
- Separate functions: data_loader, schema_discovery, generate_section, build_document.

## Dataset
- File: data/sample_input.csv
- IBM HR Analytics dataset — 1,470 rows, 35 columns
- Key columns: Attrition, Department, JobSatisfaction, PerformanceRating, MonthlyIncome, OverTime, YearsAtCompany

## Repository Structure
ai-executive-briefing-generator/
├── .env
├── .gitignore
├── CLAUDE.md
├── briefing_generator.py
├── prompts.md
├── data/
│   └── sample_input.csv
├── output/
│   └── sample_briefing.docx
└── README.md
