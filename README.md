# example-glue-py

## Description

The files to update:

- `statement.md`: The problem statement
- `problem.yml`: Problem configuration
- `aoi.config.yml`: Server binding
- `data/*`: The judge data

## Usage

1. Setup AOI CLI (If you already have it, skip this step)

- Run `yarn aoi server set`
- Enter server name (should be same in `aoi.config.yml`)
- Enter server URL (the URL is the **API Endpoint** eg. https://your-instance/api)
- Run `yarn aoi server login`
- Following the instructions to login

2. Update `statement.md`, `problem.yml`, `aoi.config.yml`, and `data/*`

3. Run `yarn aoi problem deploy -s -d "Data version message" -S -r` to deploy the problem

- `-s` to update statement and metadata
- `-d` to specify the data version message
- `-S` to set data version as active
- `-r` to rejudge all solutions
