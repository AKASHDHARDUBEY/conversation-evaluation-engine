# Prompt Log - Conversation Evaluation System

This document logs the development, design iteration, and engineering choices behind the system prompts used to evaluate dialogue turns against dynamic facets.

## Prompt Architecture Strategy
To prevent prompt length issues and context dilution when scaling to 300+ (and eventually 5,000+) facets, we implemented a dual-stage architecture:
1. **Retrieval Stage:** Semantic similarity filter utilizing `all-MiniLM-L6-v2` dense embeddings to retrieve the top $K$ relevant facets.
2. **Evaluation Stage:** Targeted LLM prompt using local open-weight inference.

---

## Iteration 1: Naive Evaluation (Attempted Monolithic)
* **Goal:** Process the input text against all facets simultaneously.
* **Prompt:**
  ```text
  Evaluate the following text against all 300 facets. Assign a score from 1 to 5 for each.
  Text: "[INPUT_TEXT]"
  ```
Failure Modes:
Exceeded context constraints.
Model attention diluted; returned highly repetitive scores or missed key facets.
Failed to structure the response reliably as JSON.

## Iteration 2: Targeted RAG Prompt with Static Output
* **Goal:** Evaluate only against top-K retrieved facets, requiring JSON formatting.
* **Prompt:**
  ```text
  For the dialogue text: "[INPUT_TEXT]"
  Please score these retrieved facets: [FACETS_LIST]
  Return a score and reasoning in JSON format.
  ```
Failure Modes:
LLM frequently outputted conversational text or markdown blocks (```json) surrounding the JSON, causing parsing exceptions in standard library loaders.
No confidence interval was captured.

## Iteration 3: Production Prompt (Current System)
* **Goal:** Robust JSON formatting, strict schema compliance, confidence metrics, and deterministic structured outputs.
* **Prompt:**
  ```text
  You are an expert dialogue system evaluation engine. Analyze the following conversation turn.

  CONVERSATION TURN:
  "{text}"

  Evaluate the turn ONLY against these specific retrieved facets:
  {facets_context}

  For each facet listed above, you must assign:
  - A score from 1 to 5 (where 1 = no manifestation, 5 = extreme manifestation).
  - An evaluation confidence score from 0.0 to 1.0.
  - A concise, evidence-based reasoning sentence explaining the score based on the dialogue context.

  You must return your response strictly as valid JSON matching this schema:
  {{
    "evaluations": [
      {{
        "facet": "Exact Name of Facet",
        "score": integer_between_1_and_5,
        "confidence": float_between_0_and_1,
        "reasoning": "your rationale"
      }}
    ]
  }}
  Do not write any markdown dialogue intro or outro text. Return only raw JSON.
  ```
Status: Operational. Supported by regex-based JSON validation and programmatic retries to handle parsing variances.
