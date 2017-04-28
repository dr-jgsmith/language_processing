import numpy as np
import pickle
from collections import defaultdict, Counter
from itertools import tee
from scipy.sparse import lil_matrix
import pandas as pd
import difflib

class SDR:
    """********************************************************************************
        
        In general this class will be used to convert tokenized document to a
        sparse distributed representation of the document. The SDR is generated
        from the "binarization" of words in the document. These are then saved as
        indexes, or locations in x,y space where the value of 1 is given the x,y 
        coordinates.

    *******************************************************************************"""

    def __init__(self, token_text=None):
        self.token_text = token_text
        self.series_list = []
        self.sparse_dict = {}


    def create_vec_dict(self):
        # function to create a dictionary of key, value pairs of words with a numerical id. The id serves as a location identifier
        # The dictionary results in a 1 x N series/matrix.
        self.key_val_tokens = {}
        for word in self.token_text:
            location = self.token_text.index(word)
            self.key_val_tokens[word] = location

        self._save_vec_dict(self.key_val_tokens)
        return self.key_val_tokens


    def update_vec_checker(self, word):
        # load most current version of the dictionary
        self.check_list = self._open_vec_dict()
        x = self.check_list.get(word)
        # iterate through the keys to see if the word is present
        if x == None:
            self.location = len(self.check_list) + 1
            self.check_list[word] = self.location
            self._save_vec_dict(self.check_list)
            return self.location
        else:
            self.location = x
            return self.location


    def update_vec_dict(self):
        self._save_vec_dict(self.check_list)
        return None


    def _save_vec_dict(self, tokens):
        self.token_dict = tokens
        pkl_file = open('word_list.pkl', 'wb')
        pickle.dump(self.token_dict, pkl_file)
        pkl_file.close()


    def _open_vec_dict(self):
        pkl_file = open('word_list.pkl', 'rb')
        self.vec_dict = pickle.load(pkl_file)
        return self.vec_dict


    def count_word_occ(self):
        cnt = Counter(self.token_text)
        self.count_list = [cnt[i] for i in self.token_text]
        self.word_count = self.count_list[0::2]
        return self.word_count

    def get_unique_list(self, token_list):
        self.unique_set = list(set(token_list))
        return self.unique_set


    def ordered_list_dict(self, new_list, old_list):
        self.new_set = old_list
        self.z = [self.new_set.append(x) for x in new_list if x not in old_list]
        return self.z

    def vector_as_list(self):
        #take a list of tokenss after self.update_vec_checker is called.
        self.series = []
        for word in self.token_text:
            self.update_vec_checker(word) #function should be called separately. This is just a placeholder for testing and should be removed.
            x = self.location #
            self.series.append(x)

        return self.series


    def vector_as_lol(self):
        self.check_list = self._open_vec_dict()
        check = [max(self.series), len(self.check_list)]
        for i in self.series:
            new_series = []
            i = i-1
            layer = [0] * max(check)
            layer[i] = 1
            new_series.append(layer)
            self.series_list.append(new_series)

        return self.series_list


    def vector_as_series(self):
        self.check_list = self._open_vec_dict()
        check = [max(self.series), len(self.check_list)]
        for i in self.series:
            i = i-1
            layer = [0] * max(check)
            layer[i] = 1
            s = pd.Series(data=layer)
            self.series_list.append(s)

        return self.series_list

    #create a union of vector sequences - this function produces results for generating a stacked array/dataframe
    def vector_as_union(self, series):
        self.check_list = self._open_vec_dict()
        check = [max(series), len(self.check_list)]
        layer = [0] * max(check)
        #assign values of 1 for all locations of i in self.series
        for i in self.series:
            i = i-1
            layer[i] = 1

        self.series_union = pd.Series(data=layer)
        return self.series_union


    #convert a list of series_union sequences into a stack of unions - called when stacking document vectors
    def union_array_stack(self, series_stack):
        self.union_stack = pd.concat(series_stack, axis=1)
        return self.union_stack


    #convert a list of series_union sequences into a stack of TRANSPOSED unions - called when stacking document vectors
    def union_array_stack_T(self, series_stack):
        self.union_stack = pd.concat(series_stack, axis=1)
        self.union_stack_T = self.union_stack.T
        return self.union_stack_T


    def vector_as_df(self):
        self.df_series = pd.concat(self.series_list, axis=1)
        return self.df_series


    def df_transpose(self):
        self.df_series = self.df_series.T
        return self.df_series


    def vector_array_np(self):
        self.full_array = np.array(self.series_list)
        return self.full_array


    def vector_tosparse(self):
        self.sparse_rep = lil_matrix(self.full_array)
        return self.sparse_rep



    def normalize_series_len(self):
        a = [len(i) for i in self.series_list if len(i) > len(self.check_list)]
        #self.vector_layer = np.array(layer)
            #self.series_list.append(self.vector_layer)


    def vector_array_full_index(self):
        self.series_tpl = []
        for word in self.token_text:
            self.update_vec_checker(word)  # Not sure I like calling this function from within the vector_array() function. Will need to consider.
            tp_index = word, self.location, 0, len(self.check_list)
            self.series_tpl.append(tp_index)

        return self.series_tpl

