Security Updates
* Updated urllib3 from 2.3.0 → 2.5.0 (CVE-2024-37891)
* Updated requests from 2.31.0 → 2.32.4 (CVE-2024-35195)
* Updated setuptools from 40.5.0 → 78.1.1 (CVE-2024-6345)
* Updated Scrapy from 2.12.0 → 2.13.4 for compatibility
* Added XPath syntax validation to catch malformed queries before crawl execution
* Sanitized file paths in error messages to prevent information disclosure
* Enabled AutoThrottle by default to prevent accidental DoS against targets

Added Features
* Added URL scheme detection: warns on non-HTTP/HTTPS schemes but allows processing for flexibility
* Added `--no-validate` flag to skip XPath syntax validation
* Added `-d, --delay` flag to set download delay between requests (controls Scrapy's `DOWNLOAD_DELAY` setting)
* Added `--no-throttle` flag to disable AutoThrottle for faster scanning (controls Scrapy's `AUTOTHROTTLE_ENABLED` setting)
* Added `--max-delay` flag to configure maximum AutoThrottle delay (controls Scrapy's `AUTOTHROTTLE_MAX_DELAY` setting)
