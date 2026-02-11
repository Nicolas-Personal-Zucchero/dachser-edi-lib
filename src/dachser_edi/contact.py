import xml.etree.ElementTree as ET
from typing import Optional
from pydantic import BaseModel, Field

from .base import EdiObject

class Contact(BaseModel, EdiObject):
    name: Optional[str] = Field(default=None, max_length=35)
    phone: Optional[str] = Field(default=None, max_length=25)
    email: Optional[str] = Field(default=None, max_length=150)
    first_name: Optional[str] = Field(default=None, max_length=35)
    fax: Optional[str] = Field(default=None, max_length=25)
    mobile: Optional[str] = Field(default=None, max_length=25)

    def to_element(self):
        root = ET.Element("ContactInformation")
        self._add_text_element(root, "ContactName", self.name)
        self._add_text_element(root, "ContactPhoneNumber", self.phone)
        self._add_text_element(root, "ContactEmail", self.email)
        self._add_text_element(root, "ContactFirstName", self.first_name)
        self._add_text_element(root, "ContactMobilePhoneNumber", self.mobile)
        self._add_text_element(root, "ContactFaxNumber", self.fax)
        return root