import pandas as pd
import re
import os

def clean_name(name):
    if type(name) != str:
        return ""
    name = re.sub(r'^\d+\.\s*', '', name)
    return name.strip().rstrip(':')

def get_category(text):
    text = text.lower()
    if any(w in text for w in ['depression', 'sadness', 'affect', 'emotion', 'mood', 'joy', 'bliss']):
        return "Emotion"
    if any(w in text for w in ['violence', 'safety', 'harm', 'drug', 'ethical', 'disrespect']):
        return "Safety"
    if any(w in text for w in ['reasoning', 'math', 'formula', 'logic', 'cognitive']):
        return "Cognitive"
    if any(w in text for w in ['spiritual', 'faith', 'sufi', 'sacred', 'hindu', 'bible']):
        return "Spiritual"
    if any(w in text for w in ['grammar', 'vocabulary', 'spelling', 'structure', 'sentence']):
        return "Linguistic"
    return "Behavior"

def get_desc(cat, facet):
    descs = {
        "Emotion": f"How much emotion relates to {facet}.",
        "Safety": f"Any safety issues regarding {facet}.",
        "Cognitive": f"Logical reasoning about {facet}.",
        "Spiritual": f"Spiritual or cultural values in {facet}.",
        "Linguistic": f"Language structure about {facet}.",
        "Behavior": f"General behavior related to {facet}."
    }
    return descs.get(cat, f"Evaluate {facet}.")

def main():
    if not os.path.exists("Facets Assignment.csv"):
        print("Missing Facets Assignment.csv")
        return
        
    df = pd.read_csv("Facets Assignment.csv")
    first_col = df.columns[0]
    
    df['Cleaned_Facet'] = df[first_col].apply(clean_name)
    df['Category'] = df['Cleaned_Facet'].apply(get_category)
    df['Description'] = df.apply(lambda r: get_desc(r['Category'], r['Cleaned_Facet']), axis=1)
    
    df.to_csv("cleaned_facets.csv", index=False)
    print(f"Saved {len(df)} rows to cleaned_facets.csv")

if __name__ == "__main__":
    main()
