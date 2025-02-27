# Import des Blueprint Moduls um den Endpunkt beim BormServer zu registrieren.
# Import des request Moduls um die Anfrage zu bearbeiten.
from flask import Blueprint, request 
# Import des Kundenspezifischen Kontaktmoduls um die Projektinfos abzufragen.
from custom.projects_talking.projects_talking import get_new_duedate

# Endpunkt "adresse" registrieren
api = Blueprint('projects_talking', __name__)


# Endpunkt /cadwork registrieren um Projektinfos anhand Dateipfad
# und Dateinamen abzufragen.
@api.route('/duedate')
def set_duedate():
    """Dateiinfos aus der URL holen"""
    # Abfrage der Anfragedaten
    guid = request.args.get("guid")
    date = request.args.get("date")
    # Aufruf der get_contact Funktion aus dem Kundenspezifischen Adressmoduls.
    data = get_new_duedate(guid, date)
    # Senden der Antwort
    return {"project": data}
