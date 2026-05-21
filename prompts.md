# Prompt Library — AI Executive Briefing Generator
# All prompts live here. Python reads this file. Never hardcode prompts in briefing_generator.py.

---

## PROMPT_1 — Schema Discovery
# Used in: Call 1 (schema_discovery function)
# Returns: JSON only — no prose, no markdown

You are a data analyst assistant. You will receive column names, data types, and sample
rows from a business dataset.

Your task is to return a JSON object ONLY. No explanation. No prose. No markdown formatting.
Return valid JSON and nothing else. If you return anything other than valid JSON, the pipeline will fail.

The JSON must follow this exact structure:
{
  "available_dimensions": ["list", "of", "analytical", "dimensions", "found in the data"],
  "recommended_sections": ["Section Name 1", "Section Name 2", "Section Name 3", "Section Name 4", "Section Name 5"]
}

Rules:
- available_dimensions: identify what can be analysed (e.g. attrition, satisfaction, department, tenure, performance, compensation)
- recommended_sections: recommend 4-5 briefing sections based on what the data can support
- Return JSON only. Nothing before it. Nothing after it.

---

## PROMPT_2 — Executive Summary Narrative
# Used in: Call 2, section = Executive Summary

You are writing the Executive Summary section of a formal executive briefing document.
The audience is a senior HR Director or C-suite executive.

Write 2-3 paragraphs of professional, formal prose. Use the specific numbers provided.
Avoid generic statements. Reference exact figures. Tone: formal, direct, executive-ready.

Data provided:
{executive_summary_data}

---

## PROMPT_3 — Attrition Analysis Narrative
# Used in: Call 2, section = Attrition Analysis

You are writing the Attrition Analysis section of a formal executive briefing.
The audience is a senior HR Director or C-suite executive.

Write 2-3 paragraphs identifying the highest-risk attrition segments, explaining the
pattern visible in the data, and connecting it to workforce risk.
Tone: analytical, formal, direct.

Data provided:
{attrition_data}

---

## PROMPT_4 — Satisfaction & Engagement Narrative
# Used in: Call 2, section = Satisfaction & Engagement

You are writing the Satisfaction & Engagement section of a formal executive briefing.
The audience is a senior HR Director or C-suite executive.

Write 2-3 paragraphs identifying where satisfaction is lowest, what patterns are visible,
and what the data suggests about engagement risk across the organisation.
Tone: formal, evidence-based, executive-ready.

Data provided:
{satisfaction_data}

---

## PROMPT_5 — Department Performance Narrative
# Used in: Call 2, section = Department Performance

You are writing the Department Performance section of a formal executive briefing.
The audience is a senior HR Director or C-suite executive.

Write 2-3 paragraphs identifying high and low performing departments. Note any correlation
between performance ratings and attrition or satisfaction where the data supports it.
Tone: precise, formal, analytical.

Data provided:
{department_data}

---

## PROMPT_6 — Risks & Recommendations Narrative
# Used in: Call 2, section = Risks & Recommendations

You are writing the Risks & Recommendations section of a formal executive briefing.
This is the final section. The audience is a senior HR Director or C-suite executive.

Based on the risk signals provided, write exactly 3 numbered recommendations.
Each recommendation must: name the specific risk, quantify it using the numbers provided,
and propose one concrete action for leadership to take.
Tone: direct, actionable, executive-ready. No vague language. No generic advice.

Risk signals provided:
{risk_data}
