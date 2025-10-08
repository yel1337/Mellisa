import ascii
from scrapy.utils.project import get_project_settings
from misc.misc_prompts import Misc
from spiders.m_spider import ScrapeParameters
from pathlib import Path
from scrapy.crawler import CrawlerProcess
import ascii.description_ascii
import argparse
import atexit
import signal
import os
import sys
import re
from urllib.parse import urlparse
from security_config import get_ethical_settings
mellisa = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, mellisa)

class CustomHelpFormatter(argparse.RawDescriptionHelpFormatter):
    def start_section(self, heading):
        if heading.lower() == 'positional arguments':
            heading = 'COMMANDS'
        return super().start_section(heading)


def run_spider(output_file=None, ethical_mode=True, **kwargs):
    settings = get_project_settings()
    spider_name = "param_spider"

    # Apply ethical security testing settings
    if ethical_mode:
        ethical_settings = get_ethical_settings()
        settings.update(ethical_settings)

    # directory where mellisa.py is located
    project_root = Path(__file__).resolve().parent
    output_folder = project_root / "output"
    output_folder.mkdir(exist_ok=True)

    # full path to the output file
    output_path = output_folder / output_file if output_file else None

    if output_file:
        settings.update({
            'FEED_FORMAT': 'json',
            'FEED_URI': output_path,
            'FEED_EXPORT_ENCODING': 'utf-8'
        })

    process = CrawlerProcess(settings)
    process.crawl(spider_name, **kwargs)
    process.start()

def validate_url(url):
    """Validate URL format for security testing purposes."""
    try:
        result = urlparse(url)
        if not result.scheme:
            # Add http if no scheme provided
            url = f"http://{url}"
            result = urlparse(url)

        if result.scheme not in ['http', 'https']:
            print(f"Warning: Unusual scheme '{result.scheme}' - proceeding for security testing")

        if not result.netloc:
            print(f"Error: Invalid URL format: {url}")
            return None

        return url
    except Exception as e:
        print(f"Error parsing URL: {e}")
        return None

def remove_char(domain):
    charsRemove = ["https://", "http://", "www."]
    for prefix in charsRemove:
        domain = domain.replace(prefix, "")

    domain = domain.rstrip("/")
    domain = re.sub(r'[\/:*?"<>|#]', '_', domain)

    return f"{domain}.json"

def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    flag_file = os.path.join(script_dir, ".first_run_flag")

    parser = argparse.ArgumentParser(description=ascii.description_ascii.mellisa_ascii,
                                    formatter_class=CustomHelpFormatter)
    parser.add_argument('url', help="URL of the website to crawl for security testing")
    parser.add_argument('--no-robots', action='store_true',
                       help="Ignore robots.txt (use only for authorized testing)")
    parser.add_argument('--delay', type=float, default=1.0,
                       help="Delay between requests in seconds (default: 1.0)")
    args = parser.parse_args()
    spider_kwargs = {}

    if "--help" in sys.argv:
        print(ascii.description_ascii.mellisa_ascii)
    if args.url:
        validated_url = validate_url(args.url)
        if not validated_url:
            print("Please provide a valid URL for security testing")
            sys.exit(1)

        domain_name = remove_char(validated_url)
        spider_kwargs['start_urls'] = [validated_url]

        # Display testing configuration
        print(f"Target: {validated_url}")
        print(f"Delay between requests: {args.delay}s")
        print(f"Respecting robots.txt: {'No (Authorized testing mode)' if args.no_robots else 'Yes'}")
        print("\n⚠️  Note: This tool is for authorized security testing only")
        print("Ensure you have permission to test the target website\n")

        # Configure ethical settings
        ethical_settings = get_ethical_settings(
            respect_robots=not args.no_robots,
            delay=args.delay
        )

        run_spider(output_file=domain_name, ethical_mode=True, **spider_kwargs)

if __name__ == "__main__":
    main()
