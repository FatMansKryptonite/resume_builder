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
    keyword_dict = {key: [key] for key in keys}

    current_key = None
    for elem in match:
        if elem in keys:
            # If the element is a key, switch the current key
            current_key = elem
        elif current_key:
            # If there is a current key, append the element to its list
            keyword_dict[current_key].append(elem)

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



