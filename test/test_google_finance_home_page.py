import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from src.pages.google_finance_home_page import GoogleFinancePage


@pytest.fixture
def setup_browser():
    # Setup Chrome WebDriver using webdriver_manager
    # Default driver value
    driver = None
    options = Options()
    options.add_argument("--headless")
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.maximize_window()
    except Exception as e:
        pytest.fail(f"Failed to start driver: {e}")
    yield driver

    if driver:
        driver.quit()


@pytest.fixture
def google_finance_page(setup_browser):
    # Initialize the GoogleFinancePage with WebDriver
    return GoogleFinancePage(setup_browser)


@pytest.fixture
def test_data():
    return ['NFLX', 'MSFT', 'TSLA']


def test_page_loads_and_title_contains_google_finance(google_finance_page):
    """Test that Google Finance page loads successfully and the title is correct."""
    assert google_finance_page.is_page_loaded(), "Google Finance page failed to load correctly."


def test_stock_symbols_retrieval(google_finance_page):
    """Verify stock symbols from 'You may be interested in' section are retrieved."""
    stock_symbols = google_finance_page.get_interested_in_stock_symbols()
    assert len(stock_symbols) > 0, f"No stock symbols found in 'You may be interested in' section: {stock_symbols}"


def test_compare_retrieved_and_test_data_symbols(google_finance_page, test_data):
    """Verify comparison between retrieved stock symbols and test data."""
    retrieved_symbols = google_finance_page.get_interested_in_stock_symbols()
    common_symbols, only_in_retrieved, only_in_test_data = google_finance_page.compare_symbols(retrieved_symbols,
                                                                                               test_data)
    assert common_symbols is not None, "Set is empty"


def test_only_in_retrieved_symbols(google_finance_page, test_data):
    """Test comparing stock symbols retrieved with test data."""
    retrieved_symbols = google_finance_page.get_interested_in_stock_symbols()
    common_symbols, only_in_retrieved, only_in_test_data = google_finance_page.compare_symbols(retrieved_symbols,
                                                                                               test_data)
    print("Symbols only in retrieved list:", only_in_retrieved)
    assert only_in_retrieved is not None, "retrieved list is empty"


def test_only_in_test_data(google_finance_page, test_data):
    """Test comparing stock symbols retrieved with test data."""
    retrieved_symbols = google_finance_page.get_interested_in_stock_symbols()
    common_symbols, only_in_retrieved, only_in_test_data = google_finance_page.compare_symbols(retrieved_symbols,
                                                                                               test_data)
    print("Symbols only in test list:", only_in_test_data)
    assert only_in_test_data is not None, "only test data is empty"
