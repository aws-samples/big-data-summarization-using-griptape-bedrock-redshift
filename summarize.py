import os
import boto3
from griptape.drivers import (
    AmazonRedshiftSqlDriver,
    AmazonBedrockPromptDriver,
    BedrockClaudePromptModelDriver,
    BedrockTitanPromptModelDriver,
    BedrockTitanEmbeddingDriver,
)
from griptape.loaders import SqlLoader
from griptape.memory import TaskMemory
from griptape.rules import Ruleset, Rule
from griptape.structures import Agent
from griptape.tools import SqlClient, FileManager, TaskMemoryClient
from griptape.artifacts import TextArtifact, BlobArtifact
from griptape.memory.task.storage import BlobArtifactStorage, TextArtifactStorage
from griptape.drivers import LocalVectorStoreDriver
from griptape.engines import (
    VectorQueryEngine,
    PromptSummaryEngine,
    CsvExtractionEngine,
    JsonExtractionEngine,
)
from dotenv import load_dotenv

# By default read the .env file
load_dotenv()


session = boto3.Session(region_name=os.environ["AWS_REGION"])
sql_loader = SqlLoader(
    sql_driver=AmazonRedshiftSqlDriver(
        database=os.environ["REDSHIFT_DATABASE"],
        session=session,
        database_credentials_secret_arn=os.environ["REDSHIFT_CREDENTIALS_SECRETS_MANAGER_ARN"],
        workgroup_name=os.getenv("REDSHIFT_WORKGROUP_NAME"),
    )
)

sql_tool = SqlClient(
    sql_loader=sql_loader,
    table_name="people",
    table_description="contains information about tech industry professionals",
    engine_name="redshift",
)

file_manager = FileManager()

task_memory_client = TaskMemoryClient(off_prompt=True)

ruleset = Ruleset(
    name="HumansOrg Agent",
    rules=[
        Rule("Act and introduce yourself as a HumansOrg, Inc. support agent"),
        Rule("Your main objective is to help with finding information about people"),
        Rule("Only use information about people from the sources available to you"),
    ],
)


prompt_driver = AmazonBedrockPromptDriver(
    model="anthropic.claude-v2",
    prompt_model_driver=BedrockClaudePromptModelDriver(),
    session=session,
)
task_memory_prompt_driver = AmazonBedrockPromptDriver(
    model="amazon.titan-text-express-v1",
    prompt_model_driver=BedrockTitanPromptModelDriver(),
    session=session,
)

task_memory_embedding_driver = BedrockTitanEmbeddingDriver(session=session)


agent = Agent(
    tools=[sql_tool, file_manager, task_memory_client],
    rulesets=[ruleset],
    prompt_driver=prompt_driver,
    embedding_driver=task_memory_embedding_driver,
    task_memory=TaskMemory(
        artifact_storages={
            TextArtifact: TextArtifactStorage(
                query_engine=VectorQueryEngine(
                    prompt_driver=task_memory_prompt_driver,
                    vector_store_driver=LocalVectorStoreDriver(
                        embedding_driver=task_memory_embedding_driver
                    ),
                ),
                summary_engine=PromptSummaryEngine(
                    prompt_driver=task_memory_prompt_driver
                ),
                csv_extraction_engine=CsvExtractionEngine(
                    prompt_driver=task_memory_prompt_driver
                ),
                json_extraction_engine=JsonExtractionEngine(
                    prompt_driver=task_memory_prompt_driver
                ),
            ),
            BlobArtifact: BlobArtifactStorage(),
        }
    ),
)

agent.run(
    "Summarize a report of tech industry professional's names and occupations "
    "and save to the current directory in a file called occupations.txt"
)
