"""
Central configuration for the Playwright test suite.
Override any value via environment variable.
"""
import os

# Application
BASE_URL = os.getenv("BASE_URL", "https://marben.staging.instaff.org")
LOGIN_URL = f"{BASE_URL}/login?next=%2F"

# Browser
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
SLOW_MO = int(os.getenv("SLOW_MO", "0"))  # ms between actions – useful for debugging

# Timeouts (milliseconds)
DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "30000"))
NAVIGATION_TIMEOUT = int(os.getenv("NAVIGATION_TIMEOUT", "30000"))

# User credentials
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "marben@hutility.com")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "Temp1234!!")
EMPLOYEE_EMAIL = os.getenv("EMPLOYEE_EMAIL", "marben+employee1@hutility.com")
EMPLOYEE_PASSWORD = os.getenv("EMPLOYEE_PASSWORD", "Temp1234!!")

# Geolocation (used for context creation)
GEOLOCATION = {"latitude": 37.7749, "longitude": -122.4194}
