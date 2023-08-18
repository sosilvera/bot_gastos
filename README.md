# Gastos bot

Me gustaria que cuando reciba un mensaje, tener una funcion que me devuelva la siguiente estructura:
msj = {
    "nombre": ejemplo,
    "id_chat": 1234,
    "text": Hola como estas
}

Despues, me gustaria tener flujos definidos, que reconozcan el mensaje y tengan seteadas respuestas:
- Flujo de Hola
- Flujo de Seguir ayudando
- Flujo de Crear Gasto
- Flujo de Consultar gasto total para el proximo mes
- Flujo de Consultar gasto total para un determinado mes
- Flujo para Consultar un gasto por banco para el proximo mes
- Obtener un grafico de gastos a 6 meses
- Obtener un grafico de gastos a 6 meses por banco



Podrias armarme el chatBot, suponiendo que tengo como punto de entrada la variable "msj" y suponiendo que para cada flujo tengo una funcion que me devuelve exactamente el texto que le voy a dar al usuario que llame al bot.

Ademas, podría modificar la estructura de la base para registrar usuarios. El id del usuario puede ser el id del chat. Ademas se podria tener el concepto de Familia, con una tabla intermedia que sea Usuario_Familia, y que los gastos se agrupen por familia, pero se hagan por usuario.
Se puede hacer un metodo de autenticacion en donde, cuando el usuario A habla con el bot y pide registrarse a la familia FA, se mande un mensaje a todos los usuarios de esa familia, y el primero que responda OK haga que el user A quede agregado.