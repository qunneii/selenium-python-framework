import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from log_config import LogConfig
from extent_report import ExtentReport
import os
from datetime import datetime

logger = LogConfig.setup_logger()

extent_report = ExtentReport("Selenium_Test_Execution_Report")

@pytest.fixture(scope="class")
def setup_class(request):
    logger.info("=" * 80)
    logger.info("SETUP CLASS: Initializing test class")
    logger.info(f"Test Class: {request.cls.__name__}")
    logger.info("=" * 80)
    
    yield
    
    logger.info("=" * 80)
    logger.info("TEARDOWN CLASS: Cleaning up test class")
    logger.info("=" * 80)

@pytest.fixture(scope="function")
def setup_method(request):
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    
    logger.info("-" * 80)
    logger.info(f"SETUP METHOD: {request.node.name}")
    logger.info("-" * 80)
    
    logger.info("Initializing Chrome WebDriver...")
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)
    
    logger.info("WebDriver initialized successfully")
    
    test_name = request.node.name
    test_description = request.node.function.__doc__ or "No description"
    test_info = extent_report.start_test(test_name, test_description)
    extent_report.log(test_info, "INFO", "Test started")
    extent_report.log(test_info, "INFO", f"Browser: Chrome")
    
    request.cls.driver = driver
    request.cls.test_info = test_info
    request.cls.extent_report = extent_report
    
    yield
    
    logger.info("-" * 80)
    logger.info(f"TEARDOWN METHOD: {request.node.name}")

    if request.node.rep_call.failed:
        import time
        logger.error("Test FAILED - Capturing screenshot...")
        time.sleep(1)
        screenshot_name = f"FAILED_{request.node.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        screenshot_path = os.path.join("screenshots", screenshot_name)
        driver.save_screenshot(screenshot_path)
        logger.error(f"Screenshot saved: {screenshot_path}")
        extent_report.add_screenshot(test_info, screenshot_path)
        extent_report.log(test_info, "ERROR", f"Screenshot captured: {screenshot_name}")
    
    driver.quit()
    logger.info("WebDriver closed")
    logger.info("-" * 80)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

def pytest_sessionfinish(session, exitstatus):
    logger.info("=" * 80)
    logger.info("TEST SUITE COMPLETED")
    logger.info("=" * 80)

    report_path = extent_report.generate_report()
    logger.info(f"Extent Report generated: {report_path}")
    logger.info("=" * 80)