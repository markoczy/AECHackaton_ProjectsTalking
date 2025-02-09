import xml.etree.ElementTree as ET

def read_user_attribute(file_path, tag_name, attribute_name):
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    # Use XPath to find the element with the specified tag
    element = root.find(f".//Project/Guid/@Value")
    
    if element is not None:
        # Retrieve the attribute value
        attribute_value = element.get(attribute_name)
        return attribute_value
    else:
        return None

# Example usage
file_path = 'ProdTimeX.xml'
tag_name = 'ProjectsTalkingGUID'
attribute_name = 'UserAttribute'

attribute_value = read_user_attribute(file_path, tag_name, attribute_name)
print(f'The UserAttribute value of {tag_name} is: {attribute_value}')