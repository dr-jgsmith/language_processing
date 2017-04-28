import requests
import lxml
from bs4 import BeautifulSoup
import feedparser
import pickle
import scholarly
import wikipedia
import time


class HtmlMapper:

    """*****************************************************************************
        
        HtmlMapper is a simple class and associated methods for crawling and scraping 
        html content. It makes heavy use of Requests and BeautifulSoup.
        Basic usage includes extracting all links from a site.
        Second-order link extraction can be performed with a link extraction of the 
        terminating links.
        
    *******************************************************************************"""

    def __init__(self, term=None, start_url=None):
        self.start_url = start_url
        self.term = term
        self.edges = []

    def get_seed_links(self):
        self.start_list = []

        self.start_list.append(self.start_url)

        s = requests.Session()

        s.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'

        r = s.get(self.start_url)
        self.c = r.content

        soup = BeautifulSoup(self.c)

        for link in soup.find_all("a"):
            data = link.get("href")

            if data == None:
                pass
            elif data[:5] == "https":
                row = (self.start_url, data + "/")
                self.edges.append(row)
                self.start_list.append(data)
            elif data[:1] == "/":
                new = self.start_url + data[1:]
                row = (self.start_url, new)
                self.edges.append(row)

                self.start_list.append(new)
            else:
                pass

        return self.start_list

    # Second order web scrap for link retreival. This function can only work if a link list has been generatated from the previous function call.
    def _deep_link_scrape(self, link_list):

        self.link_list = link_list

        for i in self.link_list:
            s = requests.Session()
            s.headers[
                'User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
            r = s.get(i)
            c = r.content

            soup = BeautifulSoup(c)

            for link in soup.find_all("a"):
                data = link.get("href")

                if data == None:
                    pass
                elif data[:5] == "https":
                    row = (i, data + "/")
                    self.edges.append(row)
                elif data[:1] == "/":
                    new = i + data[1:]
                    row = (i, new + "/")
                    self.edges.append(row)
                else:
                    pass

        return self.edges

    # Simple function for calling a python requests response to render html as a raw/binary output.
    def get_raw_html(self):
        s = requests.Session()
        s.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'


        self.r = s.get(self.start_url)

        return self.r.raw

    # Simple function for calling a python requests response to render html as a text string.
    def get_data_from_link(self):
        s = requests.Session()
        s.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'

        r = s.get(self.start_url)
        self.texts = r.text

        return self.texts

    
    #Search Google Scholar

    def search_scholar(self):
        search_query = scholarly.search_pubs_query(self.term)
        self.result = next(search_query).fill()

        return self.result


    #Search wikipedia and get entry summary.

    def search_wiki(self, wikiterm):
        split_term = wikiterm.replace('_', ' ')
        try:
            self.summary = wikipedia.summary(split_term)
            return self.summary
        except wikipedia.exceptions.DisambiguationError:
            pass
        except wikipedia.exceptions.PageError:
            pass
        except wikipedia.exceptions.WikipediaException:
            time.sleep(100)
            pass


class RSSStreams:
    # URL = None
    # URL_AUTHOR = None

    def __init__(self, list_sources=None, add_sources_name=None, add_source_url=None):
        """
            Empty intializer.
            This will change with the addition of class options.
            e.g options will include the ability to add feedlinks and feed titles.
        """
        self.list_sources = list_sources
        self.add_sources = add_sources_name
        self.add_source_url = add_source_url

        # List of RSS feeds that we will fetch and combine
        self.newsurls = {
            'apnews': 'http://hosted2.ap.org/atom/APDEFAULT/3d281c11a76b4ad082fe88aa0db04909',
            'googlenews': 'http://news.google.com/?output=rss',
            'reutersBiz': 'http://feeds.reuters.com/reuters/businessNews',
            'yahoonews': 'http://news.yahoo.com/rss/',
            'disasters': 'http://www.gdacs.org/xml/rss.xml',
            'reutersMoney': 'http://feeds.reuters.com/news/wealth',
            'reutersEnv': 'http://feeds.reuters.com/reuters/environment',
            'reutersTech': 'http://feeds.reuters.com/reuters/technologyNews',
            'reutersSci': 'http://feeds.reuters.com/reuters/scienceNews',
            'NWS_Alerts': 'https://alerts.weather.gov/cap/us.php?x=0'
        }

    # This function calls the FeedParser Lib to execute the rss parsing.
    def parseRSS(self, rss_url):

        self.rss_url = rss_url

        return feedparser.parse(self.rss_url)

        # Function grabs the rss feed headlines (titles) and returns them as a list

    def getHeadlines(self, rss_url):

        self.rss_url = rss_url

        self.headlines = []

        self.feed = self.parseRSS(self.rss_url)

        for newsitem in self.feed['items']:
            self.headlines.append(newsitem['title'])
            self.headlines.append(newsitem['link'])
            self.headlines.append(newsitem['summary'])
            self.headlines.append(newsitem['updated'])

        # print('Printing subset of headlines...', set(headlines))
        return self.headlines

    # A list to hold all headlines
    def getRssFeed(self):
        self.allheadlines = []
        # Iterate over the feed urls
        for key, url in self.newsurls.items():
            # Call getHeadlines() and combine the returned headlines with allheadlines

            self.allheadlines.extend(self.getHeadlines(url))

        self.news_list = set(self.allheadlines)
        return self.news_list

