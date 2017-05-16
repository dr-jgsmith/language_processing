Spire - NLP - Tools
===================


Spire is a set of modules written in Python 3.6 for solving various natural language processing tasks. Like [TextBlob](https://textblob.readthedocs.io), Spire uses [NLTK](http://www.nltk.org/), and in some places uses TextBlob instead. Spire also uses the [Spacy](https://spacy.io) natural language processing platform for larger scale text processing. Spire comes with interfaces for mining text data (e.g. Wikipedia, RSS News, National Weather Service, Google Scholar), this includes crawling and scraping website content. Results are generated in JSON, with the next version outputing JSON-LD following [schema.org](http://schema.org/) entries.

----------

Installation
-------------
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

Getting Started
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
Parse tree for Wiki Article "disaster"
```
Tree('S', [Tree('VAN', [Tree('NMM', [Tree('NNP', [('disaster', 'NN')])])]), Tree('VAN', [('is', 'VBZ'), Tree('NMM', [Tree('NNP', [('serious', 'JJ'), ('disruption', 'NN')])])]), ('of', 'IN'), ('the', 'DT'), Tree('VAN', [Tree('NMM', [Tree('NNP', [('functioning', 'NN')])])]), ('of', 'IN'), Tree('VAN', [Tree('NMM', [Tree('NNP', [('community', 'NN')])])]), ('or', 'CC'), Tree('VAN', [Tree('NMM', [Tree('NNP', [('society', 'NN')])])]), Tree('VAN', [('involving', 'VBG'), Tree('NMM', [Tree('NNP', [('widespread', 'JJ'), ('human', 'NN')])])]), (',', ','), Tree('VAN', [Tree('NMM', [Tree('NNP', [('material', 'NN')])])]), (',', ','), Tree('VAN', [Tree('NMM', [Tree('NNP', [('economic', 'JJ')])])]), ('or', 'CC'), Tree('VAN', [Tree('NMM', [Tree('NNP', [('environmental', 'JJ'), ('loss', 'NN')])])]), ('and', 'CC'), Tree('VAN', [Tree('NMM', [Tree('NNP', [('impacts', 'NNS')])])]), (',', ','), ('which', 'WDT'), ('exceeds', 'VBZ'), ('the', 'DT'), Tree('VAN', [Tree('NMM', [Tree('NNP', [('ability', 'NN')])])]), ('of', 'IN'), ('the', 'DT'), Tree('VAN', [('affected', 'VBN'), Tree('NMM', [Tree('NNP', [('community', 'NN')])])]), ('or', 'CC'), Tree('VAN', [Tree('NMM', [Tree('NNP', [('society', 'NN')])])]), ('to', 'TO'), ('cope', 'VB'), ('using', 'VBG'), ('its', 'PRP$'), Tree('VAN', [Tree('NMM', [Tree('NNP', [('own', 'JJ'), ('resources', 'NNS')])])]), ('.', '.')
```
Tree labels (e.g. `Tree('VAN', [Tree('NMM'`) where you see `'VAN'` or `'NMM'` correspond to a specific grammar rule. Grammars can be defined using the NLTK Regex syntax. And multiple grammars can be defined and stored within Spire for use in case-by-case scenarios.

The grammar used in these examples is grammar_II (a public attribute).
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
For now, the default return is an unordered set of words and phrases retained from a given document. Finally, the results are processed and prepped to be loaded into a JSON formatted doc.
```
data_dump = process.phrase_dump(term, x, c_response)
articles.append(data_dump)

data = json.dumps(articles, indent=4, separators=(',',':'))
```
 
        
**Check your results!**


TransformText.py
-------------------

HtmlMapper.py
-------------------