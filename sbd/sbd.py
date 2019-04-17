import argparse
import os
import pdfkit
import re
import validators
from robobrowser import RoboBrowser


def remove_non_ascii_chars(text):
    return re.sub(r'[^\x00-\x7F]+', ' ', text)


base_url = 'https://learning.oreilly.com'

parser = argparse.ArgumentParser(
    description='A small program to download books from Safari Books Online for offline storage.')
parser.add_argument('safari_book_url',
                    help='Safari book url, ex. https://www.safaribooksonline.com/library/view/book-name/book-code/')


def main():
    args = parser.parse_args()
    url = args.safari_book_url

    if not validators.url(url):
        print("URL is invalid, please pass proper URL")
        exit()

    cookies = [{ "BrowserCookie": "xxx" },
            { "csrfsafari": "xxx" },
            { "logged_in": "xxx" },
            { "user_identifier": "xxx" },
            { "sessionid": "xxx" }]

    br = RoboBrowser(parser='lxml')
    br.open(url)

    for cookie in cookies:
        br.session.cookies.update(cookie)

    error_list = br.parsed.find_all("ul", class_='errorlist')

    if error_list.__len__() != 0:
        print("Invalid cookies: " + error_list[0].contents[0].text)
        exit()
    else:
        print("Valid cookies")

    complete_book = ''

    ## reopen URL with new cookies
    br.open(url)
    ## include TOC page
    content = br.parsed.find("section", {"class": "detail-book"})
    for img in content.findAll('img'):
        img['src'] = img['src'].replace("/library/", base_url + "/library/")
    for links in content.findAll('a'):
        links['href'] = links['href'].replace("/library/", base_url + "/library/")
    complete_book += remove_non_ascii_chars(content.__str__())

    url_list = []

    for chapter in br.parsed.find_all("a", class_='t-chapter'):
        url_list.append(chapter['href'])

    author = br.parsed.find('meta', {"property": 'og:book:author'})['content']
    title = br.parsed.find('meta', {"itemprop": 'name'})['content']
    author_title = author + ' - ' + title
    filename = str(author_title) + '.pdf'

    print('Downloading ' + author_title)
    # fetch all the book pages
    for x in range(0, url_list.__len__()):
        print("Downloading chapter " + str(x + 1) + " out of " + str(url_list.__len__()))
        br.open(url_list[x])
        content = br.parsed.find("div", {"id": "sbo-rt-content"})
        for img in content.findAll('img'):
            img['src'] = img['src'].replace("/library/", base_url + "/library/")
        for links in content.findAll('a'):
            links['href'] = links['href'].replace("/library/", base_url + "/library/")
        complete_book += remove_non_ascii_chars(content.__str__())

    print("Generating pdf...")
    pdfkit.from_string(complete_book, filename, options=dict(encoding="utf-8", quiet=''))
    print("Done! Saved as '" + filename + "'")
