# Dachser EDI Library

Una libreria Python per la generazione e la validazione di file XML conformi agli standard EDI per ordini di trasporto (Transport Order), specifici per l'integrazione con i sistemi Dachser.

Questa libreria utilizza Pydantic per garantire che i dati inseriti rispettino i vincoli di lunghezza e formato richiesti prima della generazione dell'XML.

## Requisiti

* Python 3.9 o superiore
* Pydantic >= 2.0

## Installazione

È possibile installare la libreria direttamente dal repository GitHub o in locale.

### Installazione da GitHub
```bash
pip install git+[https://github.com/Nicolas-Personal-Zucchero/dachser-edi-lib.git](https://github.com/Nicolas-Personal-Zucchero/dachser-edi-lib.git)