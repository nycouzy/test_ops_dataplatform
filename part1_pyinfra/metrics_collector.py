"""Metrics API"""

from flask import Flask, Response, make_response

app = Flask(__name__)


@app.route("/health")
def get_health() -> Response:
    """Get health metric.

    Returns:
        Response: health status.
    """
    return make_response({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
