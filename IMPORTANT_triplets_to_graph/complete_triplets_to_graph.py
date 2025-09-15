from sort_correction import sort_triplets_into_relations_and_attributes
from new_sort_node import sort_nodes_and_edges

textbook_title = "北师大七年级上册"
sort_triplets_into_relations_and_attributes(rf"C:\Tsinghua University Internship\biology_textbook\{textbook_title}.txt",
                                            rf"C:\Tsinghua University Internship\triplets_to_graph\outputs\{textbook_title}_relation.json",
                                            rf"C:\Tsinghua University Internship\triplets_to_graph\outputs\{textbook_title}_attribute.json")
sort_nodes_and_edges(rf"C:\Tsinghua University Internship\triplets_to_graph\outputs\{textbook_title}_relation.json",
                     rf"C:\Tsinghua University Internship\triplets_to_graph\outputs\{textbook_title}_attribute.json",
                     rf"C:\Tsinghua University Internship\triplets_to_graph\outputs\{textbook_title}_nodes.js",
                     rf"C:\Tsinghua University Internship\triplets_to_graph\outputs\{textbook_title}_edges.js")
