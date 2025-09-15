import json
from collections import Counter

def extract_unique_attributes_with_counts(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        triplets = json.load(f)

    seen_attributes = set()
    attribute_counter = Counter()
    examples = {}

    # Count attributes and collect example
    for triplet in triplets:
        if len(triplet) != 3:
            continue
        subject, attr, obj = triplet
        attribute_counter[attr] += 1
        if attr not in seen_attributes:
            seen_attributes.add(attr)
            examples[attr] = f"{subject} {attr} {obj}"

    output = []
    for attr in seen_attributes:
        output.append({
            "attribute": attr,
            "count": attribute_counter[attr],
            "example": examples[attr]
        })

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"✅ Attributes with counts saved to: {output_path}")


def extract_unique_relations_with_counts(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        triplets = json.load(f)

    seen_relations = set()
    relation_counter = Counter()
    examples = {}

    # Count relations and collect example
    for triplet in triplets:
        if len(triplet) != 3:
            continue
        subject, rel, obj = triplet
        relation_counter[rel] += 1
        if rel not in seen_relations:
            seen_relations.add(rel)
            examples[rel] = f"{subject} {rel} {obj}"

    output = []
    for rel in seen_relations:
        output.append({
            "relation": rel,
            "count": relation_counter[rel],
            "example": examples[rel]
        })

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"✅ Relations with counts saved to: {output_path}")
