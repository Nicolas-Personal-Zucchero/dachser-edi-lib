from enum import Enum

class Division(str, Enum):
    EUROPEAN = "T"
    FOOD = "F"
    AIR_SEA = "A"

class Product(str, Enum):
    # Delivery on next working day dependent on Km-zones
    TARGOSPEED = "Z"
    # Delivery on next working day by 10:00, dependent on Km-zones
    TARGOSPEED_10 = "S"
    # Delivery on next working day by 12:00, dependent on Km-zones
    TARGOSPEED_12 = "E"
    # Delivery on next working day (only after consultation with responsible DACHSER-branch)
    TARGOSPEED_PLUS = "X"
    # Delivery on a given date. The required delivery appointment has to be specified in the corresponding fields (according to the data format). With non-federal holidays a separate clearance with the responsible DACHSER-branch is needed.
    TARGOFIX = "V"
    # Delivery on a given date by 10:00. The required delivery appointment has to be specified in the corresponding fields (according to the data format). With non-federal holidays a separate clearance with the responsible DACHSER-branch is needed.
    TARGOFIX_10 = "R"
    # Delivery on a given date by 12:00. The required delivery appointment has to be specified in the corresponding fields (according to the data format). With non-federal holidays a separate clearance with the responsible DACHSER-branch is needed.
    TARGOFIX_12 = "W"
    # Delivery within the scope of standard transit time (generally within 2 working days)
    TARGOFLEX = "Y"
    # Delivery “free kerb side” beside the truck at the consignee exclusively for free house terms. A delivery appointment has to be agreed with the consignee. The required contact information have to be specified within the corresponding fields (according to the data format).
    TARGO_ON_SITE = "A"
    # Delivery in 1-man-handling “free delivered to maximum one customer specified unloading point” at the consignee. A delivery appointment has to be agreed with the consignee. The required contact information have to be specified within the corresponding fields (according to the data format).
    TARGO_ON_SITE_PLUS = "B"
    # Delivery within the scope of transit time beyond the limits of the entargo countries.
    CLASSICLINE = "N"
    # Delivery “free kerb side” beside the truck at the consignee exclusively for the incoterm "free delivered" on a given date. The consignor agrees a delivery appointment (the day) with the consignee. The required delivery appointment has to be specified in the corresponding fields (according to the data format). The delivery branch asks the consignee the time slot for the delivery (in the morning or in the afternoon).
    TARGO_ON_SITE_FIX = "U"

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
    CARTON = "KT"
    SACK = "S"
    BARREL = "F"
    BIG_BAG = "BB"

from enum import Enum

class CountryCode(str, Enum):
    # Europa Occidentale e Centrale
    AT = "AT"  # Austria
    BE = "BE"  # Belgio
    CH = "CH"  # Svizzera
    DE = "DE"  # Germania
    FR = "FR"  # Francia
    LI = "LI"  # Liechtenstein
    LU = "LU"  # Lussemburgo
    MC = "MC"  # Monaco
    NL = "NL"  # Paesi Bassi

    # Europa del Sud
    AD = "AD"  # Andorra
    ES = "ES"  # Spagna
    GR = "GR"  # Grecia
    IT = "IT"  # Italia
    MT = "MT"  # Malta
    PT = "PT"  # Portogallo
    SM = "SM"  # San Marino
    VA = "VA"  # Città del Vaticano

    # Europa del Nord
    DK = "DK"  # Danimarca
    EE = "EE"  # Estonia
    FI = "FI"  # Finlandia
    GB = "GB"  # Regno Unito
    IE = "IE"  # Irlanda
    IS = "IS"  # Islanda
    LT = "LT"  # Lituania
    LV = "LV"  # Lettonia
    NO = "NO"  # Norvegia
    SE = "SE"  # Svezia

    # Europa dell'Est e Balcani
    AL = "AL"  # Albania
    BA = "BA"  # Bosnia ed Erzegovina
    BG = "BG"  # Bulgaria
    BY = "BY"  # Bielorussia
    CZ = "CZ"  # Cechia
    HR = "HR"  # Croazia
    HU = "HU"  # Ungheria
    MD = "MD"  # Moldavia
    ME = "ME"  # Montenegro
    MK = "MK"  # Macedonia del Nord
    PL = "PL"  # Polonia
    RO = "RO"  # Romania
    RS = "RS"  # Serbia
    RU = "RU"  # Russia
    SI = "SI"  # Slovenia
    SK = "SK"  # Slovacchia
    UA = "UA"  # Ucraina

    # Nazioni Transcontinentali / Area Caucasica
    AM = "AM"  # Armenia
    AZ = "AZ"  # Azerbaigian
    CY = "CY"  # Cipro
    GE = "GE"  # Georgia
    TR = "TR"  # Turchia

class MeasurementName(str, Enum):
    WEIGHT = "Weight"
    VOLUME = "Volume"
    LOADING_METER = "LoadingMeter"
    LENGTH = "Length"
    WIDTH = "Width"
    HEIGHT = "Height"

class UnitCode(str, Enum):
    CENTILITER = "CLT"        # Centilitri (Volume liquidi)
    CUBIC_CENTIMETER = "CMQ"  # Centimetri cubi (Volume / Cubaggio)
    CENTIMETER = "CMT"        # Centimetri (Lunghezza)
    CUBIC_DECIMETER = "DMQ"   # Decimetri cubi (Volume / Cubaggio)
    DECIMETER = "DMT"         # Decimetri (Lunghezza)
    GRAM = "GRM"              # Grammi (Peso / Massa)
    HECTOLITER = "HLT"        # Ettolitri (Volume liquidi)
    KILOGRAM = "KGM"          # Chilogrammi (Peso / Massa)
    LITER = "LTR"             # Litri (Volume liquidi)
    MILLILITER = "MLT"        # Millilitri (Volume liquidi)
    MILLIMETER = "MMT"        # Millimetri (Lunghezza)
    CUBIC_METER = "MTQ"       # Metri cubi (Volume / Cubaggio)
    METER = "MTR"             # Metri lineari (Lunghezza)

class MeasurementType(str, Enum):
    GROSS_WEIGHT = "GRO"
    NET_WEIGHT = "NET"
    CHARGEABLE_WEIGHT = "CHA"

class TextType(str, Enum):
    DELIVERY_INSTRUCTION = "ZU",
    NOTIFICATION_ON_DELIVERY = "AS"
    SCHEDULED_APPOINTMENT = "AP"
    OTHER_INFORMATION = "SI"