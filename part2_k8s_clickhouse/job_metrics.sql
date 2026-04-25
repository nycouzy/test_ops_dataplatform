CREATE TABLE IF NOT EXISTS test_ops_data_platform.job_metrics (
    job_id String,
    timestamp DateTime,
    duration_sec UInt32,
    success Bool
)
ENGINE = MergeTree
ORDER BY (job_id, timestamp);