import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import nltk
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')

def wrap_text(text, line_length):
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        if len(current_line.split()) == line_length:
            lines.append(current_line.strip())
            current_line = ""
        current_line += word + " "
    if current_line:
        lines.append(current_line.strip())
    return "\n".join(lines)

def create_summary(paragraph, num_sentences):
    sentences = nltk.sent_tokenize(paragraph)
    sentence_scores = {}
    for sentence in sentences:
        sentence_scores[sentence] = score_sentence(sentence)
    top_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]
    summary = ' '.join(top_sentences)
    return summary

def score_sentence(sentence):
    words = nltk.word_tokenize(sentence.lower())
    stop_words = set(stopwords.words('english'))
    content_words = [word for word in words if word not in stop_words]
    return len(content_words)

def remove_parentheses(text):
    """Removes any text inside parentheses from a given string."""
    while True:
        start = text.find("(")
        end = text.find(")")
        if start == -1 or end == -1 or end < start:
            break
        text = text[:start] + text[end + 1:]
    return text

def remove_brackets(text):
    """Removes any text inside square brackets from a given string."""
    pattern = r"\[[^]]*\]"
    return re.sub(pattern, "", text)

list1 = []
data = ""
st.title("Summary.com")
st.write('by Utkarsh Singh')
st.divider()
inp = st.text_input("Enter your text here")
url = f'https://en.wikipedia.org/wiki/{inp}'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
paragraphs = soup.find_all('p')

for p in paragraphs:
    para = p.text
    list1.append(para)
list1 = [item for item in list1 if item != '\n']
data = list1[0] + list1[1] 
data = remove_parentheses(data)
data = remove_brackets(data)
summ = wrap_text(create_summary(data, num_sentences=2), 11)
code_container = st.container()

with code_container:
        st.code(summ, language='None')
        code_container.markdown(
            f"""
            <style>
            .css-1aumxhk {{
                max-height: 300px;
                overflow-y: scroll;
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )

st.divider()

with st.container():
    with st.expander("View Full data"):
        code = wrap_text(data,11)
        code_container = st.container()
        with code_container:
            st.code(code, language='None')

        code_container.markdown(
            f"""
            <style>
            .css-1aumxhk {{
                max-height: 300px;
                overflow-y: scroll;
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )




