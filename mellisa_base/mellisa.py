import ascii
from urllib.parse import urlparse
from scrapy.utils.project import get_project_settings
from pathlib import Path
from scrapy.crawler import CrawlerProcess
from ascii.description_ascii import mellisa_ascii  
import argparse
import atexit
import signal
import os
import sys
import re
mellisa = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, mellisa)
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'mellisa_base.settings')

class CustomHelpFormatter(argparse.RawDescriptionHelpFormatter):
    def start_section(self, heading):
        if heading.lower() == 'positional arguments':
            heading = 'commands'
        elif heading.lower() == 'optional arguments':
            heading = 'options'
        return super().start_section(heading)


def run_spider(output_file=None, **kwargs):
    settings = get_project_settings()
    spider_name = "param_spider"

    # directory where mellisa.py is located
    project_root = Path(__file__).resolve().parent
    output_folder = project_root / "output"
    output_folder.mkdir(exist_ok=True)

    # full path of the output file
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

    return output_file

# commit @1eebe226194b68d88da9c3ab1d6685431d15fa08
# by JWhiteUX from hotfix/v1.1.0
#
# URL validation with scheme detection
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

def event_handler(event, args, parser):
    if event is args.custom_xpath and args.custom_xpath:
        return True
    elif event is args.custom_xpath and args.custom_xpath == None:
        return None

def return_if_args(args):
    if args:
        return True
    else:
        return False

def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    flag_file = os.path.join(script_dir, ".first_run_flag")
    GREEN = "\033[92m"
    RESET = "\033[0m"
    parser = argparse.ArgumentParser(usage=argparse.SUPPRESS,
                                    description=mellisa_ascii,
                                    epilog=f"""
examples:
    {GREEN}./mellisa.sh https://example.com{RESET}                    - Run the crawler in Default Mode
    {GREEN}./mellisa.sh https://example.com -c <custom_query>{RESET}  - Run the crawler with Custom XPath
""",
                                    formatter_class=CustomHelpFormatter)

    parser.add_argument('url', help="URL of the website to crawl")
    parser.add_argument('-c', '--custom_xpath', help="Custom XPATH Query")
    args = parser.parse_args()
    validated_url = validate_url(args.url)

    spider_kwargs = {}

    if args.url and args.custom_xpath is None:
        event_condition = event_handler(args.custom_xpath, args, parser)
        domain_name = remove_char(args.url)
        spider_kwargs['start_urls'] = [validated_url]
        print(f"target: {args.url}")
        run_spider(output_file=domain_name, **spider_kwargs)       
        
    elif args.url and args.custom_xpath:
        event_condition = event_handler(args.custom_xpath, args, parser)
        domain_name = remove_char(args.url)
        spider_kwargs['start_urls'] = [validated_url]
        print(f"target: {args.url}")
        spider_kwargs['custom_xpath'] = args.custom_xpath
        run_spider(output_file=domain_name, **spider_kwargs)

    return return_if_args(validated_url)

if __name__ == "__main__":
    main()
