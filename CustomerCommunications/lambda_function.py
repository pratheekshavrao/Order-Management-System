import boto3
import logging
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_client = boto3.client('s3')
ses = boto3.client('ses')
rds_client = boto3.client('rds-data')


#database declarations
database_name = 'orders_management_aurora'
secret_store_arn = 'arn:aws:secretsmanager:us-east-1:471376517949:secret:rds-db-credentials/cluster-KBPJLBNDMCIOMAYSASMPW6IHSI/test_username/1706120307628-3FB3ed'
db_cluster_arn = 'arn:aws:rds:us-east-1:471376517949:cluster:orders-db-cluster'


#SES declarations
source_email = "pratheeksha.rao89@gmail.com"
charset = 'utf-8'

def send_email(dest_email):
    try:
        response = ses.send_email(
            Source = source_email,
            Destination = {
                'ToAddresses': [
                    dest_email,
                ]
            },
            Message={
                'Subject': {
                    'Data': 'Order Confirmation',
                    'Charset': charset
                },
                'Body': {
                    'Text': {
                        'Data': 'Your order is has been received and is now being processed. Please feel free to reach out to our customer support team for any queries.',
                        'Charset': charset
                    }
                }
            }
        )
    
        logger.info(f"ses response {response}")
    
    except Exception as e:
        logger.error(f"Could not send email: {e}")
        return None
            
def execute_statement(customer_id):
    
    #SQL statement for inserting into database
    sql_statement = f"SELECT cust_email_id from customer_contact_info where cust_id = '{customer_id}'" 
    
    try:
        response = rds_client.execute_statement(
            secretArn = secret_store_arn,
            database = database_name,
            resourceArn = db_cluster_arn,
            sql = sql_statement
            )
        dest_email = response['records'][0][0]['stringValue']
        print(dest_email)
        
        send_email(dest_email)
        return response
        
    except Exception as e:
        logger.error(f"Could not connect to Aurora Serverless MySQL instance: {e}")
        return None
 

def lambda_handler(event, context):
    sns_message = json.loads(event['Records'][0]['Sns']['Message'])
    bucket_name = sns_message['Records'][0]['s3']['bucket']['name']
    object_name = sns_message['Records'][0]['s3']['object']['key']
    
    obj = s3_client.get_object(Bucket = bucket_name,Key = object_name)
    data = obj['Body'].read().decode('utf-8')
    json_data = json.loads(data)
    customer_id = json_data["customerId"]
    print(f"customer_id = {customer_id}")
   
    
    # Execute the SQL Statement and log the response
    response = execute_statement(customer_id)
    
    logger.info(f"SQL Execution response {response}")
    
    
    