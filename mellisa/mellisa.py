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
mellisa = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, mellisa)

class CustomHelpFormatter(argparse.RawDescriptionHelpFormatter):
    def start_section(self, heading):
        if heading.lower() == 'positional arguments':
            heading = 'COMMANDS'
        return super().start_section(heading)


def run_spider(output_file=None, **kwargs):
    settings = get_project_settings()
    spider_name = "param_spider"

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

    parser.add_argument('url', help="URL of the website to crawl")
    parser.add_argument('-c',
                        '--custom_xpath',
                        help="Custom XPATH Query")

    args = parser.parse_args()
    spider_kwargs = {}

    if args.url and args.custom_xpath is None:
        print("NORMAL...")
        domain_name = remove_char(args.url)
        spider_kwargs['start_urls'] = [args.url]
        print(f"target: {args.url}")       
    if args.custom_xpath:
        print("CUSTOM...")
        domain_name = remove_char(args.url)
        spider_kwargs['start_urls'] = [args.url]
        spider_kwargs['custom_xpath'] = args.custom_xpath
    
    run_spider(output_file=domain_name, **spider_kwargs)

if __name__ == "__main__":
    main()
