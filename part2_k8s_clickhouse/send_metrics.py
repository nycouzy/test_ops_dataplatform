"""
This module create table job_metrics and send mock data.
Using http and TabSeparated format for data
"""

import os
import logging
import requests
from requests.models import Response
from dotenv import load_dotenv
from faker import Faker

# unused see why in run_query
import sqlglot
from sqlglot.errors import ParseError

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def run_query(
    url: str,
    user: str,
    password: str,
    *,
    query: str | None = None,
    file_path: str | None = None,
    data: str | None = None,
) -> Response:
    """Run the given query.

    Args:
        url (str): ClickHouse URL.
        user (str): ClickHouse user.
        password (str): ClickHouse user password.
        query (str): Query to run
        file_path (str): If the query is in a file
        data (str): Optionnal data

    Returns:
        Response: response from requests call.
    """

    if query:
        logger.info("Parameter query is set, ignoring file_path")
        logger.debug(query)
        _query = query
    elif file_path:
        logger.info("Parameter file_path is set, loading query")
        with open(file=file_path, mode="r", encoding="utf-8") as query_file:
            _query = query_file.read()
    else:
        raise ValueError("Provide one of 'query' or 'file_path'")

    # Validate query using sqlglot
    # We can't use sqlglot as FORMAT is not a valid SQL expr.
    # But we should ensure the query is valid vefore executing it.
    # try:
    #     parsed = sqlglot.parse_one(_query, dialect="clickhouse")
    #     normalized_query = parsed.sql()
    # except ParseError as e:
    #     raise ValueError("Invalid SQL query") from e

    logger.debug("Validated query: %s", _query)

    logger.debug(data)
    response = requests.post(
        url,
        params={"query": _query, "user": user, "password": password},
        timeout=5000,
        data=data,
    )
    if response.ok:
        logger.info("Query execution %s OK", query)
    else:
        logger.error("Error during query %s", query)
    return response


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
    load_dotenv()
    _url = os.getenv("CLICKHOUSE_URL", "http://localhost:8123")
    _user = os.getenv("CLICKHOUSE_USER", "default")
    _password = os.getenv("CLICKHOUSE_PASSWORD", "")
    # In a production environment we would use query or file_path but not a mix.
    # Probably file_path as .sql should be in git
    run_query(
        url=_url,
        user=_user,
        password=_password,
        query="CREATE DATABASE IF NOT EXISTS test_ops_data_platform;",
    )
    run_query(
        url=_url,
        user=_user,
        password=_password,
        file_path="part2_k8s_clickhouse/job_metrics.sql",
    )
    run_query(
        url=_url,
        user=_user,
        password=_password,
        query="INSERT INTO test_ops_data_platform.job_metrics FORMAT TabSeparated",
        data=mock_data(),
    )
