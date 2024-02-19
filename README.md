
# Order Management System

The Order Management System is a robust and scalable solution designed to handle customer orders seamlessly.This system accepts customer orders from a Front End system through an AWS API Gateway which acts as a secure point of entry.Upon receiving an order, the system generates a file and stores it in an S3 bucket. This file serves as a central repository for order-related information.The S3 file creation event triggers an SNS topic whcih has Lambda functions as suscribers.The SNS topic allows for decoupling between S3 and the subsequent Lambda functions.One of the Lambda functions accepts the order information as input and generates billing information in USD and updates it into a billing database. The other Lambda function extracts email information from databse and handles the Order Confirmation communication to customer.

![alt text](https://github.com/pratheekshavrao/Order-Management-System/blob/main/Images/Order_management_system.jpeg)

## Steps for execution

1.	Sign into AWS console. Navigate to API Gateway and create an Order resource with Object as its Child resource and PUT as method. Modify the URL parameters in Integration Request settings  as shown in         screenshot below.
  	
    ![alt text](https://github.com/pratheekshavrao/Order-Management-System/blob/main/Images/OrderManagementAPICreated.jpg)
  	
3.	Next create a S3 bucket from S3 console.
   
    ![alt text](https://github.com/pratheekshavrao/Order-Management-System/blob/main/Images/OrderManagementS3Bucket.jpg)
  	
5.	Provide permissions to the API gateway to access S3 to upload objects into it following the Least Privilege Principle.
   
    ![alt text](https://github.com/pratheekshavrao/Order-Management-System/blob/main/Images/APIGatewayS3AccessRole.jpg)
  	
7.	Navigate to SNS console and create a new SNS topic. Create an event  notification from S3 console to trigger the designated SNS topic for PutObject event. Also modify SNS access policy to allow the S3 bucket 
    to trigger this SNS topic.

    ![alt text](https://github.com/pratheekshavrao/Order-Management-System/blob/main/Images/OrderCapturedNotificationSNS.jpg)


    ![alt text](https://github.com/pratheekshavrao/Order-Management-System/blob/main/Images/S3EventNotificationSNS.jpg)


    ![alt text](https://github.com/pratheekshavrao/Order-Management-System/blob/main/Images/S3AllowTriggerSNSPolicy.jpg)
  	
9.	Create 2 Lambda functions  - Initiate  Billing and Customer Communications from Lambda console. Then set these two Lambda functions as subscriptions to the SNS topic created.

  	![alt text](https://github.com/pratheekshavrao/Order-Management-System/blob/main/Images/InitiateBillingLambdaCreation.jpg)

  	![alt text](https://github.com/pratheekshavrao/Order-Management-System/blob/main/Images/CustomerComminicationsLambdaCreation.jpg)
	
13.	The Initiate Billing Lambda function processes the order data from the event, converts the Bill Amount to USD for consistency, and updates the billing data into the Billing Data table.
    
15.	The Customer Communications Lambda function extracts customer email information from Customer Contact Info table and sends an order confirmation email to customer using SES.
    
16.	Create an Aurora serverless database cluster using the below Python code. Then from the Query Editor create two tables – Billing Data and Customer Contact Info. Populate the Customer Contact Info table with test data.
    
	![alt text](https://github.com/pratheekshavrao/Order-Management-System/blob/main/Images/DatabaseCreated.jpg)

	![alt text](https://github.com/pratheekshavrao/Order-Management-System/blob/main/Images/BillingDataTableCreated.jpg)

   	![alt text](https://github.com/pratheekshavrao/Order-Management-System/blob/main/Images/CustomerContactInfoTableCreated.jpg)

       ![alt text](https://github.com/pratheekshavrao/Order-Management-System/blob/main/Images/CustomerContactInfoTableContents.jpg)

17.	Navigate to SES console and verify the identities of the sender and receiver email addresses.

       ![alt text](https://github.com/pratheekshavrao/Order-Management-System/blob/main/Images/SESVerifiedIdentities.jpg)    

19.	For local testing of Lambda functions, download the functions to Cloud9 environment, create event.json and template .yaml files. Use below code from terminal to test the functions.

       ![alt text](https://github.com/pratheekshavrao/Order-Management-System/blob/main/Images/LocalInvokeCode.jpeg)
        
20.	 Once local testing is successful, upload the Lambda functions into AWS console. For Initiate Billing function add permissions to access S3, RDS Database to the execution role. Similarly for Customer Communications function, add permissions to access S3,RDS database and also SES.
    
22.	Use the Postman tool to PUT a test record to the API Gateway.

	![alt text](https://github.com/pratheekshavrao/Order-Management-System/blob/main/Images/PutRecordUsingPostman.jpg)


## Results and Observations

•	Upon the customer order being submitted through API Gateway, a file containing the customer order details is generated in the S3 bucket.

![alt text](https://github.com/pratheekshavrao/Order-Management-System/blob/main/Images/ObjectCreatedS3.jpg)
	
![alt text](https://github.com/pratheekshavrao/Order-Management-System/blob/main/Images/ObjectContents.jpg)

•	Initiate Billing function updates the Billing Data table with the order details.

![alt text](https://github.com/pratheekshavrao/Order-Management-System/blob/main/Images/RecordsInsertedBillingDataTable.jpg)

•	Customer Communication function sends an email to customer email ID using SES.

![alt text](https://github.com/pratheekshavrao/Order-Management-System/blob/main/Images/EmailReceived.jpg)


