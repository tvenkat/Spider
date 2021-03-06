from urllib.request import urlopen
from link_finder import LinkFinder
from general import *


class Spider:

    # Class variables (shared among all instances)
    project_name = ''
    base_url = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()

    def __init__(self, project_name, base_url):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        self.boot()
        self.crawl_page('Initializer', Spider.base_url)

    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print(thread_name + ' crawling: ' + page_url)
            Spider.add_links_to_set('queue', Spider.gather_links(page_url))
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            Spider.update_files()

    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            response = urlopen(page_url)
            if response.getheader('Content-Type') == 'text/html':
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(html_string)
        except:
            print('Error: can not crawl ' + page_url)
            return set()
        return finder.page_links()

    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)

    @staticmethod
    def add_links_to_set(name, links):
        target = set()
        if name == 'queue':
            target = Spider.queue
        if name == 'crawled':
            target = Spider.crawled
        for link in links:
            if link in Spider.queue:
                continue
            if link in Spider.crawled:
                continue
            target.add(link)
