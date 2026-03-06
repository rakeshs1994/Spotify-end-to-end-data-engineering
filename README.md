# Spotify End-To-End Data Engineering Project

### Introduction:

In this project, we will build an ETL (Extract, Transform, Load) pipeline using the Spotify API on AWS. The pipeline will retrive data from the Spotify API, transformed it to desired format, and load it into AWS data store. 

### Architecture:

<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/f0c0fff1-e292-4fa6-b316-75302f40e7eb" />





<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/3504a53d-ae2d-452f-90f6-ed2fa0a762cc" />




<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/cfcba283-f57f-4f3a-b7a8-9a3cd777a7a0" />






### About Dataset/API
This API containes information about music artist, album and songs - https://developer.spotify.com/documentation/web-api

### Services used:

1. **S3 (Simple storage service) :** is a cloud-based object storage service provided by AWS (Amazon Web Services). It allows you to store and retrieve any amount of data, at any time, from anywhere on the web.

2. **AWS Lambda:** AWS Lambda is a serverless compute service from Amazon Web Services. That means we can run our code without managing servers. You just upload our code, and AWS takes care of running it and scaling it..

3. **Cloud Watch:** Amazon CloudWatch is a monitoring and observability service from AWS. It collects logs, metrics, and events from your AWS resources (like EC2, Lambda, RDS, S3, etc.) and lets you track performance, set alarms, and get alerts.

4. **Glue Crawler:** An AWS Glue Crawler is a tool in AWS Glue that scans your data sources (like S3, RDS, Redshift, DynamoDB, etc.), figures out the schema (columns, data types, partitions, formats), and then creates or updates metadata tables in the AWS Glue Data Catalog.

5. **Data Catalog:** The AWS Glue Data Catalog is a central metadata repository (like a database of “data about your data”) in AWS. It stores information (schemas, table definitions, partitions, locations, formats) about your data stored in S3, RDS, Redshift, DynamoDB, etc.

6. **Amazon Athena:**  Amazon Athena  is an interactive query service that makes it easy to analyse data in Amazon S3 using standard SQL. You can use Athena to analyze data in your  Glue Data Catalog or in other s3 buckets.

7. **Snowflake:** Snowflake is a cloud-based Data Warehouse Platform  designed for storing, processing, and analyzing large amounts of structured and semi-structured data.

### Project Execution Flow:
Extract Data from API -> Lamda Trigger (every 1 hour) -> Run Extract code -> Store Raw Data -> Trigger Transform Function -> Transform Data and Load It ->
Query using Athena/Query from Snowflake.
