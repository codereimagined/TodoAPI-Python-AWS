#!/usr/bin/env python3
import os

from aws_cdk import (
    App,
    Stack,
    aws_apigateway,
    aws_lambda,
    aws_dynamodb,
)
from constructs import Construct


class PyRestApiStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        todo_table = aws_dynamodb.TableV2(
            self,
            "TodoTablePy",
            partition_key=aws_dynamodb.Attribute(
                name="id",type=aws_dynamodb.AttributeType.STRING
            ),
            billing=aws_dynamodb.Billing.on_demand(),
        )
        environment = {"TABLE_NAME": todo_table.table_name}
        if os.environ.get("ENV") == "local":
            environment["DYNAMODB_ENDPOINT_URL"] = "http://host.docker.internal:8000"
        todo_lambda = aws_lambda.Function(
            self,
            "TodoAPILambda",
            runtime=aws_lambda.Runtime.PYTHON_3_11,
            code=aws_lambda.Code.from_asset("build/deployment.zip"),
            handler="services.index.handler",
            environment=environment,
        )

        todo_table.grant_read_write_data(todo_lambda)

        api = aws_apigateway.RestApi(self, "Todo-API-Python")
        api_resource = api.root.add_resource(path_part="api")
        todo_resource = api_resource.add_resource(path_part="todos")

        todo_lambda_integration = aws_apigateway.LambdaIntegration(todo_lambda)
        todo_resource.add_method("GET", todo_lambda_integration)
        todo_resource.add_method("POST", todo_lambda_integration)

        todo_id_resource = todo_resource.add_resource(path_part="{todo_id}")
        todo_id_resource.add_method("GET", todo_lambda_integration)
        todo_id_resource.add_method("DELETE", todo_lambda_integration)


app = App()
PyRestApiStack(app, "TodoAPIPythonStack",
    # If you don't specify 'env', this stack will be environment-agnostic.
    # Account/Region-dependent features and context lookups will not work,
    # but a single synthesized template can be deployed anywhere.
    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
)

app.synth()
