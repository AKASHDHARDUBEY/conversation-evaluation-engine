import os
import json
import pandas as pd
import streamlit as st
from engine import evaluate_turn, LOG_FILE

st.set_page_config(page_title="Evaluation Engine", layout="wide")

st.title("Conversation Evaluator")
st.write("Evaluate dialogue turns against a set of metrics.")

st.sidebar.header("Settings")
k_val = st.sidebar.slider("Number of facets to retrieve", min_value=1, max_value=12, value=4)

if st.sidebar.button("Clear Logs"):
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
    st.sidebar.success("Logs cleared.")

text_input = st.text_area(
    "Enter a sentence to evaluate:",
    "If you don't back down right now, I will find out where you work and make sure you pay for this.",
    height=100
)

if st.button("Run Evaluation", type="primary"):
    with st.spinner("Evaluating..."):
        try:
            result = evaluate_turn(text_input, k=k_val)
            metrics = result["metrics"]
            
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Total Latency", f"{metrics['total_latency_sec']:.2f}s")
            c2.metric("Search Speed", f"{metrics['retrieval_latency_sec']:.4f}s")
            c3.metric("Avg Confidence", f"{metrics['average_confidence']*100:.1f}%")
            c4.metric("Avg Score", f"{metrics['average_score']:.2f}")
            
            st.success("Done!")
            st.subheader("Results")
            
            evals = result.get("evaluations", [])
            if not evals:
                st.warning("No evaluations returned. Make sure Ollama is running.")
            else:
                for item in evals:
                    facet = item.get('facet', 'Unknown')
                    score = item.get('score', 0)
                    with st.expander(f"{facet} - Score: {score}/5", expanded=True):
                        col1, col2 = st.columns([1, 4])
                        col1.progress(score / 5)
                        col2.write(f"**Confidence:** {item.get('confidence', 0.0):.2f} | **Reasoning:** {item.get('reasoning', 'None')}")
                        
        except Exception as e:
            st.error(f"Error: {e}")

st.divider()
st.subheader("History")

if os.path.exists(LOG_FILE):
    try:
        with open(LOG_FILE, 'r') as f:
            logs = json.load(f)
            
        history = []
        for l in logs:
            history.append({
                "Time": l["metrics"]["timestamp"],
                "Text": l["text"],
                "Latency (s)": round(l["metrics"]["total_latency_sec"], 2),
                "Avg Score": round(l["metrics"]["average_score"], 2),
                "Avg Confidence": round(l["metrics"]["average_confidence"], 2)
            })
        st.dataframe(pd.DataFrame(history), use_container_width=True)
    except:
        st.write("Could not load logs.")
else:
    st.info("No past logs found.")
