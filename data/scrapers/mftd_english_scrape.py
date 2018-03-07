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


def main():

    url = "http://www.mftd.org/search.php?action=search&act=show&langname=English&author=&verse=&hq=&tq="
    all_links = find_story_links_on_page(url)
    url = "http://www.mftd.org/search.php?action=search&act=show&langname=English&author=&verse=1&hq=&tq="
    verse_links = find_story_links_on_page(url)
    story_links = set(all_links) - set(verse_links)

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
            with open('../raw/mftd_english/{:04d}.txt'.format(i), 'w') as f:
                f.write(text)



if __name__ == "__main__":
    main()
