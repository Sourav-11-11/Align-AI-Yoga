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
        try:
            config_dict = {
                "host": current_app.config.get("DB_HOST"),
                "user": current_app.config.get("DB_USER"),
                "password": current_app.config.get("DB_PASSWORD"),
                "port": current_app.config.get("DB_PORT"),
                "database": current_app.config.get("DB_NAME"),
                "charset": "utf8mb4",
            }
            
            # Log configuration (without password)
            safe_config = {k: ("***" if k == "password" else v) for k, v in config_dict.items()}
            logger.debug(f"Connecting to database: {safe_config}")
            
            g.db = mysql.connector.connect(**config_dict)
            logger.debug("Database connection established successfully")
        except Exception as exc:
            logger.error(f"Database connection failed: {exc}")
            raise RuntimeError(f"Failed to connect to database: {exc}")
    return g.db


def execute(query: str, values: tuple = ()) -> None:
    """Run a write query (INSERT / UPDATE / DELETE)."""
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(query, values)
        db.commit()
        logger.debug(f"Query executed successfully: {query[:100]}...")
    except Exception as exc:
        db.rollback()
        logger.error(f"DB write failed: {exc}\nQuery: {query}\nValues: {values}")
        raise
    finally:
        cursor.close()


def fetchall(query: str, values: tuple = ()) -> list:
    """Run a SELECT and return all matching rows."""
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(query, values)
        results = cursor.fetchall()
        logger.debug(f"Query executed, returned {len(results)} rows: {query[:100]}...")
        return results
    except Exception as exc:
        logger.error(f"DB read failed: {exc}\nQuery: {query}\nValues: {values}")
        raise
    finally:
        cursor.close()


def fetchone(query: str, values: tuple = ()) -> "tuple | None":
    """Run a SELECT and return the first matching row (or None)."""
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(query, values)
        result = cursor.fetchone()
        logger.debug(f"Query executed: {query[:100]}...")
        return result
    except Exception as exc:
        logger.error(f"DB read failed: {exc}\nQuery: {query}\nValues: {values}")
        raise
    finally:
        cursor.close()
