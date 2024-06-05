# Eine Liste von Dictionaries
list = []

for i in range(0, 9):
    
    i = {
            "id" : i,
            "subject": "Hallo",
            "content": "Du bist doof"
        }
    
    list.append(i)

# Ein Schlüssel-Wert-Paar, das überprüft werden soll
schluessel = "id"
wert = 2

# Ein Schlüssel-Wert-Paar zu jedem Dictionary in der Liste hinzufügen, wenn das bestimmte Schlüssel-Wert-Paar nicht vorhanden ist
for dict in list:
    if dict.get(schluessel) != wert:
        dict["Neuer Schlüssel"] = "Neuer Wert"

# Die aktualisierte Liste ausgeben
for i, email in enumerate(list):
    print(f"Email {i+1}: {email}")
