# Email ETL CDK Pipeline

An AWS CDK application that processes CSV files sent via email through an automated pipeline.

## Architecture

This project implements an email-based ETL (Extract, Transform, Load) pipeline using AWS services:
- **SES**: Receives email with CSV attachments and sends processed results 
- **S3**: Stores the received CSV files
- **Lambda**: Processes the CSV files and generates results

## Prerequisites

- AWS Account and configured AWS CLI
- Python 3.9+
- Node.js 14+ (for AWS CDK)
- AWS CDK Toolkit (`npm install -g aws-cdk`)

## Setup and Deployment

1. Clone the repository
2. Create a virtual environment: `python -m venv .venv`
3. Activate the virtual environment: 
   - Linux/macOS: `source .venv/bin/activate`
   - Windows: `.venv\Scripts\activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Deploy the stack: `cdk deploy`

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for development workflow and guidelines.

## License

[MIT](LICENSE)