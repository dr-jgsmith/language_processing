from HtmlMapper import HtmlMapper
from transformtext import TransformText
import json

###########################TEST DATA######################################################
#lets get some text data - terms to use for wikipedia search
term_list = ['climate change', 'adaptation', 'agriculture', 'Famine', 'Food_security', 'Food safety', 'ideology',
             'statistics', 'democracy', 'sociology', 'sustainability', 'The War of 1812', 'collective intelligence',
             'system dynamics', 'weather', 'evil', 'war', "dante's inferno", "Mozart", 'disaster']


text1 = "The Rhine is a European river that begins in the Swiss canton of Graubünden in the southeastern Swiss Alps, forms part of the Swiss-Austrian, Swiss-Liechtenstein, Swiss-German and then the Franco-German border, then flows through the Rhineland and eventually empties into the North Sea in the Netherlands. The largest city on the river Rhine is Cologne, Germany, with a population of more than 1,050,000 people. It is the second-longest river in Central and Western Europe (after the Danube), at about 1,230 km (760 mi), with an average discharge of about 2,900 m3/s (100,000 cu ft/s)."
text2 = "The five senses are taste, touch, hearing, sight, and smell. The tongue is the organ responsible for receiving information about taste, our skin for touch, our ears for sounds, eyes for sight, and nose for smell. Our senses take in information about the surrounding environment and that information is then transferred to the brain."
text3 = "The  House's Freedom Caucus, a group of conservative Republicans, had been pushing for language that would eliminate these required services, but House leaders originally said it couldn't be done under the special procedures through which the legislation is being moved through Congress. These require only 51 votes and don't allow for a Democratic filibuster. Wednesday night, Sen. Mike Lee, R-Utah, said the Senate parliamentarian had told him the insurance provisions would not necessarily violate those budget procedures." 


doc_list = [text1, text2, text3]
resp_data = []
articles = []

######################################



#Open a file we can write to for saving our data
f = open("json_dump.json", "a")

#iterate through a list of terms to check output.
for term in term_list:
    search = HtmlMapper() #call HtmlMapper class to search and get articles
    response = search.search_wiki(term) #Calls search wiki method and returns json/text response
    resp_data.append(response)
    

for response in resp_data:
    process = TransformText(response)
    c_response = process.clean_html(process.t_text) #remove any unwanted markup in a given text response

    words = process.space_tagger(c_response) #calle the spacy.io POS Tagging method
    parsed_words = process.parse(words) #create np chunks

    process.np_sub_chunks(parsed_words) #retrun list of np chunks
    x = process.return_sub_chunks(lower=False) #return unique list of chunks
    data_dump = process.phrase_dump(term, x, c_response) #convert response data into a json format dump
    
    articles.append(data_dump)
        
#Write results to json output   
data = json.dumps(articles, indent=4, separators=(',',':'))
f.write(data)
f.close()