import xml.etree.ElementTree as ET

class EdiObject:
    
    def validate(self):
        """Method to override in subclasses for validation"""
        pass

    def to_element(self) -> ET.Element:
        """Convert the object to an XML element"""
        raise NotImplementedError("You must implement to_element in subclasses")

    def _add_text_element(self, parent, tag, value):
        if value is not None and value != "":
            el = ET.SubElement(parent, tag)
            el.text = str(value)