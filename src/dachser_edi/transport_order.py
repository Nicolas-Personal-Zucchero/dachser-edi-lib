import xml.etree.ElementTree as ET
from typing import Annotated, List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field

from .partners import Consignor, Consignee, Forwarder
from .base import EdiObject
from .shipment_line import ShipmentLine
from .enums import Division, Action, Currency, Product, TextType

# --- Sotto-modelli per pulire i dizionari ---

class CodDetails(BaseModel):
    code: str
    amount: float
    currency: Currency

class PreliminaryShipmentDetails(BaseModel):
    action: Action
    collection_date_from: datetime
    collection_date_until: datetime
    loading_point: str

class GoodsValue(BaseModel):
    amount: float
    currency: Currency

# --- Classe Principale ---

class TransportOrder(BaseModel, EdiObject):
    # --- Header Fields ---
    sender_id: str = Field(..., description="Technical EDI Sender")
    receiver_id: str = Field(..., description="Technical EDI Receiver")
    document_id: str = Field(..., min_length=5, max_length=5)
    document_date: datetime = Field(...)
    test: bool = False

    # Optional Header Fields
    transport_number: Optional[str] = Field(default=None, max_length=10)
    customer_shipment_reference: str = Field(..., max_length=35)

    # --- Partners ---
    consignor: Consignor
    consignee: Consignee
    forwarder: Forwarder

    # --- Shipment Info ---
    original_term: Optional[str] = None
    original_term_location: Optional[str] = None
    division: Optional[Division] = None
    dachser_product: Optional[Product] = None
    order_group: Optional[str] = None

    # --- Dates (Manteniamo datetime objects qui) ---
    shipment_date: Optional[datetime] = None
    delivery_date_fixed: Optional[datetime] = None
    delivery_date_earliest: Optional[datetime] = None
    delivery_date_latest: Optional[datetime] = None

    # --- Values ---
    goods_value: Optional[GoodsValue] = None

    # --- Flags (Default False) ---
    is_dangerous: bool = False
    tail_lift_required: bool = False
    picked_up_by_consignee_at_delivery_branch: bool = False
    customs_relevant: bool = False

    # --- Logistics ---
    dispatch_relation: Optional[str] = None
    sub_relation: Optional[str] = None
    
    # Nested Models (sostituiscono i dizionari)
    preliminary_shipment: Optional[PreliminaryShipmentDetails] = None
    cod: Optional[CodDetails] = Field(default=None, alias="COD")

    # --- Lines ---
    # Validazione: la lista non può essere vuota
    lines: List[ShipmentLine] = Field(..., min_length=1)

    # --- Notes ---
    notes: Optional[List[str]] = None

    # --- Footer ---
    # Validazione: lista con almeno 1 elemento, in cui ogni stringa ha esattamente 20 caratteri
    ssccs: List[Annotated[str, Field(min_length=20, max_length=20)]] = Field(..., alias="SSCCS", min_length=1)

    # --- Helper per formattazione date XML ---
    def _format_utc_date(self, date_obj: Optional[datetime]) -> Optional[str]:
        if not date_obj:
            return None
        utc_date = date_obj.astimezone(timezone.utc)
        return utc_date.strftime('%Y-%m-%dT%H:%M:%SZ')

    # --- XML Generation ---

    def generate_xml_string(self) -> str:
        root = ET.Element("ForwardingOrderInformation")
        
        self._build_document_header(root)
        shipment_header = self._build_transport_structure(root)

        self._build_partners(shipment_header)
        self._build_general_shipment_info(shipment_header)
        self._build_dates(shipment_header)
        self._build_values_and_flags(shipment_header)
        self._build_logistics_details(shipment_header)
        
        self._build_shipment_lines(shipment_header)
        self._build_shipment_text(shipment_header)
        self._build_package_identification(shipment_header)

        ET.indent(root, space="    ", level=0)
        return ET.tostring(root, encoding="utf-8", method="xml").decode()

    # --- Internal Builders (Adattati per leggere i campi Pydantic) ---

    def _build_document_header(self, parent):
        header = ET.SubElement(parent, "DocumentHeader")
        
        edi_sender = ET.SubElement(header, "EDISender")
        p_info_sender = ET.SubElement(edi_sender, "PartnerInformation")
        self._add_text_element(p_info_sender, "PartnerID", self.sender_id)

        edi_receiver = ET.SubElement(header, "EDIReceiver")
        p_info_receiver = ET.SubElement(edi_receiver, "PartnerInformation")
        self._add_text_element(p_info_receiver, "PartnerID", self.receiver_id)

        self._add_text_element(header, "DocumentID", self.document_id)
        
        doc_date = ET.SubElement(header, "DocumentDate")

        self._add_text_element(doc_date, "Date", self._format_utc_date(self.document_date))

        self._add_text_element(header, "TestFlag", "1" if self.test else "0")

    def _build_transport_structure(self, parent):
        transport_attrs = {"Number": self.transport_number} if self.transport_number else {}
        order = ET.SubElement(parent, "Transport", transport_attrs)

        shipment_header = ET.SubElement(order, "ShipmentHeader", {
            "CustomerShipmentReference": self.customer_shipment_reference
        })
        return shipment_header

    def _build_partners(self, parent):
        parent.append(self.consignor.to_element())
        parent.append(self.consignee.to_element())
        parent.append(self.forwarder.to_element())

    def _build_general_shipment_info(self, parent):
        if self.original_term:
            self._add_text_element(parent, "OriginalTerm", self.original_term)
        if self.original_term_location:
            self._add_text_element(parent, "OriginalTermLocation", self.original_term_location)
        if self.division:
            self._add_text_element(parent, "Division", self.division.value)
        if self.dachser_product:
            self._add_text_element(parent, "DachserProduct", self.dachser_product.value)
        if self.order_group:
            self._add_text_element(parent, "OrderGroup", self.order_group)

    def _build_dates(self, parent):
        date_fields = [
            ("ShipmentDate", self.shipment_date),
            ("DeliveryDateFixed", self.delivery_date_fixed),
            ("DeliveryDateEarliest", self.delivery_date_earliest),
            ("DeliveryDateLatest", self.delivery_date_latest)
        ]

        for tag_name, date_val in date_fields:
            if date_val:
                date_elem = ET.SubElement(parent, tag_name)
                self._add_text_element(date_elem, "Date", self._format_utc_date(date_val))

    def _build_values_and_flags(self, parent):
        if self.goods_value:
            val_elem = ET.SubElement(parent, "GoodsValue")
            self._add_text_element(val_elem, "Amount", str(self.goods_value.amount))
            self._add_text_element(val_elem, "Currency", self.goods_value.currency.value)

        self._add_text_element(parent, "ADRflag", "Y" if self.is_dangerous else None) #Non viene messo se False
        self._add_text_element(parent, "TailLiftRequired", "Y" if self.tail_lift_required else None) #Non viene messo se False
        self._add_text_element(parent, "ConsigneeCollectionIndicator", "Y" if self.picked_up_by_consignee_at_delivery_branch else "N")

    def _build_logistics_details(self, parent):
        if self.dispatch_relation:
            self._add_text_element(parent, "DispatchRelation", self.dispatch_relation)
        if self.sub_relation:
            self._add_text_element(parent, "SubRelation", self.sub_relation)

        self._add_text_element(parent, "CustomsIndicator", "Y" if self.customs_relevant else "N")

        if self.preliminary_shipment:
            prelim_elem = ET.SubElement(parent, "PreliminaryShipment")
            self._add_text_element(prelim_elem, "Action", self.preliminary_shipment.action.value)
            self._add_text_element(prelim_elem, "CollectionDateFrom", self._format_utc_date(self.preliminary_shipment.collection_date_from))
            self._add_text_element(prelim_elem, "CollectionDateUntil", self._format_utc_date(self.preliminary_shipment.collection_date_until))
            self._add_text_element(prelim_elem, "LoadingPoint", self.preliminary_shipment.loading_point)

        if self.cod:
            cod_element = ET.SubElement(parent, "COD", {"Code": self.cod.code})
            self._add_text_element(cod_element, "Amount", str(self.cod.amount)) 
            self._add_text_element(cod_element, "Currency", self.cod.currency.value)

    def _build_shipment_lines(self, parent):
        for line in self.lines:
            parent.append(line.to_element())

    def _build_shipment_text(self, parent):
        if self.notes:
            text_element = ET.SubElement(parent, "ShipmentText", {"TextType": TextType.DELIVERY_INSTRUCTION.value})
            for n in self.notes:
                self._add_text_element(text_element, "Text", n)
            self._add_text_element(text_element, "TextLanguage", "IT")

    def _build_package_identification(self, parent):
        if self.ssccs:
            for sscc in self.ssccs:
                pkg_id = ET.SubElement(parent, "PackageIdentification")
                self._add_text_element(pkg_id, "SSCCBarCode", sscc)
