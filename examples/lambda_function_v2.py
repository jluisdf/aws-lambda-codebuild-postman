import json 
import datetime

def lambda_handler(event, context):
    # TODO implement 
    print(event)
    data = {
        'output': 'Hello from '+ event['Country'],
        'timestamp': datetime.datetime.utcnow().isoformat()
    }
    return {'statusCode': 200,
            'body': json.dumps(data),
            'headers': {'Content-Type': 'application/json'}}

def sum(a, b):
    for n in (a, b):
        if not isinstance(n, int) and not isinstance(n, float):
            raise TypeError
    return a + b

def doblar(a): return a*2
def sumar(a,b): return a+b  
def es_par(a): return 1 if a%2 == 0 else 0

def respond(status, res):
    return {
        'statusCode':status,
        'body': json.dumps(res),
        'headers': {
            'Content-Type': 'application/json','Access-Control-Allow-Origin':'*'
        }
        
        
    }


content = {
    "type": "warning",
    "status": 200,
    "code": "200",
    "message":"Esta es una prueba"
}

#print(respond(200, content))
print(sum(2, 3))