"""
Database Setup Script
Run this once to create database and tables
"""

import mysql.connector
from mysql.connector import Error
from typing import List, Dict, Optional, Tuple
import logging
import os

from config_entity import DatabaseConfig

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, config=DatabaseConfig):
        self.config = config
        self.connection_pool = None
        
        if config.enabled:
            self._create_connection_pool()

    def _create_connection_pool(self):
        self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name="finews_pool",
            pool_size=self.config.pool_size,
            pool_reset_session=True,
            host=self.config.host,
            port=self.config.port,
            database=self.config.database,
            user=self.config.user,
            password=self.config.password,
            charset=self.config.charset
        )
        logger.info("MySQL connection pool created")

    def get_connection(self):
        if not self.config.enabled or not self.connection_pool:
            return None
        try:
            return self.connection_pool.get_connection()
        except Error as e:
            logger.error(f"Error getting connection: {e}")
            return None
        
    

    