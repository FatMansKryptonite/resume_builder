import re


def get_nested_item(nested_dict: dict, keywords: list) -> object:
    current_level = nested_dict
    for keyword in keywords:
        if keyword in current_level:
            current_level = current_level[keyword]
        else:
            raise ValueError("Keywords do not fit json dictionary")
    return current_level


def get_tiered_matches(keys: list, match: list) -> dict:
    keyword_dict = {key: [] for key in keys}

    key_mask = [elem in keys for elem in match]
    keyword_tree = None
    for i in range(len(match)):
        is_key = key_mask[i]
        elem = match[i]

        if is_key:
            keyword_tree = [elem]
        else:
            keyword_tree.append(elem)

        if i+1 == len(match) or key_mask[i+1]:
            keyword_dict[keyword_tree[0]].append(keyword_tree)

    return keyword_dict


def get_keywords(file_str: str) -> list:
    pattern = r'(€\w+:\w+(?:\[\w+(?::\w+)+\])*€)'
    tags = re.findall(pattern, file_str)

    all_keywords = []
    for tag in tags:
        keywords = [tag]

        pattern = r'(\w+)'
        keywords += re.findall(pattern, tag)

        all_keywords += [keywords]

    return all_keywords
