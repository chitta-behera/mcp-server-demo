# MCP Server Demo

This is a demonstration implementation of an MCP (Model Control Protocol) server with a client that uses AWS Bedrock's Claude model.

## Features

- Simple addition tool
- Greeting resource
- AWS Bedrock integration with Claude 3.5 Sonnet

## Setup

1. Install dependencies:
```bash
pip install -e .
```

2. Configure AWS credentials for Bedrock access

## Usage

1. Start the server:
```bash
python server.py
```

2. Run the client:
```bash
python client.py
```

The demo includes a simple addition tool and a greeting resource. The client uses Claude 3.5 Sonnet to interpret user queries and call the appropriate tools.