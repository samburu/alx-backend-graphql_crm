#!/usr/bin/env python3
import sys
import os
from datetime import datetime, timedelta
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# GraphQL endpoint
GRAPHQL_ENDPOINT = "http://localhost:8000/graphql"

def main():
    try:
        # Set up GraphQL client
        transport = RequestsHTTPTransport(
            url=GRAPHQL_ENDPOINT,
            verify=True,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)

        # Compute last 7 days
        today = datetime.utcnow().date()
        seven_days_ago = today - timedelta(days=7)

        # GraphQL query for orders in last 7 days
        query = gql(
            """
            query GetRecentOrders($start_date: Date!) {
              orders(filter: {order_date_gte: $start_date}) {
                id
                customer {
                  email
                }
                order_date
              }
            }
            """
        )

        params = {"start_date": seven_days_ago.isoformat()}

        result = client.execute(query, variable_values=params)

        # Log file
        log_path = "/tmp/order_reminders_log.txt"
        with open(log_path, "a") as f:
            timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            for order in result.get("orders", []):
                log_line = f"[{timestamp}] Order ID: {order['id']} | Customer: {order['customer']['email']}\n"
                f.write(log_line)

        print("Order reminders processed!")

    except Exception as e:
        print(f"Error processing reminders: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
