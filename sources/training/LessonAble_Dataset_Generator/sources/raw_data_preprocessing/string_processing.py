import num2words
from datetime import datetime
import re

def time_to_seconds(time_string) -> float:
    """
    converts the string time to seconds
    Returns:
    -------
    the time_string converted in seconds

    """
    date_time = datetime.strptime(time_string.rstrip().lstrip(), "%H:%M:%S,%f")
    a_timedelta = date_time - datetime(1900, 1, 1)
    seconds = a_timedelta.total_seconds()
    return seconds

def convert_comma_numbers(s):
    s = s.lstrip('.').rstrip('.')
    pattern = re.compile("(\d+,\d+)")
    if pattern.match(s):
        string = s.replace(',', '.')
        return string
    else:
        return s

def text_num_2_str(text, language) -> str:
    """
    converts a text containing numbers to a text with those numbers converted to strings in the given language. For now IT and EN are supported
    
    Returns:
    -------
    the string with the converted numbers into text.
    """
    new_text = re.sub('[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?', lambda x: num2words.num2words(int(x.group()), lang=language) if x.group().isdigit() else num2words.num2words(float(convert_comma_numbers(x.group())), lang=language) , text)
    return new_text

def process_string(sentence, language):
  # 1. convert the numbers to string with the assigned language
  new_sentence = text_num_2_str(sentence, language)
  new_sentence = re.sub("[^0-9a-zA-Z.,'!?_À-ÿ\s]+", '', new_sentence)
  new_sentence_without_double_spaces = re.sub(' +', ' ', new_sentence)
  return new_sentence_without_double_spaces
