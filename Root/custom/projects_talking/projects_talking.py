import bormapi.database as db
from bormapi.exceptions import BormApiDbException


def get_pro_infos(filepath: str, filename: str):
    """Projektinfos anhand vom Dateipfad aus der DokV ermitteln"""
    pro_query = """\
        SELECT PROJEKTNR, PROJEKTBEZ FROM PRO_STAMM
        WHERE PROJEKT_ID IN (SELECT PROJEKT_ID
        FROM DOKV_MAIN WHERE DOKV_ID IN
        (SELECT DOKV_ID FROM DOKV_DATA
        WHERE DOKV_PATH LIKE REPLACE(@filepath, '/','\\')
        AND DOKV_NAME LIKE @filename))
        """

    parameters = {'@filepath': filepath, '@filename': filename}

    pro_data = []
    try:
        _, pro_data = db.reader.read_as_list_of_dicts(pro_query, parameters)
    except BormApiDbException as e:
        print("Exception occured: %s", e)

    return pro_data
