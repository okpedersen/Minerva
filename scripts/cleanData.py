
# Alt til lowercase
# Mellomrom foran tegn
# Fjerne newline
# Filer ../scrapers/text/text*.txt (1-209)

SPECIAL_CHARS = ('.', ',', '"', ':', ';', '!', '?')

def main():
    for i in range(1, 210):
        with open('../scrapers/text/text' + str(i) + '.txt') as f:
            text = f.read()
            text = text.lower()
            text = text.replace('\n', ' ')
            for c in SPECIAL_CHARS:
                text = text.replace(c, " "+c+" ")
            text = " ".join(text.split())
            with open('../clean_data/text/text' + str(i) + '.txt', 'w') as out:
                out.write(text)







if __name__ == '__main__':
    main()
