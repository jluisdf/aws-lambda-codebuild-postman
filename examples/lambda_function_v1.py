import mysql.connector
from mysql.connector import Error
import json


def lambda_handler(event, context):
    
    
    connection = mysql.connector.connect(    
        host="",
        database="",
        user="",
        passwd=""
    )

    db_response = get_data(connection)
    
    if 'status' in db_response:
        return respond(db_response['status'], db_response)
    else:
        return respond(200, db_response)

def get_data(connection):

    try:
        
        if connection.is_connected():

            cursor = connection.cursor()
            query = " SELECT FIESTATUSID+1, FCDESCRIPCION FROM TAESTATUSTICKET " 
            cursor.execute(query)
            row = cursor.fetchone()

            content =[]

            while row is not None:
                result = {
                    "id": str(row[0]),
                    "name": str(row[1])
                }
                content.append(result)                
                row = cursor.fetchone()

            if 'result' not in locals():
                content = {
                    "type":"error",
                    "status":404,
                    "code":"404",
                    "help_url":"/statusticket",
                    "message":"Not found"
                }

    except Error as e:
        print("Error Conexion database", e)
        content = {
            "type":"error",
            "status":400,
            "code":"400",
            "help_url":"/statusticket",
            "message":"Bad Request. Database error"
        }
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            
    return content



def respond(status, res):
    return {
        'statusCode':status,
        'body': json.dumps(res),
        'headers': {
            'Content-Type': 'application/json','Access-Control-Allow-Origin':'*'
        }
        
        
    }

