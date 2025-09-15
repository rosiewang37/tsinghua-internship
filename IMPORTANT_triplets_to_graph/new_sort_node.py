import json

def sort_nodes_and_edges(relation_input_path, attribute_input_path, js_relation_output, js_attribute_output):
    # Load JSON data
    with open(relation_input_path, "r", encoding="utf-8") as f:
        triplets_relation = json.load(f)

    # Load attribute JSON data
    with open(attribute_input_path, "r", encoding="utf-8") as f:
        triplets_attribute = json.load(f)

    # Prepare structures
    node_dict = {}
    edges = []

    for triplet in triplets_relation:
        head, relation, tail = triplet
        # Ensure head exists in node_dict
        if head not in node_dict:
            node_dict[head] = {"id": head, "name": head, "info": ""}
        if tail not in node_dict:
            node_dict[tail] = {"id": tail, "name": tail, "info": ""}

        edges.append({
            "source": head,
            "target": tail,
            "relation": relation
        })

    for triplet in triplets_attribute:
        head, attribute, tail = triplet

        # Ensure head exists in node_dict
        if head not in node_dict:
            node_dict[head] = {"id": head, "name": head, "info": ""}

        node_dict[head]["info"] += f"{attribute}: {tail}\n"

    # Convert node_dict to list of flat node dictionaries
    nodes = list(node_dict.values())
    # print(nodes)


    def dict_to_js(d):
        return "{ " + ", ".join(f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in d.items()) + " }"


    js_nodes_array = "[\n" + ",\n".join(dict_to_js(d) for d in nodes) + "\n]"
    # Save as JavaScript file
    with open(js_relation_output, "w", encoding="utf-8") as f:
        f.write("const nodes = " + js_nodes_array + ";")
    print("✅ JavaScript head written to new_nodes.js")

    js_edges_array = "[\n" + ",\n".join(dict_to_js(d) for d in edges) + "\n]"
    with open(js_attribute_output, "w", encoding="utf-8") as f:
        f.write("const edges = " + js_edges_array + ";")
    print("✅ JavaScript head written to new_edges.js")
