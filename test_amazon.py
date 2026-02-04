import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from log_config import LogConfig
import time

logger = LogConfig.setup_logger()

@pytest.mark.usefixtures("setup_class", "setup_method")
class TestAmazonWebsite:
    #тест нг
    @pytest.mark.smoke
    @pytest.mark.priority(1)
    def test_amazon_homepage_loads(self):
        #смоук тест
        test_info = self.test_info
        logger.info("TEST STARTED: test_amazon_homepage_loads")
        self.extent_report.log(test_info, "INFO", "Navigating to Amazon homepage")
        
        try:
            logger.info("Navigating to https://www.amazon.com")
            self.driver.get("https://www.amazon.com")
            self.extent_report.log(test_info, "INFO", "URL loaded: https://www.amazon.com")
            
            wait = WebDriverWait(self.driver, 15)
            wait.until(EC.presence_of_element_located((By.ID, "nav-logo-sprites")))
            
            logger.info(f"Page title: {self.driver.title}")
            assert "Amazon" in self.driver.title, "Amazon not in title"
            self.extent_report.log(test_info, "PASS", f"Page title verified: {self.driver.title}")
            
            logo = self.driver.find_element(By.ID, "nav-logo-sprites")
            assert logo.is_displayed(), "Amazon logo not displayed"
            logger.info("Amazon logo is displayed")
            self.extent_report.log(test_info, "PASS", "Amazon logo is visible")
            
            logger.info("TEST PASSED: test_amazon_homepage_loads")
            self.extent_report.end_test(test_info, "PASS")
            
        except AssertionError as e:
            logger.error(f"Assertion failed: {str(e)}")
            self.extent_report.log(test_info, "ERROR", str(e))
            self.extent_report.end_test(test_info, "FAIL", str(e))
            raise
        except Exception as e:
            logger.error(f"Test failed with exception: {str(e)}")
            self.extent_report.log(test_info, "ERROR", str(e))
            self.extent_report.end_test(test_info, "FAIL", str(e))
            raise
    
    @pytest.mark.regression
    @pytest.mark.priority(2)
    def test_search_functionality(self):
        #регрешн тест
        test_info = self.test_info
        logger.info("TEST STARTED: test_search_functionality")
        self.extent_report.log(test_info, "INFO", "Testing search functionality")
        
        try:
            logger.info("Navigating to https://www.amazon.com")
            self.driver.get("https://www.amazon.com")
            self.extent_report.log(test_info, "INFO", "Navigated to Amazon")
            
            wait = WebDriverWait(self.driver, 15)
            search_box = wait.until(EC.presence_of_element_located((By.ID, "twotabsearchtextbox")))
            logger.info("Search box found")
            self.extent_report.log(test_info, "INFO", "Search box located")
            
            search_query = "laptop"
            search_box.clear()
            search_box.send_keys(search_query)
            logger.info(f"Entered search query: {search_query}")
            self.extent_report.log(test_info, "INFO", f"Search query entered: {search_query}")
            
            search_button = self.driver.find_element(By.ID, "nav-search-submit-button")
            search_button.click()
            logger.info("Search button clicked")
            self.extent_report.log(test_info, "INFO", "Search submitted")
            
            time.sleep(2)
            results = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-component-type='s-search-result']")))
            
            all_results = self.driver.find_elements(By.CSS_SELECTOR, "[data-component-type='s-search-result']")
            assert len(all_results) > 0, "No search results found"
            logger.info(f"Found {len(all_results)} search results")
            self.extent_report.log(test_info, "PASS", f"Search returned {len(all_results)} results")
            
            assert search_query.lower() in self.driver.page_source.lower()
            logger.info("Search term found in page source")
            self.extent_report.log(test_info, "PASS", "Search term verified in results")
            
            logger.info("TEST PASSED: test_search_functionality")
            self.extent_report.end_test(test_info, "PASS")
            
        except Exception as e:
            logger.error(f"Test failed: {str(e)}")
            self.extent_report.log(test_info, "ERROR", str(e))
            self.extent_report.end_test(test_info, "FAIL", str(e))
            raise
    
    @pytest.mark.regression
    @pytest.mark.priority(3)
    def test_navigation_menu(self):
        #регрешн тест
        test_info = self.test_info
        logger.info("TEST STARTED: test_navigation_menu")
        self.extent_report.log(test_info, "INFO", "Testing navigation menu")
        
        try:
            self.driver.get("https://www.amazon.com")
            self.extent_report.log(test_info, "INFO", "Navigated to Amazon")
            
            wait = WebDriverWait(self.driver, 15)
            nav_bar = wait.until(EC.presence_of_element_located((By.ID, "nav-main")))
            logger.info("Navigation bar found")
            self.extent_report.log(test_info, "INFO", "Navigation bar located")
            
            menu_button = self.driver.find_element(By.ID, "nav-hamburger-menu")
            assert menu_button.is_displayed(), "Menu button not displayed"
            logger.info("Menu button is visible")
            self.extent_report.log(test_info, "PASS", "Menu button is visible and accessible")
            
            logger.info("TEST PASSED: test_navigation_menu")
            self.extent_report.end_test(test_info, "PASS")
            
        except Exception as e:
            logger.error(f"Test failed: {str(e)}")
            self.extent_report.log(test_info, "ERROR", str(e))
            self.extent_report.end_test(test_info, "FAIL", str(e))
            raise
    
    @pytest.mark.smoke
    @pytest.mark.priority(4)
    def test_intentional_failure_demo(self):
        #демо тест
        test_info = self.test_info
        logger.info("TEST STARTED: test_intentional_failure_demo")
        self.extent_report.log(test_info, "WARNING", "This test will intentionally fail")
        
        try:
            self.driver.get("https://www.amazon.com")
            self.extent_report.log(test_info, "INFO", "Navigated to Amazon")

            wait = WebDriverWait(self.driver, 15)
            wait.until(EC.presence_of_element_located((By.ID, "nav-logo-sprites")))
            time.sleep(2)
            logger.info("Page fully loaded")
            self.extent_report.log(test_info, "INFO", "Page fully rendered")
            #спец фейл
            logger.warning("Attempting intentional assertion failure...")
            self.extent_report.log(test_info, "WARNING", "Executing assertion that will fail")
            assert "eBay" in self.driver.title, "Expected eBay in title (intentional failure)"
            
        except AssertionError as e:
            logger.error(f"TEST FAILED (Expected): {str(e)}")
            self.extent_report.log(test_info, "ERROR", "Assertion failed as expected")
            self.extent_report.end_test(test_info, "FAIL", str(e))
            raise