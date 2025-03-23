import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--xpath_query",
        action="store",
        default="//title/text()",
        help="XPath query to test against test URLs"
    )

@pytest.fixture
def xpath_query(request):
    return request.config.getoption("--xpath_query")