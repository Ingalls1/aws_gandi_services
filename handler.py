import json
from zeep import Client
from zeep.helpers import serialize_object


def get_saldo(card):
    # Definir la URL del servicio web
    url = 'https://bluetest.mx/FlowGandhiCom/ws/blueengine.asmx?wsdl'

    # Crear un cliente Zeep
    client = Client(url)

    # Definir los parámetros de la solicitud
    loginId = '0804g4ndh1'
    password = 'x6wmk9Zfes'
    transactionDate = '10 04 2023 15:07:35'
    cardId = card
    referenceId = '10 04 2023 10:29:53'
    referenceId2 = '3572000201154'

    # Realizar la llamada al método ValidateCard
    result = client.service.ValidateCard(
        loginId=loginId,
        password=password,
        transactionDate=transactionDate,
        cardId=cardId,
        referenceId=referenceId,
        referenceId2=referenceId2
    )


    # Convertir la respuesta a un diccionario Python
    response_dict = serialize_object(result)

    balance_amount = response_dict['BalanceAmount']

    # Imprimir el valor de BalanceAmount
    print("BalanceAmount:", balance_amount)


    # Imprimir la respuesta
    return str(balance_amount)



def hello(event, context):
    payload = json.loads(event['body'])
    cards = payload['card']
    points = []

    for card in cards:
        saldo = get_saldo(card)
        card_info = {"BalanceAmount":saldo, "cardNumber":card}
        point = card_info
        points.append(point)
    
    if event["path"] == "/hello":
        return {
            "statusCode": 200,
            "body": json.dumps(points),
        }
    else:
        return {
            "statusCode": 404,
            "body": "Not Found"
        }
