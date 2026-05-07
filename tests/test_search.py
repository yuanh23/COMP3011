from src.search import SearchEngine


def sample_index():
    return {
        "good": {
            "https://example.com/page1": {
                "frequency": 2,
                "positions": [0, 3],
            },
            "https://example.com/page2": {
                "frequency": 1,
                "positions": [5],
            },
        },
        "friends": {
            "https://example.com/page1": {
                "frequency": 1,
                "positions": [1],
            },
        },
        "books": {
            "https://example.com/page2": {
                "frequency": 1,
                "positions": [2],
            },
        },
    }


def test_print_word_returns_index_for_existing_word():
    search_engine = SearchEngine(sample_index())

    result = search_engine.print_word("good")

    assert "https://example.com/page1" in result
    assert "https://example.com/page2" in result


def test_print_word_is_case_insensitive():
    search_engine = SearchEngine(sample_index())

    result = search_engine.print_word("GOOD")

    assert "https://example.com/page1" in result


def test_print_word_returns_empty_dict_for_missing_word():
    search_engine = SearchEngine(sample_index())

    result = search_engine.print_word("missing")

    assert result == {}


def test_find_returns_pages_for_single_word():
    search_engine = SearchEngine(sample_index())

    result = search_engine.find("good")

    assert result == [
        "https://example.com/page1",
        "https://example.com/page2",
    ]


def test_find_returns_intersection_for_multi_word_query():
    search_engine = SearchEngine(sample_index())

    result = search_engine.find("good friends")

    assert result == ["https://example.com/page1"]


def test_find_returns_empty_list_for_missing_word():
    search_engine = SearchEngine(sample_index())

    result = search_engine.find("missing")

    assert result == []


def test_find_returns_empty_list_for_empty_query():
    search_engine = SearchEngine(sample_index())

    result = search_engine.find("")

    assert result == []