# you will need to set following secrets in the github repository:
# GITHUB_TOKEN
# Following for all environments, eg. DEV, PROD, STAGING
# DATABRICKS_<env>_HOST
# DATABRICKS_<env>_TOKEN

if [-d ".dvc/tmp"]
  dvc repro
  dvc push
else
  dvc init -f
  # pip uninstall pathlib # if the command gives: 'PosixPath' object has no attribute 'read_text' attribute error
  mkdir .dvc/backup
  dvc run -n input_path_dvc  -p conf/pipeline_configs/feature_table_creator.yml:input_s3_path -f echo "DVC Completed"
  dvc remote add -d local_dir .dvc/backup/
  dvc pull
fi

# TODO for testing purposes, remove this
export DATABRICKS_HOST=https://dbc-79ee8895-9a53.cloud.databricks.com
export DATABRICKS_TOKEN=dapib7b9ee9e57d9d622c5f14a9b343fdf3b
