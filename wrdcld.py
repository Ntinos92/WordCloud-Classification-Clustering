from os import path
from wordcloud import WordCloud, STOPWORDS
import pandas as pd


# Read the whole text.
print("*****************Reading train_set.csv file.*****************")
df = pd.read_csv('train_set.csv',sep='\t')
politics_text = ""
film_text = ""
football_text = ""
business_text = ""
technology_text = ""
for i in range(0, len(df["Content"])):
    if df["Category"][i] == "Politics":
        politics_text += df["Content"][i] + " "
    elif df["Category"][i] == "Film":
        film_text += df["Content"][i] + " "  
    elif df["Category"][i] == "Football":
        football_text += df["Content"][i] + " "  
    elif df["Category"][i] == "Business":
        business_text += df["Content"][i] + " "  
    elif df["Category"][i] == "Technology":
        technology_text += df["Content"][i] + " "    
print("*****************Reading train_set.csv file done.*****************")

stopwords = STOPWORDS.copy()
stopwords.add("said")
stopwords.add("also")
stopwords.add("told")
stopwords.add("one")
stopwords.add("last")
stopwords.add("new")
stopwords.add("say")
stopwords.add("year")
stopwords.add("will")
stopwords.add("yes")
stopwords.add("no")
stopwords.add("although")
stopwords.add("first")
stopwords.add("day")


# Generate a word cloud image
wordcloud1 = WordCloud(stopwords=stopwords).generate(politics_text)
wordcloud2 = WordCloud(stopwords=stopwords).generate(film_text)
wordcloud3 = WordCloud(stopwords=stopwords).generate(football_text)
wordcloud4 = WordCloud(stopwords=stopwords).generate(business_text)
wordcloud5 = WordCloud(stopwords=stopwords).generate(technology_text)

# Display the generated image:
# the matplotlib way:
import matplotlib.pyplot as plt
plt.imshow(wordcloud1, interpolation='bilinear')
plt.axis("off")

plt.imshow(wordcloud2, interpolation='bilinear')
plt.axis("off")

plt.imshow(wordcloud3, interpolation='bilinear')
plt.axis("off")

plt.imshow(wordcloud4, interpolation='bilinear')
plt.axis("off")

plt.imshow(wordcloud5, interpolation='bilinear')
plt.axis("off")

# lower max_font_size
print("*****************Generating wordlcloud for politics.*****************")
wordcloud1 = WordCloud(max_font_size=40).generate(politics_text)
plt.figure()
plt.imshow(wordcloud1, interpolation="bilinear")
plt.axis("off")
plt.show()

print("*****************Generating wordlcloud for films.*****************")
wordcloud2 = WordCloud(max_font_size=40).generate(film_text)
plt.figure()
plt.imshow(wordcloud2, interpolation="bilinear")
plt.axis("off")
plt.show()

print("*****************Generating wordlcloud for football.*****************")
wordcloud3 = WordCloud(max_font_size=40).generate(football_text)
plt.figure()
plt.imshow(wordcloud3, interpolation="bilinear")
plt.axis("off")
plt.show()

print("*****************Generating wordlcloud for business.*****************")
wordcloud4 = WordCloud(max_font_size=40).generate(business_text)
plt.figure()
plt.imshow(wordcloud4, interpolation="bilinear")
plt.axis("off")
plt.show()

print("*****************Generating wordlcloud for technology.*****************")
wordcloud5 = WordCloud(max_font_size=40).generate(technology_text)
plt.figure()
plt.imshow(wordcloud5, interpolation="bilinear")
plt.axis("off")
plt.show()
