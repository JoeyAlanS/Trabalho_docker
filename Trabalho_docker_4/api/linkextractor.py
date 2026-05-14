#!/usr/bin/env python3

import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def extract_links(url):
    res = requests.get(url, timeout=10, headers=HEADERS)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")
    base = url
    links = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if not href:
            continue
        links.append({
            "text": " ".join(link.text.split()) or "[IMG]",
            "href": urljoin(base, href),
        })
    return links


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("\nUsage:\n\t{} <URL>\n".format(sys.argv[0]))
        sys.exit(1)
    for link in extract_links(sys.argv[-1]):
        print("[{}]({})".format(link["text"], link["href"]))
