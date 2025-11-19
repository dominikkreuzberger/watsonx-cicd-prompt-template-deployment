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

prompt_template = PromptTemplate(name="New prompt from cicd",
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


meta_props = {
    client.deployments.ConfigurationMetaNames.NAME: "prompt-deployment",
    client.deployments.ConfigurationMetaNames.TASK: {
        "credentials": {
            "api_key": os.getenv("WATSONX_TASK_CREDENTIAL")
        }
    }
}



stored_prompt_template = prompt_mgr.store_prompt(prompt_template=prompt_template)

from ibm_watsonx_ai import APIClient

client = APIClient(wml_credentials=credentials)
client.set.default_project(project_id)

prompt_input_text = prompt_mgr.load_prompt(prompt_id=stored_prompt_template.prompt_id, 
                                           astype=PromptTemplateFormats.STRING)

meta_props = {
    client.deployments.ConfigurationMetaNames.NAME: "SAMPLE DEPLOYMENT PROMPT TEMPLATE",
    client.deployments.ConfigurationMetaNames.ONLINE: {},
    client.deployments.ConfigurationMetaNames.TASK:
        "credentials": {
            "api_key": os.getenv("WATSONX_TASK_CREDENTIAL")
        },
    client.deployments.ConfigurationMetaNames.BASE_MODEL_ID: "ibm/granite-3-8b-instruct"}

deployment_details = client.deployments.create(artifact_id=stored_prompt_template.prompt_id, meta_props=meta_props)