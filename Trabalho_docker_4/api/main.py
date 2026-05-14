#!/usr/bin/env python3

import os
import json

import redis
from flask import Flask, request, Response

from linkextractor import extract_links

app = Flask(__name__)

redis_client = redis.from_url(
    os.getenv("REDIS_URL", "redis://localhost:6379"),
    decode_responses=True,
)


@app.route("/")
def index():
    return "Usage: http://<hostname>[:<port>]/api/<url>"


@app.route("/api/<path:url>")
def api(url):
    qs = request.query_string.decode("utf-8")
    if qs:
        url = url + "?" + qs

    cached = redis_client.get(url)
    if cached is not None:
        return Response(cached, mimetype="application/json")

    links = extract_links(url)
    body = json.dumps(links, indent=2)
    redis_client.set(url, body)
    return Response(body, mimetype="application/json")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
