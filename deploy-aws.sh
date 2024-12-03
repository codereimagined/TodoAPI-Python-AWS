npm install -g aws-cdk

python3 -m venv .venv
. ./.venv/bin/activate
pip install -r requirements.txt
cdk bootstrap
cdk deploy --require-approval never
deactivate
