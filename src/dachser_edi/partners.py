import xml.etree.ElementTree as ET
from typing import Optional
from pydantic import BaseModel, Field

from .base import EdiObject
from .address import Address
from .contact import Contact
from .enums import DachserContactType

class BasePartner(BaseModel, EdiObject):
    id: Optional[str] = Field(default=None, max_length=17)
    gln: Optional[str] = Field(default=None, min_length=13, max_length=13)
    name: Optional[str] = Field(default=None, max_length=30)
    _address_type: Optional[str] = None

    def to_element(self):
        param = {"AddressType": self._address_type} if self._address_type else {}
        shipment_address = ET.Element("ShipmentAddress", param)
        partner_info = ET.Element("PartnerInformation")
        self._add_text_element(partner_info, "PartnerID", self.id)
        self._add_text_element(partner_info, "PartnerGLN", self.gln)
        self._add_text_element(partner_info, "PartnerName", self.name)
        shipment_address.append(partner_info)
        return shipment_address

class Forwarder(BasePartner):
    _address_type = "FW"
    pass

class AddressablePartner(BasePartner):
    address: Optional[Address] = None
    contact: Optional[Contact] = None

    def to_element(self):
        root = super().to_element()
        
        partner_info = root.find("PartnerInformation")
        if self.address:
            partner_info.append(self.address.to_element())
        if self.contact:
            partner_info.append(self.contact.to_element())

        return root

class Consignor(AddressablePartner):
    _address_type = "CZ"
    pass

class Consignee(AddressablePartner):
    address: Address
    contact_type: Optional[DachserContactType] = None

    _address_type = "CN"
    
    def to_element(self):
        root = super().to_element()
        
        if self.contact_type:
            self._add_text_element(root, "ServiceContactType", self.contact_type.value)

        return root