# External libs
from googletrans import Translator
import zipfile, io, requests, re
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

def get_anime_info(anime_name, filename, start_time):
    minute = get_minute(start_time)
    episode = filename.split('/')[-1]
    return ' ***' + anime_name + '*** (' + episode + ', ' + minute + ')'

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
                Tradução
            </div>
        </a>
        <div style="position:absolute;padding:5px;">
            ''' + traducao + '''
        </div>
    </div>
    '''