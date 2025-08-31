# crm/tasks.py
from datetime import datetime
from celery import shared_task
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import requests


@shared_task
def generate_crm_report():
    """
    Generate weekly CRM report: total customers, orders, revenue.
    Logs results to /tmp/crm_report_log.txt
    """
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=True,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # GraphQL query
    query = gql(
        """
        query {
            totalCustomers
            totalOrders
            totalRevenue
        }
        """
    )

    try:
        result = client.execute(query)
        customers = result.get("totalCustomers", 0)
        orders = result.get("totalOrders", 0)
        revenue = result.get("totalRevenue", 0)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"{timestamp} - Report: {customers} customers, {orders} orders, {revenue} revenue\n"

        with open("/tmp/crm_report_log.txt", "a") as f:
            f.write(log_line)

        return "CRM report generated successfully"
    except Exception as e:
        return f"Error generating report: {str(e)}"
