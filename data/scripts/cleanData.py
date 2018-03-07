import sys
import os

# Alt til lowercase
# Mellomrom foran tegn
# Fjerne newline
# Filer ../scrapers/text/text*.txt (1-209)

SPECIAL_CHARS = ('.', ',', '"', ':', ';', '!', '?')

def clean_text_from_file(filename):
    with open(filename) as f:
        text = f.read().replace('\n', ' ')
        for c in SPECIAL_CHARS:
            text = text.replace(c, " "+c+" ")
        text = " ".join(text.split())
    return text


def main():
    if len(sys.argv) < 3:
        print("./script [input location] [output location]")
    in_path = sys.argv[1]
    out_path = sys.argv[2]


    if os.path.isfile(in_path):
        clean_text = clean_text_from_file(in_path)
        with open(out_path) as f:
            f.write(clean_text)
    else:
        if not os.path.isdir(out_path):
            print("Invalid directory specified!")
        for filename in os.listdir(in_path):
            clean_text = clean_text_from_file(os.path.join(in_path, filename))
            _, name = os.path.split(filename)
            with open(os.path.join(out_path, name), 'w') as f:
                f.write(clean_text)



if __name__ == '__main__':
    main()
