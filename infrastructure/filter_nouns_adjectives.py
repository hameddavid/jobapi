import nltk
from nltk import pos_tag, word_tokenize
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords') 
def filter_nouns_adjectives(text):
    try:

        tokens = word_tokenize(text)
        tagged_tokens = pos_tag(tokens)
        filtered_tokens = [word for word, tag in tagged_tokens if tag.startswith('N') or tag.startswith('J')]
        filtered_tokens = [word.lower() for word in filtered_tokens if word.lower() not in stopwords.words('english')]
    except Exception as e:
           filtered_tokens = text  # returns the original text
    return filtered_tokens
'''
# Example usage:
user_input = "This is an example sentence with some keywords."
filtered_keywords = filter_nouns_adjectives(user_input)
print(filtered_keywords)
'''