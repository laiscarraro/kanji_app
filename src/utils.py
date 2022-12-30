# External libs
from googletrans import Translator
import zipfile, io, requests, re, time
from bs4 import BeautifulSoup
import streamlit as st
import pykakasi
import uuid
import gtts

def extract_zip(filename, max=100, fetch=True, content=True):
    '''
    Extract .zip subtitle files.
    '''
    if fetch:
        r = requests.get(filename, stream=True).content
        z = io.BytesIO(r)
    else:
        z = filename

    try:
        input_zip = zipfile.ZipFile(z)
    except zipfile.BadZipFile:
        return None, None
    
    filenames = input_zip.namelist()

    if not content:
        return filenames

    else:
        try:
            files = [input_zip.read(name).decode('utf8') for name in filenames[:min(max, len(filenames))]]
        except UnicodeDecodeError:
            return None, None

        return filenames, files

def kanji_html(sent):
    kks = pykakasi.kakasi()
    converted = kks.convert(sent)
    hiragana = [word['hira'] for word in converted]
    katakana = [word['kana'] for word in converted]

    html = ''
    for h in range(len(converted)):
        original = converted[h]['orig']
        furigana = hiragana[h]
        if original != furigana and original != katakana[h]:
            html += '<ruby><rb>' + original + '</rb><rt>' + furigana + '</rt></ruby>'
        else:
            html += original

    return html

def color_target_kanji(sent, kanji):
    html = kanji_html(sent)
    md = ''
    for char in html:
        if kanji == char:
            md += '<span style="color:lightgreen;">'
            md += char
            md += '</span>'
        else:
            md += char
    return md

def get_audio(sent):
    tts = gtts.gTTS(sent, lang='ja')
    tts.save('sent.mp3')

def get_translation(sent):
    translator = Translator()
    translation = translator.translate(sent).text
    return re.sub('\W', ' ', translation)

def get_translation_html(sent):
    translation = get_translation(sent)
    html = '<p style="color:lightgray;">' + translation + '</p></ul>'
    return html

def get_minute(start_time):
    time = re.findall('\d\d:\d\d:\d\d', start_time)
    return ' '.join(time)

def get_episode_number(filename):
    patterns = [
        's\d+e\d+',
        '\d+.srt',
        '\\b\d+\\b'
    ]
    pattern = '|'.join(patterns)
    episode_number = re.sub(
        '.srt', '',
        ''.join(
            re.findall(pattern, filename.lower())
        )
    )
    return episode_number

def make_episode_link(anime_name, episode_number):
    anime_clean = re.sub('\W', ' ', anime_name)
    anime = '-'.join(anime_clean.split())
    url = 'http://animefire.net/animes/'
    try:
        episode_number = int(episode_number)
        return url + anime + '/' + str(episode_number)
    except:
        return ''

def get_episode_video_url(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    }
    page = requests.get(url, headers=headers)
    time.sleep(0.5)
    webpage = BeautifulSoup(page.text, 'html.parser')
    iframe = webpage.find_all('iframe')
    video_url = iframe[0]['src']

    return video_url

def get_anime_info(anime_name, filename, start_time):
    minute = get_minute(start_time)
    episode = filename.split('/')[-1]
    return ' ***' + anime_name + '*** (' + episode + ', ' + minute + ')'

def get_player_link(anime_name, filename, content, start_time):
    episode_number = get_episode_number(filename)
    anime_clean = re.sub('\W', ' ', anime_name)
    link = "Player?"
    link += "episode="+episode_number
    link += "&name="+'+'.join(anime_clean.split())
    link += "&content="+'+'.join(content)
    link += '&start_time='+str(get_minute(start_time))

    st.write('''
        <br>
        <a target="_self" style="text-decoration:none;color:gray;" href="'''+ link +'''">
            <button class="css-1x8cf1d edgvbvh10">
                Assistir
            </button>
        </a>
        <br>
        ''', unsafe_allow_html=True
    )
    st.markdown('---')

def findLongestConseqSubseq(arr):
    n = len(arr)
    arr = arr + [-1]
 
    ans_list = []
    lista_provisoria = []
    for i in range(1, n+1):
        if arr[i]-arr[i-1] == 1:
            lista_provisoria.append(arr[i-1])
        else:
            lista_provisoria.append(arr[i-1])
            if len(lista_provisoria) > len(ans_list):
                ans_list = lista_provisoria
            lista_provisoria = []
 
    return ans_list

def make_spoiler_html(sent):
    traducao = get_translation(sent)
    id_ = str(uuid.uuid4())
    return '''
    <style>
        #trad'''+ id_ + ''' {
            text-align:center;
            position:absolute;
            z-index:1;
            width:100%;
        }
        #trad'''+ id_ + ''':target {
            display: none;
        }
    </style>
    <div style="position:relative">
        <a href="#trad'''+ id_ + '''" style="text-decoration:none;color:grey;">
            <div id="trad'''+ id_ + '''" style="backgroundColor:#f0f0f0;border-radius:4px;padding:5px;">
                Exibir tradução
            </div>
        </a>
        <div style="position:absolute;padding:5px;">
            ''' + traducao + '''
        </div>
    </div>
    '''