import argparse
import json

from src.crawler import Crawler
from src.indexer import Indexer
from src.search import SearchEngine


START_URL = "https://quotes.toscrape.com/"


def print_help() -> None:
    print("Available commands:")
    print("  build              Crawl website, build index, and save it")
    print("  load               Load index from data/index.json")
    print("  print <word>       Print inverted index for a word")
    print("  find <query>       Find pages containing all query terms")
    print("  help               Show this help message")
    print("  exit               Exit the program")


def main() -> None:
    parser = argparse.ArgumentParser(description="COMP3011 Search Engine Tool")
    parser.add_argument(
        "--delay",
        type=int,
        default=6,
        help="Delay between requests in seconds. Use 6 for coursework demo.",
    )
    args = parser.parse_args()

    indexer = Indexer()
    search_engine = None

    print("COMP3011 Search Engine Tool")
    print("Type 'help' to see available commands.")

    while True:
        command = input("> ").strip()

        if command == "":
            print("Please enter a command.")
            continue

        parts = command.split()
        action = parts[0].lower()
        arguments = parts[1:]

        try:
            if action == "build":
                crawler = Crawler(START_URL, delay=args.delay)
                pages = crawler.crawl()
                index = indexer.build_index(pages)
                indexer.save()
                search_engine = SearchEngine(index)
                print(f"Built index for {len(pages)} pages.")

            elif action == "load":
                index = indexer.load()
                search_engine = SearchEngine(index)
                print("Index loaded successfully.")

            elif action == "print":
                if search_engine is None:
                    print("No index loaded. Run build or load first.")
                    continue

                if not arguments:
                    print("Usage: print <word>")
                    continue

                result = search_engine.print_word(arguments[0])
                print(json.dumps(result, indent=2))

            elif action == "find":
                if search_engine is None:
                    print("No index loaded. Run build or load first.")
                    continue

                query = " ".join(arguments)

                if not query:
                    print("Usage: find <query>")
                    continue

                results = search_engine.find(query)

                if results:
                    for url in results:
                        print(url)
                else:
                    print("No pages found.")

            elif action == "help":
                print_help()

            elif action in {"exit", "quit"}:
                print("Goodbye.")
                break

            else:
                print(f"Unknown command: {action}")
                print_help()

        except Exception as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()