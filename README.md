🚀 CI/CD with GitHub Actions Workflow: Deloying automaticall with CI/CD Watsonx Prompt Templates

This workflow automatically runs the Python script python-scripts/python-script-watsonx-prompt-deployment.py whenever changes are pushed to the main branch or when manually triggered.
It is designed to deploy Watsonx prompt templates using credentials securely stored in GitHub Secrets.

📌 What the Workflow Does

Triggers on:

Pushes to main

Manual execution via Workflow Dispatch

Sets up the environment:

Checks out the repository

Installs Python 3.11

Installs dependencies from requirements.txt (if present)

Runs the deployment script:

Executes python-script-watsonx-prompt-deployment.py

With the following content:
This Python script automates the creation, management, and deployment of IBM Watsonx AI prompt templates. It performs the following tasks:

Imports libraries required for Watsonx AI prompt and deployment management.

Reads environment variables for API credentials, project ID, and task credentials.

Initializes a PromptTemplateManager for interacting with the Watsonx project.

Defines a prompt template with instructions, input variables, and example interactions.

Stores the prompt template in the specified project and unlocks it for editing.

Optionally updates the prompt template (commented out in the script).

Initializes the Watsonx AI API client and sets the default project.

Loads and lists existing prompt templates in the project.

Creates or retrieves user task credentials for secure API access.

Lists existing deployments before deployment.

Defines deployment metadata with a unique serving name.

Deploys the stored prompt template as an AI service in Watsonx.

Lists all deployments after deployment and prints deployment details.

The script is designed for CI/CD pipelines, allowing automated prompt template deployment and management within IBM Watsonx AI.


⚙️ Overview Workflow 
![Workflow-Diagram](img/workflow.png)
