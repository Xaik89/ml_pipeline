# Machine Learning Pipeline for AWS (with mock)

Example how to build a machine learning full pipeline
clien_code -> DB -> S3 and run on this transformations or/and machine learning models.
(AWS simulated by "LocalStack" soft)

LocalStack runs under docker-compose.
There also an example how to build SQS queue bounded with Lambda Functions, that runs in additional docker.

# Structure of code

lambdas - package for lambda functions
localstack - docker-compose config for AWS simulations
scripts - to populate AWS DB and S3 from dataset
src - source code for manage queries and additional proccesing

# STEPS to start this package

make poetry-download
make install
make aws-cli-install

Download dataset to this folder from this site:
https://www.kaggle.com/paramaggarwal/fashion-product-images-small

1) run: `docker-compose up` from localstack folder
2) from another terminal:
   run script to init DB and S3: `bash scripts/create_and_fill_db.sh` 
   run from poetry env: `python api.py --query {number_of_query}` 
   (number_of_quer equals from 1 to 5, check api code to understand what options you have)

   or you can run jupyter notebook with examples.
