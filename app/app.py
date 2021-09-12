#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Main application module."""

import flask

app = flask.Flask(__name__)


@app.route("/")
def index():
    """Render main page."""
    return flask.render_template("index.html")


def main():
    """Run application in debug mode."""
    app.run(port=8080, debug=True)


if __name__ == "__main__":
    main()
