import xml.etree.ElementTree as ET
from typing import Optional
from pydantic import BaseModel, Field

from .base import EdiObject
from .enums import CountryCode

class Address(BaseModel, EdiObject):
    street: str = Field(..., min_length=1)
    city: str = Field(..., min_length=1)
    postal_code: str = Field(..., min_length=1, max_length=9)
    country_code: CountryCode
    supplement_information: Optional[str] = None

    def to_element(self):
        root = ET.Element("AddressInformation")
        self._add_text_element(root, "Street", self.street)
        self._add_text_element(root, "City", self.city)
        self._add_text_element(root, "PostalCode", self.postal_code)
        self._add_text_element(root, "CountryCode", self.country_code.value)
        self._add_text_element(root, "SupplementInformation", self.supplement_information)
        return root