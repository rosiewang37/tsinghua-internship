import json
with open(r"C:\Tsinghua University Internship\triplets_to_graph\人教版\outputs\人教版初中生物课本三元组_relation.json", "r", encoding="utf-8") as f:
    triplets = json.load(f)

target = "细菌"

# Find and print triplets containing the target
matched_triplets = [triplet for triplet in triplets if target in triplet]

num_triplets = 0

for triplet in matched_triplets:
    print(triplet)
    num_triplets += 1
    
print(f'Number of triplets that contains {target}: {num_triplets}')