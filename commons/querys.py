from schema.models import Bancos, Periodos, Gastos,DeudaBCRA,Gasto_Mes,db
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
import urllib
from datetime import datetime
import commons.env as env

class Querys():
    def __init__(self):
        params = urllib.parse.quote_plus(env.STRING_CONNECTION)
        engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
        db.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)

        self.session = Session()
        
    def insertGasto(self, gasto):
        self.session.add(gasto)
        self.session.commit()
        return gasto.idGasto

    def insertGastoMes(self, idPrimeraCuota, idGasto, valorCuota, cantidadCuotas):
        for i in range(idPrimeraCuota, idPrimeraCuota+cantidadCuotas):
            cuota = Gasto_Mes(
                idGasto = idGasto,
                idPeriodo = i,
                monto = valorCuota
            )
            self.session.add(cuota)
        
        self.session.commit()

    def queryBancos(self):
        bancos = self.session.query(Bancos).all()
        return [{'id':banco.idBanco, 'nombre': banco.nombre} for banco in bancos]

    def queryConsumosPorMes(self):
        query = self.session.query(Gasto_Mes.idGastoMes,Periodos.descripcion, Gastos.descripcion, Gasto_Mes.monto, Bancos.nombre).\
            select_from(Gasto_Mes).\
            join(Gastos, Gastos.idGasto == Gasto_Mes.idGasto).\
            join(Bancos, Bancos.idBanco == Gastos.idBanco).\
            join(Periodos, Gasto_Mes.idPeriodo == Periodos.idPeriodo).\
            order_by(Gasto_Mes.idPeriodo)

        result = []
        for row in query.all():
            result.append({
                'periodo': row[0],
                'descripcion': row[1],
                'monto': row[2],
                'banco': row[3]
            })

        return result
    
    def queryTotalesPorMes(self):
        totalesMes = self.session.query(Gasto_Mes.idPeriodo, func.sum(Gasto_Mes.monto).label('Monto'))\
                    .group_by(Gasto_Mes.idPeriodo)\
                    .all()
        return [{'idPeriodo':t.idPeriodo, 'monto':t.Monto} for t in totalesMes]

    def queryTotalesPorTarjetaProximoMes(self, periodo):        
        totalesTarjeta = self.session.query(Bancos.nombre, func.sum(Gastos.monto).label("totales")).\
                            join(Gastos, Bancos.idBanco == Gastos.idBanco).\
                            filter(Gasto_Mes.idPeriodo == periodo).\
                            group_by(Bancos.nombre, Gastos.idBanco).\
                            all()
        return [{'nombre': t.nombre, 'totales': t.totales} for t in totalesTarjeta]

    def queryTotalesPorTarjeta(self):
        totalesTarjeta = self.session.query(Bancos.nombre, func.sum(Gastos.monto).label("totales")).\
                            join(Gastos, Bancos.idBanco == Gastos.idBanco).\
                            group_by(Bancos.nombre, Gastos.idBanco).\
                            all()
        return {t['nombre']: t['totales'] for t in totalesTarjeta}

    def queryTotales(self):
        return
    
    def queryDeudaBCRA(self):
        return
    
    def queryPeriodoByMes(self, mes, anio):
        idPeriodo = self.session.query(Periodos.idPeriodo)\
            .filter(Periodos.NumeroMes == mes)\
            .filter(Periodos.NumeroAnio == anio)\
            .first()
        
        return idPeriodo[0]
    
    def queryTotalByPeriodo(self, periodo):
        monto = self.session.query(func.sum(Gasto_Mes.monto))\
                .filter(Gasto_Mes.idPeriodo == periodo)\
                .first()
        
        return monto[0]

    # Cierro la sesion de la base
    def sessionClose(self):
        self.session.close()