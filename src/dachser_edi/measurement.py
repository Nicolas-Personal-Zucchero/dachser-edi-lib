import xml.etree.ElementTree as ET
from typing import Optional
from pydantic import BaseModel

from .base import EdiObject
from .enums import MeasurementName, MeasurementType, UnitCode

class Measurement(BaseModel, EdiObject):
    name: MeasurementName
    value: float
    unit: UnitCode
    code: Optional[MeasurementType] = None

    def to_element(self):
        attributes = {"Code": self.code.value} if self.code else {}
        
        root = ET.Element(self.name.value, attributes)
        
        measurement_element = ET.SubElement(root, "Measurement")
        
        self._add_text_element(measurement_element, "Value", str(self.value))
        self._add_text_element(measurement_element, "Unit", self.unit.value)
        
        return root