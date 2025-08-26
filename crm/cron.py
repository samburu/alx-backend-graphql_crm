# crm/cron.py
import os
from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def log_crm_heartbeat():
    """
    Logs a heartbeat every 5 minutes and (optionally) hits the GraphQL hello field.
    """
    ts = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    logfile = "/tmp/crm_heartbeat_log.txt"

    # Always log heartbeat
    with open(logfile, "a") as f:
        f.write(f"{ts} CRM is alive\n")

    # Optional GraphQL check using gql client
    try:
        transport = RequestsHTTPTransport(
            url=os.getenv("GRAPHQL_URL", "http://localhost:8000/graphql"),
            use_json=True,
            retries=2,
            verify=True,
            headers={},  # add auth headers here if needed
        )
        client = Client(transport=transport, fetch_schema_from_transport=False)
        result = client.execute(gql("{ hello }"))
        hello = result.get("hello")
        with open(logfile, "a") as f:
            f.write(f"{ts} GraphQL hello: {hello}\n")
    except Exception as e:
        with open(logfile, "a") as f:
            f.write(f"{ts} GraphQL check failed: {e}\n")
