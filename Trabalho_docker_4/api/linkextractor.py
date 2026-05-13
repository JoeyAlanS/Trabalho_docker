#!/usr/bin/env python

import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def extract_links(url):
    try:
        # [FIX] Adicionar timeout obrigatório
        res = requests.get(url, timeout=10)
        res.raise_for_status()  # Falha se não for 200
        
        soup = BeautifulSoup(res.text, "html.parser")
        base = url
        # TODO: Update base if a <base> element is present with the href attribute
        links = []
        for link in soup.find_all("a"):
            href = link.get("href")
            # [FIX] Apenas adicionar se href existir
            if href:
                links.append({
                    "text": " ".join(link.text.split()) or "[IMG]",
                    "href": urljoin(base, href)
                })
        return links
    except Exception as e:
        # [FIX] Log e retorna lista vazia em vez de 500
        print(f"[EXTRACTOR ERROR] {url}: {type(e).__name__}: {str(e)}", file=sys.stderr)
        return []

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("\nUsage:\n\t{} <URL>\n".format(sys.argv[0]))
        sys.exit(1)
    for link in extract_links(sys.argv[-1]):
        print("[{}]({})".format(link["text"], link["href"]))