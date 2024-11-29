Run DynamoDB locally
```
docker run -d -p 8000:8000 amazon/dynamodb-local

aws dynamodb create-table \
   --table-name TodoTablePy56A52504 \
   --attribute-definitions AttributeName=id,AttributeType=S \
   --key-schema AttributeName=id,KeyType=HASH \
   --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
   --endpoint-url http://localhost:8000

aws dynamodb list-tables --endpoint-url http://localhost:8000

sam local start-api -t ./cdk.out/TodoAPIPythonStack.template.json
```
