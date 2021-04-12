import json

def lambda_handler(event, context):

    # print(event)
    result = {'statusCode': 200,
            'body': {'name': 'JLuis'},
            'headers': {'Content-Type': 'application/json'}}

    return respond(200, result)
    # print(respond(200, result))

def respond(status, res):
    return {
        'statusCode': status,
        'body': json.dumps(res),
        'headers': {
            'Content-Type': 'application/json','Access-Control-Allow-Origin':'*'
        }
    }


# lambda_handler('', '')