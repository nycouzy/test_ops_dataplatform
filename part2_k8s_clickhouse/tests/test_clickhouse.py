""" Tests for clickhouse """

import os
from typing import Any
from dotenv import load_dotenv
import requests

load_dotenv()

url = os.getenv("CLICKHOUSE_URL")
user = os.getenv("CLICKHOUSE_USER")
password = os.getenv("CLICKHOUSE_PASSWORD")


def run_test_query(query: str) -> Any:
    """Run test query

    Args:
        query (str): Query to execute

    Returns:
        dict: Query results
    """
    return requests.post(
        url,
        params={"query": query, "user": user, "password": password},
        timeout=5000,
    ).json()


def test_job_metrics_table_exists():
    """Test if table query_jobs exists"""
    assert (
        run_test_query(
            """
                SELECT count()
                FROM system.tables
                WHERE database = 'test_ops_data_platform'
                AND name = 'job_metrics'
            """
        )
        == 1
    )


def test_job_metrics_table_is_not_empty():
    """ test if table if not empty """
    assert (
        run_test_query(
            """
                SELECT count(1)
                FROM test_ops_data_platform.job_metrics
            """
        )
        > 0
    )
