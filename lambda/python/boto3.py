import boto3
import os

def lambda_handler(event, context):
	try:
		for record in event['Records']:
			if record['eventName'] == 'INSERT':
				 handle_insert(record)
			elif record['eventName'] == 'MODIFY':
				print("Lambda did not triggered as we dont need it to be for dynamoDB modify events.")
			elif record['eventName'] == 'REMOVE':
				print("Lambda did not triggered as we dont need it to be for dynamoDB remove events.")
		return "Success!"
	except Exception as e:
		print(e)
		return "Error"

def handle_insert(record):
	print("Handling INSERT Event")

	newImage = record['dynamodb']['NewImage']
	deploy_version = newImage['version']['N']
	print("Version = " + deploy_version)

	accesskey = os.environ['accesskey']
	secretkey = os.environ['secretkey']
	region = os.environ['region']

	ecs_client = boto3.client(
	'ecs',
	aws_access_key_id=accesskey,
	aws_secret_access_key=secretkey,
	region_name=region
	)
	cluster_name = "demo-cluster"														# change cluster name
	service_name = "demo-service"														#chnage service name
	task_name = "sample-python-app-td:"+ deploy_version									#chnage task definition name
	

	ecs_client.update_service(
		cluster=cluster_name,
		service=service_name,
		taskDefinition=task_name,
		desiredCount=4,
		deploymentConfiguration={
			'maximumPercent': 100,
			'minimumHealthyPercent': 50
		}
	)
