from transformers import pipeline
from commons.querys import Querys
from schema.models import Gastos
import utils.utils as u
import utils.graphics as gh
import datetime

class Bot():
    def __init__(self, msg, classifier):
        self.q = Querys()
        self.name = msg["name"]
        self.id = msg["userId"]
        self.isResponse = msg["response"]

        self.labels = [
            "Hola",
            "Te sigo ayudando?",
            "Crear Gasto",
            "Consultar gasto total para el proximo mes",
            "Consultar gasto total para un determinado mes",
            "Consultar un gasto por banco para el proximo mes",
            "Obtener un grafico de gastos a 6 meses por banco",
            "No se reconoció ninguna acción específica."
        ]

        self.labels_dic = {
            "Hola": self.hi(),
            "Te sigo ayudando?": self.keepHelping(),
            "Crear Gasto": self.createGastoFirstResponse(),
            "Consultar gasto total para el proximo mes": self.queryNextMonth(),
            "Consultar gasto total para un determinado mes": self.queryTotalsByMonth(u.filterMonth(msg["text"])),
            "Consultar un gasto por banco para el proximo mes": self.queryTotalsByCardByMonth(msg["text"]),
            "Obtener un grafico de gastos a 6 meses por banco": self.getGraphForSixMonth(),
            "No se reconoció ninguna acción específica.": self.defectMessage(),
            "Continuar creacion": self.createGastoSecondResponse(msg["text"]) 
        }

        self.responseMsg = self.process_text_pipeline(msg["text"], classifier)

    def process_text_pipeline(self, text, classifier):
        process =  classifier(text, candidate_labels = self.labels)
        print(process)
        self.proccess_result = process["labels"][0]

    def hi(self):
        return {"msg": f"Hola {self.name}, en que puedo ayudarte?", "need_response": False, "image": False}
    
    def keepHelping(self):
        return {"msg":f"{self.name}, en que mas puedo ayudarte?", "need_response": False, "image": False}
    
    def createGastoFirstResponse(self):
        datos = """
            Nombre:
            Monto:
            Banco:
            Cantidad de Cuotas:
            Porcentaje Interes:
            Valor Cuota:
            Mes de Primer cuota:
        """
        return {
            "msg": f"Hola {self.name}, necesito que ingreses los siguientes datos en un solo mensaje: {datos}",
            "need_response": True,
            "image": False
            }

    def createGastoSecondResponse(self, text):
        bancos = self.q.queryBancos()
        gasto = u.parseGasto(text, bancos)
        # Obtener mes actual y sumarle 1
        mesActual = datetime.date.today().month
        idPrimeraCuota = self.q.queryPeriodoByMes(mesActual + 1, 2023)
        idUltimaCuota = idPrimeraCuota + gasto["cantidad_cuotas"]

        nuevo_gasto = Gastos(
                descripcion=gasto["descripcion"],
                monto=gasto["monto"],
                idBanco=gasto["idBanco"],
                cuotasTotales=gasto["cantidad_cuotas"],
                cuotasPagas=0,
                intereses=gasto["intereses"],
                valorCuota=gasto["valor_cuota"],
                MesPrimeraCuota=idPrimeraCuota,
                MesUltimaCuota=idUltimaCuota
        )
        
        # Agregar el gasto a la base de datos
        idGasto = self.q.insertGasto(nuevo_gasto)
        
        self.q.insertGastoMes(idPrimeraCuota, idGasto, gasto["valor_cuota"], gasto["cantidad_cuotas"])

    def queryNextMonth(self):
        mesActual = datetime.date.today().month
        periodo = self.q.queryPeriodoByMes(mesActual + 1, 2023)
        total = self.q.queryTotalByPeriodo(periodo)

        return {
            "msg": f"{self.name} el total para el próximo mes es de {total}", 
            "need_response": False,
            "image": False
        }

    def queryTotalsByMonth(self, month):
        periodo = self.q.queryPeriodoByMes(month, 2023)
        result = self.q.queryTotalByPeriodo(periodo)
        return {
            "msg": f"{self.name} el total para el mes de {month} es de {str(result)}", 
            "need_response": False,
            "image": False
        }
    
    def queryTotalsByCardByMonth(self, text):
        banks = self.q.queryBancos()
        card = u.getCards(banks, text)
        month = u.filterMonth(text)
        
        periodo = self.q.queryPeriodoByMes(month, 2023)
        consumos = self.q.queryTotalesPorTarjetaProximoMes(periodo)
        
        consumoTarjeta = consumos[card]
        
        return {
            "msg": f"{self.name} los consumos para la tarjeta {card} en el mes de {month} es de {str(consumoTarjeta)}", 
            "need_response": False,
            "image": False
        }

    def getGraphForSixMonth(self):
        consumos = self.q.queryConsumosPorMes()
        gh.plot_evolucion_gastos(consumos)
        return {"msg": '../images/evolucionGastos.png', "need_response": False, "image": True}

    def defectMessage(self):
        return {"msg": f"{self.name} no entendi lo que me dijiste", "need_response": False}

    def getResponse(self):
        if self.isResponse:
            return self.labels_dic["Continuar creacion"]
        else:
            print(self.proccess_result)
            return self.labels_dic[self.proccess_result]