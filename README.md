"""
# Selenium Python Test Automation Framework

A professional test automation framework built with Python, Selenium, pytest, and custom reporting.

## Features

- ✅ **Pytest Framework** - Python's powerful testing framework
- ✅ **Comprehensive Logging** - Detailed execution logs with timestamps
- ✅ **Beautiful HTML Reports** - Custom Extent-style reports with embedded screenshots
- ✅ **Automatic Screenshot Capture** - Screenshots on test failures
- ✅ **Page Object Pattern Ready** - Scalable architecture
- ✅ **Cross-browser Support** - Easily configurable for different browsers

## Tech Stack

- **Python 3.8+**
- **Selenium WebDriver** - Browser automation
- **pytest** - Testing framework
- **WebDriver Manager** - Automatic driver management
- **Python logging** - Professional logging system

## Project Structure

```
selenium-python-framework/
├── README.md
├── requirements.txt
├── pytest.ini
├── run_tests.py
├── conftest.py
├── log_config.py
├── extent_report.py
├── test_amazon.py
├── logs/                  (auto-generated)
├── reports/               (auto-generated)
└── screenshots/           (auto-generated)
```

## Setup Instructions

### 1. Prerequisites
- Python 3.8 or higher
- Chrome browser installed

### 2. Clone Repository
```bash
git clone <repository-url>
cd selenium-python-framework
```

### 3. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

## Running Tests

### Run All Tests
```bash
python run_tests.py
```

### Run Specific Test Groups
```bash
# Run smoke tests only
python run_tests.py -m smoke

# Run regression tests only
python run_tests.py -m regression
```

### Run with Pytest Directly
```bash
# Run all tests
pytest test_amazon.py -v -s

# Run specific test
pytest test_amazon.py::TestAmazonWebsite::test_amazon_homepage_loads -v

# Run by marker
pytest test_amazon.py -m smoke -v
```

## Test Reports

### Generated Artifacts

1. **HTML Reports** - `reports/Selenium_Test_Execution_Report_[timestamp].html`
   - Test summary with pass/fail statistics
   - Detailed test execution logs
   - Embedded screenshots for failures
   - Interactive expandable test details

2. **Log Files** - `logs/test_execution_[timestamp].log`
   - Detailed execution logs with timestamps
   - Multiple log levels (DEBUG, INFO, WARNING, ERROR)
   - File and console output

3. **Screenshots** - `screenshots/FAILED_[testname]_[timestamp].png`
   - Automatically captured on test failures
   - Full page screenshots
   - Embedded in HTML reports

### View Reports
```bash
# Open latest HTML report (macOS)
open reports/*.html

# Open latest HTML report (Linux)
xdg-open reports/*.html

# Open latest HTML report (Windows)
start reports/*.html
```

## Test Cases

### Implemented Tests

1. **test_amazon_homepage_loads**
   - Verifies Amazon homepage loads successfully
   - Validates page title
   - Checks logo visibility
   - Groups: smoke, regression
   - Priority: 1

2. **test_search_functionality**
   - Tests search feature
   - Enters search query
   - Validates search results
   - Groups: regression
   - Priority: 2

3. **test_navigation_menu**
   - Verifies navigation menu presence
   - Checks menu accessibility
   - Groups: regression
   - Priority: 3

4. **test_intentional_failure_demo**
   - Demonstrates screenshot capture on failure
   - Shows error handling
   - Groups: smoke
   - Priority: 4

## Configuration

### pytest.ini
Controls pytest behavior:
- Test discovery patterns
- Logging configuration
- Marker definitions
- Output verbosity

### log_config.py
Logging configuration:
- File and console handlers
- Log format with timestamps
- Log levels and filtering
- Automatic log directory creation

### extent_report.py
Custom HTML report generator:
- Test execution summary
- Individual test details
- Screenshot embedding
- Interactive UI

## Framework Architecture

### Test Lifecycle

```
pytest startup
    ↓
conftest.py loads
    ↓
setup_class (before all tests in class)
    ↓
For each test:
    setup_method (before test)
        ↓
    test execution
        ↓
    teardown (after test)
        ↓
    screenshot capture (if failed)
    ↓
End of all tests
    ↓
Generate HTML report
```

### Fixtures (pytest annotations)

- `setup_class` - Runs once before all tests in class (like @BeforeClass)
- `setup_method` - Runs before each test (like @BeforeMethod)
- Teardown - Automatic cleanup after each test (like @AfterMethod)
- `pytest_sessionfinish` - Runs after all tests complete (like @AfterSuite)

## Customization

### Adding New Tests
```python
@pytest.mark.smoke  # Add test marker
@pytest.mark.priority(5)
def test_new_feature(self):
    """Test description"""
    test_info = self.test_info
    logger.info("TEST STARTED: test_new_feature")
    
    try:
        # Your test code here
        self.driver.get("https://example.com")
        # Add assertions
        
        logger.info("TEST PASSED")
        self.extent_report.end_test(test_info, "PASS")
    except Exception as e:
        logger.error(f"TEST FAILED: {str(e)}")
        self.extent_report.end_test(test_info, "FAIL", str(e))
        raise
```

### Changing Browser
```python
# In conftest.py, modify setup_method:

# For Firefox
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service, options=firefox_options)

# For Edge
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager

service = Service(EdgeChromiumDriverManager().install())
driver = webdriver.Edge(service=service, options=edge_options)
```

### Adding New Test Markers
```python
# In pytest.ini, add:
markers =
    smoke: Smoke tests
    regression: Regression tests
    integration: Integration tests  # Add new marker
    api: API tests                  # Add new marker
```

## Troubleshooting

### Issue: ChromeDriver version mismatch
**Solution:** WebDriver Manager automatically handles this. Ensure you have the latest version:
```bash
pip install --upgrade webdriver-manager
```

### Issue: Tests hang or timeout
**Solution:** Increase implicit wait time in `conftest.py`:
```python
driver.implicitly_wait(20)  # Increase from 10 to 20 seconds
```

### Issue: Screenshots are blank/white
**Solution:** Add delay before screenshot capture:
```python
import time
time.sleep(2)  # Wait for page to render
driver.save_screenshot(screenshot_path)
```

### Issue: Permission denied on logs/reports folders
**Solution:** Ensure write permissions:
```bash
chmod -R 755 logs/ reports/ screenshots/
```

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create Pull Request

## Best Practices

1. **Always use virtual environment** - Isolate project dependencies
2. **Keep logs and reports in .gitignore** - Don't commit generated files
3. **Use meaningful test names** - Clear test purpose from name
4. **Add docstrings to tests** - Explain what test validates
5. **Log important steps** - Aid debugging when tests fail
6. **Group related tests** - Use pytest markers effectively
7. **Keep tests independent** - Each test should run standalone

## CI/CD Integration

### GitHub Actions Example
```yaml
name: Selenium Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: pytest test_amazon.py -v
    
    - name: Upload reports
      uses: actions/upload-artifact@v2
      if: always()
      with:
        name: test-reports
        path: reports/
```

## License
This project is licensed under the MIT License.  
See the [LICENSE](LICENSE) file for details.
## Contact

For questions or issues, please open an issue on GitHub.
"""