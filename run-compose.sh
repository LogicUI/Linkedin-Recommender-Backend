#!/bin/bash

source .env

# Default profile
PROFILE="dev"

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -p|--profile) PROFILE="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

# Set environment variables based on the profile
if [ "$PROFILE" == "dev" ]; then
    export POSTGRES_USER=$POSTGRES_USER_DEV
    export POSTGRES_PASSWORD=$POSTGRES_PASSWORD_DEV
    export POSTGRES_DB=$POSTGRES_DB_DEV
elif [ "$PROFILE" == "test" ]; then
    export POSTGRES_USER=$POSTGRES_USER_TEST
    export POSTGRES_PASSWORD=$POSTGRES_PASSWORD_TEST
    export POSTGRES_DB=$POSTGRES_DB_TEST
elif [ "$PROFILE" == "prod" ]; then
    export POSTGRES_USER=$POSTGRES_USER_PROD
    export POSTGRES_PASSWORD=$POSTGRES_PASSWORD_PROD
    export POSTGRES_DB=$POSTGRES_DB_PROD
else
    echo "Unknown profile: $PROFILE"
    exit 1
fi

# Run Docker Compose with the specified profile
docker-compose --profile $PROFILE up