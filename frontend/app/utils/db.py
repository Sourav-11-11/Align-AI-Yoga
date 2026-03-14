"""
Database utility helpers.

Supports both SQLite (for production on Render) and MySQL (for local dev).
Uses Flask's application context (g) so a fresh connection is created per
request and automatically closed by the teardown hook in create_app().
"""

import logging
import sqlite3
import os
from flask import current_app, g

logger = logging.getLogger(__name__)


def get_db():
    """Return the request-scoped DB connection, creating it if needed.
    
    Automatically detects SQLite vs MySQL based on config.
    """
    if "db" not in g:
        db_type = current_app.config.get("DB_TYPE", "sqlite").lower()
        
        if db_type == "sqlite":
            g.db = _get_sqlite_connection()
        else:
            g.db = _get_mysql_connection()
    
    return g.db


def _get_sqlite_connection():
    """Create SQLite connection."""
    try:
        db_path = current_app.config.get("SQLITE_DB_PATH", "app.db")
        
        # Ensure directory exists
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
        
        logger.debug(f"Connecting to SQLite database: {db_path}")
        
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        
        # Create tables on first connect
        _create_sqlite_tables(conn)
        
        logger.debug("SQLite connection established successfully")
        return conn
        
    except Exception as exc:
        logger.error(f"SQLite connection failed: {exc}")
        raise RuntimeError(f"Failed to connect to SQLite database: {exc}")


def _get_mysql_connection():
    """Create MySQL connection."""
    try:
        import mysql.connector
        
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
        logger.debug(f"Connecting to MySQL database: {safe_config}")
        
        conn = mysql.connector.connect(**config_dict)
        logger.debug("MySQL connection established successfully")
        return conn
        
    except Exception as exc:
        logger.error(f"MySQL connection failed: {exc}")
        raise RuntimeError(f"Failed to connect to MySQL database: {exc}")


def _create_sqlite_tables(conn):
    """Create SQLite tables if they don't exist."""
    cursor = conn.cursor()
    try:
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Yoga poses table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS yoga_poses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pose_name TEXT UNIQUE NOT NULL,
                description TEXT,
                difficulty_level TEXT,
                benefits TEXT,
                precautions TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # User pose history
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_pose_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                pose_id INTEGER NOT NULL,
                accuracy_score REAL DEFAULT 0,
                duration_seconds INTEGER DEFAULT 0,
                feedback TEXT,
                image_path TEXT,
                performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (pose_id) REFERENCES yoga_poses(id) ON DELETE CASCADE
            )
        """)
        
        # Recommendations
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                recommended_pose_ids TEXT,
                recommendation_reason TEXT,
                generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        
        conn.commit()
        logger.debug("SQLite tables created/verified")
        
    except Exception as exc:
        logger.error(f"Failed to create SQLite tables: {exc}")
        raise
    finally:
        cursor.close()


def execute(query: str, values: tuple = ()) -> None:
    """Run a write query (INSERT / UPDATE / DELETE)."""
    db = get_db()
    
    if isinstance(db, sqlite3.Connection):
        cursor = db.cursor()
    else:
        cursor = db.cursor()
    
    try:
        cursor.execute(query, values)
        db.commit()
        logger.debug(f"Query executed successfully: {query[:100]}...")
    except Exception as exc:
        try:
            db.rollback()
        except:
            pass
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

