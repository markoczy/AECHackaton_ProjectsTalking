# API Key: N9MKRMxO1F4iuoCPIAaBMcaROQS4gDHWCs5NYm7Gaiz


import sys
import requests

filepath = uc.get_3d_file_path()
filename = uc.get_3d_file_name()



# print("Der Pfad ist: {} und der Dateiname ist: {}".format(filepath, filename))
# print(ofp)

# URL und Header für die REST-Schnittstelle
url = f"http://localhost:10170/api/py/projects_talking/duedate?filepath={filepath}&filename={filename}"
headers = {
    "BORM-API-KEY": "N9MKRMxO1F4iuoCPIAaBMcaROQS4gDHWCs5NYm7Gaiz",  # API-Key im Header
    # "Content-Type": "application/json"
}

# WIP BuB: Funktionierte so nicht, weil der Pfad als HTML Formatiert wurde statt mit "/" also mit "%2F"
# URL-Parameter hinzufügen
# params = {
#     "filepath": ofp,
#     "filename": filename
# }

# Anfrage an die REST-Schnittstelle senden
try:
    # response = requests.get(url, headers=headers, params=params)
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Prüft auf HTTP-Fehler

    print(response)

    # JSON-Antwort parsen
    data = response.json()

    print(data)

    # Parameter aus der JSON-Antwort extrahieren
    project_list = data.get("project")

    if project_list and isinstance(project_list, list) and len(project_list) > 0:
        projektnr = project_list[0].get("PROJEKTNR")
        projektbez = project_list[0].get("PROJEKTBEZ")

        # Ausgabe der Parameter
        if projektnr is not None and projektbez is not None:
            # Debug
            # print(f"PROJEKTNR: {projektnr}")
            # print(f"Projektbezeichnung: {projektbez}")
            uc.set_project_name(projektbez)
            uc.set_project_number(projektnr)
        else:
            print("Die erwarteten Parameter 'PROJEKTNR' und 'PROJEKTBEZ' wurden nicht gefunden.")
    else:
        print("Das 'project'-Array ist leer oder fehlt.")

except requests.exceptions.RequestException as e:
    print(f"Fehler bei der Anfrage: {e}")
