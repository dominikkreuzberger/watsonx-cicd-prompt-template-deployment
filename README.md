🚀 CI/CD - GitHub Actions Workflow: Watsonx Prompt Deployment

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

Injects Watsonx environment variables from GitHub Secrets

Overview workflow

![Workflow-Diagram](img/workflow.png)
