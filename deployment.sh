echo "Deploy $STACK_NAME stack"

sourcebucket=final_project_$STACK_NAME
aws s3 mb s3://$sourcebucket --region $REGION
cp lambda_function/* venv/lib/python3.6/dist-packages
rm package.yaml
sam package --template-file template.yaml --s3-bucket $sourcebucket --output-template-file package.yaml

aws cloudformation deploy --stack-name $STACK_NAME --template-file package.yaml \
--region $REGION --capabilities CAPABILITY_IAM \
--parameter-overrides \
    RunUnitTest="true"
