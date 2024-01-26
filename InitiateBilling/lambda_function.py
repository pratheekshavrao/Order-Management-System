import boto3
import logging
import json
import io

s3_client = boto3.client('s3')
rds_client = boto3.client('rds-data')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

#currency conversion dictionary
currency_conversion = {'USD': 1, 'CAD': 0.79, 'MXN': 0.05}

#database declarations
database_name = 'orders_management_aurora'
secret_store_arn = 'arn:aws:secretsmanager:us-east-1:471376517949:secret:rds-db-credentials/cluster-KBPJLBNDMCIOMAYSASMPW6IHSI/test_username/1706120307628-3FB3ed'
db_cluster_arn = 'arn:aws:rds:us-east-1:471376517949:cluster:orders-db-cluster'

def process_record( parsed_data):
    customer_id = parsed_data["customerId"]
    customer_name = parsed_data["customerName"]
    country = parsed_data["country"]
    product_line = parsed_data["productLine"]
    bill_date = parsed_data["billDate"]
    currency = parsed_data["currency"]
    bill_amount = parsed_data["billAmount"]
    
    # Print or use the values
    print("Customer ID:", customer_id)
    print("Customer Name:", customer_name)
    print("Country:", country)
    print("Product Line:", product_line)
    print("Bill Date:", bill_date)
    print("Currency:", currency)
    print("Bill Amount:", bill_amount)

    bill_amount = float(bill_amount)
 
#convert curreny to USD
    bill_amount_usd = 0
    rate = currency_conversion[currency]
    bill_amount_usd = bill_amount * rate
    print(f"currency: {currency}, bill amount: {bill_amount} , usd bill amount: {bill_amount_usd}")
    
#SQL statement for inserting into database
    sql_statement = ("INSERT IGNORE INTO billing_data "
                        "(customer_id, customer_name, country, product_line, bill_date, currency, bill_amount, bill_amount_usd) "
                        "VALUES (:customer_id, :customer_name, :country, :product_line, :bill_date, :currency, :bill_amount, :bill_amount_usd)"
    )
#SQL parameters for SQL statement
    sql_parameters = [
        {'name': 'customer_id', 'value': {'stringValue': customer_id}},
        {'name': 'customer_name', 'value': {'stringValue': customer_name}},
        {'name': 'country', 'value': {'stringValue': country}},
        {'name': 'product_line', 'value': {'stringValue': product_line}},
        {'name': 'bill_date', 'value': {'stringValue': bill_date}},
        {'name': 'currency', 'value': {'stringValue': currency}},
        {'name': 'bill_amount', 'value': {'doubleValue': bill_amount}},
        {'name': 'bill_amount_usd', 'value': {'doubleValue': bill_amount_usd}}
        ]
        
# Execute the SQL Statement and log the response
    response = execute_statement(sql_statement, sql_parameters)
    logger.info(f"SQL Execution response {response}")
            
def execute_statement(sql, sql_parameters):
    try:
        response = rds_client.execute_statement(
            secretArn = secret_store_arn,
            database = database_name,
            resourceArn = db_cluster_arn,
            sql = sql,
            parameters = sql_parameters
            )
        
    except Exception as e:
        logger.error(f"Could not connect to Aurora Serverless MySQL instance: {e}")
        return None
        
    return response
    
    
    
def lambda_handler(event, context):
    sns_message = json.loads(event['Records'][0]['Sns']['Message'])
    
    bucket_name = sns_message['Records'][0]['s3']['bucket']['name']
    object_name = sns_message['Records'][0]['s3']['object']['key']
    
    obj = s3_client.get_object(Bucket = bucket_name,Key = object_name)
    data = obj['Body'].read().decode('utf-8')
    json_data = json.loads(data)
    print( json_data)
    process_record( json_data)
    
    logger.info("Lambda has finished execution")