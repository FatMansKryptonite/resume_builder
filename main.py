import subprocess


def main():
    subprocess.call(['pdflatex', 'cv/cv_7.tex'])


if __name__ == '__main__':
    main()
