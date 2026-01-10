"""
Database Manager for AquaVision AI
Handles all database operations for detection history, user profiles, and community features
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import os

class DatabaseManager:
    """Manages SQLite database for AquaVision AI"""
    
    def __init__(self, db_path: str = "aquavision.db"):
        """Initialize database connection and create tables if needed"""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        """Establish database connection"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Enable dict-like access
        self.cursor = self.conn.cursor()
    
    def create_tables(self):
        """Create all necessary tables"""
        
        # Detection History Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS detections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                image_path TEXT,
                species TEXT NOT NULL,
                disease TEXT NOT NULL,
                species_confidence REAL,
                disease_confidence REAL,
                treatment_applied TEXT,
                notes TEXT,
                gradcam_path TEXT,
                alert_sent BOOLEAN DEFAULT 0
            )
        ''')
        
        # User Profiles Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                location TEXT,
                join_date TEXT NOT NULL,
                profile_image TEXT,
                bio TEXT,
                total_detections INTEGER DEFAULT 0,
                expert_verified BOOLEAN DEFAULT 0
            )
        ''')
        
        # Community Posts Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS community_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                timestamp TEXT NOT NULL,
                image_path TEXT NOT NULL,
                species TEXT,
                disease TEXT,
                description TEXT,
                verification_count INTEGER DEFAULT 0,
                expert_verified BOOLEAN DEFAULT 0,
                location TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Post Comments Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS post_comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id INTEGER,
                user_id INTEGER,
                timestamp TEXT NOT NULL,
                comment TEXT NOT NULL,
                is_expert BOOLEAN DEFAULT 0,
                FOREIGN KEY (post_id) REFERENCES community_posts(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Treatment Success Stories
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS success_stories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                disease TEXT NOT NULL,
                treatment_method TEXT NOT NULL,
                duration_days INTEGER,
                success_rate INTEGER,
                before_image TEXT,
                after_image TEXT,
                description TEXT,
                timestamp TEXT NOT NULL,
                helpful_count INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Alerts Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                detection_id INTEGER,
                alert_type TEXT NOT NULL,
                sent_at TEXT NOT NULL,
                read_at TEXT,
                message TEXT,
                FOREIGN KEY (detection_id) REFERENCES detections(id)
            )
        ''')
        
        # Water Quality Logs
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS water_quality (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                pH REAL,
                temperature REAL,
                ammonia REAL,
                nitrite REAL,
                nitrate REAL,
                notes TEXT
            )
        ''')
        
        # Multi-Fish Detections
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS multi_fish_detections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                parent_detection_id INTEGER,
                fish_index INTEGER,
                bbox_x INTEGER,
                bbox_y INTEGER,
                bbox_width INTEGER,
                bbox_height INTEGER,
                species TEXT,
                disease TEXT,
                confidence REAL,
                FOREIGN KEY (parent_detection_id) REFERENCES detections(id)
            )
        ''')
        
        self.conn.commit()
    
    # ==================== DETECTION HISTORY ====================
    
    def add_detection(self, species: str, disease: str, image_path: str = None,
                     species_conf: float = 0.0, disease_conf: float = 0.0,
                     notes: str = None, gradcam_path: str = None) -> int:
        """Add a new detection to history"""
        timestamp = datetime.now().isoformat()
        
        self.cursor.execute('''
            INSERT INTO detections 
            (timestamp, image_path, species, disease, species_confidence, 
             disease_confidence, notes, gradcam_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (timestamp, image_path, species, disease, species_conf, 
              disease_conf, notes, gradcam_path))
        
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_detection_history(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Get recent detection history"""
        self.cursor.execute('''
            SELECT * FROM detections
            ORDER BY timestamp DESC
            LIMIT ? OFFSET ?
        ''', (limit, offset))
        
        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_detection_stats(self) -> Dict:
        """Get statistics about detections"""
        self.cursor.execute('SELECT COUNT(*) as total FROM detections')
        total = self.cursor.fetchone()['total']
        
        self.cursor.execute('''
            SELECT disease, COUNT(*) as count 
            FROM detections 
            GROUP BY disease
            ORDER BY count DESC
        ''')
        by_disease = [dict(row) for row in self.cursor.fetchall()]
        
        self.cursor.execute('''
            SELECT species, COUNT(*) as count 
            FROM detections 
            GROUP BY species
            ORDER BY count DESC
        ''')
        by_species = [dict(row) for row in self.cursor.fetchall()]
        
        return {
            'total_detections': total,
            'by_disease': by_disease,
            'by_species': by_species
        }
    
    def search_detections(self, species: str = None, disease: str = None,
                          start_date: str = None, end_date: str = None) -> List[Dict]:
        """Search detection history with filters"""
        query = 'SELECT * FROM detections WHERE 1=1'
        params = []
        
        if species:
            query += ' AND species LIKE ?'
            params.append(f'%{species}%')
        
        if disease:
            query += ' AND disease LIKE ?'
            params.append(f'%{disease}%')
        
        if start_date:
            query += ' AND timestamp >= ?'
            params.append(start_date)
        
        if end_date:
            query += ' AND timestamp <= ?'
            params.append(end_date)
        
        query += ' ORDER BY timestamp DESC'
        
        self.cursor.execute(query, params)
        return [dict(row) for row in self.cursor.fetchall()]
    
    def update_detection_notes(self, detection_id: int, notes: str):
        """Update notes for a detection"""
        self.cursor.execute('''
            UPDATE detections SET notes = ? WHERE id = ?
        ''', (notes, detection_id))
        self.conn.commit()
    
    def mark_treatment_applied(self, detection_id: int, treatment: str):
        """Mark treatment as applied for a detection"""
        self.cursor.execute('''
            UPDATE detections SET treatment_applied = ? WHERE id = ?
        ''', (treatment, detection_id))
        self.conn.commit()
    
    # ==================== ALERTS ====================
    
    def add_alert(self, detection_id: int, alert_type: str, message: str) -> int:
        """Create a new alert"""
        sent_at = datetime.now().isoformat()
        
        self.cursor.execute('''
            INSERT INTO alerts (detection_id, alert_type, sent_at, message)
            VALUES (?, ?, ?, ?)
        ''', (detection_id, alert_type, sent_at, message))
        
        # Mark detection as alert sent
        self.cursor.execute('''
            UPDATE detections SET alert_sent = 1 WHERE id = ?
        ''', (detection_id,))
        
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_unread_alerts(self) -> List[Dict]:
        """Get all unread alerts"""
        self.cursor.execute('''
            SELECT * FROM alerts WHERE read_at IS NULL
            ORDER BY sent_at DESC
        ''')
        return [dict(row) for row in self.cursor.fetchall()]
    
    def mark_alert_read(self, alert_id: int):
        """Mark an alert as read"""
        read_at = datetime.now().isoformat()
        self.cursor.execute('''
            UPDATE alerts SET read_at = ? WHERE id = ?
        ''', (read_at, alert_id))
        self.conn.commit()
    
    # ==================== COMMUNITY FEATURES ====================
    
    def create_user(self, username: str, email: str, location: str = None) -> int:
        """Create a new user profile"""
        join_date = datetime.now().isoformat()
        
        self.cursor.execute('''
            INSERT INTO users (username, email, location, join_date)
            VALUES (?, ?, ?, ?)
        ''', (username, email, location, join_date))
        
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_user(self, user_id: int = None, username: str = None) -> Optional[Dict]:
        """Get user by ID or username"""
        if user_id:
            self.cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        elif username:
            self.cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        else:
            return None
        
        row = self.cursor.fetchone()
        return dict(row) if row else None
    
    def create_community_post(self, user_id: int, image_path: str, species: str,
                             disease: str, description: str, location: str = None) -> int:
        """Create a new community post"""
        timestamp = datetime.now().isoformat()
        
        self.cursor.execute('''
            INSERT INTO community_posts 
            (user_id, timestamp, image_path, species, disease, description, location)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, timestamp, image_path, species, disease, description, location))
        
        # Increment user's total detections
        self.cursor.execute('''
            UPDATE users SET total_detections = total_detections + 1 
            WHERE id = ?
        ''', (user_id,))
        
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_community_feed(self, limit: int = 50, location: str = None) -> List[Dict]:
        """Get community feed with optional location filter"""
        if location:
            self.cursor.execute('''
                SELECT p.*, u.username, u.expert_verified as user_is_expert
                FROM community_posts p
                JOIN users u ON p.user_id = u.id
                WHERE p.location LIKE ?
                ORDER BY p.timestamp DESC
                LIMIT ?
            ''', (f'%{location}%', limit))
        else:
            self.cursor.execute('''
                SELECT p.*, u.username, u.expert_verified as user_is_expert
                FROM community_posts p
                JOIN users u ON p.user_id = u.id
                ORDER BY p.timestamp DESC
                LIMIT ?
            ''', (limit,))
        
        return [dict(row) for row in self.cursor.fetchall()]
    
    def add_post_comment(self, post_id: int, user_id: int, comment: str) -> int:
        """Add a comment to a post"""
        timestamp = datetime.now().isoformat()
        
        # Get user expert status
        user = self.get_user(user_id=user_id)
        is_expert = user['expert_verified'] if user else False
        
        self.cursor.execute('''
            INSERT INTO post_comments (post_id, user_id, timestamp, comment, is_expert)
            VALUES (?, ?, ?, ?, ?)
        ''', (post_id, user_id, timestamp, comment, is_expert))
        
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_post_comments(self, post_id: int) -> List[Dict]:
        """Get all comments for a post"""
        self.cursor.execute('''
            SELECT c.*, u.username 
            FROM post_comments c
            JOIN users u ON c.user_id = u.id
            WHERE c.post_id = ?
            ORDER BY c.timestamp ASC
        ''', (post_id,))
        
        return [dict(row) for row in self.cursor.fetchall()]
    
    def add_success_story(self, user_id: int, disease: str, treatment_method: str,
                          duration_days: int, success_rate: int, description: str,
                          before_image: str = None, after_image: str = None) -> int:
        """Add a treatment success story"""
        timestamp = datetime.now().isoformat()
        
        self.cursor.execute('''
            INSERT INTO success_stories 
            (user_id, disease, treatment_method, duration_days, success_rate,
             before_image, after_image, description, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, disease, treatment_method, duration_days, success_rate,
              before_image, after_image, description, timestamp))
        
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_success_stories(self, disease: str = None, limit: int = 20) -> List[Dict]:
        """Get success stories, optionally filtered by disease"""
        if disease:
            self.cursor.execute('''
                SELECT s.*, u.username 
                FROM success_stories s
                JOIN users u ON s.user_id = u.id
                WHERE s.disease LIKE ?
                ORDER BY s.helpful_count DESC, s.timestamp DESC
                LIMIT ?
            ''', (f'%{disease}%', limit))
        else:
            self.cursor.execute('''
                SELECT s.*, u.username 
                FROM success_stories s
                JOIN users u ON s.user_id = u.id
                ORDER BY s.helpful_count DESC, s.timestamp DESC
                LIMIT ?
            ''', (limit,))
        
        return [dict(row) for row in self.cursor.fetchall()]
    
    # ==================== MULTI-FISH DETECTION ====================
    
    def add_multi_fish_detection(self, parent_id: int, fish_index: int,
                                 bbox: Tuple[int, int, int, int], species: str,
                                 disease: str, confidence: float):
        """Add a single fish from multi-fish detection"""
        x, y, w, h = bbox
        
        self.cursor.execute('''
            INSERT INTO multi_fish_detections
            (parent_detection_id, fish_index, bbox_x, bbox_y, bbox_width, bbox_height,
             species, disease, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (parent_id, fish_index, x, y, w, h, species, disease, confidence))
        
        self.conn.commit()
    
    def get_multi_fish_results(self, parent_id: int) -> List[Dict]:
        """Get all fish from a multi-fish detection"""
        self.cursor.execute('''
            SELECT * FROM multi_fish_detections
            WHERE parent_detection_id = ?
            ORDER BY fish_index
        ''', (parent_id,))
        
        return [dict(row) for row in self.cursor.fetchall()]
    
    # ==================== WATER QUALITY ====================
    
    def add_water_quality_log(self, pH: float = None, temperature: float = None,
                              ammonia: float = None, nitrite: float = None,
                              nitrate: float = None, notes: str = None):
        """Log water quality parameters"""
        timestamp = datetime.now().isoformat()
        
        self.cursor.execute('''
            INSERT INTO water_quality 
            (timestamp, pH, temperature, ammonia, nitrite, nitrate, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (timestamp, pH, temperature, ammonia, nitrite, nitrate, notes))
        
        self.conn.commit()
    
    def get_water_quality_history(self, days: int = 30) -> List[Dict]:
        """Get water quality history for specified days"""
        cutoff_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        cutoff_date = cutoff_date.isoformat()
        
        self.cursor.execute('''
            SELECT * FROM water_quality
            WHERE timestamp >= date('now', '-' || ? || ' days')
            ORDER BY timestamp DESC
        ''', (days,))
        
        return [dict(row) for row in self.cursor.fetchall()]
    
    # ==================== UTILITY ====================
    
    def export_to_json(self, output_file: str = "aquavision_export.json"):
        """Export all data to JSON file"""
        data = {
            'detections': self.get_detection_history(limit=10000),
            'stats': self.get_detection_stats(),
            'alerts': self.get_unread_alerts(),
            'export_date': datetime.now().isoformat()
        }
        
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        return output_file
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def __del__(self):
        """Cleanup on deletion"""
        self.close()


# Singleton instance
_db_instance = None

def get_database() -> DatabaseManager:
    """Get singleton database instance"""
    global _db_instance
    if _db_instance is None:
        _db_instance = DatabaseManager()
    return _db_instance
