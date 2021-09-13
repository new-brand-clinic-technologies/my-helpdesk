#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Main application module."""

import flask
import sqlalchemy

from sqlalchemy.orm import sessionmaker

from helpd.models import Base, User, Ticket

app = flask.Flask(__name__)

db_engine = sqlalchemy.create_engine("postgresql://help:help@db/help")
db_factory = sessionmaker(bind=db_engine, expire_on_commit=False)

@app.before_first_request
def create_tables():
    """Creates all tables."""
    Base.metadata.create_all(db_engine)


@app.before_request
def establish_connection():
    """Gets a connection from the pool."""
    flask.g.db = sqlalchemy.orm.scoped_session(db_factory)()


@app.teardown_appcontext
def teardown_database(exc: Exception = None):
    """Commits or rolls back the cursor."""
    database = flask.g.pop("db")
    if exc is None:
        database.commit()
    else:
        database.rollback()


@app.route("/")
def index():
    """Render main page."""
    return flask.render_template("index.html")


@app.route("/login", methods=["POST"])
def login_post():
    """Logins a user."""

    # TODO: fix
    flask.session["user_id"] = 1

    return flask.redirect(flask.url_for("/admin"), code=303)


def main():
    """Run application in debug mode."""
    app.run(port=8080, debug=True)


if __name__ == "__main__":
    main()
