import mysql.connector
from mysql.connector import Error
import json
import os


def lambda_handler(event, context):

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

    db_response = insert_db(connection, countryId, brandId, body)

    return respond(db_response['status'], db_response)

def insert_db(connection, countryId, brandId, body):

    try:

        if connection.is_connected():
            cursor = connection.cursor()

            # VALIDAMOS QUE EXISTA MENU EN LA SUCURSAL A INSERTAR
            query_menu = " SELECT CASE WHEN COUNT(1) > 0 THEN FISUCURSALMENUID ELSE 0 END AS MENU "\
                " FROM TASUCURSALMENU " \
                " WHERE FIPAISID = " + str(countryId) +\
                " AND FIMARCAID = " + str(brandId) + \
                " AND FISUCURSALID = " + str(body['branchId']) +\
                " AND FIAGREGADORID = " + str(body['aggregatorId'])

            cursor.execute(query_menu)
            result = cursor.fetchone()
            menu_id = result[0]

            if menu_id == 0:
                return  {
                    "type": "error",
                    "status": 203,
                    "code": "203",
                    "content": [],
                    "exception": "",
                    "help_url": "uri=/admin/coupons",
                    "message": "No existe menú en la sucursal " + str(body['branchId'])
                }

            # VERIFICAMOS SI LA PROMOCION ESTA REGISTRADA
            querycount = " SELECT COUNT(1) "\
                " FROM TAPROMOCION "\
                " WHERE FISUCURSALMENUID = " + str(menu_id) +\
                " AND FIPAISID = " + str(countryId) +\
                " AND FIMARCAID = " + str(brandId) +\
                " AND FCCODIGOCUPON = '" + str(body['couponCoreCode']) + "' "

            cursor.execute(querycount)
            result = cursor.fetchone()
            promocion = result[0]

            if promocion > 0:
                content = {
                    "type": "error",
                    "status": 203,
                    "code": "203",
                    "content": [],
                    "exception": "",
                    "help_url": "uri=/admin/coupons",
                    "message": "La promocion ya existe en la sucursal " + str(body['branchId'])
                }
                return content


            # VALIDAMOS SI LA PROMOCION ESTA REGISTRADA EN PROMOCIONPUNTOVENTA
            querycount = " SELECT COUNT(1) "\
                " FROM TAPROMOCIONPUNTOVENTA "\
                " WHERE FIPAISID = " + str(countryId) +\
                " AND FIMARCAID = " + str(brandId) +\
                " AND FIPROMPTOVTAID = " + str(body['couponCodePOS'])

            cursor.execute(querycount)
            result = cursor.fetchone()
            promocion_venta = result[0]

            # SI NO EXISTE EN PROMOCIONPUNTOVENTA INSERTAMOS
            if promocion_venta == 0:
                insert_venta = "INSERT INTO TAPROMOCIONPUNTOVENTA " \
                    " (FIPAISID,FIMARCAID,FIPROMPTOVTAID,FCDESCRIPCION,FDFECHAALTA,FIESTATUS) "\
                    " VALUES (%s,%s,%s,%s,now(),1)"

                val = (countryId, brandId, body['couponCodePOS'], body['couponName'])
                cursor.execute(insert_venta, val)                

                insert_ok = cursor.rowcount

                if insert_ok <= 0:
                    return {                
                        "type": "error",
                        "status": 400,
                        "code": "400",
                        "content": [],
                        "exception": "",
                        "help_url": "uri=/admin/coupons",
                        "message": "Bad Request. sentence can't insert in table promcionpuntoventa."
                    }

            # INSERTAMOS PROMOCION
            # generando id para promocion
            promocion_id = str(body['couponCoreCode'])
            max_cupon = 200
            mode_ticket = (1 if body['couponMode'] == 1 else 0)
            mode_item = (1 if body['couponMode'] == 2 else 0)

            insert_promocion = "INSERT INTO TAPROMOCION "\
                " (FISUCURSALMENUID,FCPROMOCIONID,FIPAISID, FIMARCAID, "\
                " FIPROMPTOVTAID,FITIPOPROMOCIONID,FCNOMBRE,FNVALOR, " \
                " FNMONTOMIN,FNMONTOMAX,FNPORCENTAJEMIN,FNPORCENTAJEMAX, "\
                " FNTOTALTICKETMIN,FITICKET,FIITEM,FIMAXCUPON,FCCODIGOCUPON, "\
                " FDFECHAALTA, FDFECHAINICIOOFERTA, " \
                " FDFECHAFINOFERTA,FIESTATUS, FIPOSICION) VALUES " \
                " (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now(),%s,%s,1, 0)"

            if body['couponType'] == 1:
                value = (menu_id, promocion_id, countryId, brandId,
                            body['couponCodePOS'], body['couponType'], body['couponName'], body['value'],
                            body['minAmmount'], body['maxAmmount'], 0, 0,
                            body['minTotalTicket'], mode_ticket, mode_item, max_cupon, body['couponCoreCode'],
                            body['startDate'], body['endDate']
                )
            else:
                value = (menu_id, promocion_id, countryId, brandId,
                            body['couponCodePOS'], body['couponType'], body['couponName'], body['value'],
                            0, 0, body['minAmmount'], body['maxAmmount'],
                            body['minTotalTicket'], mode_ticket, mode_item, max_cupon, body['couponCoreCode'],
                            body['startDate'], body['endDate']
                )

            cursor.execute(insert_promocion, value)
            connection.commit()

            cursor.rowcount

            if cursor.rowcount > 0:
                return  {
                    "status" :200,
                    "code": "200",
                    "content": [],
                    "exception": "",
                    "help_url": "uri=/admin/coupons",
                    "couponCode": body['couponCoreCode'],
                    "statusId": 1,
                    "message": "Cupón registrado correctamente sucursal " + str(body['branchId'])
                }                    
            else:
                return  {
                    "type": "error",
                    "status": 400,
                    "code": "400",
                    "content": [],
                    "exception": "",
                    "help_url": "uri=/admin/coupons",
                    "message": "Bad Request. sentence can't insert in table promocion."
                }
        

    except Error as e:
        print("Error Conexion database", e)
        content = {
            "type": "error",
            "status": 400,
            "code": "400",
            "content": [],
            "exception": "",
            "help_url": "uri/admin/coupons",
            "message": "Bad Request. Database error. Database connection error."
        }
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
    return content

def respond(status, res):
    return {
        'statusCode': status,
        'body': json.dumps(res),
        'headers': {
            'Content-Type': 'application/json','Access-Control-Allow-Origin':'*'
        }
    }


