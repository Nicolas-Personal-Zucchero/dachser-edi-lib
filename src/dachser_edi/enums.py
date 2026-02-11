from enum import Enum

class Division(str, Enum):
    EUROPEAN = "T"
    FOOD = "F"
    AIR_SEA = "A"

class Action(str, Enum):
    ORIGINAL = "9"
    UPDATE = "5"
    DELETION = "1"

class Currency(str, Enum):
    BGN = "BGN"
    CHF = "CHF"
    DKK = "DKK"
    EUR = "EUR"
    GBP = "GBP"
    HUF = "HUF"
    NOK = "NOK"
    PLN = "PLN"
    SEK = "SEK"
    USD = "USD"
    RON = "RON"
    RUB = "RUB"
    CZK = "CZK"
    TRY = "TRY"
    
class DachserContactType(str, Enum):
    # Notifica automatica che la merce è in arrivo.
    # REQ: Nome + Cellulare e/o Email.
    AUTOMATED_NOTIFICATION = "AS"
    
    # Appuntamento telefonico concordato con operatore.
    # REQ: Nome + Telefono fisso o Cellulare.
    PHONE_BOOKING = "AT"
    
    # Appuntamento concordato via link automatico (SMS/Email).
    # REQ: Nome + Cellulare o Email.
    AUTOMATED_BOOKING = "AP"
    
    # Chiamata dell'autista circa 1 ora prima della consegna.
    # REQ: Nome + Telefono fisso o Cellulare.
    PHONE_NOTIFICATION_1H = "AC"

class PackingType(str, Enum):
    EURO_PALLET = "EU" #Pallet a scambio
    LOSS_PALLET = "EW" #Pallet a perdita
    BOX = "KT" #Cartoni

class CountryCode(str, Enum):
    IT = "IT"
    DE = "DE"
    FR = "FR"
    ES = "ES"
    AT = "AT"
    CH = "CH"

class MeasurementName(str, Enum):
    WEIGHT = "Weight"
    VOLUME = "Volume"
    LOADING_METER = "LoadingMeter"
    LENGTH = "Length"
    WIDTH = "Width"
    HEIGHT = "Height"

class UnitCode(str, Enum):
    CLT = "CLT"
    CMQ = "CMQ"
    CMT = "CMT"
    DMQ = "DMQ"
    DMT = "DMT"
    GRM = "GRM"
    HLT = "HLT"
    KGM = "KGM"
    LTR = "LTR"
    MLT = "MLT"
    MMT = "MMT"
    MTQ = "MTQ"
    MTR = "MTR"

class MeasurementType(str, Enum):
    GROSS_WEIGHT = "GRO"
    NET_WEIGHT = "NET"
    CHARGEABLE_WEIGHT = "CHA"