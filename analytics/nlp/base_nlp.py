import string
import re

class BaseNLP(object):
    """Implementation of NLP base class"""

    def __init__(self, text=None):
        """Construct a BaseNLP object
        
        Args:
            text (list) : list of text strings
        """
        self._text = None

        if text:
            self.load_text_data(text)

    def load_text_data(self, text):
        if not isinstance(text,list):
            self._text = [text]
        else:
            self._text = text

        if not all(isinstance(item,str) for item in self._text):
            raise TypeError('text must be of type string or list of strings')

    def clean_text_util(self, text):
        '''Utility function to clean text by removing links, special characters 
        using simple regex statements. 

        Args:
            text (list) : list of strings

        Return:
            text (list) : cleaned strings
        '''

        orig_text = ''
        if not isinstance(text,list):
            orig_text = [text]
        else:
            orig_text = text

        if not all(isinstance(item,str) for item in orig_text):
            raise TypeError('text must be of type string or list of strings')

        cleaned_text = []
        stop_chars = ''.join(string.punctuation).replace('@','')
        stop_chars += '…“”’‘'
        for sentence in orig_text:
            clean_sent = ' '.join(sentence.lower().splitlines())
            clean_sent.encode(errors='ignore').decode('utf-8')
            clean_sent = ' '.join(re.sub("(\w+:\/\/\S+)"," ",clean_sent).split())
            for ch in stop_chars:
                clean_sent = clean_sent.replace(ch,'')
            cleaned_text.append(clean_sent)

        if isinstance(text,list):
            return cleaned_text
        else:
            return cleaned_text[0]
