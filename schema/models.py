from sqlalchemy import Boolean, Column , ForeignKey
from sqlalchemy import DateTime, Integer, String, Text, Float
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Bancos(db.Model):
    __tablename__ = "Bancos"

    idBanco = Column(Integer, primary_key=True)
    nombre = Column(String(100))

    banco_limite = relationship("Banco_Limites", backref="Banco",  overlaps="banco,banco_limite")
    deudaBCRA = relationship("DeudaBCRA", backref="Bancos", overlaps="banco,deudaBCRA")
    gastos = relationship("Gastos", backref="Banco",  overlaps="banco,gastos")

class Banco_Limites(db.Model):
    __tablename__ = "Banco_Limites"

    id = Column(Integer, primary_key=True, index=True)
    idBancoLimites = Column(Integer, ForeignKey("Bancos.idBanco"))
    limite_total = Column(Float)
    limite_actual = Column(Float)


class Periodos(db.Model):
    __tablename__ = "Periodos"

    idPeriodo = Column(Integer, primary_key=True, index=True)
    NumeroMes = Column(Integer)
    NumeroAnio = Column(Integer)
    descripcion = Column(String(50))

    gasto_mes = relationship("Gasto_Mes", backref="Periodos", overlaps="periodos,gasto_mes")

class DeudaBCRA(db.Model):
    __tablename__ = "DeudaBCRA"

    idDeuda = Column(Integer, primary_key=True, index=True)
    idBanco = Column(Integer, ForeignKey("Bancos.idBanco"))
    total = Column(Float)
    situacion = Column(String(50))


class Gastos(db.Model):
    __tablename__ = "Gastos"

    idGasto = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String(100))
    monto = Column(Float)
    idBanco = Column(Integer, ForeignKey("Bancos.idBanco"))
    fechaCompra = Column(String(10), default=datetime.today().strftime('%Y-%m-%d'))
    cuotasTotales = Column(Integer, default=1)
    cuotasPagas = Column(Integer, default=0)
    intereses = Column(Boolean, default=False)
    valorCuota = Column(Float, default=0)
    MesPrimeraCuota = Column(Integer, ForeignKey("Periodos.idPeriodo"))
    MesUltimaCuota = Column(Integer, ForeignKey("Periodos.idPeriodo"))

    mes_primera_cuota_rel = relationship("Periodos", foreign_keys=[MesPrimeraCuota])
    mes_ultima_cuota_rel = relationship("Periodos", foreign_keys=[MesUltimaCuota])
    gasto_mes = relationship("Gasto_Mes", backref="Gastos",  overlaps="gastos,gasto_mes")

class Gasto_Mes(db.Model):
    __tablename__ = "Gasto_Mes"

    idGastoMes = Column(Integer, primary_key=True, index=True)
    idPeriodo = Column(Integer, ForeignKey("Periodos.idPeriodo"))
    idGasto = Column(Integer, ForeignKey("Gastos.idGasto"))
    monto = Column(Float)

    