"""Tests for clickhouse"""

import os
from dotenv import load_dotenv

from part2_k8s_clickhouse.send_metrics import run_query

load_dotenv(dotenv_path="part2_k8s_clickhouse/.env")


_url = os.getenv("CLICKHOUSE_URL", "")
_user = os.getenv("CLICKHOUSE_USER", "")
_password = os.getenv("CLICKHOUSE_PASSWORD", "")


def test_job_metrics_table_exists():
    """Test if table query_jobs exists"""
    assert (
        run_query(
            url=_url,
            user=_user,
            password=_password,
            query="""
                SELECT count()
                FROM system.tables
                WHERE database = 'test_ops_data_platform'
                AND name = 'job_metrics'
            """,
        ).json()
        == 1
    )


def test_job_metrics_table_is_not_empty():
    """test if table if not empty"""
    assert (
        run_query(
            url=_url,
            user=_user,
            password=_password,
            query="""
                SELECT count(1)
                FROM test_ops_data_platform.job_metrics
            """,
        ).json()
        > 0
    )
