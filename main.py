import subprocess


def main():
    for document in ['cv', 'cover_letter']:
        subprocess.call(['pdflatex',
                         '-output-directory', 'output',
                         '-aux-directory', 'auxiliary_output',
                         f'{document}.tex'])


if __name__ == '__main__':
    main()
