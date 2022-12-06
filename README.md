# mlops_poc

## Repository Setup
1. To run the GitHub actions workflows we require the following GitHub actions secrets:
   * `DATABRICKS_STAGING_HOST` URL of Databricks staging workspace
   * `DATABRICKS_STAGING_TOKEN` Databricks access token for staging workspace
   * `DATABRICKS_PROD_HOST` URL of Databricks production workspace
   * `DATABRICKS_PROD_TOKEN` Databricks access token for production workspace
   * `GH_TOKEN` GitHub personal access token
2. Run [setup.sh](setup.sh)
3. The following command trains and register the poc model for demo: 
   * dbx deploy --jobs=PROD-telco-churn-initial-model-train-register --environment=prod --files-only
   * dbx launch --job=PROD-telco-churn-initial-model-train-register --environment=prod --as-run-submit --trace
4. To access s3 buckets refer: [Secure access to S3 buckets using instance profiles](https://docs.databricks.com/administration-guide/cloud-configurations/aws/instance-profiles.html)
5. To run inference dag, create a new connection in airflow with type=Databricks


## Dev workflow
The purpose of building a Dev pipeline is to perform exploratory data analysis, build featurization tables, and train models using Dev data and features. At the end of this stage, the CI pipeline will produce the following artifacts 
* Dev model along with experiments tracking data
* Feature tables
* Version-controlled source code in the dev branch

## Staging workflow
1.	The developer creates a Pull Request (merge request) from the dev to the main branch on GitHub
2.	The GitHub Action for PR gets triggered ([PR workflow code](.github/workflows/onpullrequest.yml))
3.	Unit tests are executed on the latest changes in the source ([Unit tests](tests/unit))
4.	Integration tests are executed ([Integration tests](tests/integration))
5.	Post the unit and integration tests pass, the PR is marked as passing for manual review and approval. At this step, a reviewer approves the changes and merges the PR
6.	PR is merged in the main branch
7.	Another GitHub Action is triggered based on the PR merge ([PR Merge workflow code](.github/workflows/onrelease.yml))
8.	Using the updated source code in the main branch, model training kicks off
9.	A new model is registered in the MLFlow registry
10.	There is also a notification (email e.g.) sent out to inform the new model's availability to human reviewers so that this can be QA’ed and approved.
11.	Manual review and QA are conducted on this new model.
12.	Post the sign-off, the release process kicks off which includes cutting a release tag on GitHub
13.	Post the tagging is done, the downstream CD or Production update pipeline is triggered



## CD