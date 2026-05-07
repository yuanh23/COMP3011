# COMP3011 Search Engine Tool

This project is a Python command-line search engine tool for COMP3011 Coursework 2.

The tool crawls the target website, builds an inverted index, stores the index in the file system, and allows users to search for pages containing specific query terms.

Target website:

https://quotes.toscrape.com/

## Features

- Crawls quote pages from the target website
- Respects a 6-second politeness window between requests
- Builds an inverted index of words found on each page
- Stores word statistics including frequency and positions
- Supports case-insensitive search
- Saves and loads the index from `data/index.json`
- Provides an interactive command-line interface
- Includes unit tests for crawler parsing, indexing, and searching

## Project Structure

```text
COMP3011/
  src/
    __init__.py
    crawler.py
    indexer.py
    search.py
    main.py
  tests/
    test_crawler.py
    test_indexer.py
    test_search.py
  data/
    .gitkeep
  .gitignore
  requirements.txt
  README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/yuanh23/COMP3011.git
cd COMP3011
```

Create a virtual environment:

```bash
python3.12 -m venv .venv
```

Install the required dependencies:

```bash
.venv/bin/python -m pip install -r requirements.txt
```

## Dependencies

The project uses the following Python libraries:

- `requests` for sending HTTP requests
- `beautifulsoup4` for parsing HTML pages
- `pytest` for running the test suite

These dependencies are listed in `requirements.txt`.

## Usage

Run the command-line search tool:

```bash
.venv/bin/python -m src.main
```

For faster testing during development, the request delay can be set to 0:

```bash
.venv/bin/python -m src.main --delay 0
```

For the coursework demonstration, the default 6-second delay should be used:

```bash
.venv/bin/python -m src.main
```

After starting the program, the following prompt will appear:

```text
COMP3011 Search Engine Tool
Type 'help' to see available commands.
>
```

## Commands

### Build

The `build` command crawls the target website, builds the inverted index, and saves it to `data/index.json`.

```text
build
```

Example output:

```text
Built index for 10 pages.
```

### Load

The `load` command loads a previously saved index from `data/index.json`.

```text
load
```

Example output:

```text
Index loaded successfully.
```

### Print

The `print` command prints the inverted index for a specific word.

```text
print nonsense
```

This returns the pages where the word appears, together with word statistics such as frequency and positions.

### Find

The `find` command returns pages containing the search query terms.

Single-word query:

```text
find indifference
```

Multi-word query:

```text
find good friends
```

The search is case-insensitive, so `Good`, `GOOD`, and `good` are treated as the same word.

### Exit

Exit the program:

```text
exit
```

## Testing

Run all tests using:

```bash
.venv/bin/python -m pytest
```

The test suite covers:

- tokenisation and lowercase conversion
- punctuation removal
- inverted index construction
- frequency recording
- word position recording
- saving and loading the index
- single-word search
- multi-word search
- missing words
- empty queries
- crawler HTML parsing

Crawler tests use sample HTML instead of live network requests. This makes the tests faster and more reliable because they do not depend on the website being available during testing.

## Design Notes

The project is separated into different modules to make the code easier to understand, test, and maintain.

### Crawler

The crawler is implemented in `src/crawler.py`.

It uses `requests` to fetch HTML pages and `BeautifulSoup` to parse the page content. It extracts quote text, authors, and tags from each page. It also detects the next-page link so that the crawler can continue through the website.

A delay is used between successive requests to respect the required politeness window.

### Indexer

The indexer is implemented in `src/indexer.py`.

It tokenises page text by:

- converting text to lowercase
- removing punctuation
- extracting alphanumeric words

The inverted index is stored as a nested dictionary:

```python
{
    "word": {
        "page_url": {
            "frequency": 2,
            "positions": [0, 5]
        }
    }
}
```

This structure makes it easy to find all pages containing a word and to retrieve statistics about where the word appears.

### Search

The search logic is implemented in `src/search.py`.

For a single-word query, the search engine returns all pages containing that word.

For a multi-word query, the search engine finds the intersection of pages containing each query word. This means that `find good friends` returns pages that contain both `good` and `friends`.

### Command-Line Interface

The command-line interface is implemented in `src/main.py`.

It provides an interactive shell with the required commands:

- `build`
- `load`
- `print`
- `find`

It also handles simple edge cases such as empty commands, missing query terms, unknown commands, and trying to search before an index has been built or loaded.

## Error Handling

The program includes basic error handling for:

- missing index files
- invalid or unknown commands
- empty search queries
- searching before loading or building an index
- HTTP request errors through `raise_for_status()`

## Version Control

Git was used throughout development. The repository history shows incremental development through separate commits for project setup, crawler implementation, indexer implementation, search logic, command-line interface, tests, and documentation.

## GenAI Use

Generative AI was used as a support tool during development.

It helped with:

- planning the project structure
- understanding how to organise crawler, indexer, and search modules
- suggesting possible unit tests
- improving README wording
- identifying edge cases such as empty queries and missing words

However, the generated suggestions were reviewed and tested manually. Some parts needed adjustment during development, especially around Python version compatibility and making the tests reliable without using live network requests.

Using GenAI helped speed up the planning process, but it was still necessary to understand, run, debug, and explain the code independently.