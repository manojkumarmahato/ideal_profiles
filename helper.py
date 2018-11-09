import json
from wordcloud import WordCloud, STOPWORDS
from matplotlib import pyplot as plt
from process_text import *


def load_data(file_name):
    """
    Open the saved json data file and load the data into a dict.
    
    Parameters:
        file_name: the saved file name, e.g. "machine_learning_engineer.json"
    
    Returns:
        postings_dict: data in dict format   
    
    """

    with open(file_name, 'r') as f:
        postings_dict = json.load(f)
        return postings_dict



def plot_wc(text, max_words=200, stopwords_list=[], to_file_name=None):
    """
    Make a word cloud plot using the given text.
    
    Parameters:
        text -- the text as a string
    
    Returns:
        None    
    """
    wordcloud = WordCloud().generate(text)
    stopwords = set(STOPWORDS)
    stopwords.update(stopwords_list)

    wordcloud = WordCloud(background_color='white',
                         stopwords=stopwords,
                         #prefer_horizontal=1,
                         max_words=max_words, 
                         min_font_size=6,
                         scale=1,
                         width = 800, height = 800, 
                         random_state=8).generate(text)
    
    plt.figure(figsize=[16,16])
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()
    
    if to_file_name:
        to_file_name = to_file_name + ".png"
        wordcloud.to_file(to_file_name)



def plot_profile(title, first_n_postings, max_words=200, return_posting=False):
    """
    Loads the corresponding json file, extracts the first_n job postings and plot the wordcloud profile.
    
    Parameters:
        title: the job title such as "data scientist"
        first_n_postings: int, the first n job postings to use for the plot.
    
    Returns:
        nth_posting: the nth job posting as a string. This helps to verify the first_n_postings param used.
    
    """
    # Convert title to full file name then load the data
    file_name = '_'.join(title.split()) + '.json'
    data = load_data(file_name)
    # Get the posting
    if return_posting:
        n_posting = data[str(first_n_postings)]
        return n_posting
    
    text_list = make_text_list(data, first_n_postings)
    cleaned_text = clean_text(text_list)
    
    # Get the stop words to use
    with open('stopwords.csv', 'r', newline='') as f:
        reader = csv.reader(f)
        stop_list = list(reader)[0]
    
    # Join the tokens into a string for plotting
    text = ' '.join(cleaned_text)
    to_file_name = '_'.join(title.split())
    plot_wc(text, max_words, stopwords_list=stop_list, to_file_name=to_file_name)
    
    #return n_posting   
