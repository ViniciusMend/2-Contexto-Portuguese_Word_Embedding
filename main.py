import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from gensim.models import KeyedVectors
from st_aggrid import AgGrid
 
from hidden.hidden_words import HIDDEN_WORDS
 
@st.cache(allow_output_mutation=True)
def load_data():
    results = pd.read_excel("data/results.xlsx")
    words = pd.read_excel("data/palavras.xlsx")
    model = KeyedVectors.load_word2vec_format("data/skip_s50.txt", binary=False, encoding="utf8")
    return results, words, model
 
results, words, model = load_data()

with st.sidebar:
    choose = option_menu(
        "Contexto", ["Jogo", "Lista Palavras", "Sobre"],
        icons=['layers', 'info-circle', 'search'],
        menu_icon="layers", default_index=0,
        styles={
            "container": {"padding": "3!important", "background-color": "#FFFBF5"},
            "icon": {"color": "black", "font-size": "18px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee", "color":"grey"},
            "nav-link-selected": {"background-color": "#B5E2DC"},
            "color": "black"
        }
    )
 
def local_css(file_name):
    """
    Define a função responsável pelo carregamento do arquivo style.css
    que contém o estilo dos elementos da aplicação.
 
    Parameters:
        file_name (string): Caminho do arquivo style.css
    """
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
 
def title(text):
    """
    Define a função responsável pelo estilo dos cabeçalhos das colunas.
 
    Parameters:
        text (string): Nome do título do cabeçalho.
    """
    return f"""
        <p style = "text-align:left; color:black; font-weight:bold; padding-left:10px; font-size:18px;">
            {text}
        </p>"""
 
def guess_left(text, background):
    """
    Define a função responsável pelo estilo das palavras de tentativas do usuário.
 
    Parameters:
        text (string): Palavras inserida pelo usuário
    """
    return f"""
        <p style = "background-color: {background}; color:black;
        font-size:18px; border-radius: 7px; text-align:left; padding-left:10px; ">
            {text}
        </p>"""
 
def guess_center(text, background, align):
    """
    Define a função responsável pelo estilo das palavras de tentativas do usuário com maior proximidade.
 
    Parameters:
        text (string): Palavras inserida pelo usuário
    """
    return f"""
        <p style= 'background-color: {background}; color: black;
            font-size: 18px; border-radius: 7px; text-align: {align};'>
            {text}
        </p>"""
 
def block_sucess(option, len):
    if st.session_state.success == True:
        return f"""
            <div style= 'background-color: rgb(170, 227, 220); color: black;
                font-size: 18px; border-radius: 7px; text-align: center;'>
                Parabéns!\n\nVocê acertou a palavra **{option}** em **{len}** tentativas.
            </div>"""
    else:
        return ""
 
def new_todo_changed():
    """
    Define o retorno de chamada quando text_input for alterado.
    """
    if st.session_state.new_todo not in results[results["HIDDEN_WORDS"]==HIDDEN_WORDS[int(option)-1]]["Word"].tolist():
        st.session_state.alert = "Palavra desconhecida"
    elif st.session_state.new_todo in [st.session_state.todos[x]["word"] for x in range(0, len(st.session_state.todos))]:
        st.session_state.alert = "Palavra já inserida"
    elif st.session_state.new_todo:
        st.session_state.todos.append(
            {
                "word": st.session_state.new_todo
            }
        )
        st.session_state.alert = ""
       
        if st.session_state.new_todo == results[results["HIDDEN_WORDS"]==HIDDEN_WORDS[int(option)-1]]["HIDDEN_WORDS"].tolist()[0]:
            st.session_state.success = True
    st.session_state.new_todo = ""
 
def clear():
    st.session_state.todos = []
    st.session_state.alert = ""
    st.session_state.dict_positions = {}
    st.session_state.success = False
    st.session_state.word = ""
    st.session_state.alert_lista = ""
 
def show_jogo():
    global option

    local_css("style/style.css")
 
    if "todos" not in st.session_state:
        # Define o estado inicial da aplicação.
        st.session_state.todos = []
        st.session_state.alert = ""
        st.session_state.dict_positions = {}
        st.session_state.success = False
 
    def hint(option, position):
        if len(st.session_state.dict_positions)>0:
            position = min([a["Position"] for a in st.session_state.dict_positions.values()])
        else:
            position = len(results[(results["HIDDEN_WORDS"]==HIDDEN_WORDS[int(option)-1])])
        new_position = int(position/2)
        
        if new_position != 0:
            hint = results[(results["HIDDEN_WORDS"]==HIDDEN_WORDS[int(option)-1]) & (results["Position"]==new_position)]["Word"].tolist()[0]
            st.session_state.new_todo = hint
            new_todo_changed()
 
    def giveUp(option):
        giveUp = results[(results["HIDDEN_WORDS"]==HIDDEN_WORDS[int(option)-1]) & (results["Position"]==1)]["Word"].tolist()[0]
        st.session_state.new_todo = giveUp
        new_todo_changed()
    
    st.write("")
    option = st.sidebar.selectbox('Selecione a palavra oculta a tentar descobrir', ([str(i+1) for i in range(0, 10)]), on_change=clear)
 
    col1, col2, col3 = st.columns([8,1,1])
    col1.markdown("### CONTEXTO - PYTHON")
    col2.button("Dica", on_click=hint, args=[option, min([a["Position"] for a in st.session_state.dict_positions.values()]) if len(st.session_state.dict_positions)>0 else len(results[(results["HIDDEN_WORDS"]==HIDDEN_WORDS[int(option)-1])])])
    col3.button("Desistir", on_click=giveUp, args=[option])
 
    st.text_input("", placeholder="Digite uma palavra", on_change=new_todo_changed, key="new_todo")
 
    st.write(st.session_state.alert)
    st.markdown(block_sucess(option, len(st.session_state.todos)), unsafe_allow_html=True)
    col1, col2, col3 = st.columns([0.15, 0.7, 0.15])
 
    if len(st.session_state.todos)>0:
        col1.markdown(title("Tentativa"), unsafe_allow_html=True)
        col2.markdown(title("Palavra"), unsafe_allow_html=True)
        col3.markdown(title("Posição"), unsafe_allow_html=True)
   
    for i, todo in enumerate(st.session_state.todos):
        if (i+1 == len(st.session_state.todos))&(len(st.session_state.todos)>0):
            st.session_state.dict_positions[i]={"Word":todo["word"], "Position":results[(results["HIDDEN_WORDS"]==HIDDEN_WORDS[int(option)-1]) & (results["Word"]==todo["word"])]["Position"].tolist()[0]}
            Position = results[(results["HIDDEN_WORDS"]==HIDDEN_WORDS[int(option)-1]) & (results["Word"]==todo["word"])]["Position"].tolist()[0]
            if int(Position) <= 500:
                col1.markdown(guess_left(i+1, "rgb(170, 227, 220)"), unsafe_allow_html=True)
                col2.markdown(guess_left(todo["word"], "rgb(170, 227, 220)"), unsafe_allow_html=True)
                col3.markdown(guess_center(Position, "rgb(170, 227, 220)", "center"), unsafe_allow_html=True)
            elif (Position > 500) & (Position <= 1000):
                col1.markdown(guess_left(i+1, "rgb(249, 217, 154)"), unsafe_allow_html=True)
                col2.markdown(guess_left(todo["word"], "rgb(249, 217, 154)"), unsafe_allow_html=True)
                col3.markdown(guess_center(Position, "rgb(249, 217, 154)", "center"), unsafe_allow_html=True)
            else:
                col1.markdown(guess_left(i+1, "rgb(255, 190, 182)"), unsafe_allow_html=True)
                col2.markdown(guess_left(todo["word"], "rgb(255, 190, 182)"), unsafe_allow_html=True)
                col3.markdown(guess_center(Position, "rgb(255, 190, 182)", "center"), unsafe_allow_html=True)
 
    if len(st.session_state.todos)>0:
        col1.write("")
        col1.write("")
        col2.write("")
        col2.write("")
        col3.write("")
        col3.write("")
   
    lista_ordenada = [st.session_state.dict_positions[a] for a in sorted(st.session_state.dict_positions, key=lambda x: int(st.session_state.dict_positions[x]['Position']))]
    for i, todo in enumerate(lista_ordenada):
        if len(lista_ordenada)>0:
            if int(todo["Position"]) <= 500:
                col1.markdown(guess_left(i+1, "rgb(170, 227, 220)"), unsafe_allow_html=True)
                col2.markdown(guess_left(todo["Word"], "rgb(170, 227, 220)"), unsafe_allow_html=True)
                col3.markdown(guess_center(todo["Position"], "rgb(170, 227, 220)", "center"), unsafe_allow_html=True)
            elif (int(todo["Position"]) > 500) & (int(todo["Position"]) <= 1000):
                col1.markdown(guess_left(i+1, "rgb(249, 217, 154)"), unsafe_allow_html=True)
                col2.markdown(guess_left(todo["Word"], "rgb(249, 217, 154)"), unsafe_allow_html=True)
                col3.markdown(guess_center(todo["Position"], "rgb(249, 217, 154)", "center"), unsafe_allow_html=True)
            else:
                col1.markdown(guess_left(i+1, "rgb(255, 190, 182)"), unsafe_allow_html=True)
                col2.markdown(guess_left(todo["Word"], "rgb(255, 190, 182)"), unsafe_allow_html=True)
                col3.markdown(guess_center(todo["Position"], "rgb(255, 190, 182)", "center"), unsafe_allow_html=True)
 
def lista_palavras():
    if st.session_state.new_word:
        if st.session_state.new_word not in words["Word"].tolist():
            st.session_state.alert_lista = "Palavra desconhecida"
        else:
            st.session_state.word = st.session_state.new_word
            st.session_state.alert_lista = ""
    st.session_state.new_word = ""

def show_lista_palavras():
    
    local_css("style/style.css")

    if "word" not in st.session_state:
        # Define o estado inicial da aplicação.
        st.session_state.word = ""
        st.session_state.alert_lista = ""

    st.markdown("### CONTEXTO - PYTHON")
    
    st.markdown("""
                <p style = "text-align:center; color:black; font-weight:bold; font-size:18px;">
                    Aqui são apresentadas a lista de 500 palavras mais relacionadas a palavra inserida
                </p>""", unsafe_allow_html=True)
    st.text_input("", placeholder="Digite uma palavra", on_change=lista_palavras, key="new_word")

    st.write(st.session_state.alert_lista)

    if st.session_state.word != "":
        df = pd.DataFrame(model.most_similar(st.session_state.word, topn=500), columns=["Palavra", "Similaridade"])
        df["Posição"] = df.index+1
        AgGrid(df)

def info():

    local_css("style/style-info.css")

    st.markdown("# CONTEXTO - PYTHON")
    st.markdown("## Informações sobre a aplicação")
    st.markdown("""
        Eu desenvolver essa aplicação como projeto de Data Science, como forma 
        de apromiramento de habilidades em Python, Streamlit e Natural Language Processing (NLP).
        
        Esse projeto é um *recoding* do [Contexto](https://contexto.me/), um game baseado em um 
        algoritmo que descreve e analisa o grau de similaridade, ou contexto, em que as palavras 
        são utilizadas na linguaguem do Português. As características técnicas do projeto podem ser
        encontradas [aqui]() e abaixo são destacadas algumas informações relevantes.
    """)

    with st.container():
        _, text_col = st.columns((0.05,2))

        with text_col:
            st.subheader("Jogo")
            st.write("""
                A primeira aba, Jogo, apresenta o projeto em si, em que o usuário define, dentre um conjunto
                de 10 palavras, a palavra que deseja tentar descobrir. Assim, inserindo uma palavra na caixa
                de entrada, o modelo calcula o grau de proximidade do par de palavras (palavra secreta e
                palavra inserida). O objetivo do jogo é encontrar a palavra de número 1.

                A base de dados utilizada para calcular a proximidade das palavras vem do [NILC](http://www.nilc.icmc.usp.br/embeddings),
                e o modelo utilizado é o Word2Vec Skip-Gram 1000 dimensões.
                """)

    with st.container():
        _, text_col = st.columns((0.05,2))

        with text_col:
            st.subheader("Lista Palavras")
            st.write("""
                A segunda aba, Lista Palavras, é um módulo complementar ao Contexto original, em que
                é possível visualizar a lista das 500 palavras mais relacionadas a palavra inserida.

                O modelo utilizado nessa aba é o Word2Vec Skip-Gram 50 dimensões, por ser menor e consequentemente,
                mais rápido no cálculo da tabela.
            """)

    st.markdown("""
        Ademais, para determinar as palavras que seriam possíveis ou não de serem interpretadas pelo modelo,
        buscou-se desenvolver uma base de dados com as palavras mais comuns da língua Portuguesa.
        
        A base de dados, disponível [aqui](https://www.ime.usp.br/~pf/estruturas-de-dados/aulas/sandbox/br-utf8.txt), consta com 261798 palavras, e após uma sequência de tratamentos,
        resultou em 50118 palavras, sendo essa base utilizada em ambas as abas dessa aplicação.
    """)

if __name__ == "__main__":
    if choose == "Jogo":
        show_jogo()
    elif choose == "Lista Palavras":
        show_lista_palavras()
    else:
        info()
