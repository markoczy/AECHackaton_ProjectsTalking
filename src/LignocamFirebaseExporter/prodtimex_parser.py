import xml.etree.ElementTree as ET


class LoadData:
    def __init__(self, load_production_time, load_filename, load_item_guid):
        self.load_production_time = load_production_time
        self.load_filename = load_filename
        self.load_item_guid = load_item_guid
    def __str__(self):
        return f"LoadData: {self.load_production_time}, {self.load_filename}, {self.load_item_guid}"


def get_xml_root(file_path):
    # Parse the XML file
    tree = ET.parse(file_path)
    return tree.getroot()

def get_loads(root: ET.Element):
    return root.findall('.//Load')

def get_load_production_time(load: ET.Element):
    return load.get('LoadProductionTime')

def get_load_filename(load: ET.Element):
    return load.get('LoadFilename')

def get_load_items(parent: ET.Element):
    return parent.findall('.//LoadItem')

def get_load_item_guid(load_item: ET.Element):
    return load_item.find('.//LoadItemPart').get('GUID')

def get_load_data(root: ET.Element)-> list[LoadData]:
    loads = get_loads(root)
    load_data = []
    for load in loads:
        load_production_time = get_load_production_time(load)
        load_filename = get_load_filename(load)
        load_items = get_load_items(load)
        load_item_guid = get_load_item_guid(load_items[0]) # assuming there's one part per load for now..
        load_data.append(LoadData(load_production_time, load_filename, load_item_guid))
    return load_data

root = get_xml_root("../../data/lignocam/Hackathon.ISO/9550A9CA-5969-4E22-85BC-A1B378E97737.XML")
load_data = get_load_data(root)
for ld in load_data:
    print(ld)

