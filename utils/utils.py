meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre",
         "noviembre", "diciembre"]

def filterMonth(text):
    text_lower = text.lower()
    mes_in_text = ""
    for i in meses:
        if i in text_lower:
            mes_in_text = i
            break
    
    return mes_in_text

def getCards(banks, text):
    text_lower= text.lower()
    bank = ""

    for i in banks:
        if i in text_lower:
            bank = i
            break
    
    return bank

def parseGasto(text, banks):
    
    result = {
          "descripcion": "Buzo",
          "monto": 1000,
          "idBanco": 5,
          "cantidad_cuotas": 12,
          "intereses": 0,
          "valor_cuota": 15
    }

    return result