import pandas as pd
import matplotlib.pyplot as plt

def graficar_evolucion_gastos(data):
    # Extraemos los valores de los gastos y la descripción
    print(data)
    descripcion = [d["descripcion"] for d in data]
    gastos = [d["banco"] for d in data]

    # Creamos el gráfico de línea
    plt.plot(descripcion, gastos, marker='o')

    # Añadimos etiquetas a los ejes y título
    plt.xlabel('Mes')
    plt.ylabel('Gastos en pesos')
    plt.title('Evolución de los gastos')

    # Guardamos la imagen en un archivo llamado "evolucion_gastos.png"
    print("Estoy en graficar")
    plt.savefig('evolucion_gastos.png')

def plot_evolucion_gastos(datos):
    # Crear un diccionario para almacenar los gastos totales por mes
    gastos_por_mes = {}

    # Iterar sobre los datos para sumar los gastos de cada mes
    for d in datos:
        mes = d['descripcion']
        gasto = d['banco'] # Deberia ser d['gasto'], hay que cambiar el servicio
        if mes in gastos_por_mes:
            gastos_por_mes[mes] += gasto
        else:
            gastos_por_mes[mes] = gasto
            
    # Convertir el diccionario en dos listas separadas (meses y gastos)
    meses = list(gastos_por_mes.keys())
    gastos = list(gastos_por_mes.values())

    fig, ax = plt.subplots()

    ax.fill_between(meses, gastos, label='Evolucion de gastos', color='tab:red')
    ax.grid(axis = 'y', color = 'gray', linestyle = 'dashed')
    plt.xticks(rotation=45)
    ax.legend(loc = 'upper right')
    # plt.show()

    # Guardar la imagen
    plt.savefig('../images/evolucionGastos.png')