print("=== Importing Libaries ===")
from ibm_watsonx_ai.foundation_models.prompts import PromptTemplateManager, PromptTemplate
from ibm_watsonx_ai.foundation_models.utils.enums import ModelTypes, DecodingMethods, PromptTemplateFormats
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
import os

print("=== Reading environment variables ===")
watsonx_apikey = os.getenv("WATSONX_API_KEY")
watsonx_url = os.getenv("WATSONX_URL")
project_id = os.getenv("WATSONX_PROJECT_ID")
watsonx_task_credential = os.getenv("WATSONX_TASK_CREDENTIAL")
credentials = {
    "apikey": watsonx_apikey,
    "url": watsonx_url
}   

print("=== PreparingPromptTemplateManager ===")
prompt_mgr = PromptTemplateManager(credentials=credentials,
                                   project_id=project_id)

print("=== Define prompt template === ")
#Adjust parameters as needed: https://ibm.github.io/watsonx-ai-python-sdk/v1.4.7/prompt_template_manager.html
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

print("=== Store Defined prompt template in Project  === ")
stored_prompt_template = prompt_mgr.store_prompt(prompt_template=prompt_template)
print(stored_prompt_template)

print("=== Stored prompt template ID === ")
prompt_id = stored_prompt_template.prompt_id
print(f"Stored prompt template ID: {prompt_id}")

print("=== Unlock stored prompt template for editing   === ")
#Unlock stored prompt template for editing 
prompt_mgr.unlock(prompt_id=stored_prompt_template.prompt_id)
print(f"promptid {prompt_id} directly unlocked for editing.")

#Update existing prompt template with new name
# print("=== Update prompt template  === ")
# updated_prompt_template = PromptTemplate(name="New name")
# prompt_mgr.update_prompt(prompt_id, updated_prompt_template)
# print("Prompt template name updated.")

#Initialize API client
from ibm_watsonx_ai import APIClient
client = APIClient(wml_credentials=credentials)
client.set.default_project(project_id)

#Load prompt templates
prompt_input_text = prompt_mgr.load_prompt(prompt_id=stored_prompt_template.prompt_id, 
                                           astype=PromptTemplateFormats.STRING)

print("=== List prompt templates in Project  === ")
df_prompts = prompt_mgr.list()
df_prompts.sort_values("LAST MODIFIED", ascending=False)
print(df_prompts)

print("=== User Task Credentails Configuration  === ")
#Task credentails: https://www.ibm.com/docs/en/watsonx/saas?topic=projects-managing-task-credentials#accessing-task-credentials
from ibm_watsonx_ai.wml_client_error import WMLClientError

#Create or retrieve task credentials
TARGET_NAME = "wx task credentials"

# Try to create new task credentials
try:
    print("Creating new task credential...")
    task_credential = client.task_credentials.store(TARGET_NAME)

except WMLClientError as e:
    # Handle "already exists" case gracefully
    if "Task Credentials have already been stored" in str(e):
        print("Task credential already exists, retrieving it instead...")

        # Find existing credentials
        creds = client.task_credentials.list()
        existing = None
        for c in creds:
            if isinstance(c, dict) and c.get("metadata", {}).get("name") == TARGET_NAME:
                existing = c

        if existing:
            task_credential = existing
        else:
            # Fallback — list may not return credentials if running in a SPACE
            print("Warning: credential exists but not visible in this scope.")
            task_credential = {"name": TARGET_NAME}

    else:
        # Other errors should not be ignored
        print("Unexpected error while creating task credential:")
        print(e)
        task_credential = None  # or exit if needed
print("Using task credential:", task_credential)


print("=== List all deployments before Deployment  === ")
df_deployments = client.deployments.list()
print(df_deployments)

print("=== Define Deployment Meta Data  === ")
meta_props = {
    client.deployments.ConfigurationMetaNames.NAME: "Prompt Template deployed by CICD",
    client.deployments.ConfigurationMetaNames.ONLINE: {},
    client.deployments.ConfigurationMetaNames.BASE_MODEL_ID: "ibm/granite-3-8b-instruct"
}
# client.deployments.ConfigurationMetaNames.SERVING_NAME: "unique_serving_name_id_12345"

print("=== Create Deployment with Deployment metadata  === ")
deployment_details = client.deployments.create(artifact_id=stored_prompt_template.prompt_id, meta_props=meta_props)
print("=== Deployment details === ")
print(deployment_details)
print("=== Deployment ID === ")
deployment_id = deployment_details['metadata']['id']
print(f"Deployment ID: {deployment_id}")


print("=== List all deployments after Deployment  === ")
df_deployments = client.deployments.list()
print(df_deployments)

print("=== Done === ")