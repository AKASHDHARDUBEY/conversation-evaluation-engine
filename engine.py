import json
import time
import re
import os
import requests
import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

OLLAMA_URL = os.getenv("OLLAMA_HOST", "http://localhost:11434") + "/api/generate"
MODEL_NAME = "qwen2:7b"
LOG_FILE = "evaluation_logs.json"

print("Loading embedding model...")
embed_model = SentenceTransformer('all-MiniLM-L6-v2')

_faiss_index = None
_metadata_df = None

def init_index():
    global _faiss_index, _metadata_df
    
    if not os.path.exists("cleaned_facets.csv"):
        raise Exception("cleaned_facets.csv not found")
        
    _metadata_df = pd.read_csv("cleaned_facets.csv")
    texts = _metadata_df['Cleaned_Facet'].tolist()
    
    print("Creating embeddings...")
    embeddings = embed_model.encode(texts, convert_to_tensor=False)
    embeddings = np.array(embeddings).astype('float32')
    
    _faiss_index = faiss.IndexFlatL2(embeddings.shape[1])
    _faiss_index.add(embeddings)
    print("Index created.")

def search_facets(text, k=5):
    if _faiss_index is None:
        init_index()
        
    vec = embed_model.encode([text], convert_to_tensor=False)
    vec = np.array(vec).astype('float32')
    
    dists, idxs = _faiss_index.search(vec, k)
    
    results = []
    for i, idx in enumerate(idxs[0]):
        row = _metadata_df.iloc[idx]
        results.append({
            "facet": row['Cleaned_Facet'],
            "category": row['Category'],
            "description": row['Description'],
            "distance": float(dists[0][i])
        })
    return results

def extract_json(text):
    text = text.strip()
    match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL | re.IGNORECASE)
    if match:
        text = match.group(1)
    else:
        match = re.search(r'(\{.*\})', text, re.DOTALL)
        if match:
            text = match.group(1)
            
    text = re.sub(r'[\x00-\x1F\x7F]', '', text)
    return json.loads(text)

def run_llm(prompt, retries=3):
    for i in range(retries):
        try:
            res = requests.post(OLLAMA_URL, json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
                "format": "json"
            }, timeout=45)
            res.raise_for_status()
            
            data = extract_json(res.json().get("response", ""))
            
            if "evaluations" in data:
                return data
                
        except Exception as e:
            print(f"Failed (attempt {i+1}): {e}")
            time.sleep(1)
            
    return {"evaluations": []}

def evaluate_turn(text, k=5):
    t0 = time.time()
    
    facets = search_facets(text, k)
    t1 = time.time()
    
    context = ""
    for i, f in enumerate(facets):
        context += f"{i+1}. {f['facet']} - {f['description']}\n"
        
    prompt = f"""
Analyze this text:
"{text}"

Evaluate it against these categories:
{context}

For each category, give:
- A score from 1 to 5 (1 = not present, 5 = highly present)
- A confidence score from 0.0 to 1.0
- A short reason

Return ONLY valid JSON in this exact format:
{{
  "evaluations": [
    {{
      "facet": "Name",
      "score": 3,
      "confidence": 0.8,
      "reasoning": "reason here"
    }}
  ]
}}
"""
    
    t2 = time.time()
    result = run_llm(prompt)
    t3 = time.time()
    
    scores = [x.get('score', 0) for x in result.get('evaluations', [])]
    confs = [x.get('confidence', 0.0) for x in result.get('evaluations', [])]
    
    record = {
        "text": text,
        "metrics": {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_latency_sec": t3 - t0,
            "retrieval_latency_sec": t1 - t0,
            "inference_latency_sec": t3 - t2,
            "average_score": float(np.mean(scores)) if scores else 0.0,
            "average_confidence": float(np.mean(confs)) if confs else 0.0
        },
        "evaluations": result.get("evaluations", [])
    }
    
    try:
        logs = []
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r') as f:
                logs = json.load(f)
        logs.append(record)
        with open(LOG_FILE, 'w') as f:
            json.dump(logs, f, indent=2)
    except:
        pass
        
    return record
