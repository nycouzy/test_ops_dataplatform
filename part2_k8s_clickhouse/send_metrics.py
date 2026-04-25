"""
Création de la table + insertion de mock data
"""

import os
import logging
import requests
from requests.models import Response
from dotenv import load_dotenv
from faker import Faker

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
load_dotenv()

logger = logging.getLogger(__name__)
"""logger du module"""

url = os.getenv("CLICKHOUSE_URL")
user = os.getenv("CLICKHOUSE_USER")
password = os.getenv("CLICKHOUSE_PASSWORD")


def run_query(query: str, data: str = "") -> Response:
    """Run the given query.

    Args:
        query (str): Query to run
        data (str): Optionnal data

    Returns:
        dict: json response.
    """

    logger.debug(query)
    logger.debug(data)
    response = requests.post(
        url,
        params={"query": query, "user": user, "password": password},
        timeout=5000,
        data=data,
    )
    if response.ok:
        logger.info("Query execution %s OK", query)
        return response
    else:
        logger.error("Error during query %s", query)
        raise RuntimeError(f"Error during {query} execution")


def create_table(table_name: str) -> Response:
    """Load the given table name sql file and execute statement in ClickHouse

    Args:
        table_name (str): Table name used to load sql script.

    Returns:
        dict: json response.
    """

    with open(
        f"part2_k8s_clickhouse/{table_name}.sql", "r", encoding="utf-8"
    ) as query_file:
        logger.info("Creating table %s...", table_name)
        return run_query(query=query_file.read())


def insert_data(table_name: str, data: str) -> Response:
    """Insert mock data into table.

    Args:
        table_name (str): Table to insert to
        data (str): TabSeparated formatted data

    Returns:
        dict: json response.
    """

    return run_query(query=f"INSERT INTO {table_name} FORMAT TabSeparated", data=data)


def mock_data(nb_line: int = 10) -> str:
    """Mock data for job_metrics table.

    Args:
        nb_line (int): Nb line to generate

    """
    fake = Faker()
    return "\n".join(
        f"{fake.uuid4()}\t"
        f"{fake.date_time().strftime('%Y-%m-%d %H:%M:%S')}\t"
        f"{fake.random_int(1, 500)}\t"
        f"{int(fake.boolean())}"
        for _ in range(nb_line)
    )


if __name__ == "__main__":
    create_table(table_name="job_metrics")
    insert_data(table_name="job_metrics", data=mock_data())
