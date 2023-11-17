# Big data summarization using Griptape, Amazon Bedrock and Amazon Redshift

This is the sample code for a Big data summarization example blog using the popular open-source library Griptape, Amazon Bedrock and Amazon Redshift. In this sample, we use TitanXL LLM to summarize but Anthropic's Claude v2 will be used to drive the application.

This application sample demnostrates how data can be pulled from Amazon Redshift and then passed to the summarization model. The driving model is isolated from the actual data and uses the tools provided to it to orchestrate the application. 

## Installation and running instructions

* Simply create a new python virtual environment and install the requirements by running `pip install -r requirements.txt`
* Create a `.env` file with relevant environment variables (change the values based on your deployment)

```shell
REDSHIFT_WORKGROUP_NAME=humansorg
REDSHIFT_DATABASE=dev
AWS_REGION=us-west-2
REDSHIFT_CREDENTIALS_SECRETS_MANAGER_ARN=<arn for the secrets manager redshift credentials>
```
  
* Start the application by running `python summarize.py`

## Creating an Amazon Redshift instance and loading data

* Start by following [this guide](https://docs.aws.amazon.com/redshift/latest/mgmt/serverless-console-first-time-setup.html) to create a new Redshift serverless instance
* Use [Python Faker](https://faker.readthedocs.io/en/master/) to create synthetic data and insert it into your data warehouse instance OR
* You can just insert the data manually by executing the following code block. First create the table and grant your username access to the table.
* Finally insert the data into the table.

```sql
CREATE TABLE people (
    id smallint default 0,
    first_name varchar(100) default 'General',
    last_name varchar(100) default 'General',
    occupation varchar(100) default 'General'
);
GRANT ALL PRIVILEGES ON TABLE people TO "IAM:your-iam-user-with-redshift-access";
```

```sql
INSERT INTO people VALUES
(1, 'Lee', 'Andrews', 'Engineer, electrical'),
(2, 'Michael', 'Woods', 'Therapist, art'),
(3, 'Joshua', 'Allen', 'Therapist, sports'),
(4, 'Eric', 'Foster', 'English as a second language teacher'),
(5, 'John', 'Daniels', 'Printmaker'),
(6, 'Matthew', 'Barton', 'Podiatrist'),
(7, 'Audrey', 'Wilson', 'IT technical support officer'),
(8, 'Leah', 'Knox', 'Social research officer, government'),
(9, 'David', 'Macdonald', 'Public relations account executive'),
(10, 'Erica', 'Ramos', 'Accountant, chartered public finance');
```

# Resources

* [Amazon Bedrock available models](https://aws.amazon.com/bedrock/)
* [Amazon Redshift Serverless docs](https://docs.aws.amazon.com/redshift/latest/mgmt/serverless-whatis.html)
* [Griptape documentation](https://docs.griptape.ai/)


## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

