import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os, ssl

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

@st.cache
def data():
    AWS_BUCKET_URL = "https://melon-testing-word-count.s3.us-west-2.amazonaws.com/melon_word_processed.csv"
    df = pd.read_csv(AWS_BUCKET_URL, index_col=False)
    return df

df = data()
df['text'] = df['text'].astype(str)

text_input = st.text_input(
    "Enter some text 👇"
)

if text_input:
    st.write("House of Commons Word Count:  ", text_input)

results = []
words_search = [f' {text_input.lower()}']
for index, row in df.iterrows():
    for word in words_search:
        result = {
            'date': row['date'],
            'party': row['party'],
            'word': word,
            'count': row['text'].count(word),
            }
        results.append(result) 
df1 = pd.DataFrame(results)


fig, ax = plt.subplots(figsize=(16, 8))
heading = f'House of Commons: {words_search}'
g = sns.barplot(data=df1, x='date', y='count', hue='party', palette="pastel", ax=ax)
g.set(title=heading)

st.pyplot(fig)
