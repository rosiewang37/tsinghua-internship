from query_glm_updated import GLMModel, query, msg
import json
import requests

# Load triples
input_path = r"C:\Tsinghua University Internship\assess_triplets\valid_triplets.json"
with open(input_path, "r", encoding="utf-8") as f:
    triples = json.load(f)

# Wikipedia context (optional)


def fetch_wikipedia_summary(entity: str) -> str:
    try:
        res = requests.get(
            f"https://en.wikipedia.org/api/rest_v1/page/summary/{entity}")
        return res.json().get("extract", "") if res.status_code == 200 else ""
    except:
        return ""

# Prompt builder


def build_validation_prompt(field, subj, rel, obj, context=""):
    return f"""
你是一个{field}领域专家。请判断下列三元组是否符合事实，并给出简洁的理由。
Triple: "{subj}" - "{rel}" - "{obj}"
Context: {context or "无"}

请严格输出 JSON：
{{ "is_valid": <true|false>, "reason": "<简洁说明>" }}
"""

# Validation using GLM-4-Air


def validate_triple(field, subj, rel, obj, use_context=True):
    context = fetch_wikipedia_summary(subj) if use_context else ""
    prompt = build_validation_prompt(field, subj, rel, obj, context)
    response, reason = query([msg("user", prompt)], model=GLMModel.GLM_4_Air)

    try:
        json_str = response[response.find("{"): response.rfind("}")+1]
        return json.loads(json_str)
    except Exception:
        return {"is_valid": False, "reason": f"无效输出: {response}"}


# Initialize counters
total_count = 0
true_count = 0
false_triplets = []

# Validate all and save
output_path = r"C:\Tsinghua University Internship\assess_triplets\accuracy_triples_validation_results.jsonl"
false_output_path = r"C:\Tsinghua University Internship\assess_triplets\false_accuracy_triplets.json"

with open(output_path, "w", encoding="utf-8") as fout:
    for subj, rel, obj in triples:
        total_count += 1
        result = validate_triple('生物', subj, rel, obj)
        record = {"triple": [subj, rel, obj], **result}
        fout.write(json.dumps(record, ensure_ascii=False) + "\n")
        print(record)

        if result["is_valid"]:
            true_count += 1
        else:
            false_triplets.append(record)

# Save false triplets to separate file
with open(false_output_path, "w", encoding="utf-8") as f_false:
    json.dump(false_triplets, f_false, ensure_ascii=False, indent=2)

# Calculate statistics
false_count = total_count - true_count
true_percentage = (true_count / total_count) * 100 if total_count > 0 else 0

# Print summary
print("\nValidation Summary:")
print(f"Total triplets: {total_count}")
print(f"True triplets: {true_count}")
print(f"False triplets: {false_count}")
print(f"Percentage of true triplets: {true_percentage:.2f}%")
print(f"False triplets saved to: {false_output_path}")

# Save valid triplets as list of lists (no reason, only triplet structure)
valid_triplets = []

# Re-read the output file line by line and collect valid ones
with open(output_path, "r", encoding="utf-8") as fin:
    for line in fin:
        try:
            record = json.loads(line)
            if record.get("is_valid") is True:
                valid_triplets.append(record["triple"])
        except:
            continue

# Save to JSON file
valid_output_path = r"C:\Tsinghua University Internship\assess_triplets\accurate_triplets.json"
with open(valid_output_path, "w", encoding="utf-8") as f_valid:
    json.dump(valid_triplets, f_valid, ensure_ascii=False, indent=2)

print(f"Valid triplets saved to: {valid_output_path}")

