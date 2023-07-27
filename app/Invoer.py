import streamlit as st

def Invoer():
    invoergeg = ()
    st.title("Invoer schepsels")
    name = st.text_input("Naam dier: ")
    soort = st.selectbox('Soort schepsel', ('INC', 'VOG', 'PLA', 'ZOG','VIS'))
    st.write('U heeft gekozen:', soort)
    kleur = st.text_input("Omschrijving kleur: ")
    aantal = int(st.number_input("Aantal schepsel: ", value=1))
    omgeving = st.text_input("Waar gespot? ")
    datum = st.date_input('Voer een datum in: ')
    temperatuur = st.number_input("Temperatuur (Celcius): ")
    
    foto = st.file_uploader('Upload een foto: ', type=['jpg', 'jpeg', 'png'])
    invoergeg = (name, soort, kleur, aantal, omgeving, datum, temperatuur)
    return invoergeg