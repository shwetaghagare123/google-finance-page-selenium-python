from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumpagefactory import PageFactory
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GoogleFinancePage(PageFactory):
    def __init__(self, driver):
        self.driver = driver
        self.base_url = "https://www.google.com/finance"
        self.go_to_url()

    locators = {
        'interested_section': "//ul[@class='sbnBtf']",
        'symbols': "//ul[@class='sbnBtf']//div[@class='COaKTb']"
    }

    def go_to_url(self):
        """Open the Google Finance page."""
        self.driver.get(self.base_url)

    def is_page_loaded(self):
        """Wait for the page title to be present and check if it's correct."""
        try:
            WebDriverWait(self.driver, 10).until(EC.title_contains("Google Finance"))
            return "Google Finance" in self.driver.title
        except TimeoutException:
            logger.error("Page load timeout: The title 'Google Finance' did not appear within 10 seconds.")
            return False

    def get_interested_in_stock_symbols(self):
        """Retrieve stock symbols from the 'You may be interested in' section."""
        try:
            # Wait for the section to be visible (adjust selector as needed)
            interested_section = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.locators.get('interested_section')))
            )

            # Retrieve all stock symbols within this section
            symbols = interested_section.find_elements(By.XPATH, self.locators.get('symbols'))
            retrieved_symbols = [symbol.text for symbol in symbols if symbol.text]

            if not retrieved_symbols:
                logger.warning("No stock symbols found in the 'You may be interested in' section")
            # Extract and return the text (stock symbols)
            return retrieved_symbols
        except TimeoutException:
            logger.error("Timeout: Could not locate the 'You may be interested in' section.")
            return []

    @staticmethod
    def compare_symbols(retrieved_symbols, test_data):
        """Compares retrieved symbols with test data and returns results.

        Args:
            retrieved_symbols (list): List of retrieved symbols.
            test_data (list): List of expected symbols.

        Returns:
            tuple: Tuple containing common symbols, symbols only in retrieved list, and symbols only in test data.
        """
        retrieved_symbols_set = set(retrieved_symbols)
        test_data_set = set(test_data)

        common_symbols = retrieved_symbols_set.intersection(test_data_set)
        only_in_retrieved = retrieved_symbols_set.difference(test_data_set)
        only_in_test_data = test_data_set.difference(retrieved_symbols_set)

        return common_symbols, only_in_retrieved, only_in_test_data
