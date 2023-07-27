import streamlit as st
import sqlite3, os, glob, time
import pandas as pd
from PIL import Image
from zoekplaatje import fotozoek

def hoogste_ID():
    conn = sqlite3.connect('C:\sqlite/acgas/acgas.db')
    c = conn.cursor()

    c.execute('SELECT * FROM schepsel ORDER BY id DESC LIMIT 1')
    highest_id = c.fetchone()[0]
    conn.close()
    return highest_id

def zoeksoort():
    soort = st.selectbox('Soort schepsel', ('INC', 'VOG', 'PLA', 'ZOG','VIS'))
    st.write('U heeft gekozen:', soort)
    if st.button('OK'):
       st.write('U heeft op OK geklikt!')
        
       conn = sqlite3.connect('C:\sqlite/acgas/acgas.db')
       cur = conn.cursor()
       cur.execute(f"SELECT ID, naam FROM schepsel WHERE soort = '{soort}' ")
       tabelres = cur.fetchall()

       conn.close()
       return tabelres
    else:
       st.write('U heeft niet op OK geklikt.')

def zoekplaats():
    plaats = st.text_input('Plaats (dorp of stad):')
    conn = sqlite3.connect('C:\sqlite/acgas/acgas.db')
    cur = conn.cursor()
    #cur.execute(f"SELECT ID, naam FROM schepsel WHERE soort = '{soort}' ")
    #omgevingres = cur.fetchall()
    cur.execute(f"SELECT naam, aantal FROM schepsel INNER JOIN meetgegevens ON schepsel.ID = meetgegevens.ID WHERE meetgegevens.plaats = '{plaats}' ")
    
    conn.close()
    soortres = cur.fetchall()

    conn.close()
    if st.button('Zoek'):
       st.write(f'Zoekactie gestart voor plaats {plaats}.')
       return soortres
    else:
       st.write('Klik op Zoek..')

def zoeknaam(naam):
    zoekletters = naam[0:]
    conn = sqlite3.connect('C:\sqlite/acgas/acgas.db')
    cur = conn.cursor()
    cur.execute(f"SELECT ID, naam FROM schepsel WHERE INSTR(naam, '{zoekletters}') > 0 ")
    records = cur.fetchall()
    
    conn.close()
    if records == []: return 0,'Sorry, schepsel niet gevonden in database.'
    else:
        onderwerp = records[0][1]
        print(records)
        return records, onderwerp

def checknaam(naamschepsel):
    """ Controleer de invoer van naam op hoofdletters."""
    check = True
    for letter in naamschepsel:
        if letter in 'abcdefghijklmnopqrstuvwxyz ':
            continue
        else: 
            check = False
            return check
    return check
              
def getmeetgeg(ID):
    """ Meet gegevens ophalen uit DB voor zoekactie op naam. """
    conn = sqlite3.connect('C:\sqlite/acgas/acgas.db')
    cur = conn.cursor()
    cur.execute(f"SELECT omgeving, temperatuur_C, plaats, tijdstip FROM meetgegevens WHERE ID = '{ID}' ")
    records = cur.fetchall()
    
    conn.close()
    return records

def Invoer():
    vw = True
    invoergeg = ()
    ID = hoogste_ID()+1
    st.title("Invoer schepsels")
    naam = st.text_input("Naam schepsel: ")
        
    soort = st.selectbox('Soort schepsel', ('INC','VOG','PLA','ZOG','VIS'))
    st.write('U heeft gekozen:', soort)
    kleur = st.text_input("Omschrijving kleur: ")
    aantal = int(st.number_input("Aantal schepsel: ", value=1))
    omgeving = st.text_input("Waar gespot? ")
    datum = st.date_input('Voer een datum in: ')
    plaats = st.text_input("Plaats: ")
    temperatuur = st.number_input("Temperatuur (Celcius): ")
    
    #foto = st.file_uploader('Upload een foto: ', type=['jpg', 'jpeg', 'png'])
    invoergeg = (ID, naam, soort, kleur, aantal, omgeving, datum, plaats, temperatuur)
    if st.button('OK'):
       vw = checknaam(naam)
       if vw: 
           st.write(f'record {ID} is aangemaakt in DB. ')
           return invoergeg
       else: st.write(f'Naam schepsel {naam} mag geen hoofdletter(s) in ztaan!')
    else:
       st.write('U heeft niet op OK geklikt.')

def record_verwijderen(recnr):

    conn = sqlite3.connect('C:\sqlite/acgas/acgas.db')
    cur = conn.cursor()
    try:
        cur.execute(f"DELETE FROM schepsel WHERE ID = {recnr} ")
        cur.execute(f"DELETE FROM meetgegevens WHERE ID = {recnr} ")
        fb = f'Record {recnr} is verwijderd uit DB.'

    except:
        fb = f'Record {recnr} verwijderen is mislukt!!'

    conn.commit()
    conn.close()
    return fb

def Overzicht():

    conn = sqlite3.connect('C:\sqlite/acgas/acgas.db')
    cur = conn.cursor()
    cur.execute("SELECT schepsel.ID, schepsel.naam, meetgegevens.plaats FROM schepsel, meetgegevens WHERE schepsel.ID = meetgegevens.ID ORDER BY schepsel.naam ASC") 
    records = cur.fetchall()
    conn.close()
    return records

def main():
    
    st.title('All Creations great and small')
    menu = ['Hoofdmenu', 'Invoer', 'Opzoeken', 'Onderhoud']
    choice = st.sidebar.selectbox('Menu', menu)

    if choice == 'Hooofdmenu':
        st.subheader('Hoofdmenu')

    elif choice == 'Onderhoud':
        menu_onderhoud = 'Overzicht DB', 'Record verwijderen'
        keuze_onderhoud = st.sidebar.selectbox('Onderhoud', menu_onderhoud)

        #Overzicht geven van alle records:
        if keuze_onderhoud == 'Overzicht DB':
               st.write("Hieronder staat een overzicht van alle creations in de DB:")
               results = Overzicht()
               tabel1 = pd.DataFrame(results, columns=['RecordID', 'Naam','Plaats'])         
               st.table(tabel1)
        
        #Records verwijderen:
        elif keuze_onderhoud == 'Record verwijderen':
            st.write("De records die je hier kiest worden definitief verwijderd.")
            record = st.number_input('Geef recordnummer, die verwijderd word: ', min_value=1)
            if st.button('Verwijderen'):
               feedback_verwijderen = record_verwijderen(record)
               st.write(feedback_verwijderen)


    elif choice == 'Opzoeken':
        st.subheader('Hier kun je info opzoeken')
        menu = ['Soorten', 'Datum', 'Plaats', 'Naam']
        keuze = st.sidebar.selectbox('Zoeken', menu)
        if keuze == 'Soorten': 
            zoekres = zoeksoort()
            tabel = pd.DataFrame(zoekres, columns=['RecordID', 'Naam'])         
            st.table(tabel)

        elif keuze == 'Plaats':
            plaatsres = zoekplaats()
            tabel = pd.DataFrame(plaatsres, columns=['Naam', 'Aantal'])         
            st.table(tabel)
        elif keuze == 'Naam':
            #Fotomap leegmaken
            mapje = 'C:\sqlite/acgas/app/fotos/*'
            files = glob.glob(mapje)
            for f in files:
                    os.remove(f)
            schepsel= st.text_input('Welk schepsel zoek je? ')
            if st.button('Zoek'):
               recordnr, onderwerp = zoeknaam(schepsel)
               st.text(onderwerp)
               i = 0
               st.write('Gevonden resultaten:')
               for record in recordnr:
                   ID = recordnr[i][0]
                   meetgegevens = getmeetgeg(ID)
                   st.write(f'Recordnr: {recordnr[i][0]} | {recordnr[i][1]} ; {meetgegevens[0][0]} in {meetgegevens[0][2]} bij temperatuur {meetgegevens[0][3]} C, datum {meetgegevens[0][1]}')
                   i += 1

               # Drie afbeeldingen of foto's ophalen via Flickr
               feedback = fotozoek(onderwerp)
               st.write(f'Melding Flickr site: {feedback}')
               files = glob.glob(mapje)
               if not files:
                   st.write('Flickr heeft hiervan geen afbeeldingen gevonden.')
               else:  
                  st.write(f'Flickr heeft de volgende drie afbeeldingen van {onderwerp} gevonden:')                
                  for f in files:
                      image = Image.open(f)
                      st.image(image, caption='afbeelding')
                      time.sleep(2)
               
            else: st.write('Druk op zoek...')
            
            

    elif choice == 'Invoer':
        
        try: 
           geg = Invoer()
           print(geg)
        
           conn = sqlite3.connect('C:\sqlite/acgas/acgas.db')
           c = conn.cursor()
           #c.execute("SELECT * FROM media")
       
           c.execute("INSERT INTO schepsel (ID, naam, soort, kleur, aantal) VALUES (?, ?, ?, ?, ?)", (geg[0], geg[1], geg[2], geg[3], geg[4]))
           c.execute("INSERT INTO meetgegevens (omgeving, temperatuur_c, plaats, tijdstip) VALUES (?, ?, ?, ?)", (geg[5], geg[6], geg[7], geg[8]))
        
           conn.commit()
           conn.close()

        except:
            st.write('Mededeling SQLite DB: Record nog niet ingevoerd of record fout ingevuld.')

        



if __name__ == "__main__":
    main()