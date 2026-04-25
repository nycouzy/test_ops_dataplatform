"""
This module create table job_metrics and send mock data
Using clickhouse_connect client and polars / arrow.
"""

import os
import logging

from dotenv import load_dotenv
from clickhouse_connect import get_client
from clickhouse_connect.driver import Client
from faker import Faker
import polars as pl


logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def mock_data_df(nb_line: int = 10) -> pl.DataFrame:
    """Mock data for job_metrics table.

    Args:
        nb_line (int): Nb line to generate

    """
    fake = Faker()
    df = pl.DataFrame(
        data=[
            [
                fake.uuid4(),
                fake.date_time().strftime("%Y-%m-%d %H:%M:%S"),
                fake.random_int(1, 500),
                int(fake.boolean()),
            ]
            for _ in range(nb_line)
        ],
        schema=["job_id", "timestamp", "duration_sec", "success"],
        orient="row",
    )
    logger.debug("Data generated: %s", df)
    return df


def execute_command_from_script(client: Client, file_path: str) -> None:
    """Execute a SQL command.

    Args:
        file_path (str): Path of SQL script.
    """
    with open(file=file_path, mode="r", encoding="utf-8") as query_file:
        query = query_file.read()

    client.command(query)


def insert_data(client: Client, table_name: str, data: pl.DataFrame) -> None:
    """Insert data from a polars df.

    Args:
        table_name (str): Table to insert to.
        data (pl.Dataframe): DataFrame of data.
    """
    r = client.insert_arrow(table=table_name, arrow_table=data.to_arrow())
    logger.debug("summary=%s", r.summary)


if __name__ == "__main__":
    load_dotenv()

    _client = get_client(
        host=os.getenv("CLICKHOUSE_HOST", "localhost"),
        username=os.getenv("CLICKHOUSE_USER", "default"),
        password=os.getenv("CLICKHOUSE_PASSWORD", ""),
        database="test_ops_data_platform",
        port=8123,
    )

    logger.info("Create table job_metrics")
    execute_command_from_script(
        client=_client, file_path="part2_k8s_clickhouse/job_metrics.sql"
    )
    logger.info("Insert mock data into job_metrics")
    insert_data(client=_client, table_name="job_metrics", data=mock_data_df())
