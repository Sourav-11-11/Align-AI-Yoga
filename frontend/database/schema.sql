-- ============================================================================
-- Align AI Yoga - Database Schema
-- ============================================================================
-- Initialize the yoga database with required tables

-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS yoga;
USE yoga;

-- ────────────────────────────────────────────────────────────────────────────
-- Users table: stores user account information
-- ────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ────────────────────────────────────────────────────────────────────────────
-- User sessions: tracks active user sessions (optional)
-- ────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS user_sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    session_token VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_session_token (session_token),
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ────────────────────────────────────────────────────────────────────────────
-- Yoga poses: stores information about yoga poses
-- ────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS yoga_poses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pose_name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    difficulty_level VARCHAR(50),
    benefits TEXT,
    precautions TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_pose_name (pose_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ────────────────────────────────────────────────────────────────────────────
-- User pose history: tracks poses user has performed
-- ────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS user_pose_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    pose_id INT NOT NULL,
    accuracy_score FLOAT,
    duration_seconds INT,
    feedback TEXT,
    performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (pose_id) REFERENCES yoga_poses(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_pose_id (pose_id),
    INDEX idx_performed_at (performed_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ────────────────────────────────────────────────────────────────────────────
-- User recommendations: stores AI-generated yoga recommendations
-- ────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS user_recommendations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    recommended_pose_ids JSON,
    recommendation_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
