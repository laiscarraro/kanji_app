import streamlit as st
from src.utils import make_episode_link, get_episode_video_url

params = st.experimental_get_query_params()
episode_link = None
name = ''
episode = ''
content = ''
start_time = ''
mensagem = 'Ajustar informações do link'

try:
    episode = params['episode'][0]
    name = params['name'][0]
    content = params['content'][0]
    start_time = params['start_time'][0]

    episode_link = make_episode_link(name, episode)

except:
    mensagem = 'Insira as informações sobre o anime que gostaria de assistir'

with st.expander(mensagem):
    name = st.text_input('Nome do anime', value=name)
    episode = st.text_input('Episódio', value=episode)

    if st.button('Atualizar'):
        episode_link = make_episode_link(name, episode)
    
    if episode_link is not None:
        st.markdown(
            '<a href="'+episode_link+'"> Testar link (' + episode_link + ') </a>',
            unsafe_allow_html=True
        )

col1, col2 = st.columns(2)
if episode_link != '':
    try:
        video_url = get_episode_video_url(episode_link)

        st.markdown('Assista a partir de **' + start_time + '**')
        st.markdown('''
        <iframe 
            width=500
            height=300
            src="'''+video_url+'''"></iframe>
        ''', unsafe_allow_html=True)
        st.write(content)
    except:
        st.warning('O vídeo não pôde ser carregado. Confira o link nas configurações acima.')
else:
    st.warning('Episódio não encontrado. Confira as informações do episódio nas configurações acima.')