import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt
from sklearn.preprocessing import LabelEncoder

st.cache_data
def load_data():
    data = pd.read_csv('fr-en-dnb-par-etablissement.csv', delimiter=';')
    # Convertir la colonne Commune en nombre int ou float et aussi drop les lignes avec des string(que je veux en int)
    data['Commune'] = pd.to_numeric(data['Commune'], errors='coerce')
    data.dropna(subset=['Commune'], inplace=True)
    data['Code département'] = data['Code département'].astype(float)
    data['Code académie'] = data['Code académie'].astype(float)
    data['Taux de réussite'] = data['Taux de réussite'].str.replace('%', '', regex=True).str.replace(',', '.', regex=True).astype(float)
    # faire l'encodage des regions
    label_encoder = LabelEncoder()
    data['Libellé département_numérique'] = label_encoder.fit_transform(data['Libellé département'])
    return data

data = load_data()

def taux_par_region1(data):
    st.title('Diplôme national du brevet par établissement')

    fig1, ax1 = plt.subplots(figsize=(12, 10))
    ax1 = sns.barplot(data=data, x='Libellé région', y='Taux de réussite')
    plt.xlabel('Région')
    plt.ylabel('Taux de réussite')
    plt.title('Région avec le meilleur taux de réussite depuis 2008')
    plt.xticks(rotation=90)
    st.pyplot(fig1)



def taux_par_region2(data):
    chart = alt.Chart(data).mark_bar().encode(
        x='Libellé région',
        y='Taux de réussite'
    ).properties(
         width=1000,
        title='Taux de réussite par région'
    )
    st.altair_chart(chart)

def taux_par_region3(région):

    dataset_par_region = data[data['Libellé région'] == région]

    chart = alt.Chart(dataset_par_region).mark_bar().encode(
        x='Session:N',
        y=alt.Y('Taux de réussite:Q', axis=alt.Axis(format='%')),
        color='Session:N'
    ).properties(
        width=1000,
        title=f'Taux de réussite par année pour la région {région}'
    )
    #affiche
    st.altair_chart(chart)


def faire_un_filtre(année, région, département):

    nouveau_dataset = data[(data["Libellé département"] == département) & (data["Session"] == année) & (data['Libellé région'] == région)]

    #Affichage des données filtrées
    if st.checkbox("Afficher les données"):
        st.write('Résultat de',année,'dans le',département,région,':')
        st.write(nouveau_dataset)

     #dessiner le graph
    chart = alt.Chart(nouveau_dataset)
    mentions = ["Admis sans mention", "Nombre_d_admis_Mention_AB", "Admis Mention bien", "Admis Mention très bien"]


    for mention in mentions:
        chart = chart.mark_bar().encode(
            x='Lycée/Collège',
            y=alt.Y(mention, stack="normalize"),
            color=alt.Color('Mention:N', scale=alt.Scale(scheme='set1'))
        ).transform_calculate(
            Mention=f'"{mention}"'
        )

    #Créer une barre pour le nombre total d'admis
    chart = chart.mark_bar(size=10, color='black').encode(
        x=alt.X('Patronyme:O', title='Lycées'),
        y='sum(Admis):Q',
        tooltip=['Patronyme', 'sum(Admis)']
    )

    #Personnaliser le graphique
    chart = chart.properties(
        width=1000,
        title="Résultats des Lycées",
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    )
    #affiche
    st.altair_chart(chart)


#Mes pages

# Titre de la barre latérale
st.sidebar.title("Sommaire")
# Pages de l'application
pages = ["Contexte","Voir les visualisations", "Exploration des données", "Plus de visualisation", "About me"]
# Sélection de la page depuis la barre latérale
page = st.sidebar.radio("Aller vers la page :", pages)

if page == pages[0]:
    # Titre de la page
    st.title("Analyse des Résultats des Examens")
    st.write(
    "Bienvenue dans notre application d'analyse des résultats des examens. "
    "Cette application vous permet d'explorer et d'interagir avec les données des résultats des examens, "
    "fournissant des informations précieuses sur la performance des étudiants."
    )
    st.write(
    "Notre objectif est de vous offrir une vue approfondie des résultats des examens, y compris les taux de réussite, "
    "les mentions, et d'autres statistiques pertinentes. Vous pouvez personnaliser vos analyses en utilisant les options "
    " de filtrage et ainsi découvrir des tendances et des informations utiles."
    )

if page == pages[1]:

    #1er grah
    taux_par_region1(data)

    #2ème graph
    région = st.selectbox('Sélectionnez une région :', data['Libellé région'].unique())
    taux_par_region3(région)

    #3ème grah
    st.title("Taux par région")
    taux_par_region2(data)

    # Option de personnalisation
    st.write('Faire un filtre')
    année = st.selectbox('Sélectionnez une année :', data['Session'].unique())
    région = st.selectbox('selectionner une région :', data['Libellé région'].unique())
    département = st.selectbox('Sélectionnez une département :', data['Libellé département'].unique())
    faire_un_filtre(année, région, département)


if page == pages[2]:
    if st.checkbox("Afficher les données"):
        st.write(data)

if page == "Plus de visualisation":
    st.write('partie 1')

if page == pages[3]:


    st.title("Taux de réussite par région")
    st.bar_chart(data.groupby('Libellé région')['Taux de réussite'].mean())

    st.title("Nombre d'admis")
    st.line_chart(data['Admis'])


if page == pages[4]:
    linkedin_link = "https://www.linkedin.com/"
    st.write('FOFANA Kassoum')
    st.markdown(linkedin_link)


