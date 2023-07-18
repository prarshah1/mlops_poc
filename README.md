# <b><u> MLP Business Inference </u></b>

# 1. Project Setup

### Virtual environment
It is expected that developers always use a virtual env to run commands or work inside this project.

### Jupyter
To use Jupyter notebooks or JupyterLab in your project:

```
pip install jupyter
pip install jupyterlab
jupyter notebook
```

### Local setup - typically one time
You can run [setup.sh](setup.sh) which will install requirements and setup pre-commit.
Edit `conf/environemnts\.user.env` with SUFFIX as your domain username. This is needed for local development only using dbx.
Do not commit / push this change to repo.

```
bash setup.sh
```
<br>


# 2. Project Structure

## Conf

[conf](conf) folder should be used to store configuration files used in the environments and pipelines.

### Environments

These configurations are used for storing workspace specific configs for dev, staging and prod.
[.base_data_params.env](environments/.base_data_params.env) is used for configurations that are common to all the environments.
See conf/readme.md and .user.env for more details related to development configurations.

### Pipeline configuration

The [pipeline_configs](pipeline_configs) folder is specifying the configuration for each stage of the pipeline.

### Deployment file

The [deployment.yml](deployment.yml) file contains job specifications and their parameters, cluster configs which is used by DBX(databricks command line tool) to submit jobs.

> *Note:*
> - Please do not check in any local configuration to version control.
> - Please do not put access credentials in any configuration folder other than local.

## Notebooks

It contains the model train and model inference notebooks written in spark.

## Lib

There is no lib in-built in the repo. The common lib (mlp-lib) gets installed from s3/databricks.
See setup.py, install-deps.sh and common-libs.yml for more information
For automated CI/CD, everything is taken care by repo admins via Environment variables and Github actions.
For local, you can either build the mlp-lib from source repo or download from s3.

## Resources

Used to store data accessed in the project, if any.

## Src

Contains jobs that use the mlp_lib for creating workflow tasks. <br>
Users can add their custom transformers in the [transformer](src/transformers) folder

## Tests

[integration](tests/integration) contains integration tests which fetch configurations from [resources](tests/resources) folder. <br>
[resources](tests/resources) contains configuration files. <br>
[unit](tests/unit) contains unit tests for every stage.


### Install DBX and Databricks CLI
- Intro to dbx - https://dbx.readthedocs.io/en/latest/intro/
- Refer dbx cli setup - https://github.com/databrickslabs/dbx
- Refer databricks cli setup - https://docs.databricks.com/dev-tools/cli/index.html

<br>

## Databricks setup

To setup Databricks-cli refer [databricks_cli_setup](https://docs.databricks.com/dev-tools/cli/index.html)
You will also need to set following secrets in the github repository to run integration tests:
- DATABRICKS_HOST
- DATABRICKS_TOKEN <br>


## Github workflows

- On pull request - any new PR for dev branch
- On PR merge - whenever PR is merged in dev
- On release (tag) - when a release tag va.b.c is created
<br>
Note that the workflows on PR and PR merge should always be checked for success before reviews.
One can also trigger these workflows (esp On PR) on demand from GitHub on specific branch to pro-actively check status or health of that branch even before creating a PR or merging it.
Avoid running pr-merge and release workflow manually unless you know what you really want.

## Code Formatting

The pre-commit hooks are present in [.pre-commit-config.yaml](.pre-commit-config.yaml),
and all its config is in [pyproject.toml](pyproject.toml) <br>

To exclude formatting a block of code in black, use
```commandline
# fmt: off
<code>
# fmt: on
```
To exclude rules in flake8 mention the rules to exclude in the config.

Refer [Flake8 Rules](https://www.flake8rules.com/) for list of rules.

To run manually use:
```
pre-commit install
pre-commit run -a
```
<br>
