import requests
import sys
import os.path as path

from bs4 import BeautifulSoup


def find_story_links_on_page(url):
    # request page
    r = requests.get(url)
    if (r.status_code != 200):
        print("Error! Status code {} when fetching list of stories.".format(r.status.code))
        sys.exit(1)

    soup = BeautifulSoup(r.content, 'html5lib')

    anchors = soup.find_all('a')
    story_links = []
    for a in anchors:
        if "action=story" in a['href']:
            story_links.append(a['href'])

    return story_links


def mftd_scrape(language=""):

    # get the root directory of the Minerva project
    # e.g. /something/something/Minerva
    basepath = path.normpath(path.realpath(__file__))
    while path.basename(basepath) != "Minerva":
        basepath = path.dirname(basepath)

    # Check for supported language
    language = language.lower()
    if language not in ("norwegian", "english"):
        print("Possibly unsupported language")
        print("Exiting...")
        sys.exit(1)

    # Get URLs to story pages
    url = "http://www.mftd.org/search.php?action=search&act=show&langname={ln}&author=&verse=&hq=&tq=".format(ln=language.capitalize())
    all_links = find_story_links_on_page(url)
    url = "http://www.mftd.org/search.php?action=search&act=show&langname={ln}&author=&verse=1&hq=&tq=".format(ln=language.capitalize())
    verse_links = find_story_links_on_page(url)
    story_links = sorted(list(set(all_links) - set(verse_links)))


    # parse all stories
    for i, link in enumerate(story_links, 1):
        url = "http://www.mftd.org/{}".format(link)
        r = requests.get(url)
        if (r.status_code != 200):
            print("Error! Status code {} when fetching story {}".format(r.status.code), url)
            sys.exit(1)

        print("{}, {}".format(i, url))

        soup = BeautifulSoup(r.content, 'html5lib')

        story_tag = soup.find('div', id="story").find('div', id="story")
        if story_tag == None:
            print("Found None-tag! Ignoring..")
        else:
            text = story_tag.get_text()
            for br in story_tag.find_all("br"):
                br.replace_with("\n")
            text = "\n".join(p.get_text() for p in story_tag.find_all('p'))
            with open(path.join(basepath, 'data', 'raw', 'mftd_{}'.format(language), '{:04d}.txt'.format(i)), 'w') as f:
                print(f.name)
                f.write(text)

