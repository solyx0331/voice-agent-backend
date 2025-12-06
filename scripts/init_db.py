"""
Database initialization script (standalone)
Run this script to initialize the database and create sample data
"""
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db.init_db import main
import asyncio

if __name__ == "__main__":
    asyncio.run(main())

