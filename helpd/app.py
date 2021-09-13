#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Main application module."""

import os

import flask
import sqlalchemy

from sqlalchemy.orm import sessionmaker

from helpd.models import Base, User, Ticket

app = flask.Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]

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


@app.route("/tickets")
def tickets():
    """Render tickets list."""
    if "user_id" not in flask.session:
        return flask.redirect(flask.url_for("index"), code=303)

    tickets_list = (flask.g.db.query(Ticket)
                    .order_by(Ticket.created)
                    .limit(10)
                    .all())

    return flask.render_template("tickets.html", tickets=tickets_list)


@app.route("/tickets/admin/<ticket_id>", methods=["GET"])
def get_ticket(ticket_id):
    """Render ticket for reply."""
    if "user_id" not in flask.session:
        return flask.redirect(flask.url_for("index"), code=303)

    ticket = (flask.g.db.query(Ticket)
              .filter(Ticket.id == ticket_id)
              .one())

    return flask.render_template("ticket.html", is_admin=True, ticket=ticket)


def main():
    """Run application in debug mode."""
    app.run(port=8080, debug=True)


if __name__ == "__main__":
    main()
