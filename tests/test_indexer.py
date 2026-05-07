from src.crawler import Page
from src.indexer import Indexer


def test_tokenize_lowercase_and_removes_punctuation():
    indexer = Indexer()

    tokens = indexer.tokenize("Good friends, GOOD life!")

    assert tokens == ["good", "friends", "good", "life"]


def test_build_index_records_frequency_and_positions():
    pages = [
        Page(
            url="https://example.com/page1",
            text="Good friends are good",
        )
    ]

    indexer = Indexer()
    index = indexer.build_index(pages)

    assert index["good"]["https://example.com/page1"]["frequency"] == 2
    assert index["good"]["https://example.com/page1"]["positions"] == [0, 3]
    assert index["friends"]["https://example.com/page1"]["frequency"] == 1
    assert index["friends"]["https://example.com/page1"]["positions"] == [1]


def test_build_index_handles_multiple_pages():
    pages = [
        Page(url="https://example.com/page1", text="good friends"),
        Page(url="https://example.com/page2", text="good books"),
    ]

    indexer = Indexer()
    index = indexer.build_index(pages)

    assert set(index["good"].keys()) == {
        "https://example.com/page1",
        "https://example.com/page2",
    }


def test_save_and_load_index(tmp_path):
    pages = [
        Page(url="https://example.com/page1", text="good friends"),
    ]

    file_path = tmp_path / "index.json"

    indexer = Indexer()
    original_index = indexer.build_index(pages)
    indexer.save(str(file_path))

    new_indexer = Indexer()
    loaded_index = new_indexer.load(str(file_path))

    assert loaded_index == original_index