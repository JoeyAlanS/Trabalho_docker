#!/usr/bin/env python3

from flask import Flask, request, jsonify

from linkextractor import extract_links

app = Flask(__name__)


@app.route("/")
def index():
    return "Usage: http://<hostname>[:<port>]/api/<url>"


@app.route("/api/<path:url>")
def api(url):
    try:
        qs = request.query_string.decode("utf-8")
        if qs:
            url = url + "?" + qs
        links = extract_links(url)
        return jsonify(links)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
