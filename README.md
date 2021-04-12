# https://docs.aws.amazon.com/cli/latest/reference/lambda/

# Crear lambda
aws lambda create-function --function-name mylambdafunctioncli --zip-file fileb://app.zip --region us-east-1 --role arn:aws:iam::470036567262:role/AWSLambdaFullAccess --runtime python3.7 --handler lambda_function.lambda_handler


# Actualizar
aws lambda update-function-code --function-name mylambdafunctioncli --zip-file fileb://app.zip --region us-east-1 
--handler app/index.handler


# Informacion de la lambda
aws lambda get-function --function-name mylambdafunctioncli --region us-east-1

# Ejecutar funcion
aws lambda invoke --function-name mylambdafunctioncli --region us-east-1 response.json