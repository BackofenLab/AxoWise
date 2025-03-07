# """
# Browser utilities for web scraping.
# """

# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# from webdriver_manager.core.os_manager import ChromeType
# from fake_useragent import UserAgent
# import os
# import time

# from config.settings import HEADLESS, USER_AGENT_ENABLED
# from utils.logger import get_logger

# # Set up logger
# logger = get_logger(__name__)


# def setup_chrome_driver(use_random_user_agent=False):
#     """
#     Set up Chrome driver with appropriate options.
    
#     Args:
#         use_random_user_agent (bool, optional): Whether to use a random user agent. Defaults to False.
        
#     Returns:
#         webdriver.Chrome: Configured Chrome WebDriver instance.
#     """
#     chrome_options = Options()
    
#     # Set user agent if enabled
#     if use_random_user_agent and USER_AGENT_ENABLED:
#         ua = UserAgent()
#         user_agent = ua.random
#         chrome_options.add_argument(f'user-agent={user_agent}')
    
#     # Basic options for all drivers
#     # if HEADLESS:
#     chrome_options.add_argument('--disable-blink-features=AutomationControlled')
#     chrome_options.add_argument('--headless=new')  # new headless mode
#     chrome_options.add_argument('--no-sandbox')
#     chrome_options.add_argument('--disable-dev-shm-usage')
#     chrome_options.add_argument("start-maximized")
#     chrome_options.add_argument('--disable-gpu')
#     chrome_options.add_argument('--remote-debugging-port=9222')  # Fix for DevToolsActivePort issue

#     # Try different installation methods in sequence
#     try:
#         # Direct initialization without service object (most compatible)
#         driver = webdriver.Chrome(options=chrome_options)
#         return driver
#     except Exception as e1:
#         logger.warning(f"Direct Chrome initialization failed: {str(e1)}")
#         try:
#             # First try using WebDriver Manager with Chromium
#             service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
#             driver = webdriver.Chrome(service=service, options=chrome_options)
#             return driver
#         except Exception as e2:
#             logger.warning(f"Chromium initialization failed: {str(e2)}")
#             try:
#                 # Try Chrome if Chromium fails
#                 service = Service(ChromeDriverManager().install())
#                 driver = webdriver.Chrome(service=service, options=chrome_options)
#                 return driver
#             except Exception as e3:
#                 logger.error(f"All Chrome initialization methods failed: {str(e3)}")
#                 raise


# def setup_chrome_driver_minimal():
#     """
#     Set up Chrome driver with minimal options for maximum compatibility.
#     This is a fallback method when other approaches fail.
    
#     Returns:
#         webdriver.Chrome: Configured Chrome WebDriver instance.
#     """
#     chrome_options = Options()
#     chrome_options.add_argument('--headless')
#     chrome_options.add_argument('--no-sandbox')
#     chrome_options.add_argument('--disable-dev-shm-usage')
    
#     try:
#         driver = webdriver.Chrome(options=chrome_options)
#         return driver
#     except Exception as e:
#         logger.error(f"Minimal Chrome initialization failed: {str(e)}")
#         raise


"""
Browser utilities for web scraping.
Optimized for parallel processing.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from fake_useragent import UserAgent
import os
import time
import random
import threading
import tempfile

from config.settings import HEADLESS, USER_AGENT_ENABLED
from utils.logger import get_logger

# Set up logger
logger = get_logger(__name__)

# Track created Chrome drivers to ensure they're properly closed
_active_drivers = set()
_driver_lock = threading.Lock()


def setup_chrome_driver(use_random_user_agent=False, user_data_dir=None):
    """
    Set up Chrome driver with appropriate options for parallel processing.
    
    Args:
        use_random_user_agent (bool, optional): Whether to use a random user agent. Defaults to False.
        user_data_dir (str, optional): Directory for Chrome user data. Defaults to None.
        
    Returns:
        webdriver.Chrome: Configured Chrome WebDriver instance.
    """
    chrome_options = Options()
    
    # Set user agent if enabled
    if use_random_user_agent and USER_AGENT_ENABLED:
        ua = UserAgent()
        user_agent = ua.random
        chrome_options.add_argument(f'user-agent={user_agent}')
    
    # Basic options for all drivers
    if HEADLESS:
        chrome_options.add_argument('--headless')  # Use legacy headless mode for compatibility
    
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    
    # Critical for parallel processing: use unique data directory and port for each instance
    if not user_data_dir:
        user_data_dir = tempfile.mkdtemp(prefix=f"chrome_data_{threading.get_ident()}_")
    
    chrome_options.add_argument(f'--user-data-dir={user_data_dir}')
    
    # Use random debugging port to avoid conflicts
    debug_port = random.randint(9222, 9999)
    chrome_options.add_argument(f'--remote-debugging-port={debug_port}')
    
    # Disable shared memory for better isolation
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    # Additional options to reduce resource usage
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument('--disable-popup-blocking')
    
    # Try different initialization methods in sequence
    driver = None
    errors = []
    
    try:
        # Direct initialization without service object (most compatible)
        driver = webdriver.Chrome(options=chrome_options)
        logger.info(f"Successfully created Chrome driver with direct initialization (thread {threading.get_ident()})")
    except Exception as e1:
        errors.append(f"Direct init failed: {str(e1)}")
        try:
            # First try using WebDriver Manager with Chrome
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            logger.info(f"Successfully created Chrome driver with ChromeDriverManager (thread {threading.get_ident()})")
        except Exception as e2:
            errors.append(f"WebDriver Manager init failed: {str(e2)}")
            try:
                # Try ChromeType.CHROMIUM if Chrome fails
                service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
                driver = webdriver.Chrome(service=service, options=chrome_options)
                logger.info(f"Successfully created Chrome driver with Chromium (thread {threading.get_ident()})")
            except Exception as e3:
                errors.append(f"Chromium init failed: {str(e3)}")
                try:
                    # Last resort: minimal options
                    minimal_options = Options()
                    minimal_options.add_argument('--headless')
                    minimal_options.add_argument('--no-sandbox')
                    driver = webdriver.Chrome(options=minimal_options)
                    logger.info(f"Successfully created Chrome driver with minimal options (thread {threading.get_ident()})")
                except Exception as e4:
                    errors.append(f"Minimal init failed: {str(e4)}")
                    # All methods failed, raise comprehensive error
                    error_msg = "; ".join(errors)
                    logger.error(f"All Chrome initialization methods failed: {error_msg}")
                    raise Exception(f"Failed to initialize Chrome driver: {error_msg}")
    
    # Register driver in active set for tracking
    if driver:
        with _driver_lock:
            _active_drivers.add(id(driver))
    
    return driver


def cleanup_drivers():
    """
    Cleanup all active drivers. Call this at the end of the program.
    """
    with _driver_lock:
        active_count = len(_active_drivers)
        if active_count > 0:
            logger.warning(f"Cleaning up {active_count} active Chrome drivers")
            _active_drivers.clear()