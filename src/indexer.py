import json
import re
from pathlib import Path
from typing import Dict, List

from src.crawler import Page


Index = Dict[str, Dict[str, Dict[str, List[int] | int]]]


class Indexer:
    def __init__(self) -> None:
        self.index: Index = {}

    def tokenize(self, text: str) -> List[str]:
        return re.findall(r"[a-zA-Z0-9]+", text.lower())

    def build_index(self, pages: List[Page]) -> Index:
        self.index = {}

        for page in pages:
            words = self.tokenize(page.text)

            for position, word in enumerate(words):
                if word not in self.index:
                    self.index[word] = {}

                if page.url not in self.index[word]:
                    self.index[word][page.url] = {
                        "frequency": 0,
                        "positions": [],
                    }

                self.index[word][page.url]["frequency"] += 1
                self.index[word][page.url]["positions"].append(position)

        return self.index

    def save(self, file_path: str = "data/index.json") -> None:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", encoding="utf-8") as file:
            json.dump(self.index, file, indent=2)

    def load(self, file_path: str = "data/index.json") -> Index:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                "Index file not found. Run the build command first."
            )

        with path.open("r", encoding="utf-8") as file:
            self.index = json.load(file)

        return self.index