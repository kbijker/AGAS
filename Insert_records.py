import sqlite3


conn = sqlite3.connect('C:\sqlite/acgas/acgas.db')
c = conn.cursor()
c.execute("SELECT * FROM media")
#naam = input('Naam schepsel: ')
#soort = input('Soort (INC=Insect, VOG=Vogel, PLA=Plant): ')
#kleur = input('Kleur: ')
naam = 'Brandnetelmot'
soort = 'INC'
kleur = 'zwart-wit-paars'

aantal = 1
# - int(input('Aantal: '))
c.execute("INSERT INTO schepsel (naam, soort, kleur, aantal) VALUES (?, ?, ?, ?)", (naam, soort, kleur, aantal))

conn.commit()
conn.close()