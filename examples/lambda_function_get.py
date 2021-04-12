import mysql.connector
from mysql.connector import Error
import json


def lambda_handler(event, context):
    
    couponCode = event['pathParameters']['couponcode']
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

    db_response = get_coupons(connection, countryId, brandId, couponCode, branchId, aggregatorId)
    return respond(200, db_response)
    
    """
    if 'status' in db_response:
        return respond(db_response['status'], db_response)
    else:
        return respond(200, db_response)
    """


def get_coupons(connection, countryId, brandId, couponCode, branchId, aggregatorId):    

    try:
        
        if connection.is_connected():

            cursor = connection.cursor()
            query = " SELECT "\
                " P.FNVALOR, "\
                " P.FITIPOPROMOCIONID, "\
                " TP.FCDESCRIPCION AS DESCTIPOPROMO, "\
                " CASE "\
                "     WHEN P.FITICKET = 1 "\
                "     AND P.FIITEM = 0 THEN 1 "\
                "     ELSE CASE "\
                "         WHEN P.FIITEM = 1 "\
                "         AND P.FITICKET = 0 THEN 2 "\
                "         ELSE 0 "\
                "     END "\
                " END AS COUPONMODE, "\
                " CASE "\
                "     WHEN P.FITICKET = 1 "\
                "     AND P.FIITEM = 0 THEN 'TICKET' "\
                "     ELSE CASE "\
                "         WHEN P.FIITEM = 1 "\
                "         AND P.FITICKET = 0 THEN 'ITEM' "\
                "         ELSE 'SIN DEFINICION' "\
                "     END "\
                " END AS DESCCOUPONMODE, "\
                " P.FIPROMPTOVTAID, "\
                " P.FCNOMBRE, "\
                " M.FISUCURSALID, "\
                " S.FCNOMBRE AS NOMBRESUCURSAL, "\
                " A.FIAGREGADORID, "\
                " A.FCNOMBRE, "\
                " P.FIESTATUS, "\
                " CASE "\
                "     WHEN P.FIESTATUS = 1 THEN 'ACTIVO' "\
                "     ELSE "\
                "       'INACTIVO' "\
                "     END AS DESCESTATUS, "\
                " P.FCCODIGOCUPON, "\
                " CASE "\
                "     WHEN P.FITIPOPROMOCIONID = 1 THEN P.FNMONTOMIN "\
                "     ELSE CASE "\
                "         WHEN P.FITIPOPROMOCIONID = 2 THEN P.FNPORCENTAJEMIN "\
                "     END "\
                " END AS MIN, "\
                " CASE "\
                "     WHEN P.FITIPOPROMOCIONID = 1 THEN P.FNMONTOMAX "\
                "     ELSE CASE "\
                "         WHEN P.FITIPOPROMOCIONID = 2 THEN P.FNPORCENTAJEMAX "\
                "     END "\
                " END AS MAX,     "\
                " P.FDFECHAINICIOOFERTA, "\
                " P.FDFECHAFINOFERTA,"\
                " P.FNTOTALTICKETMIN, "\
                " P.FISUCURSALMENUID,"\
                " P.FCPROMOCIONID, P.FIPAISID, P.FIMARCAID"\
                " FROM TAPROMOCION P LEFT JOIN TASUCURSALMENU M " \
                "  ON P.FISUCURSALMENUID = M.FISUCURSALMENUID " \
                "  LEFT JOIN TAAGREGADOR A " \
                "  ON M.FIAGREGADORID = A.FIAGREGADORID " \
                "  LEFT JOIN TATIPOPROMOCION TP "\
                "  ON  P.FITIPOPROMOCIONID = TP.FITIPOPROMOCIONID "\
                "  LEFT JOIN TASUCURSAL S "\
                "  ON  M.FISUCURSALID = S.FISUCURSALID "\
                " WHERE P.FCCODIGOCUPON = '" + str(couponCode) + "' " \
                " AND M.FIPAISID = " + str(countryId) +\
                " AND M.FIMARCAID =  " + str(brandId) +\
                " AND M.FIPAISID = S.FIPAISID " +\
                " AND M.FIMARCAID = S.FIMARCAID "
                        
            if branchId is not None:
                query +=" AND M.FISUCURSALID = " + str(branchId)
            if aggregatorId is not None:
                query +=" AND M.FIAGREGADORID = " + str(aggregatorId)                

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
                    "branchId": str(row[7]),
                    "branchDesc": str(row[8]),
                    "aggregatorId": str(row[9]),
                    "aggregatorDesc": str(row[10]),
                    "statusId": str(row[11]),
                    "statusDesc": str(row[12]),
                    "couponCoreCode": str(row[13]),     
                    "minAmmount": str(row[14]),
                    "maxAmmount": str(row[15]),                    
                    "startDate": str(row[16]),
                    "endDate": str(row[17]),
                    "minTotalTicket": str(row[18]),
                    "branchMenuId": str(row[19]),
                    "promotionId": str(row[20]),
                    "countryId": str(row[21]),
                    "brandId": str(row[22])
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
