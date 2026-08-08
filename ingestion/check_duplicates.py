import json

with open("data/processed/circular1.json", "r", encoding="utf-8") as f:
    d1 = json.load(f)

with open("data/processed/circular2.json", "r", encoding="utf-8") as f:
    d2 = json.load(f)

print("circular1 title snippet:")
print(d1["text"][:200])
print()
print("circular2 title snippet:")
print(d2["text"][:200])