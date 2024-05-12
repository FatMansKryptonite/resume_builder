import subprocess
import json
import os
import utils
from datetime import date


def make_info_dict(tag_type: str, name: str, match: list) -> dict:
    with open(f'content_files/{tag_type}_files/{name}.json') as file:
        info_dict = json.load(file)

    keyword_dict = utils.get_tiered_matches(info_dict.keys(), match)
    for key, keyword_trees in keyword_dict.items():
        if len(keyword_trees) == 0:
            info_dict[key] = '' if info_dict[key] is None else str(info_dict[key])
            continue

        entries = []
        for keyword_tree in keyword_trees:
            entries.append(utils.get_nested_item(info_dict, keyword_tree))

        entry = r' \newpar '.join(entries)
        info_dict[key] = entry

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


def cvlistitem_info_list(info_dict: dict) -> list:
    info_list = [
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
    elif tag_type == 'cvlistitem':
        info_list = cvlistitem_info_list(info_dict)

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
    applications = ['novo_holdings_machine_learning_engineer']
    for application in applications:
        applicaiton_dir = os.path.join('applications', application)
        for filepath_str in os.listdir(applicaiton_dir):

            # Only treat .tex documents
            if not filepath_str.endswith('.tex'):
                continue

            # Read and parse template
            with open(os.path.join(applicaiton_dir, filepath_str), encoding='utf-8') as file:
                parsed_file_str = parse_tex_template(file.read())

            # Save parsed .tex document
            with open(os.path.join('tex_files', 'main.tex'), 'w') as file:
                file.write(parsed_file_str)

            # Render file
            file_name = filepath_str.split('.')[0]
            todays_date = date.today().strftime("%Y-%m-%d")
            subprocess.call(
                ['pdflatex',
                    '-output-directory', f'../{applicaiton_dir}',
                    '-aux-directory', '../auxiliary_output',
                    '-jobname', f'Eriksson, Ivar - {file_name} ({todays_date})',
                    'main.tex'],
                cwd='tex_files'
            )


if __name__ == '__main__':
    main()
