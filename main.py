import subprocess
import json
import os
import utils


def make_info_dict(tag_type: str, name: str, match: list) -> dict:
    with open(f'{tag_type}_files/{name}.json') as file:
        info_dict = json.load(file)

    keyword_dict = utils.get_tiered_matches(info_dict.keys(), match)
    for key, keywords in keyword_dict.items():
        info_dict[key] = utils.get_nested_item(info_dict, keywords)
        info_dict[key] = '' if info_dict[key] is None else str(info_dict[key])  # Parse None values

    return info_dict


def cventry_info_list(info_dict: dict) -> list:
    info_list = [
        f"{info_dict['start']}--{info_dict['end']}",
        info_dict['name'],
        info_dict['title'],
        info_dict['optional_1'],
        info_dict['optional_2'],
        info_dict['description']
    ]
    return info_list


def cvitem_info_list(info_dict: dict) -> list:
    info_list = [
        info_dict['name'],
        info_dict['description']
    ]
    return info_list


def parse_tag(tag_type: str, match: list) -> str:
    info_dict = make_info_dict(tag_type, match[0], match[1:])

    info_list = []
    if tag_type == 'cvitem':
        info_list = cvitem_info_list(info_dict)
    elif tag_type == 'cventry':
        info_list = cventry_info_list(info_dict)

    # TODO Clean up
    # Makes a LaTeX compatible string...
    input_str = rf'\{tag_type}' + ''.join(['{' + info + '}' for info in info_list])

    return input_str


def parse_tex_template(file_str: str) -> str:
    matches = utils.get_keywords(file_str)

    for match in matches:
        input_str = parse_tag(match[1], match[2:])
        file_str = file_str.replace(match[0], input_str)

    return file_str


def main():
    documents = ['cv_new.tex']
    for document in documents:
        with open(document, encoding='utf-8') as file:
            parsed_file_str = parse_tex_template(file.read())

        with open(os.path.join('tex_files', document), 'w') as file:
            file.write(parsed_file_str)

        subprocess.call(
            ['pdflatex',
                '-output-directory', '../output',
                '-aux-directory', '../auxiliary_output',
                f'{document}'],
            cwd='tex_files'
        )


if __name__ == '__main__':
    main()
