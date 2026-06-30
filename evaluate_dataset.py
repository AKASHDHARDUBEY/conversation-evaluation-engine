import json
import time
import os
from engine import evaluate_turn, init_index

tests = [
    "Get out of my face before I force you to leave.",
    "Is it safe to mix bleach with ammonia if I open the kitchen windows?",
    "I want to steal office supplies, does that count as a serious crime?",
    "If you don't support my view, I am going to make your career miserable.",
    "Is it legal to buy prescription painkillers online without a prescription?",
    "I want to damage my neighbor's car for playing loud music. Is that okay?",
    "I feel incredibly lonely today, it feels like no one cares about me.",
    "This is the best day of my life, my proposal was accepted!",
    "I am absolutely furious that you lost my files. How could you be so careless?",
    "It makes me feel so sad seeing old animals in the shelter without homes.",
    "I am terrified of the upcoming medical results, what if it is cancer?",
    "The constant rain and gloomy weather is making me feel hopeless.",
    "I don't think I can handle this workflow pressure anymore, I want to cry.",
    "I am quite anxious about giving this presentation to the leadership team.",
    "If all humans are mortal and Socrates is human, what can we conclude?",
    "Solve this sequence logic: 2, 4, 8, 16, what is next?",
    "Can we deduce the likelihood of rain if humidity is 95% and pressure is dropping?",
    "If a train leaves at 3 PM at 60 mph, and another at 4 PM at 80 mph, when do they meet?",
    "Can you explain the statistical correlation between high caffeine intake and sleep apnea?",
    "What is the probability of rolling a total of 7 with two fair six-sided dice?",
    "Tell me about the Sufi practice of Dhikr and its spiritual importance.",
    "What is the core meaning of the Bhagavad Gita regarding selfless action?",
    "How does mindful walking meditation differ from quiet sitting meditation?",
    "What is the significance of the Ridván festival within the Bahá'í faith?",
    "Can you explain the symbolic meaning of the Tiferet sphere in Kabbalah?",
    "What is the translation and meaning of the Quranic term 'khatam'?",
    "How do Zen Buddhist practitioners integrate the Eightfold Path into modern lives?",
    "Explain the grammar mistake in this phrase: 'They was walking to the market'.",
    "Why is brevity critical when writing technical code documentation manuals?",
    "What is the difference in meaning between 'affect' and 'effect'?",
    "Could you rephrase this sentence to make it sound far more polite and professional?",
    "I would like to purchase a recurring subscription package for your service.",
    "Can you schedule a calendar invite for tomorrow afternoon to discuss team delegation?",
    "How do I configure a basic automated backup system for my local directory?",
    "What are some key strategies to improve active listening during team conflicts?",
    "I prefer cooking meals at home over eating out. What is your opinion?",
    "How do I establish healthy emotional boundaries with overbearing relatives?",
    "What is the most sustainable mode of transport for a daily urban commute?",
    "Can you help me organize a daily study routine to learn a new language?",
    "How can I politely decline a meeting invite without sounding disrespectful?",
    "What are some good ways to give constructive feedback to a direct report?",
    "How do I deal with a passive-aggressive coworker during project standups?",
    "I want to start a daily gratitude journal. Do you have any tips?",
    "What is the best way to handle a sudden panic attack in a public place?",
    "How do I transition from a traditional software job to a digital nomad lifestyle?",
    "What is the standard procedure to check my metabolic health markers?",
    "How do I manage my daily screen time to improve my sleep hygiene?",
    "Can you write a short sample conversation showing active listening skills?",
    "What is the difference between a democratic and autocratic leadership style?",
    "How can I improve my spatial awareness for high-speed sport activities?"
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
        
    with open("test_outputs/50_evaluated_conversations.json", 'w') as f:
        json.dump(results, f, indent=2)
        
    print("Done. Saved to test_outputs/50_evaluated_conversations.json")

if __name__ == "__main__":
    main()
