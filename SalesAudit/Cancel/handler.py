import json
import concurrent.futures
from zeep import Client
import datetime
test = True
wsdl_url =  'http://aptos-sc-dev.corpo.gandhi.com.mx:4525/?singleWsdl' if test else 'http://aptos-sc-prd.corpo.gandhi.com.mx:4525/?singleWsdl'

def cancel(event,context):

    fechaHoraActual = datetime.datetime.now()
    fechaHoraFormateada = fechaHoraActual.strftime("%Y-%m-%dT%H:%M:%S")
    payload = json.loads(event['body'])
    client = Client(wsdl_url)
    amount = f'{payload["amount"]}'
    dataRequest = {
            "AccountNumber": payload['card'],
            "Amount": float(amount) ,
            "InputType":1,
            "CurrencyCode":"MXN",
            "CompanyNumber":1,
            "RegisterNumber":1,
            "SequenceNumber":payload["id"],
            "StoreNumber":11,
            "TenderType":4,
            "Action":4,
            "TransactionNumber":0
    }

    response = client.service.SubmitValueCardRequest(dataRequest,10)

    dataObj = {
        "Balance":response["Balance"],
        "id":payload["id"],
        "message":response["Message"],
        "ResultId":response["AuthorizationNumber"]
    }
    return {
        "message":"success",
        "body":dataObj,
        "status":200
    }