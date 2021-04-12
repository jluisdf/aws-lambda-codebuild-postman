import mysql.connector
from mysql.connector import Error
import json


def lambda_handler(event, context):
    
    #couponCode = event['pathParameters']['couponcode']
    countryId = event['queryStringParameters']['countryId']
    brandId = event['queryStringParameters']['brandId']
    
    if 'branchId' in event['queryStringParameters']:
        branchId = event['queryStringParameters']['branchId']
    else:
        branchId = None
    
    if 'aggregatorId' in event['queryStringParameters']:
        aggregatorId = event['queryStringParameters']['aggregatorId']
    else:
        aggregatorId = None
    
    connection = mysql.connector.connect(    
        host="",
        database="",
        user="",
        passwd=""
    )

    db_response = get_coupons(connection, countryId, brandId, branchId, aggregatorId)
    # return respond(200, db_response)
    print(respond(200, db_response))
    """
    if 'status' in db_response:
        return respond(db_response['status'], db_response)
    else:
        return respond(200, db_response)
    """

def get_coupons(connection, countryId, brandId, branchId, aggregatorId):    

    try:
        
        if connection.is_connected():

            cursor = connection.cursor()
            query = " SELECT " \
                " P.FNVALOR, " \
                " P.FITIPOPROMOCIONID, " \
                " TP.FCDESCRIPCION AS DESCTIPOPROMO,"\
                " CASE " \
                "     WHEN P.FITICKET = 1 " \
                "     AND P.FIITEM = 0 THEN 1 " \
                "     ELSE CASE " \
                "         WHEN P.FIITEM = 1 " \
                "         AND P.FITICKET = 0 THEN 2 " \
                "         ELSE 0 " \
                "     END " \
                " END AS COUPONMODE, " \
                " CASE "\
                "     WHEN P.FITICKET = 1 "\
                "     AND P.FIITEM = 0 THEN 'TICKET'"\
                "     ELSE CASE "\
                "         WHEN P.FIITEM = 1 "\
                "         AND P.FITICKET = 0 THEN 'ITEM' "\
                "         ELSE 'SIN DEFINICION' "\
                "     END "\
                " END AS DESCCOUPONMODE,"\
                " P.FIPROMPTOVTAID, " \
                " P.FCNOMBRE,     " \
                " P.FCCODIGOCUPON,     " \
                " SUM(P.FIESTATUS) ACTIVO, "\
                " COUNT(P.FCCODIGOCUPON) AS QUANTITY, "\
                " A.FCNOMBRE NOMBREAGREGADOR "\
                " FROM TAPROMOCION P LEFT JOIN TASUCURSALMENU M" \
                "  ON P.FISUCURSALMENUID = M.FISUCURSALMENUID" \
                "  LEFT JOIN TAAGREGADOR A" \
                "  ON M.FIAGREGADORID = A.FIAGREGADORID" \
                "  LEFT JOIN TATIPOPROMOCION TP "\
                "  ON  P.FITIPOPROMOCIONID = TP.FITIPOPROMOCIONID "\
                " WHERE M.FIPAISID = " + str(countryId) +\
                " AND M.FIMARCAID =  " + str(brandId)
                        
            if branchId is not None:
                query +=" AND M.FISUCURSALID = " + str(branchId)
            if aggregatorId is not None:
                query +=" AND M.FIAGREGADORID = " + str(aggregatorId)

            query +=" GROUP BY P.FCCODIGOCUPON, P.FITIPOPROMOCIONID, P.FIPROMPTOVTAID "
            
            # " CASE WHEN SUM(P.FIESTATUS) > 0 THEN 1 ELSE 0 END AS ACTIVO, " \ # Original ACTIVO
            print(query)
            cursor.execute(query)
            row = cursor.fetchone()

            results = []

            while row is not None:
                result = {
                    "value": str(row[0]),
                    "couponType": str(row[1]),
                    "couponTypeDesc": str(row[2]),
                    "couponMode": str(row[3]),
                    "couponModeDesc": str(row[4]),
                    "couponCodePOS": str(row[5]),
                    "couponName": str(row[6]),
                    "couponCoreCode": str(row[7]),
                    "statusId": str(row[8]),
                    "quantity": str(row[9]),
                    "aggregatorName": str(row[10])
                }
                results.append(result)                
                row = cursor.fetchone()
                content = {
                    "code": "200005",
                    "content": results,
                    "exception": "",
                    "help_url": "uri=/coupons",
                    "message": "Registros encontrados",
                    "status": 200,
                    "type": "success"
                }

            if 'result' not in locals():
                content = {
                    "code": "200005",
                    "content": [],
                    "exception": "Excepción de resultados",
                    "help_url": "uri=/coupons",
                    "message": "No se encontraron cupones con los criterios proporcionados",
                    "status": 204,
                    "type": "warning"
                }

    except Error as e:
        print("Error Conexion database", e)
        content = {
            "code": "400003",
            "content": [],
            "exception": "Error conexión base de datos",
            "help_url": "uri=/coupons",
            "message": "Error en la conexión a la base de datos",
            "status": 400,
            "type": "error"
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

event = {
    'queryStringParameters': {
        'countryId': 1,
        'brandId': 10
    }
}

lambda_handler(event, '')