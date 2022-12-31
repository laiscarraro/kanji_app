import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
from st_aggrid import GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
# from src.utils import get_translation
from src.visualization.login import initialize_page

if initialize_page():
    user = st.session_state['session'].get_user()

    st.title('Dicionário de Palavras')
    st.markdown('Na tabela abaixo, estão marcadas as palavras que você já conhece, segundo o seu deck do Anki. Estude mais Kanji para que eles sejam liberados em seus estudos! Você pode configurar as suas recomendações abaixo.')

    known_words = pd.DataFrame(
        st.session_state['anki_manager'].get_unlocked_words(),
        columns = ['Word']
    )

    words = st.session_state['anki_manager'].get_words()
    words['index'] = words.index.values

    word_index = pd.merge(
        known_words, words,
        on='Word'
    )['index'].tolist()
    words = words.drop(columns=['index'])
    
    gd = GridOptionsBuilder.from_dataframe(
        words
    )

    gd.configure_selection(
        selection_mode='multiple',
        suppressRowDeselection=True,
        suppressRowClickSelection=True,
        use_checkbox=False,
        pre_selected_rows=word_index
    )
    gd.configure_pagination(
        enabled=True, 
        paginationAutoPageSize=False,
        paginationPageSize=15
    )
    options = gd.build()
    
    grid = AgGrid(
        words,
        gridOptions=options,
        update_mode=GridUpdateMode.NO_UPDATE,
        theme='alpine'
    )