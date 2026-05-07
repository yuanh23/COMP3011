from typing import Dict, List

from src.indexer import Index, Indexer


class SearchEngine:
    def __init__(self, index: Index):
        self.index = index
        self.indexer = Indexer()

    def print_word(self, word: str) -> Dict:
        tokens = self.indexer.tokenize(word)

        if not tokens:
            return {}

        search_word = tokens[0]
        return self.index.get(search_word, {})

    def find(self, query: str) -> List[str]:
        query_words = self.indexer.tokenize(query)

        if not query_words:
            return []

        matching_pages = None

        for word in query_words:
            pages_for_word = set(self.index.get(word, {}).keys())

            if matching_pages is None:
                matching_pages = pages_for_word
            else:
                matching_pages = matching_pages.intersection(pages_for_word)

        if matching_pages is None:
            return []

        return sorted(matching_pages)