import streamlit as st
import requests, time
from bs4 import BeautifulSoup

anime = '-'.join(st.text_input('Escreva o nome do anime').lower().split())
ep = str(
    st.number_input(
        'Escolha o número do episódio',
        min_value=1, max_value=1000
    )
)
url = 'http://animefire.net/animes/'+anime+'/'+ep

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}
page = requests.get(url, headers=headers)
time.sleep(0.5)
webpage = BeautifulSoup(page.text, 'html.parser')
iframe = webpage.find_all('iframe')
video_url = iframe[0]['src']

st.markdown('''
<iframe 
    width=500
    height=300
    src="'''+video_url+'''"></iframe>
''', unsafe_allow_html=True)