import json
import concurrent.futures
from zeep import Client
import datetime
test = True
wsdl_url =  'http://aptos-sc-dev.corpo.gandhi.com.mx:4525/?singleWsdl' if test else 'http://aptos-sc-prd.corpo.gandhi.com.mx:4525/?singleWsdl'

def card_info(card):
    client = Client(wsdl_url)
    data_request = {
            "AccountNumber": card,
            "FirstRecordNumber": "0",
            "RecordsPerQuery": "1",
    }
    try:
        response = client.service.SubmitVoucherSearchRequest(data_request, 10)
        cardObj = {
                "cardNumber":card,
                "BalanceAmount":float(response.Records[0]["Balance"]),
                "CurrencyCode": response.Records[0]["CurrencyCode"]
        }
        return cardObj
    except:
        cardObj = {
                "cardNumber":card,
                "status":"Not Found"
        }

def balance(event, context):
    payload = json.loads(event['body'])
    cards = payload['card']
    card_balance_arr = []

    def get_card_info(card):
        return card_info(card)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(get_card_info, cards))

    card_balance_arr = [result for result in results if result is not None]

    response = {
        "Status": 200,
        "Message":"Correct",
        "body": json.dumps(card_balance_arr)
    }
    return response