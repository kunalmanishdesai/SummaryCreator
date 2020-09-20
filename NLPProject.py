
import bs4 as bs
import urllib.request
import re

print("\nDefault URL: https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_India\n")
url = input("Enter URL or press enter to use Defualt URL:\n")
print()
if url == "":url = "https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_India"

scraped_data = urllib.request.urlopen(url)
article = scraped_data.read()

parsed_article = bs.BeautifulSoup(article,'lxml')

paragraphs = parsed_article.find_all('p')

article_text = ""

for p in paragraphs:
    article_text += p.text


# # Preprocessing
# 
# The first preprocessing step is to remove references from the article. Wikipedia, references are enclosed in square brackets. The following script removes the square brackets and replaces the resulting multiple spaces by a single space. Take a look at the script below:

article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
article_text = re.sub(r'\s+', ' ', article_text)


# To clean the text and calculate weighted frequences, we will create another object.

# In[25]:


formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)


# In[26]:


import nltk
nltk.download('punkt')
nltk.download('stopwords')


# The following script performs sentence tokenization:
# 

# In[27]:


sentence_list = nltk.sent_tokenize(article_text)


# To find the frequency of occurrence of each word, we use the formatted_article_text variable. We used this variable to find the frequency of occurrence since it doesn't contain punctuation, digits, or other special characters. Take a look at the following script:

# In[28]:


stopwords = nltk.corpus.stopwords.words('english')

word_frequencies = {}
for word in nltk.word_tokenize(formatted_article_text):
    if word not in stopwords:
        if word not in word_frequencies.keys():
            word_frequencies[word] = 1
        else:
            word_frequencies[word] += 1


# Finally, to find the weighted frequency, we can simply divide the number of occurances of all the words by the frequency of the most occurring word, as shown below:

# In[29]:


maximum_frequncy = max(word_frequencies.values())

for word in word_frequencies.keys():
    word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)


# # Calculating Sentence Scores
# We have now calculated the weighted frequencies for all the words. Now is the time to calculate the scores for each sentence by adding weighted frequencies of the words that occur in that particular sentence. The following script calculates sentence scores:

# In[30]:


sentence_scores = {}
for sent in sentence_list:
    for word in nltk.word_tokenize(sent.lower()):
        if word in word_frequencies.keys():
            if len(sent.split(' ')) < 30:
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word]
                else:
                    sentence_scores[sent] += word_frequencies[word]


# # Getting the Summary
# Now we have the sentence_scores dictionary that contains sentences with their corresponding score. To summarize the article, we can take top N sentences with the highest scores. The following script retrieves top 7 sentences and prints them on the screen.

# In[31]:


import heapq
summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

summary = ' '.join(summary_sentences)
print()
print(summary)

