import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

# Configuração da página
st.set_page_config(
    page_title="Billionaires Statistics (2023)",
    page_icon="💲",
    layout="wide"
)

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("/home/ramon/ds_trab2/dataset/dataset.csv")

        # Limpeza e pré-processamento dos dados
        # Removendo colunas não utilizadas
        df = df.drop(df.columns[14:], axis=1)
        df = df.drop(['organization', 'countryOfCitizenship', 'city'], axis=1)

        # Preenchendo os dados faltantes da coluna 'age' com a média
        df['age'].fillna(df['age'].mean(), inplace=True)

        # Preenchendo os dados faltantes da coluna 'country' com o valor mais frequente
        df['country'].fillna(df['country'].mode()[0], inplace=True)

        return df
    
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")
        
df = load_data()

if df is None:
    st.stop()

#-------------------------------------------
# Sidebar responsivo
st.sidebar.image("image.png", width=250)
st.sidebar.title("Filtros")
st.sidebar.markdown("Ajuste para modificar a Visualização:")

top_n = st.sidebar.slider("Quantidade de países (Top N)", min_value=1, max_value=30, value=10)
top_industries = st.sidebar.slider("Quantidade de indústrias (Top N)", min_value=1, max_value=18, value=10)

idade_min, idade_max = int(df['age'].min()), int(df['age'].max())
idade_range = st.sidebar.slider(
    "Intervalo de Idade",
    min_value=idade_min,
    max_value=idade_max,
    value=(idade_min, idade_max)
)
df = df[(df['age'] >= idade_range[0]) & (df['age'] <= idade_range[1])]

#-------------------------------------------

# Título principal com ajuste responsivo
st.title("Análise do Dataset Billionaires Statistics (2023)")
st.markdown(f"Fonte: [Billionaires Statistics Dataset (2023)](https://www.kaggle.com/datasets/nelgiriyewithana/billionaires-statistics-dataset)")

tab1, tab2 = st.tabs(["País", "Setor"])

with tab1:
    col1 = st.columns(1)[0]
    # Configuração do layout responsivo
    with col1:
        st.subheader("Distribuição de Bilionários por País")

        top_countries = df['country'].value_counts().head(top_n).reset_index()
        top_countries.columns = ['País', 'Total']

        # Definindo a cor roxa mediana para todas as barras
        roxo_mediano = "#9370DB"

        fig_top_paises = px.bar(
            top_countries,
            x='País',
            y='Total',
            title=f"Top {top_n} Países com Mais Bilionários",
            text_auto=True
        )

        # Aplicando a cor única a todas as barras
        fig_top_paises.update_traces(marker_color=roxo_mediano)

        # Ajustes responsivos no layout do gráfico
        fig_top_paises.update_layout(
            autosize=True,
            margin=dict(l=20, r=20, t=40, b=20),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_tickangle=-45
        )

        # Exibindo o gráfico em container responsivo
        st.plotly_chart(fig_top_paises, use_container_width=True)

with tab2:
    col1 = st.columns(1)[0]

    with col1:
        st.subheader("Distribuição de Bilionários por Setor")

        # Agrupando e contando os bilionários por indústria
        industria_counts = df['industries'].value_counts().head(top_industries).reset_index()
        industria_counts.columns = ['Indústria', 'Total']

        # Gráfico de barras para a distribuição de bilionários por indústria
        fig_industria = px.bar(
            industria_counts,
            x='Indústria',
            y='Total',
            title=f"Top {top_industries} Setores com Mais Bilionários",
            text_auto=True,
            color_discrete_sequence=[roxo_mediano]
        )

        fig_industria.update_layout(
            autosize=True,
            margin=dict(l=20, r=20, t=40, b=20),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_tickangle=-45
        )

        st.plotly_chart(fig_industria, use_container_width=True)

st.markdown("---")
st.subheader("Bilionários e Idade")

c1, c2 = st.columns(2)

with c1:
    # KDE (Kernel Density Estimate) para a idade dos bilionários
    fig_idade_kde = ff.create_distplot(
        [df['age'].dropna()],
        group_labels=["Idade"],
        colors=[roxo_mediano],
        show_hist=False,
        show_rug=True
    )

    # Calcular a média das idades
    media_idade = df['age'].mean()

    # Adicionar linha vertical da média ao gráfico
    fig_idade_kde.add_vline(
        x=media_idade,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Média: {media_idade:.1f}",
        annotation_position="top right"
    )

    fig_idade_kde.update_layout(
        title="Distribuição de Bilionários por Idade (KDE)",
        autosize=True,
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Idade",
        yaxis_title="Densidade",
        xaxis_tickangle=-45
    )

    st.plotly_chart(fig_idade_kde, use_container_width=True)

    with c2:
        fig_scatter = px.scatter(
            df,
            x="age",
            y="finalWorth",
            color="finalWorth",
            color_continuous_scale=px.colors.sequential.Purples,
            title="Relação entre Idade e Patrimônio Líquido (finalWorth)",
            labels={"age": "Idade", "finalWorth": "Patrimônio"},
        )
        fig_scatter.update_layout(
            autosize=True,
            margin=dict(l=20, r=20, t=40, b=20),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        

st.markdown("---")
st.subheader("Self-made vs Herdado")

co1, co2 = st.columns(2)

with co1:
    # Gráfico de pizza para Self-made vs Inherited
    self_made_counts = df['selfMade'].value_counts().reset_index()
    self_made_counts.columns = ['Tipo', 'Total']

    fig_pizza = px.pie(
        self_made_counts,
        values='Total',
        names='Tipo',
        title="Proporção de Self-made",
        hole=0.3,
        color_discrete_sequence=[roxo_mediano, "#FFFFFF"]
    )

    fig_pizza.update_traces(textposition='inside', textinfo='percent+label')
    fig_pizza.update_layout(
        autosize=True,
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    st.plotly_chart(fig_pizza, use_container_width=True)

with co2:
    # Distribuição de Self-made e Inherited por Idade
    fig_selfmade_idade = px.histogram(
        df,
        x="age",
        color="selfMade",
        nbins=30,
        barmode="overlay",
        color_discrete_sequence=[roxo_mediano, "#FFFFFF"],
        labels={"age": "Idade", "selfMade": "Tipo"},
        title="Distribuição de Self-made e Herdado por Idade"
    )
    fig_selfmade_idade.update_layout(
        autosize=True,
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Idade",
        yaxis_title="Contagem",
        legend_title="Tipo"
    )
    st.plotly_chart(fig_selfmade_idade, use_container_width=True)

st.markdown("---")
st.subheader("Bilionários e Gênero")

t1, t2 = st.tabs(["Patrimônio", "Setores"])
with t1:
    # Gráfico de pizza para a distribuição de gênero
    c1, c2 = st.columns(2)
    with c1:
        genero_counts = df['gender'].value_counts().reset_index()
        genero_counts.columns = ['Gênero', 'Total']
        fig_genero = px.pie(
            genero_counts,
            values='Total',
            names='Gênero',
            title="Distribuição de Gênero",
            hole=0.3,
            color_discrete_sequence=["#FFFFFF", roxo_mediano]
        )

        fig_genero.update_traces(textposition='inside', textinfo='percent+label')
        fig_genero.update_layout(
            autosize=True,
            margin=dict(l=20, r=20, t=40, b=20),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_genero, use_container_width=True)

    with c2:
        # Gráfico de barras para patrimônio médio por gênero
        media_patrimonio_genero = df.groupby('gender')['finalWorth'].mean().reset_index()
        media_patrimonio_genero.columns = ['Gênero', 'Patrimônio Médio']

        fig_media_patrimonio = px.bar(
            media_patrimonio_genero,
            x='Gênero',
            y='Patrimônio Médio',
            title="Patrimônio Médio por Gênero",
            text_auto='.2s',
            color='Gênero',
            color_discrete_sequence=[roxo_mediano, "#FFFFFF"]
        )

        fig_media_patrimonio.update_layout(
            autosize=True,
            margin=dict(l=20, r=20, t=40, b=20),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Gênero",
            yaxis_title="Patrimônio Médio"
        )
        st.plotly_chart(fig_media_patrimonio, use_container_width=True)

with t2:
    c1 = st.columns(1)[0]
    with c1:
        # Gráfico de barras: distribuição de bilionários por setor e gênero
        industria_genero = df.groupby(['industries', 'gender']).size().reset_index(name='Total')
        industria_genero_top = industria_genero[industria_genero['industries'].isin(
            df['industries'].value_counts().head(top_industries).index
        )]

        fig_industria_genero = px.bar(
            industria_genero_top,
            x='industries',
            y='Total',
            color='gender',
            barmode='group',
            title=f"Distribuição de Bilionários por Setor e Gênero (Top {top_industries})",
            labels={'industries': 'Setor', 'Total': 'Total', 'gender': 'Gênero'},
            color_discrete_sequence=[roxo_mediano, "#FFFFFF"]
        )
        fig_industria_genero.update_layout(
            autosize=True,
            margin=dict(l=20, r=20, t=40, b=20),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig_industria_genero, use_container_width=True)

st.markdown("---")
st.subheader("Sobre o Dashoard")
st.markdown("""
Este dashboard foi desenvolvido para analisar o dataset de bilionários de 2023,
             utilizando a biblioteca Streamlit para visualização interativa. Ele permite explorar a distribuição de bilionários por país, 
            setor, idade e gênero, além de comparar a quantidade bilionários self-made, que construíram sua fortuna, e aqueles que a herdaram.
Para mais informações, consulte a [documentação do Streamlit](https://docs.streamlit.io/) e o 
            [repositório do projeto](https://github.com/r4mon-vinicius/ciencia_de_dados).
### Autor
- [Ramon Vinícius](https://github.com/r4mon-vinicius)""")