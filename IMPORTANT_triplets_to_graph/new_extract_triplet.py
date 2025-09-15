# extract predicate (attribute and relation)
import re
from thefuzz import fuzz
from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np
import logging
import json

from query_glm_updated import GLMModel, async_create_batch, async_result_batch, msg


logger = logging.getLogger(__name__)

triplets_relation = []
triplets_attribute = []
# 提取三元组


def batch_extract_triplets_with_ChatGLM(field, texts, task=None):

    global triplets_relation, triplets_attribute

    messages_list = [
        [
            msg('user', (f'你是一个{field}领域的大师。'
                         '请详细分析下面将要给出的文本，并从中**仅提取所有语义明确、重点表达的知识三元组**'
                         '###- 忽略所有题目（包括计算题、思考题、证明题、习题答案等）和图示描述###\n'
                         '###- 忽略目录、前言、章节标题以及课本中的出版信息（如书名、出版社、编者、版本号等）。\n'
                         '要求：\n '
                         '1. 三元组提取标准\n'
                         '- 主语（subject）：文本中被清晰描述、定义或强调说明的术语或概念，通常是句子的主语,不能包含“部分”“其他”“主要”等修饰词。\n'
                         '- 谓语（predicate）可以分为：\n'
                         '- 关系（relation）：表示主语与宾语之间的结构、组成、分类、归属、连接、运输、调控等功能或结构关系。例如“属于”、“构成”、“含有”、“连接”、“分泌”、“来源于”、“有”等。“位于”“覆盖在”不是关系。\n'
                            '- 如果关系是“有”，请将其替换为“含有”；如果是“没有”，请替换为“不包含”。\n"'
                            '- 单独的“由”不是关系，但像“由...构成”、“由...发展而来”这类完整的短语可以视为关系。\n'
                         '- 属性（attribute）表示主语可测量的具体特征,明确的空间位置或客观的物理/化学特性，如“属性是”、“定义是”、“覆盖在”、“颜色是”、“数量为”、“功能是”、“位于”、“形状为”等。\n'
                         '- 如果句子是“X指…”或“X是指…”这类定义型句子，请提取为：{"subject": X, "attribute": "定义", "object": Y}，此时且仅此时Y可以是一个长句\n'
                         '- 宾语（object）：必须是一个简洁、独立的、生物学术语,不能包含“部分”“其他”“主要”等修饰词,不可为长短语、修饰语、并列结构、抽象词或动词短语。\n'
                         
                         '### 2. 严格禁止提取的类型\n'
                         '1 模糊关系(必须拒绝):\n'
                         '   - "X与Y有关联"\n'
                         '   - "X对Y很重要"\n'
                         '   - "X数量很多"\n'
                         '   - "X有重要功能"\n'
                         '   (未说明具体关联/数量/功能的都不可接受)\n'
                         '2 抽象描述(必须拒绝):\n'
                         '   - "X由多种成分组成"\n'
                         '   - "Y分布在不同部位"\n'
                         '   (未明确成分/部位的具体信息)\n\n'
                         '3. 拆分与简化\n'
                         '- 如果句子中提到多个尾实体（如“表皮、真皮、皮下组织”），请拆分为多个三元组，尾实体需简化为独立术语。\n'
                         '4. 输出格式\n'
                         '- 如果谓语为关系（relation）类型，请输出：\n'
                         '  {"subject": 主语, "relation": 关系, "object": 宾语}\n'
                         '- 如果谓语为属性（attribute）类型，请输出：\n'
                         '  {"subject": 主语, "attribute": 属性, "object": 宾语}\n'
                         '- 所有输出的三元组必须严格包含三项:"subject"、"relation"或"attribute"、"object"，缺少任何一项都不被接受\n'
                         '- 字段名必须严格为 "subject"、"relation" 或 "attribute"、"object"，不能有遗漏，不能拼写错误，不能是其他字段名。\n'
                         '5. 注意事项\n'
                         '- 严格依据原文，只提取语义明确、结构完整的三元组。\n'
                         '请现在立即根据上面的指令提取三元组，直接输出完整的json内容，不要输出任何额外信息。\n'
                         f'输入文本：\n{text}'))
            #  '1. 提取的三元组必须是原文中明确描述、重点介绍的，不要擅自归纳总结；\n'
            #  '2. 如果一个句子中提到了多个相关尾实体（如“人体皮肤的表面以及体内管腔的内表面和某些脏器的表面”），请拆分成多个三元组，并将每个尾实体简化为核心术语（如“人体皮肤”、“体内管腔”、“脏器”）；\n'
            # '3. 所有尾实体必须简洁、具体，避免使用长句或并列结构作为尾实体；\n'
            # '4. 不要提取那些仅表达“有关系”、“相关”等模糊关系的句子；\n'
            # '5. 忽略所有题目（包括计算题、思考题、证明题、习题答案等）和图示描述；\n'

            #  '其中：\n'
            #  '主语（subject）是文本中被清晰描述、定义或强调说明的术语或概念，通常是信息的主题或主语。\n'
            #  '宾语（object）是与头实体存在明确、具体语义关系的另一个术语或概念，必须是一个简洁的、具有独立意义的名词或名词短语，单个术语（不可为长短语或并列结构）\n'
            #  '谓语（predicate）可以是具体、明确的关系（relation）或者属性（attribute），其中关系是表示主语和宾语之间的结构、组成、功能或分类等关系，例如“属于”、“连接”、“包括”、“由...组成”、“通过...运输”、“来源于”等，属性是当宾语表示主语本身的特征或状态，例如大小、颜色、位置、温度、数量、作用、形状等。\n\n'
            #  '如果predicate是relation，输出格式：{"subject": 主语, "relation": 关系, "object": 宾语}，如果predicate是attribute，输出格式：{"subject": 主语, "attribute": 属性, "object": 宾语}\n'
            #  '请注意：\n'
            #  '- 只提取在原文中表达清晰、语义关系明确的三元组。\n'
            #  '- 不提取表达模糊或没有具体关系的语句（例如“X 与 Y 有密切关系”“X数量很多”不构成可接受的三元组）。\n'
            #  '请注意每次输出时，必须输出完整的json内容，同时不要输出其他内容。\n\n'
        ] for text in texts
    ]

    async_id_list = async_create_batch(messages_list, GLMModel.GLM_4_Air, task)
    model_response_texts = async_result_batch(async_id_list)

    for idx, response in enumerate(model_response_texts):
        if response is None:
            # triplets_rel.append([])
            continue

        # Process relation triplets
        for pair in re.findall(
                r'\{.*?"subject".*?"relation".*?"object".*?}',
                response,
                re.MULTILINE | re.DOTALL
        ):
            try:
                pair = json.loads(pair)
                if fuzz.partial_token_set_ratio(pair['object'], texts[idx]) >= 70:
                    triplets_relation.append(
                        [pair['subject'], pair['relation'], pair['object']])
            except Exception as e:
                print(e, pair)

        # Process attribute triplets
        for pair in re.findall(
                r'\{.*?"subject".*?"attribute".*?"object".*?}',
                response,
                re.MULTILINE | re.DOTALL
        ):
            try:
                pair = json.loads(pair)
                if fuzz.partial_token_set_ratio(pair['object'], texts[idx]) >= 70:
                    triplets_attribute.append(
                        [pair['subject'], pair['attribute'], pair['object']])
            except Exception as e:
                print(e, pair)
    #     triplets_rel_tmp = []

    #     for pair in re.findall(
    #             r'\{.*?"subject".*?"relation".*?"object".*?}',
    #             response,
    #             re.MULTILINE | re.DOTALL
    #     ):
    #         try:
    #             pair = json.loads(pair)
    #         except Exception as e:
    #             print(e, pair)
    #             continue
    #         # check def similarity
    #         if fuzz.partial_token_set_ratio(pair['object'], texts[idx]) < 70:
    #             continue
    #         triplets_rel_tmp.append([pair['subject'], pair['relation'], pair['object']])

    #     triplets_rel.append(triplets_rel_tmp)
    # return triplets_rel


# import textbook content
with open(r"C:\Tsinghua University Internship\build_KG\sample_textbook.json", "r", encoding="utf-8") as f:
    sample_textbook = json.load(f)

# extract triplets_rel from textbook
batch_extract_triplets_with_ChatGLM('生物', sample_textbook)
print(f'triplets_relation: {triplets_relation}')
print(f'triplets_attribute: {triplets_attribute}')

# Save triplets_relation to JSON
with open("new_sample_triplets_relation.json", "w", encoding="utf-8") as f:
    json.dump(triplets_relation, f, ensure_ascii=False, indent=2)

print("✅ triplets_relation saved to new_sample_triplets_relation.json")

# Save triplets_attribute to JSON
with open("new_sample_triplets_attribute.json", "w", encoding="utf-8") as f:
    json.dump(triplets_attribute, f, ensure_ascii=False, indent=2)

print("✅ triplets_attribute saved to new_sample_triplets_attribute.json")
