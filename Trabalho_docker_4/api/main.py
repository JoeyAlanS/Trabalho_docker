#!/usr/bin/env python

import os
import sys
import json
import redis
from flask import Flask
from flask import request
from linkextractor import extract_links

app = Flask(__name__)
redis_conn = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))

@app.route("/")
def index():
    return "Usage: http://<hostname>[:<prt>]/api/<url>"

@app.route("/api/<path:url>")
def api(url):
    try:
        qs = request.query_string.decode("utf-8")
        if qs != "":
            url += "?" + qs

        jsonlinks = redis_conn.get(url)
        if not jsonlinks:
            links = extract_links(url)
            jsonlinks = json.dumps(links, indent=2)
            redis_conn.set(url, jsonlinks)

        response = app.response_class(
            status=200,
            mimetype="application/json",
            response=jsonlinks
        )

        return response
    except Exception as e:
        # [FIX] Log e retorna erro descriptivo
        print(f"[API ERROR] {url}: {type(e).__name__}: {str(e)}", file=sys.stderr)
        return app.response_class(
            status=500,
            mimetype="application/json",
            response=json.dumps({"error": str(e)}, indent=2)
        )

app.run(host="0.0.0.0")