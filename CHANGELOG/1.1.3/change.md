Security Updates
* Added XPath syntax validation to catch malformed queries before crawl execution
* Sanitized file paths in error messages to prevent information disclosure
* Enabled AutoThrottle by default to prevent accidental DoS against targets

Critical Bug Fixes
* Fixed XPath processing logic (BUG-4 - CRITICAL)
  - Removed redundant code in m_spider.py that prevented all XPath patterns from being used
  - Default mode now properly processes all 100+ XPath patterns in wordlist
  - Significantly improved parameter detection accuracy from 16.7% to 100% recall
* Fixed UnboundLocalError and data accumulation in m_spider.py (PR#8 - Copilot Review)
  - Initialize extracted_datas before loop to prevent crashes with empty wordlists
  - Fixed logic to accumulate all XPath results instead of using only the last one
  - Ensures correct data extraction from all XPath patterns
* Fixed CLI argument validation in mellisa.py (PR#8 - Copilot Review)
  - Added validation to reject negative --delay and --max-delay values
  - Added logical consistency check ensuring max-delay >= delay
  - Prevents runtime errors from invalid throttling configurations
* Fixed attribute assignment error (BUG-2)
  - Corrected args_url attribute in misc_prompts.py to use URL parameter instead of function object
  - Resolved incorrect control flow logic
* Fixed function signature mismatch (BUG-3)
  - Removed self parameter from log_level() and log() functions in log_custom.py
  - Fixed parameter order in function calls in misc_prompts.py
  - Log levels now display correctly as [INFO]/[WARNING]
* Fixed redundant boolean check (BUG-5)
  - Removed unnecessary function object check in conditional logic in misc_prompts.py

Code Quality Improvements
* Removed unused variable assignments in m_spider.py (PR#8 - Copilot Review)
  - Eliminated unused self_datas assignments for improved code clarity
* Fixed XPath namespace issue in wordlist.txt
  - Updated SVG href XPath pattern to use namespace-agnostic local-name() approach
  - Prevents "Undefined namespace prefix" errors during crawling

Added Features
* Added URL scheme detection: warns on non-HTTP/HTTPS schemes but allows processing for flexibility
* Added `--no-validate` flag to skip XPath syntax validation
* Added `-d, --delay` flag to set download delay between requests (controls Scrapy's `DOWNLOAD_DELAY` setting)
* Added `--no-throttle` flag to disable AutoThrottle for faster scanning (controls Scrapy's `AUTOTHROTTLE_ENABLED` setting)
* Added `--max-delay` flag to configure maximum AutoThrottle delay (controls Scrapy's `AUTOTHROTTLE_MAX_DELAY` setting)

Documentation Updates
* Updated NetSPI lab documentation in README.md
  - Corrected repository URL from deprecated path-injection-weakness-lab to XPath-Injection-Lab
  - Updated Docker setup commands to match current repository structure

Files Modified
* mellisa_base/spiders/m_spider.py (BUG-4 cleanup, UnboundLocalError fix, data accumulation fix, unused variable removal)
* mellisa_base/mellisa.py (CLI argument validation)
* mellisa_base/misc/misc_prompts.py (BUG-2, BUG-3, BUG-5 fixes)
* mellisa_base/custom/log/log_custom.py (BUG-3 fix)
* mellisa_base/wordlist.txt (namespace fix)
* mellisa_base/tests/wordlist_test.py (fixed test URLs)
* README.md (NetSPI lab documentation update)
