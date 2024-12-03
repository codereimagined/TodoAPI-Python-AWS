# See this doc:
# https://docs.aws.amazon.com/lambda/latest/dg/python-package.html

rm -rf build/
mkdir build/

# python3 -m venv venv
python3 -m venv .venv-deploy-aws
. ./.venv-deploy-aws/bin/activate
pip install -r requirements-deploy.txt
deactivate
cd .venv-deploy/lib/python3.11/site-packages
zip -r ../../../../build/deployment.zip .
cd ../../../../
zip -g build/deployment.zip -r services
