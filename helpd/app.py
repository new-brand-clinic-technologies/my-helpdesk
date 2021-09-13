#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Main application module."""

import datetime
import os
import uuid

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


@app.route("/login", methods=["POST"])
def login():
    username = flask.request.form.get("login", "")
    password = flask.request.form.get("password", "")

    user = (flask.g.db.query(User)
            .filter(User.login == username)
            .filter(User.password == password)
            .one_or_none())

    if user is None:
        flask.flash("Incorrect password")
        return flask.redirect(flask.url_for("index"), code=303)

    flask.session["user_id"] = user.id
    return flask.redirect(flask.url_for("tickets"), code=303)


@app.route("/ticket", methods=["POST"])
def create_ticket():
    """Creates a ticket."""
    author = flask.request.form.get("name", "").strip()
    text = flask.request.form.get("question", "").strip()
    if author == "" or text == "":
        return flask.abort(400)

    tid = uuid.uuid4()
    ticket = Ticket(
        id=tid,
        created=datetime.datetime.now(),
        author=author,
        request=text
    )

    ticket.opened = False
    ticket.response = "Thank you for your question! Unfortunately, all our support team members are busy now. Please try to ask later! Your feedback is very important for us."

    flask.g.db.add(ticket)

    return flask.redirect(flask.url_for("ticket_not_admin", ticket_id=tid), code=303)


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

@app.route("/tickets/admin/<ticket_id>", methods=["POST"])
def post_ticket(ticket_id):
    """Sends reply to ticket."""
    if "user_id" not in flask.session:
        return flask.redirect(flask.url_for("index"), code=303)

    ticket = (flask.g.db.query(Ticket)
              .filter(Ticket.id == ticket_id)
              .one_or_none())
    if ticket is None:
        return flask.abort(404)
    if not ticket.opened:
        return flask.abort(400)

    ticket.opened = False
    ticket.response = flask.request.form.get("response", "")
    flask.g.db.add(ticket)

    return flask.redirect(flask.url_for("get_ticket", ticket_id=ticket_id), code=303)


def main():
    """Run application in debug mode."""
    app.run(port=8080, debug=True)


if __name__ == "__main__":
    main()
