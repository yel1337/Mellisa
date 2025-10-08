"""
Security testing configuration for Mellisa
Ensures ethical and responsible security testing practices
"""

# Ethical scraping settings
SECURITY_TESTING_CONFIG = {
    # Respect rate limiting for responsible testing
    'DEFAULT_DELAY': 1,  # Seconds between requests

    # User agent identifies the tool for transparency
    'USER_AGENT': 'Mellisa Security Testing Tool (Authorized Testing Only)',

    # Option to respect robots.txt during testing
    # Can be overridden via command line for authorized tests
    'RESPECT_ROBOTS': True,

    # Maximum depth to crawl (prevent infinite loops)
    'MAX_DEPTH': 3,

    # Maximum pages to crawl per domain
    'MAX_PAGES': 100,

    # Timeout settings
    'REQUEST_TIMEOUT': 30,

    # SSL verification (can be disabled for testing internal sites)
    'VERIFY_SSL': True,

    # Headers for responsible disclosure
    'DEFAULT_HEADERS': {
        'X-Scanner': 'Mellisa',
        'X-Purpose': 'Security-Testing',
    }
}

# URL patterns to exclude from testing (add sensitive paths)
EXCLUDED_PATTERNS = [
    '/admin/',
    '/wp-admin/',
    '/.git/',
    '/.env',
    '/config/',
]

def get_ethical_settings(respect_robots=None, delay=None):
    """
    Get Scrapy settings configured for ethical security testing

    Args:
        respect_robots: Override robots.txt setting
        delay: Override request delay

    Returns:
        Dictionary of Scrapy settings
    """
    settings = {
        'USER_AGENT': SECURITY_TESTING_CONFIG['USER_AGENT'],
        'ROBOTSTXT_OBEY': respect_robots if respect_robots is not None else SECURITY_TESTING_CONFIG['RESPECT_ROBOTS'],
        'DOWNLOAD_DELAY': delay if delay is not None else SECURITY_TESTING_CONFIG['DEFAULT_DELAY'],
        'DEPTH_LIMIT': SECURITY_TESTING_CONFIG['MAX_DEPTH'],
        'CLOSESPIDER_PAGECOUNT': SECURITY_TESTING_CONFIG['MAX_PAGES'],
        'DOWNLOAD_TIMEOUT': SECURITY_TESTING_CONFIG['REQUEST_TIMEOUT'],
        'DEFAULT_REQUEST_HEADERS': SECURITY_TESTING_CONFIG['DEFAULT_HEADERS'],
    }

    return settings