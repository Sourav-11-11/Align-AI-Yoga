"""
Database utility helpers.

Uses Flask's application context (g) so a fresh connection is created per
request and automatically closed by the teardown hook in create_app().

Why NOT a module-level cursor:
  The original app.py created mycursor once at import time. This causes
  silent failures after MySQL's `wait_timeout` (~8 hours by default) because
  the connection goes stale and commands on the old cursor throw errors.
  Per-request connections avoid this entirely.
"""

import logging
import mysql.connector
from flask import current_app, g

logger = logging.getLogger(__name__)


def get_db() -> mysql.connector.MySQLConnection:
    """Return the request-scoped DB connection, creating it if needed."""
    if "db" not in g:
        g.db = mysql.connector.connect(
            host=current_app.config["DB_HOST"],
            user=current_app.config["DB_USER"],
            password=current_app.config["DB_PASSWORD"],
            port=current_app.config["DB_PORT"],
            database=current_app.config["DB_NAME"],
            charset="utf8mb4",
        )
    return g.db


def execute(query: str, values: tuple = ()) -> None:
    """Run a write query (INSERT / UPDATE / DELETE)."""
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(query, values)
        db.commit()
    except Exception as exc:
        db.rollback()
        logger.exception("DB write failed: %s", exc)
        raise
    finally:
        cursor.close()


def fetchall(query: str, values: tuple = ()) -> list:
    """Run a SELECT and return all matching rows."""
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(query, values)
        return cursor.fetchall()
    finally:
        cursor.close()


def fetchone(query: str, values: tuple = ()) -> "tuple | None":
    """Run a SELECT and return the first matching row (or None)."""
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(query, values)
        return cursor.fetchone()
    finally:
        cursor.close()
