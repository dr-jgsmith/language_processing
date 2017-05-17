# Spire - NLP - Tools

# Table of contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Getting Started](#gettingstarted)
4. [TransformText](#transformtext)
5. [HtmlMapper](#htmlmapper)
6. [SDRCake](#sdrcake)

## Introduction
Spire is a set of modules written in Python 3.6 for solving various natural language processing tasks. Like [TextBlob1](https://textblob.readthedocs.io), Spire uses [NLTK](http://www.nltk.org/), and in some places uses TextBlob instead. Spire also uses the [Spacy](https://spacy.io) natural language processing platform for larger scale text processing. Spire comes with interfaces for mining text data (e.g. Wikipedia, RSS News, National Weather Service, Google Scholar), this includes crawling and scraping website content. Results are generated in JSON, with the next version outputing JSON-LD following [schema.org](http://schema.org/) entries, and Facebook's [Open Graph Protocol](http://opengraphprotocol.org/). 

The end goal of Spire is to provide a relatively easy to use set of tools to generate structured data from unstructured data (i.e. text) for conducting natural language understanding experiments, cognitive mapping from text, bootstrapping metadata to existing web content, as well as event or anomaly detection. 

Structured data sets can then be paired with other data to identify correlations between texts (e.g. discourse) and events such as changes in commodity and equity markets, acute and slow-burn disturbances (e.g. wildfire, drought, flood, hurricanes).

Spire development is sponsored in part by [USDA-NIFA](https://nifa.usda.gov/), [eXtension](https://extension.org) and [GODAN](http://www.godan.info/). Additional support has been received from private businesses needing a unified interface and accurate methods for doing NLP. 

----------

## Installation
Spire does not have a pip/easy_install version. This means you will need to install NLTK 3.0, TextBlob and Spacy. The required packages can be installed using pip

    $ pip install nltk
    $ pip install textblob
    $ pip install --U spacy

> **Note:** Be sure to download the corpora for NLTK and Spacy. Both use different data sets in some examples.

For more information regarding download and installation please go to: NLTK Installation; Spacy Installation.

NLP-Tools also provides integration with [Gensim](https://radimrehurek.com/gensim/). Gensim provides easy methods for exploring and solving various topic modelling problems. Gensim is easy to install - `pip install gensim`.

 The HtmlMapper.py module provides all the available methods for mining text data. Several additional python packages will need to be installed to make use of the module.

> **Note:** Important! Install ALL

    $ pip install requests
    $ pip install wikipedia
    $ pip install scholarly
    $ pip install feedparser
Now that the dependencies have been installed, you can download or clone this repository and test.

-------------------

## Getting Started
-------------------
To get started, lets open the **main.py** file in your Python IDE. Run the **main.py** file - `$ python main.py`, and check your results. The sample main.py runs through a series of NLP experiments to help you get started. 

You will notice that our two primary modules `HtmlMapper` and `TransformText` are imported.
```
from HtmlMapper import HtmlMapper
from transformtext import TransformText
import json
```
You will also notice a several lists populated with a handful of terms and several sentences. 
```
term_list = ['climate change', 'adaptation', 'agriculture', 'Famine', 'Food_security', 'Food safety', 'ideology'...]
```          

The list of terms are used as search terms for collecting Wikipedia article summaries.  The code below iterates through a list of terms, collects the summaries for each entry and appends to a list for later processing.
```
    for term in term_list:
	    #Initialize Search
	    search = HtmlMapper()
	     
	    #Search wiki - returns json/text response
	    response = search.search_wiki(term) 
	    
	    #Append response data to list
	    resp_data.append(response)
    
```
Summary text are collected and accessed via `resp_data` , a Python list containing the article summary.  The list of summaries can then be based to the `TransformText()` by iterating over each item in the summaries list.
```
for response in resp_data:
	process = TransformText(response)
		
	#Response is stripped of html tags.
	c_response = process.clean_html(process.t_text)
```
> **Result:** TextBlob("A disaster is a serious disruption of the functioning of a community or a society involving widespread human, material, economic or environmental loss and impacts, which exceeds the ability of the affected community or society to cope using its own resources.")

With the html tags removed from the text response, we can now run the results through a series of processes. The first step is to tag the text based upon parts-of-speech. In this case, we rely on Spacy's POS-Tagging tool as it is significantly more accurate in our tests.
```
words = process.space_tagger(c_response) 
parsed_words = process.parse(words) 
```
Parse tree for the [Wikipedia Article - Disaster](https://en.wikipedia.org/wiki/Disaster)
```
Tree('S', [Tree('VAN', [Tree('NMM', [Tree('NNP', [('disaster', 'NN')])])]), Tree('VAN', [('is', 'VBZ'), Tree('NMM', [Tree('NNP', [('serious', 'JJ'), ('disruption', 'NN')])])]), ('of', 'IN'), ('the', 'DT'), Tree('VAN', [Tree('NMM', [Tree('NNP', [('functioning', 'NN')])])]), ('of', 'IN'), Tree('VAN', [Tree('NMM', [Tree('NNP', [('community', 'NN')])])]), ('or', 'CC'), Tree('VAN', [Tree('NMM', [Tree('NNP', [('society', 'NN')])])]), Tree('VAN', [('involving', 'VBG'), Tree('NMM', [Tree('NNP', [('widespread', 'JJ'), ('human', 'NN')])])]), (',', ','), Tree('VAN', [Tree('NMM', [Tree('NNP', [('material', 'NN')])])]), (',', ','), Tree('VAN', [Tree('NMM', [Tree('NNP', [('economic', 'JJ')])])]), ('or', 'CC'), Tree('VAN', [Tree('NMM', [Tree('NNP', [('environmental', 'JJ'), ('loss', 'NN')])])]), ('and', 'CC'), Tree('VAN', [Tree('NMM', [Tree('NNP', [('impacts', 'NNS')])])]), (',', ','), ('which', 'WDT'), ('exceeds', 'VBZ'), ('the', 'DT'), Tree('VAN', [Tree('NMM', [Tree('NNP', [('ability', 'NN')])])]), ('of', 'IN'), ('the', 'DT'), Tree('VAN', [('affected', 'VBN'), Tree('NMM', [Tree('NNP', [('community', 'NN')])])]), ('or', 'CC'), Tree('VAN', [Tree('NMM', [Tree('NNP', [('society', 'NN')])])]), ('to', 'TO'), ('cope', 'VB'), ('using', 'VBG'), ('its', 'PRP$'), Tree('VAN', [Tree('NMM', [Tree('NNP', [('own', 'JJ'), ('resources', 'NNS')])])]), ('.', '.')
```
Tree labels (e.g. `Tree('VAN', [Tree('NMM'`) where you see `'VAN'` or `'NMM'` correspond to a specific grammar rule. Grammars can be defined using the NLTK Regex syntax. And multiple grammars can be defined and stored within Spire for use in case-by-case scenarios.

The grammar used in these examples is grammar_II (a publicly accessible attribute).
```
NNP: {<J.*|N.*>+}
NMM: {<SYM>?<CD>?<N.+>+}
VAN: {<V.*>?<J.*|N.*>*<HYPH>*<J.*|N.*>+}
NUM: {<CD>+}  
```
Once the parse tree is created, we can traverse the tree and collect sequences of chunks based on our formal grammar, and plug into Gensim to generate data models for topic modeling around concepts.
```
process.np_sub_chunks(parsed_words)
``` 
You can access the returned results of this method by calling `process.sub_chunks`. The results produce a list of lists.
```
 ['VAN', 'disaster'],
 ['NMM', 'disaster'],
 ['NNP', 'disaster'],
 ['VAN', 'is serious disruption'],
 ['NMM', 'serious disruption'],
 ['NNP', 'serious disruption'],
 ['VAN', 'functioning'],
 ['NMM', 'functioning'],
 ['NNP', 'functioning'],
 ['VAN', 'community'],
 ['NMM', 'community'],
 ['NNP', 'community'],
 ['VAN', 'society'],
 ['NMM', 'society'],
 ['NNP', 'society'],
 ['VAN', 'involving widespread human'],
 ['NMM', 'widespread human'],
 ['NNP', 'widespread human']
```
The next steps go over these results, and retain a unique set of words and phrases.
```
x = process.return_sub_chunks(lower=False)
```
   
The value for `x` is an un-ordered list created using `list(set(mylist))` 
```
> ['become disasters',
 'hits more',
 'Hazards',
 'case',
 'managed risk',
 'is serious disruption',
 'involving widespread human',
 'hazards',
 'product',
 'material',
 'percentage',
 'community',
 'times greater',
 'natural hazards',
 'uninhabited regions',
 'are 20 times greater',
 'industrialized countries',
 'affected community'...]
```
To retrieve the list in order, and with all retained instances of a word or phrase, you can call `process.sent_phrases`.
```
> '95 percent',
 'percent',
 'deaths',
 'deaths',
 'deaths',
 'hazards',
 'hazards',
 'hazards',
 'developing countries',
 'countries',
 'countries',
 'losses due',
 'losses due',
 'losses due',
 'natural hazards',
 'natural hazards',
 'natural hazards',
 'are 20 times greater',
 '20 times greater',
 'times greater',
 'percentage',
 'percentage',
 'percentage',
 'GDP',
```
For now, the default return is an un-ordered set of words and phrases retained from a given document. Finally, the results are processed and prepped to be loaded into a JSON formatted doc.
```
data_dump = process.phrase_dump(term, x, c_response)
articles.append(data_dump)

data = json.dumps(articles, indent=4, separators=(',',':'))
```
 
        
**Check your results!**
For more information on specific methods for each of the primary classes, please see **TransformText**, **HtmlMapper**, and **SDRCake**.

----------


## TransformText
The TransformText module provides a number of methods for interacting with text data. The primary set of basic language processing tools simply provides a common way for working with TextBlob (an easy to use wrapper for NLTK), NLTK itself, and Spacy.

> **Note:** Future iterations of Spire will include integration with a Sparse Distributed Representations module (*see:* SDRCake).

When you first instantiate the `TransformText()`, class you are required to pass some type of text blob into the constructor. For example, the text below is a string within a Python list.
```
text = ['A disaster is a serious disruption of the functioning of a community or a society involving widespread human, material, economic or environmental loss and impacts, which exceeds the ability of the affected community or society to cope using its own resources.']
``` 


# Initialize TransformText Class
The text string is passed as a variable or directly into TransformText(text). From this point, all of the TransformText methods are available for stemming, tokenization, parsing, tagging, etc.
```
def get_sentences(self):
	return self.t_text.sentences
	 
def get_words(self):
	return self.t_text.words

def get_bigrams(self):
	return self.t_text.ngrams(n=2)

def get_trigrams(self):
    return self.t_text.ngrams(n=3)

def get_np_chunks(self, text=None):
    if text == None:
	    return self.t_text.noun_phrases
    else:
	    self.t_text = TextBlob(text)
        return self.t_text.noun_phrases

def simple_tagger(self, text=None):
	if text == None:
        return self.t_text.tags
    else:
        self.t_text = TextBlob(text)
        return self.t_text.tags
```

These methods are simply interfaces for accessing the TextBlob API and NLTK. These methods are useful for conducting some baseline evaluation of a rudimentary NLP solution. The methods serve as a the standard for improving accuracy and speed of output. They also provide a common model for interacting with all of the different NLP packages. 

# Cleaning Text
All of these methods take a raw text string (or list of strings) as input. However, there is no guarantee that these strings are not stacked with unnecessary characters. For example, parsing through an html file results in inaccurate parse results. To solve for this, we assume that all text passed  will be malformed or include irrelevant characters. The `clean_html()` method provide support for removing these characters (e.g. html tags, css and javascript).

```
def clean_html(self, html):
        """
        Remove HTML markup from the given string.
        """
        self.str_html = str(html)

        # First we remove inline JavaScript/CSS:
        self.cleaned = re.sub(r"(?is)<(script|style).*?>.*?(</\1>)", "", self.str_html.strip())
        # Then we remove html comments. This has to be done before removing regular
        # tags since comments can contain '>' characters.
        self.cleaned = re.sub(r"(?s)<!--(.*?)-->[\n]?", "", self.cleaned)
        # Next we can remove the remaining tags:
        self.cleaned = re.sub(r"(?s)<.*?>", " ", self.cleaned)
        # Finally, we deal with whitespace
        self.cleaned = re.sub(r"&nbsp;", " ", self.cleaned)
        self.cleaned = re.sub(r"[\s]", "  ", self.cleaned)
        self.cleaned = re.sub(r"  ", " ", self.cleaned)
        self.cleaned = re.sub(r"  ", "\n", self.cleaned)

        self.clean = self.cleaned.split()

        for i in self.clean:
            if len(i) <= 1:
                self.clean.remove(i)
            else:
                pass

        self.clean = ' '.join(self.clean)

        return self.clean

```

The result is a text blob stripped of any html characters. Now, we can use the additional methods to perform some essential operations on our text data. 

# Tagging and Parsing
While there are several ways carry out parsing and tagging operations in Spire, the preferred default method uses Spacy for the tagging, and NLTK Tree Traverse method to parse and capture tagged data.

```
def space_tagger(self, text_doc):
	self.docs = []
        
    doc = self.nlp(text_doc) #load text
        
    for word in doc:
	    seq = (word.text, word.tag_)
        self.docs.append(seq)
        
    return self.docs
```
This results in a list of tuples with the word and corresponding parts-of-speech. This list is passed to the `parse(tagged_doc)` method which returns a parse tree that can be traversed rather quickly.
```
def parse(self, tagged_text):
	cp = nltk.RegexpParser(self.grammar_II)
    self.result = cp.parse(tagged_text)
    return self.result
```
As you might have noticed, this method makes use of the formal grammar defined in the constructor method for the `TransformText class` Traversing the tree performed in the `np_sub_chunk()` method which stands for Noun Phrase Sub Chunk which simply extracts noun-phrases from a text based upon the grammar rules.
```
def np_sub_chunks(self, result):
	"""
    Finds NP (nounphrase) leaf nodes of a chunk tree.
    Takes on the result list from the re_parse_chunker function.
        
	Checks to see if object in sentence tree has a label. 
    Items without labels are ignored.
    """
    self.clean_list = []
        
    #uses the nltk.Tree class and tree class methods | worth reading 
     for tree in result.subtrees():
	     phrases = []
         #load label for each expression - labels are defined by the grammar attribute
         phrases.append(tree.label())
            
         for i in tree.pos():
	         phrases.append(i[0][0])
               
      self.sub_chunks.append(phrases)
      return self.sub_chunks
```
Finally, the results are passed to the `return_sub_chunks()` method that returns the complete list of retained phrases and a unique set of phrases. These can be saved using json.dumps() or passed into a CSV file or SQL DB.

> **Note:** This will change in future versions of Spire. Return results will be an Ordered Dictionary to easy word count and phrase count. This is particularly useful for building [Sense2Vec](https://arxiv.org/abs/1511.06388) and [skip-gram](http://homepages.inf.ed.ac.uk/ballison/pdf/lrec_skipgrams.pdf) language processing models.

-------------------

## HtmlMapper
The HtmlMapper module provides a number of useful functions for collecting and extracting text data from various sources. Currently, Spire comes with access methods to Wikipedia article summaries, RSS Streams from News, Finance and National Weather Service. 

Additionally, a rudimentary search function is available using Faroo API. To use the web or news search through Faroo, you will need to visit their site and request API key. Finally, there is a very simple web crawler tool that can be used to index and scrape website content.

To begin, lets look at the `HtmlMapper()` class. The constructor takes two optional arguments. 

```
def __init__(self, term=None, start_url=None)
```
This lets you choose one input field, either using a **term** for search, or starting url for performing a crawl-n-scrape.

# Crawl and Scrape
The crawl and scrape can be done by providing a full url with an ending backslash. For  example, scraping USDA-NIFA would begin by passing the url string as `"https://nifa.usda.gov/"` This url can serve as a seed site for initializing the crawl. It is passed to the `get_seed_links()` method

```
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
```
This method returns a list of links to feed the next method that performs the URL fetch and scrape.  The link list is then passed to `deep_link_scrape(url_list)`

> **Note:** The  **deep_link_scrape(url_list)** method defaults to two layers deep from the original starting URL. The methods themselves could be wrapped inside a recursive function to scrape many levels deeper.

Finally, the results from the link scrape can be iterated over to fetch the HTML documents from each link in the list using the `get_raw_html()` or `get_data_from_link()` methods. The results output a binary, or text representation of the HTML document.  These can then be passed to the `TransformText` class and stripped of HTML characters as described in the **cleaning** section.

# Wikipedia Search
Currently Spire comes with a very simple implementation of the Wikipedia Python Package. It simply implements the search and retrieve summary method from the package. This is extremely useful for testing your different NLP methods.

Pass a search term or phrase as string type into the `search_wiki()` method. This will return the article summary or none if there is a **disambiguation Exception** or not found.

> **Note:** The Wikipedia API Python package should not be used for massive data scrapping. It is possible to use the Wiki Terms dump to generate training data for a neural net or Bayesian network. But you will need to manage the rate limits.

# RSS Streams
The RSSStreams class uses the Python Feedparser package to grab structured news and financial services data. 

> **Note:** This class is under reconstruction to make it easier to add RSS feeds on the fly. Currently, the class relies on feeds being hard-coded in the constructor method.

```
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

```


-------------------

## SDRCake
SDRCake is currently an experimental approach to generating sparse distributed arrays of data. The sparse arrays are stacked and converted to bitmap images that can be modeled for pooling spatially explicit semantic features.  

In the figure below, partial least squares is used for image classification of pooled data. In the same manner, texts can be represented as visual (spatial) and time (temporal) explicit representations.

![enter image description here]
(http://www.stat.ucla.edu/~junzhu/project/hsp/fig/HRD.png)

For more information on the pooling mechanisms see: [Image Classification by Hierarchical Spatial Pooling with Partial Least Squares Analysis](http://www.stat.ucla.edu/~junzhu/project/hsp.html)<!--se_discussion_list:{"5YAkspTuS4YLOK2XBAGBAlaA":{"selectionStart":3173,"selectionEnd":3169,"commentList":[{"content":"sh"}],"discussionIndex":"5YAkspTuS4YLOK2XBAGBAlaA"}}-->
