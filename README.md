# Machine Learning Pipeline for AWS (with mock - LocalStack)

Example of how to build a machine learning full pipeline with AWS
(AWS simulated by "LocalStack" soft).

The flow of the system is:
1) make a query to DataBase (DynamoDB)
2) write the results: images and metadata to S3
3) optionally: run transformations and computer vision deep learning models on images

LocalStack runs under docker-compose.
There is also an example of how to build SQS queue bounded with Lambda Functions, that runs in additional docker.

# Structure of the code

* lambdas - package for lambda functions
* localstack - docker-compose config for AWS simulations
* scripts - to populate AWS DB and S3 from dataset
* src - source code for manage queries and additional proccesing

# How to use it

## Installation

* make poetry-download
* make install
* make aws-cli-install

Download dataset into this folder from this site:
https://www.kaggle.com/paramaggarwal/fashion-product-images-small

## Run

1) run: `docker-compose up` from localstack folder
2) from another terminal: source poetry virtual env in  ~/.cache/pypoetry/virtualenvs/...
3) run script to init DB and S3: `bash scripts/create_and_fill_db.sh` 
4) run queries: `python api.py --query {number_of_query}`                                                                       
   (number_of_query can be a number from 1 to 5, check api code to understand which options you have)

5) you can run jupyter notebook with examples from this repo that uses api code.

---
## Architecture of the system to make it scalable

![image](https://user-images.githubusercontent.com/10304038/125674920-127f026c-423d-41fb-a6b1-ba5448b279eb.png)
