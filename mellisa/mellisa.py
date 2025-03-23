import argparse
import os
import sys 
import re
mellisa = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, mellisa)
import ascii.description_ascii
from scrapy.crawler import CrawlerProcess
from spiders.m_spider import ScrapeParameters
from misc.misc_prompts import Misc
from scrapy.utils.project import get_project_settings
import ascii

class CustomHelpFormatter(argparse.RawDescriptionHelpFormatter):
    def start_section(self, heading):
        if heading.lower() == 'positional arguments':
            heading = 'COMMANDS'
        return super().start_section(heading)

def run_spider(output_file=None, **kwargs):
    settings = get_project_settings()
    spider_name = "param_spider"

    output_folder = os.path.join(os.path.expanduser("~"), "Mellisa_src/mellisa/output")
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, output_file)

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
    parser = argparse.ArgumentParser(description=ascii.description_ascii.mellisa_ascii, formatter_class=CustomHelpFormatter)
    parser.add_argument('url', help="URL of the website to crawl")  

    args = parser.parse_args()

    spider_kwargs = {}
    if args.url:
        domain_name = remove_char(args.url)
        print(ascii.description_ascii.mellisa_ascii)
        spider_kwargs['start_urls'] = [args.url]
        print(f"target: {args.url}")
        run_spider(output_file=domain_name, **spider_kwargs)

if __name__ == "__main__":
    main()