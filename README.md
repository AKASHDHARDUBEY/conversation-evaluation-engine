# Scalable Conversation Evaluation Benchmark

An evaluation framework designed to score conversational dialogue turns across 300+ distinct dimensions covering safety, pragmatics, linguistic quality, and emotion.

## Architectural Overview

The framework uses a two-stage evaluation model to remain highly scalable:
[Input Turn] ──> [Sentence-Transformers Embedding]
│
▼ (Cosine Similarity Search)
[FAISS Vector Index] ──> [Top K Relevant Facets]
│
▼
[Local LLM (Qwen2/Llama3)] ──> [JSON Schema Validation] ──> [Streamlit UI / Logs]

### Key Highlights
* **Scalability to 5,000+ Facets:** By utilizing **FAISS (Facebook AI Similarity Search)** to index facet embeddings, the complexity of search scales logarithmically. The LLM only processes the top $K$ relevant facets, keeping prompt sizes stable, processing speeds high, and costs minimized.
* **No One-Shot/Monolithic Prompting:** Avoids putting thousands of dimensions into a single prompt.
* **Open-Weights Compatibility:** Tested locally with open-weights models ($\le$ 16B parameters) using Ollama.
* **Robust JSON Handling:** Includes a defensive regex extraction mechanism with a 3-pass retry buffer to validate LLM formatting before logging.

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd conversation-evaluator
   ```
2. **Setup the Virtual Environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. **Install and run Ollama:**
   Download Ollama and pull the model:
   ```bash
   ollama pull qwen2:7b
   ```
4. **Data Preprocessing:**
   ```bash
   python preprocess.py
   ```
5. **Start the Interactive Interface:**
   ```bash
   streamlit run app.py
   ```

### Running with Docker (Alternative Setup)

If you prefer to run the application in a containerized environment:
1. Ensure Ollama is running on your host machine.
2. Build and start the containers:
   ```bash
   docker-compose up --build
   ```
3. Access the Streamlit dashboard at `http://localhost:8501`.


## Repository Structure
* `preprocess.py`: Cleans raw CSV files and creates metadata mappings.
* `engine.py`: Handles vector indexing with FAISS, semantic search, and structured LLM calls.
* `evaluate_dataset.py`: Evaluates a dataset of 50 conversation points.
* `app.py`: Streamlit-driven user dashboard displaying metrics and logs.
* `test_outputs.zip`: Processed evaluations covering 50 conversations.
* `PROMPT_LOG.md`: Step-by-step optimization document for prompt strategies.
