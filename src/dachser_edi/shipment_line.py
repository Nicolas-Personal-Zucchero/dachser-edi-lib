import xml.etree.ElementTree as ET
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

from .measurement import Measurement, MeasurementName
from .base import EdiObject
from .enums import PackingType

class ShipmentLine(BaseModel, EdiObject):
    packages_quantity: int
    packing_type: PackingType
    description: str = Field(..., min_length=1)
    measurements: List[Measurement] = Field(..., min_length=1)

    goods_group: Optional[str] = None
    goods_group_quantity: Optional[str] = None
    marker: Optional[str] = None
    packaging_aids_position: Optional[str] = None

    @field_validator('measurements')
    @classmethod
    def check_weight_present(cls, v: List[Measurement]):
        has_weight = any(m.name == MeasurementName.WEIGHT for m in v)
        if not has_weight:
            raise ValueError("Weight Measurement is Required.")
        return v

    def to_element(self):
        root = ET.Element("ShipmentLine")
        self._add_text_element(root, "PackagesQuantity", self.packages_quantity)
        self._add_text_element(root, "PackingType", self.packing_type.value)
        
        measurements_root = ET.SubElement(root, "Measurements")
        for m in self.measurements:
            w_el = m.to_element() 
            measurements_root.append(w_el)

        self._add_text_element(root, "GoodsDescription", self.description)

        if self.goods_group: 
            self._add_text_element(root, "GoodsGroup", self.goods_group)
        if self.goods_group_quantity: 
            self._add_text_element(root, "GoodsGroupQuantity", self.goods_group_quantity)
        if self.marker: 
            self._add_text_element(root, "Marker", self.marker)
        if self.packaging_aids_position: 
            self._add_text_element(root, "PackagingAidsPosition", self.packaging_aids_position)

        return root