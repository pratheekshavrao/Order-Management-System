
# Order Management System

The Order Management System is a robust and scalable solution designed to handle customer orders seamlessly.This system accepts customer orders from a Front End system through an AWS API Gateway which acts as a secure point of entry.Upon receiving an order, the system generates a file and stores it in an S3 bucket. This file serves as a central repository for order-related information.The S3 file creation event triggers an SNS topic whcih has Lambda functions as suscribers.The SNS topic allows for decoupling between S3 and the subsequent Lambda functions.One of the Lambda functions accepts the order information as input and generates billing information in USD and updates it into a billing database. The other Lambda function extracts email information from databse and handles the Order Confirmation communication to customer.

