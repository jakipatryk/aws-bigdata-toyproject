## Project set up instruction
1. Create a S3 bucket that will be used to store all static files (jars, lambdas, etc.).
2. Let `StaticFilesBucketName` represent name of the bucket you've just created.
3. Clone the repo and go to the repo folder.
4. Choose a available name for the S3 bucket that will be used to store all the other stuff (views and reviews logs, query results, etc.).
5. Let `S3BucketName` represent that name.
6. `cd suspicious-ips-finder`
7. Adjust settings in `src/main/resources/application.properties` (change `<bucket-name>` to the value of `S3BucketName`).
8. Run `sbt package`.
9. Run `cp target/scala-2.11/suspicious-ips-finder_2.11-0.1.jar ../static/jars/suspicious-ips-finder_2.11-0.1.jar`.
10. Upload content of folder `static` into the S3 bucket created in step (1), maintaining the folder structure (so upload folder `static` into prefix `static`).
10. Create a SageMaker notebook instance and upload the content of folder `spam-detection-sagemaker` into it.
11. Run through the notebook `spam-detection.ipynb`. Save output of `deployment.endpoint` somewhere; let `SpamSageMakerEndpointName` represent that.
12. Create an EC2 instance with access to S3 and Kinesis Streams.
13. Clone the repo on the instance.
14. Adjust `config.json`, change the value of `bucket` to value of `StaticFilesBucketName`.
15. Run `python3 items-generator/generator.py`.
16. Create AWS CloudFormation stack with the `cloudformation.template` template.
17. Start Kinesis Analytics application created in the stack manually.
18. Connect to the EC2 instance created in step (12).
19. Adjust `config.json` again, change `reviews_stream_name` and `views_stream_name` to names given in the CloudFormation template parameters.
20. Run `python3 logs-generator/generator.py views` and `python3 logs-generator/generator.py reviews`.
21. Perform Athena queries on demand, make sure the average ratings query is saved with prefix `athena_query_results/items_average_ratings/`.
