import boto3
import time


rds = boto3.client('rds')

# Create user defined variables
username = 'test_username'
password = 'efvefvnl'
db_cluster_id = 'orders-db-cluster'
db_subnet_group = 'orders_db_subnet_gp'

# create a DB Cluster

try:
    get_response = rds.describe_db_clusters(DBClusterIdentifier = db_cluster_id)
    print(f"DB Cluster named '{db_cluster_id}' already exists. Skipping create")

except rds.exceptions.DBClusterNotFoundFault:
    print("DB Cluster Not Found. Creating Now")
    
    create_response = rds.create_db_cluster(
        Engine = 'aurora-mysql',
        EngineVersion = '5.7.mysql_aurora.2.08.3',
        DBClusterIdentifier = db_cluster_id,
        MasterUsername = username,
        MasterUserPassword = password,
        DatabaseName = 'orders_management_aurora',
        DBSubnetGroupName = db_subnet_group,
        EngineMode = 'serverless',
        EnableHttpEndpoint = True,
        ScalingConfiguration = {
            'MinCapacity': 1, # Minimum ACU
            'MaxCapacity': 8, # Maximum ACU
            'AutoPause': True,
            'SecondsUntilAutoPause': 300 # Pause After 5 Minutes of activity
        }
    )
    
    print(f"DB Cluster named '{db_cluster_id}' has been created")
    
    # Wait for the DB Cluster to be available
    while True:
        get_response = rds.describe_db_clusters(DBClusterIdentifier = db_cluster_id)
        status = get_response['DBClusters'][0]['Status']
        
        if status == 'available':
            break
        
        print("Waiting for the DB Cluster to be available...")
        time.sleep(40)
    