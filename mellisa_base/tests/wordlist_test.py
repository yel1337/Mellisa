import scrapy
import pytest
import requests
from parsel import Selector

# Websites to test xpath query effectivity
test_urls = ["https://books.toscrape.com",
             "https://quotes.toscrape.com",
             "https://webscraper.io/test-sites/e-commerce/allinone",
             "https://httpbin.org/html",
             "https://www.python.org/jobs/",
             "https://www.scrapethissite.com/pages/forms/",
             "https://news.ycombinator.com/",
             "https://www.imdb.com/chart/top/",
             "https://www.worldometers.info/world-population/population-by-country/",
             "https://developer.mozilla.org/en-US/docs/Web/XPath"
             ]


@pytest.mark.parametrize("url", test_urls)
def test_wordlist_integrity(url, xpath_query):
    response = requests.get(url)
    selector = Selector(response.text)
    result = selector.xpath(xpath_query).get()
    assert result is not None and result.strip() != ""
