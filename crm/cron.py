import datetime
import requests
import os

def log_crm_heartbeat():
    """
    Logs a heartbeat message every 5 minutes to confirm CRM health.
    Optionally queries GraphQL hello field for responsiveness.
    """
    log_file = "/tmp/crm_heartbeat_log.txt"
    now = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{now} CRM is alive"

    # Append to log file
    with open(log_file, "a") as f:
        f.write(message + "\n")

    try:
        response = requests.post(
            "http://localhost:8000/graphql/",
            json={"query": "{ hello }"},
            timeout=5
        )
        if response.ok:
            result = response.json()
            with open(log_file, "a") as f:
                f.write(f"{now} GraphQL response: {result}\n")
    except Exception as e:
        with open(log_file, "a") as f:
            f.write(f"{now} GraphQL check failed: {e}\n")
