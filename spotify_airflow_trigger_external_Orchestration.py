from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.amazon.aws.operators.lambda_function import LambdaInvokeFunctionOperator
# from airflow.providers.amazon.aws.operators.glue import GlueJobOperator
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor


default_args = {
    "owner": "rakesh",
    "depends_on_past":False,
    "start_date":datetime(2024,3,5)
}


dag = DAG (
    dag_id = "spotify_trigger_external",
    default_args = default_args,
    description = "DAG to trigger Lambda Function and Check s3 Upload",
    schedule = timedelta(days=1),
    catchup = False,
)


trigger_extract_lambda = LambdaInvokeFunctionOperator(
    task_id = "trigger_extract_lambda",
    function_name = "spotify_api_data_extract",
    aws_conn_id = "aws_conn_s3",
    region_name = "us-east-1",
    dag = dag,

)

check_s3_upload = S3KeySensor(
    task_id = "check_s3_upload",
    bucket_key = "s3://spotify-etl-project-rakeshs/raw_data/to_processed/*",
    wildcard_match = True,
    aws_conn_id = "aws_conn_s3",
    timeout = 60 * 60,
    poke_interval = 60,
    dag = dag,
)


trigger_transform_lambda = LambdaInvokeFunctionOperator(
    task_id = "trigger_transform_lambda",
    function_name = "spotify_transformation_load_function",
    aws_conn_id = "aws_conn_s3",
    region_name = "us-east-1",
    dag = dag,

)

 # glue job trigger
#trigger_glue_job = GlueJobOperator(
#    task_id = "trigger_glue_job",
#    job_name = "***",
#    script_location = "",
#   aws_conn_id = "aws_conn_s3",
#  region_name = "us-east-1",
#  iam_role_name = "",
# s3_bucket = "", temp parth
#    dag = dag,
#)

trigger_extract_lambda >> check_s3_upload >> trigger_transform_lambda