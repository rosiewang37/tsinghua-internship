import json
import ast

def sort_triplets_into_relations_and_attributes(triplet_txt, relation_output_path, attribute_output_path):
    # Load the file content
    with open(triplet_txt, "r", encoding="utf-8") as f:
        content = f.read()

    # Split into lines
    parts = content.strip().split('\n')
    triplet_lists = []

    for part in parts:
        try:
            if part.strip().lower() == "null" or part.strip() == "":
                continue
            triplet_list = ast.literal_eval(part)
            if isinstance(triplet_list, list):
                triplet_lists.append(triplet_list)
        except Exception as e:
            print(f"Skipped invalid line (cannot parse): {part}\nError: {e}")

    # Flatten all triplets
    combined = []
    for triplets in triplet_lists:
        combined.extend(triplets)

    # Step 1: Collect all relation and attribute values
    relation_set = set()
    attribute_set = set()

    for item in combined:
        if len(item) == 3:
            keys = list(item.keys())
            second_key = keys[1]
            value = item[second_key]
            if second_key == "relation":
                relation_set.add(value)
            elif second_key == "attribute":
                attribute_set.add(value)

    # Step 2: Normalize and classify (with deduplication)
    relation_data = []
    attribute_data = []
    seen_relations = set()
    seen_attributes = set()
    unique_relations = set()  # ✅ NEW: collect unique relation strings
    unique_attributes = set()

    for item in combined:
        try:
            if len(item) != 3:
                print(f"Skipped malformed triplet (not 3 keys): {item}")
                continue

            keys = list(item.keys())
            first_key, second_key, third_key = keys[0], keys[1], keys[2]
            value = item[second_key]

            # Convert specific values into relation keys
            if value in {"含有", "属于"}:
                second_key = "relation"
            # Convert specific values into attribute keys
            if value in {"定义", "形状", "功能","位于"}:
                second_key = "attribute"

            normalized_key = None
            if second_key in ["relation", "attribute"]:
                normalized_key = second_key
            elif value in relation_set:
                normalized_key = "relation"
            elif value in attribute_set:
                normalized_key = "attribute"
            else:
                print(f"Skipped triplet with unknown relation/attribute: {item}")
                continue

            subject = item[first_key]
            obj = item[third_key]
            triplet_tuple = (subject, value, obj)

            if normalized_key == "relation":
                if triplet_tuple not in seen_relations:
                    relation_data.append(list(triplet_tuple))
                    seen_relations.add(triplet_tuple)
                    unique_relations.add(value)  # ✅ Add valid relation string
            elif normalized_key == "attribute":
                if triplet_tuple not in seen_attributes:
                    attribute_data.append(list(triplet_tuple))
                    seen_attributes.add(triplet_tuple)
                    unique_attributes.add(value)

        except Exception as e:
            print(f"Error processing triplet: {item}\n{e}")
            continue

    # Save outputs
    with open(relation_output_path, "w", encoding="utf-8") as f:
        json.dump(relation_data, f, ensure_ascii=False, indent=2)

    with open(attribute_output_path, "w", encoding="utf-8") as f:
        json.dump(attribute_data, f, ensure_ascii=False, indent=2)

    # ✅ Save count
    relation_count = len(relation_data)
    attribute_count = len(attribute_data)
    total_count = relation_count + attribute_count
    unique_relation_count = len(unique_relations)
    unique_attribute_count = len(unique_attributes)

    counts = {
        "relationCount": relation_count,
        "attributeCount": attribute_count,
        "totalCount": total_count,
        "uniqueRelationCount": unique_relation_count,
        "uniqueAttributeCount": unique_attribute_count
    }

    with open(r"C:\Tsinghua University Internship\triplets_to_graph\outputs\counts.json", "w", encoding="utf-8") as f:
        json.dump(counts, f)

    # ✅ Save unique relations
    with open(r"C:\Tsinghua University Internship\triplets_to_graph\outputs\unique_relations.json", "w", encoding="utf-8") as f:
        json.dump(sorted(list(unique_relations)), f, ensure_ascii=False, indent=2)
    
    with open(r"C:\Tsinghua University Internship\triplets_to_graph\outputs\unique_attributes.json", "w", encoding="utf-8") as f:
        json.dump(sorted(list(unique_attributes)), f, ensure_ascii=False, indent=2)

    print(f"Files saved:\n{relation_output_path}\n{attribute_output_path}")
    print(f"Relation triplets: {relation_count}")
    print(f"Attribute triplets: {attribute_count}")
    print(f"Total triplets: {total_count}")
    print("✅ Saved unique relation types to unique_relations.json")
    print("✅ Saved unique relation types to unique_attributes.json")
