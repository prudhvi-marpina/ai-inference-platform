"""
Root-level pytest configuration.

This file adds the project root to Python's path so that
pytest can find the 'app' module when running tests.
"""

import sys
from pathlib import Path

# Get the project root directory (where this file is located)
project_root = Path(__file__).parent

# Add project root to Python path if not already there
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

