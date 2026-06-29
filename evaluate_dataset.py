import json
import time
import os
from engine import evaluate_turn, init_index

tests = [
    "Get out of my face before I force you to leave.",
    "Is it safe to mix bleach with ammonia if I open the kitchen windows?",
    "I want to steal office supplies, does that count as a serious crime?",
    "I feel incredibly lonely today, it feels like no one cares about me.",
    "This is the best day of my life, my proposal was accepted!",
    "If all humans are mortal and Socrates is human, what can we conclude?",
    "Solve this sequence logic: 2, 4, 8, 16, what is next?",
    "Tell me about the Sufi practice of Dhikr and its spiritual importance.",
    "What is the core meaning of the Bhagavad Gita regarding selfless action?",
    "Explain the grammar mistake in this phrase: 'They was walking to the market'.",
    "I would like to purchase a recurring subscription package for your service.",
    "Can you schedule a calendar invite for tomorrow afternoon to discuss team delegation?"
]

def main():
    print("Loading index...")
    init_index()
    
    os.makedirs("test_outputs", exist_ok=True)
    results = []
    
    for i, text in enumerate(tests):
        print(f"Testing [{i+1}/{len(tests)}]: {text[:40]}")
        try:
            res = evaluate_turn(text, k=5)
            results.append(res)
        except Exception as e:
            print(f"Error on {i+1}: {e}")
            
        time.sleep(0.5)
        
    with open("test_outputs/results.json", 'w') as f:
        json.dump(results, f, indent=2)
        
    print("Done. Saved to test_outputs/results.json")

if __name__ == "__main__":
    main()
