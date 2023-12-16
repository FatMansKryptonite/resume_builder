import subprocess
import re
import json
import os


def parse_cventry(match: list) -> str:
    with open(f'input_files/{match[0]}.json') as file:
        info_dict = json.load(file)

    info_list = [
        f"{info_dict['start']}--{info_dict['end']}",
        info_dict['name'],
        info_dict['title'],
        '',
        '',
        rf"\input{{../input_files/{info_dict['text'][match[1]]}}}"
    ]

    # TODO Clean up
    # Makes a LaTeX compatible string...
    input_str = r'\cventry' + ''.join([f'{{{info}}}' for info in info_list])

    return input_str


def parse_tex_template(file_str: str) -> str:

    pattern = r'(€(\w+):(\w+)(?:\[(\w+)\])*€)'
    matches = re.findall(pattern, file_str)

    for match in matches:
        if match[1] == 'cventry':
            input_str = parse_cventry(match[2:])

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
