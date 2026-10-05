"""Entry point ba cPanel "Setup Python App" (Passenger). Hanesan wsgi.py Django nian."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sismdi.settings")

from sismdi.wsgi import application  # noqa: E402
