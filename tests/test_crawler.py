from src.crawler import Crawler


def test_parse_page_extracts_quote_author_and_tags():
    html = """
    <html>
      <body>
        <div class="quote">
          <span class="text">“The world as we have created it is a process of our thinking.”</span>
          <small class="author">Albert Einstein</small>
          <a class="tag">change</a>
          <a class="tag">thinking</a>
        </div>
      </body>
    </html>
    """

    crawler = Crawler("https://quotes.toscrape.com/", delay=0)
    page, next_url = crawler.parse_page("https://quotes.toscrape.com/", html)

    assert "The world as we have created it" in page.text
    assert "Albert Einstein" in page.text
    assert "change" in page.text
    assert "thinking" in page.text
    assert page.url == "https://quotes.toscrape.com/"
    assert next_url is None


def test_parse_page_finds_next_page_url():
    html = """
    <html>
      <body>
        <div class="quote">
          <span class="text">“A quote.”</span>
          <small class="author">Author Name</small>
        </div>

        <li class="next">
          <a href="/page/2/">Next</a>
        </li>
      </body>
    </html>
    """

    crawler = Crawler("https://quotes.toscrape.com/", delay=0)
    page, next_url = crawler.parse_page("https://quotes.toscrape.com/", html)

    assert page.url == "https://quotes.toscrape.com/"
    assert next_url == "https://quotes.toscrape.com/page/2/"


def test_parse_page_handles_empty_page():
    html = """
    <html>
      <body>
        <p>No quotes here.</p>
      </body>
    </html>
    """

    crawler = Crawler("https://quotes.toscrape.com/", delay=0)
    page, next_url = crawler.parse_page("https://quotes.toscrape.com/", html)

    assert page.text == ""
    assert next_url is None