from typing import Dict

import requests
import re

from bs4 import BeautifulSoup


class Scraper:
    def __init__(self, configuration: Dict):
        self.base_url = configuration.get("scraper").get("base_url")

    def run(self, include_legacy_files: bool = False):
        ascii_links = []

        res = requests.get(self.base_url)
        res.raise_for_status()
        page = res.text
        html = BeautifulSoup(page, "html.parser")

        all_links = html.find_all("a", href=True)

        if include_legacy_files:
            for link in all_links:
                if re.search(r"Exports/aers_ascii", link["href"]):
                    ascii_links.append(link["href"])

        for link in all_links:
            if re.search(r"Exports/faers_ascii", link["href"]):
                ascii_links.append(link["href"])

        return ascii_links
