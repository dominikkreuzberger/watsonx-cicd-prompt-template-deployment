from ibm_watsonx_ai.foundation_models.prompts import PromptTemplateManager, PromptTemplate
from ibm_watsonx_ai.foundation_models.utils.enums import ModelTypes, DecodingMethods, PromptTemplateFormats
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
import os

watsonx_apikey = os.getenv("WATSONX_API_KEY")
watsonx_url = os.getenv("WATSONX_URL")
space_id = os.getenv("WATSONX_SPACE_ID")
project_id = os.getenv("WATSONX_PROJECT_ID")
watsonx_task_credential = os.getenv("WATSONX_TASK_CREDENTIAL")
credentials = {
    "apikey": watsonx_apikey,
    "url": watsonx_url
}   

prompt_mgr = PromptTemplateManager(credentials=credentials,
                                   project_id=project_id)

prompt_template = PromptTemplate(name="New Prompt Template created by CICD",
                                 model_id="ibm/granite-3-3-8b-instruct",
                                 model_params = {GenParams.DECODING_METHOD: "sample"},
                                 description="My example",
                                 task_ids=["generation"],
                                 input_variables=["object"],
                                 instruction="Answer on the following question",
                                 input_prefix="Human",
                                 output_prefix="Assistant",
                                 input_text="What is {object} and how does it work?",
                                 examples=[["What is a loan and how does it work?", 
                                            "A loan is a debt that is repaid with interest over time."]]
                                )

stored_prompt_template = prompt_mgr.store_prompt(prompt_template=prompt_template)

from ibm_watsonx_ai import APIClient

client = APIClient(wml_credentials=credentials)
client.set.default_project(project_id)

prompt_input_text = prompt_mgr.load_prompt(prompt_id=stored_prompt_template.prompt_id, 
                                           astype=PromptTemplateFormats.STRING)

# 1. List existing task credentials
existing_credentials = client.task_credentials.list()

# 2. Find credential by name
existing = None
for cred in existing_credentials:
    if cred['metadata']['name'] == "wx task credentials":
        existing = cred
        break

# 3. Use or create credential
if existing:
    print("Using existing task credential")
    task_credential = existing
else:
    print("Creating new task credential")
    task_credential = client.task_credentials.store("wx task credentials")

meta_props = {
    client.deployments.ConfigurationMetaNames.NAME: "Prompt Template deployed by CICD",
    client.deployments.ConfigurationMetaNames.ONLINE: {},
    client.deployments.ConfigurationMetaNames.BASE_MODEL_ID: "ibm/granite-3-8b-instruct"}

deployment_details = client.deployments.create(artifact_id=stored_prompt_template.prompt_id, meta_props=meta_props)