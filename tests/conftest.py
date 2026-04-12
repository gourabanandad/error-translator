import sys
from pathlib import Path

# Ensure the repository root is importable when tests run without editable install.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
