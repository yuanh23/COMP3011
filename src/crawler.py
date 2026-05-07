import time
from dataclasses import dataclass
from typing import List, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


@dataclass
class Page:
    url: str
    text: str


class Crawler:
    def __init__(self, start_url: str, delay: int = 6):
        self.start_url = start_url
        self.delay = delay

    def fetch_page(self, url: str) -> str:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text

    def parse_page(self, url: str, html: str) -> tuple[Page, Optional[str]]:
        soup = BeautifulSoup(html, "html.parser")

        quote_blocks = soup.select(".quote")
        page_parts: List[str] = []

        for quote in quote_blocks:
            quote_text = quote.select_one(".text")
            author = quote.select_one(".author")
            tags = quote.select(".tag")

            if quote_text:
                page_parts.append(quote_text.get_text(" ", strip=True))

            if author:
                page_parts.append(author.get_text(" ", strip=True))

            for tag in tags:
                page_parts.append(tag.get_text(" ", strip=True))

        page = Page(url=url, text=" ".join(page_parts))

        next_link = soup.select_one("li.next a")
        next_url = urljoin(url, next_link["href"]) if next_link else None

        return page, next_url

    def crawl(self) -> List[Page]:
        pages: List[Page] = []
        current_url: Optional[str] = self.start_url

        while current_url:
            html = self.fetch_page(current_url)
            page, next_url = self.parse_page(current_url, html)
            pages.append(page)

            if next_url:
                time.sleep(self.delay)

            current_url = next_url

        return pages