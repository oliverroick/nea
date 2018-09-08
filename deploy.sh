#!/bin/bash

PROFILE="default"
STAGE="dev"

while [ "$1" != "" ]; do
    IFS='=' read -r -a arg <<< "$1"

    case ${arg[0]} in
        --email )          EMAIL=${arg[1]}
                           ;;
        --stage )          STAGE=${arg[1]}
                           ;;
        --profile )        PROFILE=${arg[1]}
                           ;;
    esac
    shift
done

if [ -z "$EMAIL" ]
then
    echo "Argument email not provided"
    exit 1
fi


if [[ -z "${AWS_ACCESS_KEY_ID}" ]] && [[ -z "${AWS_SECRET_ACCESS_KEY}" ]]
then
    echo "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY not set, using profile $PROFILE"
    USE_PROFILE=1
fi


LAMBDAS_BUCKET=$PROFILE-nea-$STAGE-lambdas

# make a build directory to store artifacts
rm -rf build
mkdir build

# make the deployment bucket in case it doesn't exist
aws s3 mb s3://$LAMBDAS_BUCKET ${USE_PROFILE:+--profile $PROFILE}

# generate next stage yaml file
aws cloudformation package                   \
    --template-file template.yaml            \
    --output-template-file build/output.yaml \
    --s3-bucket $LAMBDAS_BUCKET              \
    ${USE_PROFILE:+--profile $PROFILE}

# the actual deployment step
aws cloudformation deploy                     \
    --template-file build/output.yaml         \
    --stack-name nea-$STAGE                   \
    --capabilities CAPABILITY_IAM             \
    ${USE_PROFILE:+--profile $PROFILE}        \
    --parameter-overrides Email=$EMAIL Environment=$STAGE
