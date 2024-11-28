#!/usr/bin/env python3
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
        todo_lambda = aws_lambda.Function(
            self,
            "TodoAPILambda",
            runtime=aws_lambda.Runtime.PYTHON_3_11,
            code=aws_lambda.Code.from_asset("build/deployment.zip"),
            handler="services.index.handler",
            environment={"TABLE_NAME": todo_table.table_name},
        )

        todo_table.grant_read_write_data(todo_lambda)

        api = aws_apigateway.RestApi(self, "Todo-API-Python")
        todo_resource = api.root.add_resource(path_part="api")

        todo_lambda_integration = aws_apigateway.LambdaIntegration(todo_lambda)
        todo_resource.add_method("GET", todo_lambda_integration)
        todo_resource.add_method("POST", todo_lambda_integration)


app = App()
PyRestApiStack(app, "TodoAPIPythonStack",
    # If you don't specify 'env', this stack will be environment-agnostic.
    # Account/Region-dependent features and context lookups will not work,
    # but a single synthesized template can be deployed anywhere.
    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
)

app.synth()
