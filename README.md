# nlp-tools

NLP- tools as a set of modules written in Python 3.6 that integrates the NLTK (http://www.nltk.org/) and Spacy (https://spacy.io) natural language processing toolkits. In addition, the sets of modules provide integration with Gensim (https://radimrehurek.com/gensim/), that can be used in topic analysis and language classification.

NLP-tools comes with an HTMLmapper class that serves to support data collection over the web. HtmlMapper provides wrappers for searching Wikipedia, Google Scholar,, and a simple web crawler that can map and extract text information from websites. Additional support is provider for collecting RSS Streams using the Feedparser library.

Basic Usage

term_list = ['climate change', 'adaptation']


#Open a file we can write to for saving our data
f = open("json_dump.json", "a")
#iterate through a list of terms to check output.
for term in term_list:
   search = HtmlMapper() #call HtmlMapper class to search and get articles
   response = search.search_wiki(term) #Calls search wiki method and returns json/text response
   resp_data.append(response)
