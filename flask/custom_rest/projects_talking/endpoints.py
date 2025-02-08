# Import des Blueprint Moduls um den Endpunkt beim BormServer zu registrieren.
# Import des request Moduls um die Anfrage zu bearbeiten.
from flask import Blueprint, request 
# Import des Kundenspezifischen Kontaktmoduls um die Projektinfos abzufragen.
from custom.projects_talking.projects_talking import get_pro_infos

# Endpunkt "adresse" registrieren
api = Blueprint('projects_talking', __name__)


# Endpunkt /cadwork registrieren um Projektinfos anhand Dateipfad
# und Dateinamen abzufragen.
@api.route('/projekt')
def get_project():
    """Dateiinfos aus der URL holen"""
    # Abfrage der Anfragedaten
    filepath = request.args.get("filepath")
    filename = request.args.get("filename")
    # Aufruf der get_contact Funktion aus dem Kundenspezifischen Adressmoduls.
    data = get_pro_infos(filepath, filename)
    # Senden der Antwort
    return {"project": data}
