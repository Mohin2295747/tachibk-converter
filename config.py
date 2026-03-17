import os
from pathlib import Path

# Directory structure
BASE_DIR = Path.cwd()
OUTPUT_DIR = BASE_DIR / "output"
BACKUP_DIR = BASE_DIR / "backup"
SCHEMA_DIR = BASE_DIR / "schemas"
EXPLAIN_DIR = BASE_DIR / "explain"
MANGA_DIR = BASE_DIR / "manga"

# File rotation
ROTATION_LIMIT = 5
ROTATION_FILE = OUTPUT_DIR / "rotation_counter.txt"
OUTPUT_BASENAME = "output_{}.json"

# Fork configurations
FORKS = {
    'mihon': 'mihonapp/mihon',
    'sy': 'jobobby04/TachiyomiSY',
    'j2k': 'Jays2Kings/tachiyomiJ2K',
    'yokai': 'null2264/yokai',
    'komikku': 'komikku-app/komikku',
}

# Ensure directories exist
for directory in [OUTPUT_DIR, BACKUP_DIR, SCHEMA_DIR, EXPLAIN_DIR, MANGA_DIR]:
    directory.mkdir(exist_ok=True)