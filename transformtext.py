import nltk, re
from nltk.tree import *
from itertools import tee
from textblob import TextBlob
from gensim import corpora, models, similarities
from collections import defaultdict, Counter
import spacy


class TransformText:
    def __init__(self, text):
        self.t_textext = str(text)
        
        self.t_textmp_phrases = defaultdict(int)

        self.stop_list = ["(", ")", "]", ".", "\\", "/", "[", '...', '–', ':', ';', '____', '___', '+', '/w', '>']

        self.sub_chunks = []
        
        #calls grammar first in list is the nount-adj/verb-noun phrase
        #this current grammar parses sentence in some very interesting ways.
        #definitely worth keep this list of expressions

        #NPS and VPH patterns 
        self.grammar_II = """
                    NNP: {<J.*|N.*>+}
                    NMM: {<SYM>?<CD>?<N.+>+}
                    VAN: {<V.*>?<J.*|N.*>*<HYPH>*<J.*|N.*>+}
                    NUM: {<CD>+}
                """
                
        self.grammar_III = """
                    NUM: {<CD>+}
                    VPH: {<V.*|N.*>*<IN>*<V.*|N.*>+}
                """
        # sequence to strip stop words and characters from the text
        # split text into string list

        self.t_text = TextBlob(self.t_textext)

        self.nlp = spacy.load('en', parser=False) #spaCY corpus https://spacy.io
        
    """*******************************************************************************
        The following set of functions use the TextBlob package to perform some simple
        text processing prcedures. Sentence chunking, basic word tokenization as well
        as n-grams, noun phrase chunking and a simple POS tagger.
        
        Note: I would only use these for basic processing -  sentence chunking/Bi-Grams.
    ******************************************************************************"""
    
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

    
    
    """***********************************************************************************
        The following set of methods break out of Textblob and use NLTK (directly), GENSIM or 
        home-rolled solutions.
        
        E.g. the tokenizer and dictionary methods provide a more sophisticated model for 
        accessing and updating terms in the corpus. 
        
        #full tokener currently only breaks down words, another version will include a 
        unicode charcter input model. The TextBlob tool to split and return a parsed word 
        list is not always accurate, or in the format we want for high performance 
        prediction.
        
        Output can be altered by modifying the stop_list parameters.
        
    ************************************************************************************"""
    def full_tokener(self):
        #takes a textblob input, splits words in a list
        tmp = self.t_text.split()
        for j in tmp:
            for word in j.split():
                list(word) #split list strings into list of characters
                tmp2 = []
                # iterate through sublist items and remove if present in the stop_list
                for chars in list(word):
                    if chars not in self.stop_list: #IMPORTANT adding or removing values will change the output
                        tmp2.append(chars)
                        joined_chars = ''.join(tmp2)
                    else:
                        del chars
                
                self.clean_list.append(joined_chars)
                
        return self.clean_list
    

    #method requires
    def sent_tokener(self):
        self.sent_tokens = []
        for i in self.t_text.sentences:
            self.sent_tokens.append(str(i).split())
                       
        return self.sent_tokens
    
    
    def clean_sent_tokens(self, sent_list):
        #takes a textblob input, splits words in a list'
        self.clean_sent = []
        
        for j in sent_list:
            list(j) #split list strings into list of characters
            tmp = []
                # iterate through sublist items and remove if present in the stop_list
            for chars in list(j):
                if chars not in self.stop_list: #IMPORTANT adding or removing values will change the output
                    tmp.append(chars)
                    joined_chars = ''.join(tmp)
                else:
                    del chars
                
            self.clean_sent.append(joined_chars)
        
        return self.clean_sent


    ########################ReGex POS Tagging#######################
    
    #baseline nltk parser
    def nltk_tagger(self, pros_list):
        """
            This provides basic functionality for tagging and parsing a single document.
            This method takes a tokenized document or list of words with 'most' special
            characters removed from the file.
        
        """
        
        self.tagged = nltk.pos_tag(pros_list) #Implements the MAXENT POS Tagger
        
        #returns a list of objects. Relevant phrase objects will have a label associated
        return self.tagged

    
    """#######################################################################################
    
    Spacy Chunker/POS Tool
    
    In order to use the spacy tools (space_tgger, and space_ent), you must pass raw text strings.
    Not lists, as in the case of the other
    
    ########################################################################################"""
    
    
    def space_tagger(self, text_doc):
        
        self.docs = []
        
        doc = self.nlp(text_doc) #load text
        
        for word in doc:
            seq = (word.text, word.tag_)
            self.docs.append(seq)
     
        #self.docs.append(sents)
        
        return self.docs
        
    
    
    def space_ent(self, text_doc):
        
        self.doc_ents = []
        
        doc = self.nlp(text_doc) #load text
        
        for word in doc.ents:
            seq = (word.text, word.label_)
            self.doc_ents.append(seq)
     
        #self.docs.append(sents)
        
        return self.doc_ents
    
    
    
    def parse(self, tagged_text):
        
        cp = nltk.RegexpParser(self.grammar_II) #
        
        self.result = cp.parse(tagged_text)
    
        return self.result

    
    
    """***********************************************************************************
        Sentence based chunker methods - As of 3/22/2017 these produce the best results.
    
    ************************************************************************************"""
    
    
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


        
    def return_sub_chunks(self, lower=True):
        """
        Process NP Chunks and returns a list of unique phrases for a given document.
        """
        phrase_set = []
        self.sent_phrases = []
        
        tag_set = ["NMM"]
        
        [phrase_set.append(chunk) for chunk in self.sub_chunks if chunk[0] in tag_set]
        
        for phrase in phrase_set:
            
            if lower == False:
                phrase[1:] = [' '.join(phrase[1:])]
            else:
                phrase[1:] = [' '.join(phrase[1:]).lower()]
            
            x = phrase[1:]
            self.sent_phrases.append(x[0])
        
        print(list(set(self.sent_phrases)))
        
        self.doc_phrases = list(set(self.sent_phrases))
        
        return self.doc_phrases
    
    
    ################################
    ################################
    ################################
    def return_chunks(self):
        """
        Process NP Chunks and returns a list of unique phrases for a given document.
        """
        phrase_set = []
        for chunk in self.chunks:
            phrase = ' '.join(chunk)
            phrase_set.append(phrase)
            
        self.doc_phrases = list(set(phrase_set))
        return self.doc_phrases


    #generate a data dump object to be passed to json.dumps method for saving dict list as json.
    def phrase_dump(self, doc_term, phrase_list, sentences):
        self.t_textmp_phrases.update(document=doc_term, phrases=phrase_list, sentences=sentences)
        
        return self.t_textmp_phrases

    
    
    
    """***********************************************************************************
        The following set of methods are currently in experimental phase.
        These include LDA and Non-Parametric Bayesian Inference Models for Topic Analysis.
        The combination of noun phrasing/named entity extraction along with topic models
        can provide a baseline for creating hierachical classification tools to detect
        hierachies of text/conceptual relationships.
    
    ************************************************************************************"""

    def gen_bag_words(self, documents):
        self.dictionary = corpora.Dictionary(documents)
        self.dictionary.save('data_dump.dic') #Note uses a different approach than SDRCake
        self.corpus = [self.dictionary.doc2bow(document) for document in documents]
        return self.corpus

    def bayesian_topic(self):
        #this leverages gensim non-parametric bayesian algorithm
        self.model = models.HdpModel(self.corpus, id2word=self.dictionary)
        return  self.model

    #IMPORTANT Method - Turns a document into an edge list - Document Terms as Network
    def pairwise(self, iterable):
        "s -> (s0,s1), (s1,s2), (s2, s3), ..."
        a, b = tee(iterable)
        next(b, None)
        self.pairs = zip(a, b)
        return self.pairs


    
    """**********************************************************************************
    
        Baseline html tag removal. Should be called all documents to ensure special characters 
        are removed. Works relatively well for our currrent purposes. It is an older method 
        originally supplied within the NLTK package but was removed in the most recent iterations. 
        I saved it because it actually works very well compared to other methods I have seen.
        
    ************************************************************************************"""
    def clean_html(self, html):
        """
        Remove HTML markup from the given string.

        :param html: the HTML string to be cleaned
        :type html: str
        :rtype: str
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
