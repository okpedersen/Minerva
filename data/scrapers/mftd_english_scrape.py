import requests
import sys
import os.path as path

from bs4 import BeautifulSoup



def main():
    # story list page
    url = "http://www.mftd.org/search.php?action=search&act=show&langname=English&author=&verse=&hq=&tq="

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

    # parse all stories
    for i, link in enumerate(story_links, 1):
        if i < 230: continue
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
            with open('../raw/mftd_english/{:04d}.txt'.format(i), 'w') as f:
                f.write(text)



if __name__ == "__main__":
    main()
