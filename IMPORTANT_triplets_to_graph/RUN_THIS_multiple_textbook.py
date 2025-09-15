from combine_txt import combine_txt_in_folder
from sort_correction import sort_triplets_into_relations_and_attributes
from new_sort_node import sort_nodes_and_edges
from chart_content import extract_unique_attributes_with_counts, extract_unique_relations_with_counts

textbook_title = "人教版初中生物课本三元组"
version = "人教版"

combine_txt_in_folder(
    folder_path=rf"C:\Tsinghua University Internship\初中生物课本三元组\{version}",
    output_path=rf"C:\Tsinghua University Internship\初中生物课本三元组\{textbook_title}.txt"
)


sort_triplets_into_relations_and_attributes(rf"C:\Tsinghua University Internship\初中生物课本三元组\{textbook_title}.txt",
                                            rf"C:\Tsinghua University Internship\triplets_to_graph\{version}\outputs\{textbook_title}_relation.json",
                                            rf"C:\Tsinghua University Internship\triplets_to_graph\{version}\outputs\{textbook_title}_attribute.json")
sort_nodes_and_edges(rf"C:\Tsinghua University Internship\triplets_to_graph\{version}\outputs\{textbook_title}_relation.json",
                     rf"C:\Tsinghua University Internship\triplets_to_graph\{version}\outputs\{textbook_title}_attribute.json",
                     rf"C:\Tsinghua University Internship\triplets_to_graph\{version}\outputs\{textbook_title}_nodes.js",
                     rf"C:\Tsinghua University Internship\triplets_to_graph\{version}\outputs\{textbook_title}_edges.js")

extract_unique_attributes_with_counts(
    input_path=rf"C:\Tsinghua University Internship\triplets_to_graph\{version}\outputs\{textbook_title}_attribute.json",
    output_path=rf"C:\Tsinghua University Internship\triplets_to_graph\{version}\outputs\attributes_with_examples_and_counts.json"
)

extract_unique_relations_with_counts(
    input_path=rf"C:\Tsinghua University Internship\triplets_to_graph\{version}\outputs\{textbook_title}_relation.json",
    output_path=rf"C:\Tsinghua University Internship\triplets_to_graph\{version}\outputs\relations_with_examples_and_counts.json"
)