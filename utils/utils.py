import datetime

meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre",
         "noviembre", "diciembre"]

def numero_proximo_mes():
    fecha_actual = datetime.datetime.now()
    siguiente_mes = (fecha_actual.month % 12) + 1
    return siguiente_mes

def filterMonth(text):
    text_lower = text.lower()
    mes_in_text = 0
    for i in range(0,len(meses)):
        if meses[i] in text_lower:
            mes_in_text = i+1
            break

    if mes_in_text == 0:
        mes_in_text = numero_proximo_mes()
    
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