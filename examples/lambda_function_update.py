# -*- coding: utf-8 -*-
import mysql.connector
from mysql.connector import Error
import json

def lambda_handler(event, context):
    
    
    couponCode = event['pathParameters']['couponcode']
    countryId = event['queryStringParameters']['countryId']
    
    brandId = event['queryStringParameters']['brandId']
    body = json.loads(event['body'])
    #body = event['body']

    connection = mysql.connector.connect(    
        host="",
        database="",
        user="",
        passwd=""
    )
    
    db_response = update_coupon(connection, countryId, brandId, couponCode, body)
    return respond(200, db_response)


def update_coupon(connection, countryId, brandId, couponCode, body):    

    try:
        
        if connection.is_connected():
            cursor = connection.cursor()

            content = None            
            isValidPtoVta = validatePtoVta(connection, body['couponCodePOS'])
            # print("ptoventa valit: "+  isValidPtoVta)
            if not isValidPtoVta :
                return {
                        "type":"error",
                        "status":400,
                        "code":"400",
                        "help_url":"/coupon/validate",
                        "message":"No se encontro el código punto de venta"
                    }
            
            #Obtenemos branchId
            if 'branchId' not in body:
                branch_id = 0
            else: 
                branch_id = body['branchId']            
            #Obtenemos menusucursalId
            if 'branchMenuId' not in body:
                menu_sucursal_id = 0
            else:
                menu_sucursal_id = body['branchMenuId']                
            #Obtenemos promotionId
            if 'promotionId' not in body:
                promotion_id = 0
            else:
                promotion_id = body['promotionId']

            #Obtenemos aggregatorId
            if 'aggregatorId' not in body:
                aggregator_id = 0
            else:
                aggregator_id = body['aggregatorId']


            monto_min = 0
            monto_max =0
            porc_min =0
            porc_max =0
            ticket = 0
            item =0
            
            # Armamos el query update
            query = " UPDATE TAPROMOCION" \
                " SET" \
                
            # Valores condicionales SET

            if 'couponType' in body:
                if body['couponType'] == 1 or body['couponType'] == 3 or body['couponType'] == 5:
                    monto_min = body['minAmmount']
                    monto_max = body['maxAmmount']
                    porc_min =0
                    porc_max =0
                else:
                    monto_min = 0
                    monto_max =0
                    porc_min = body['minAmmount']
                    porc_max = body['maxAmmount']

                query += " FNMONTOMIN = '" + str(monto_min) + "'," \
                " FNMONTOMAX = '" + str(monto_max) + "'," \
                " FNPORCENTAJEMIN = '" + str(porc_min) + "'," \
                " FNPORCENTAJEMAX = '" + str(porc_max) + "'," \


            if 'couponMode' in body: 
                if body['couponMode'] == 1:
                    ticket = 1
                    item =0
                else:
                    ticket = 0
                    item = 1

                query += " FITICKET = '" + str(ticket) + "'," \
                " FIITEM = '" + str(item) + "'," \

            if 'value' in body: 
                query += " FNVALOR = '" + str(body['value']) + "'," \

            if 'couponType' in body: 
                query += " FITIPOPROMOCIONID = '" + str(body['couponType']) + "'," \

            if 'couponCodePOS' in body: 
                query += " FIPROMPTOVTAID = '" + str(body['couponCodePOS']) + "'," \

            if 'couponCoreCode' in body: 
                query += " FCCODIGOCUPON = '" + body['couponCoreCode'] + "'," \

            if 'statusId' in body: 
                query += " FIESTATUS = '" + str(body['statusId']) + "'," \

            if 'couponName' in body: 
                query += " FCNOMBRE = '" + body['couponName'] + "'," \

            if 'startDate' in body: 
                query +=  " FDFECHAINICIOOFERTA = '" + body['startDate'] + "'," \

            if 'endDate' in body: 
                query += " FDFECHAFINOFERTA = '" + body['endDate'] + "'," \

            if 'minTotalTicket' in body: 
                query += " FNTOTALTICKETMIN = '" + str(body['minTotalTicket']) + "'," \


            # SET por default, para que no truene el query, lo dejamos al final por que no tiene coma al final
            query += " FIPAISID = '" + str(countryId) + "'" \

            # WHERE
            query += " WHERE FCCODIGOCUPON = '" + str(couponCode) + "'" \
                " AND FIPAISID = " + str(countryId) +\
                " AND FIMARCAID = " +str(brandId)

            # AND'S condicionales

            if promotion_id > 0:
                query += " AND FCPROMOCIONID = " + str(promotion_id)
            if menu_sucursal_id > 0:
                query += " AND FISUCURSALMENUID = " + str(menu_sucursal_id)
            
            if menu_sucursal_id  == 0:
                query += " AND FISUCURSALMENUID IN (SELECT FISUCURSALMENUID " \
                    " FROM TASUCURSALMENU " \
                    " WHERE FIPAISID = " + str(countryId) +\
                    " AND FIMARCAID = " +str(brandId)
                if branch_id > 0:
                    query += " AND FISUCURSALID = " + str(branch_id)
                if aggregator_id > 0 :
                    query += " AND FIAGREGADORID = " + str(aggregator_id)                
                query += " ) "
            
            # print(query)
            cursor.execute(query)
            connection.commit()            
            if cursor.rowcount < 0 :
                content = {
                    "code": "404",
                    "content": [],
                    "helpUrl": "uri=/coupon/validate",
                    "message": "Cupón no registrado.",
                    "status": 404,
                    "type": "error"
                }
            elif cursor.rowcount == 0:
                content = {
                    "code": "200",
                    "content": [],
                    "helpUrl": "uri=/coupon/validate",
                    "message": "Cupón actualizado correctamente",
                    "status": 200,
                    "type": "success"
                }
            else :
                content = {
                    #"couponCode": str(couponCode),
                    #"statusId": str(body['statusId']),
                    "code": "200",
                    "content": [],
                    "helpUrl": "uri=/coupon/validate",
                    "message": "Cupón actualizado correctamente. Registros afectado/s: " + str(cursor.rowcount),
                    "status": 200,
                    "type": "success"
                }

    except Error as e:
        print("Error Conexion database", e)
        
        if "1062" in str(e):
            content = {
                "code": "400",
                "content": [],
                "helpUrl": "uri=/coupon/validate",
                "message": "Ya existe la llave",
                "status": 400,
                "type": "error"
            }
        else:
            content = {
                "code": "500",
                "content": [],
                "helpUrl": "uri=/coupon/validate" + str(e),
                "message": "Error en la conexión a la base de datos",
                "status": 500,
                "type": "error"
            }
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            
    return content

def validatePtoVta(connection, promPtoVtaId):
    cursor = connection.cursor()
    sql_select_query = " SELECT * FROM BD_DELIVERYCORE.TAPROMOCIONPUNTOVENTA  " \
                " WHERE FIPROMPTOVTAID =  " + str(promPtoVtaId) + "" \
                " AND FIESTATUS =1 " 
                
    cursor.execute(sql_select_query)
    record = cursor.fetchall()

    for row in record:
        print("FIPROMPTOVTAID = ", row[0] )
        return True
    return False
                

def respond(status, res):
    return {
        'statusCode':res["code"],
        'body': json.dumps(res),
        'headers': {
            'Content-Type': 'application/json','Access-Control-Allow-Origin':'*'
        }
    }