from collections import Counter
import operator
import re
import pandas as pd


def get_all_lines(fname):
    """
    Read all the lines in a whatsapp
    log file in .txt format
    :param fname: path of the log file
    :return lines: list of str
    """
    with open(fname, 'r') as f:
        lines = f.readlines()
    return lines


def parse_lines_into_df(lines, log_type='iphone'):
    """
    Parse all the lines of a Whatsapp log file into a pd.DataFrame.
    Index is date and time in format 'yyyy-mm-dd hh:mm:ss'
    The data frame has two columns, 'message' and 'sender'
    :param lines: list of str
    :return df: pd.DataFrame
    """
    log_type_list = ['iphone', 'android']
    if log_type not in log_type_list:
        raise ValueError('log_type must be iphone or android')

    if log_type == 'iphone':
        expression = r'(?P<date>\d+\/\d+\/\d+) (?P<time>\d+\:\d+\:\d+)\: (?P<sender>.+?):(?P<message>.*)'
    elif log_type == 'android':
        expression = r'(?P<date>\d+\/\d+\/\d+), (?P<time>\d+\:\d+) - (?P<sender>.+?):(?P<message>.*)'
    else:
        raise ValueError('This should not happen.')
    regexp = re.compile(expression)
    match_list = []
    for line in lines:
        match = regexp.match(line)
        if match is not None:
            group_dict = match.groupdict()
            new_dict = {}
            new_dict['date'] = ' '.join([group_dict['date'], group_dict['time']])
            new_dict['message'] = group_dict['message']
            new_dict['sender'] = group_dict['sender']
            match_list.append(new_dict)
    df = pd.DataFrame(match_list)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    return df


def get_word_corpus(df):
    """
    Return a dictionary of unique words in the 'message'
    column of df (the parsed log file in pd.DataFrame format).
    keys are the words, values are the number of occurences
    :param df: pd.DataFrame, a parsed whatsapp conversation
    :return result: dict
    """
    # first lower case every letter in the 'message' column
    df['message'] = df['message'].astype(str).str.lower()
    result = Counter(" ".join(df['message'].values.tolist()).split()).items()
    return dict(result)


def sort_dict_by_values(word_dict, method='descending'):
    """
    Sort a dictionary by values
    :param word_dict:
    :param method:
    :return:
    :raises ValueError:
    """

    if method not in ['descending', 'ascending']:
        raise ValueError('method must be descending or ascending')
    sorted_x = sorted(word_dict.items(), key=operator.itemgetter(1))
    if method == 'ascending':
        return sorted_x
    else:
        return list(reversed(sorted_x))


def variations_of_word(corpus, variation_list, min_count=1):
    """
    Finds words in corpus that start with any of the words
    given in the variation_list
    :param corpus: dict
    :param variation_list: list of str
    :return subset_dict: dict
    """
    subset_dict = {}
    if type(variation_list) == str:
        variation_list = [variation_list]
    for var in variation_list:
        for word in corpus.keys():
            if word.startswith(var) and corpus[word] >= min_count:
                subset_dict[word] = corpus[word]
    df = pd.DataFrame(sort_dict_by_values(subset_dict), columns=['word', 'count'])
    df.set_index('word', inplace=True)
    return df


def get_name_list(df):
    """
    Finds all the unique names in df column 'sender'
    :param df:
    :return:
    """
    return list(df.sender.unique())


def count_user_messages(df):
    """
    Count total number of message
    by each unique user in the
    'sender' column of df

    :param lines:
    :param name_list:
    :return:
    """
    return df.groupby(df.sender).count()['message']


def corpus_to_txt(word_corpus, out_fn):
    with open(out_fn, 'w') as f:
        for pair in sort_dict_by_values(word_corpus):
            word , count = pair
            f.writelines("{} {}\n".format(word, count))
