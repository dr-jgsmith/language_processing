
from SDRCake import SDR
from gensim import corpora, models, similarities

class VisualizeEdges:
    def __init__(self, data_list):
        self.data_list = data_list

    def draw_network(self):
        G = nx.DiGraph()
        G.add_edges_from(self.data_list)
        nx.draw(G, with_labels=False)

    def draw_frm_csv(self, path_name='godan_data_links.csv'):
        self.path_name = path_name

        file = csv.reader(open(self.path_name, 'r'))

        for i in file:
            print(i)
            G.add_edges_from(i)

        nx.draw(G, with_labels=False)


class Storage:
    def __init__(self, store_type='sqlite'):
        self.store_type = store_type

    def _csv_dump(self):
        f = csv.writer(open('godan_data_links.csv', 'a', newline=""))
        for row in edges_list:
            f.writerow(row)


class Learning_Setup:

    def __init__(self):
        self.resources = []
        self.word_list = []

    def learn_dictionary(self):
        print("Calling word list.....")
        f = open("wordlist.txt", 'r')
        for line in f:
            line = line.replace('\n', '').replace('\r', '')
            self.word_list.append(line)

        process = SDR(self.word_list)
        text_dict = process.create_vec_dict()
        process._save_vec_dict(text_dict)

        return None

    def learn_gensim_dictionary(self):
        list_of_list = []
        print("Calling word list.....")
        f = open("wordlist.txt", 'r')
        for line in f:
            line = line.replace('\n', '').replace('\r', '')
            self.word_list.append(line)

        list_of_list.append(self.word_list)

        self.dictionary = corpora.Dictionary(list_of_list)
        self.dictionary.save('data_dump.dic')
        self.dictionary.token2id

        return self.dictionary
"""

class SDRFunctions(SDR):

    def __init__(self, string_text=None, token_text=None, num_text=None):


10,266 Acres affected by wetlands
521 parcels with wet langs
76% of all ag lands within wetlands.
"""