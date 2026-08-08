"""Vercel deployment carrier for canonical StegGate.

This module contains no admissibility or policy logic.  It imports the
StegCore HTTP application from an exact Git commit so the Site Vercel
project can provide a bounded alternate deployment carrier while the
canonical Render workspace is capacity-blocked.
"""

from fastapi import FastAPI
from stegcore.service import app as canonical_steggate_app

app = FastAPI(title="StegGate Vercel Carrier", docs_url=None, redoc_url=None)
app.mount("/steggate", canonical_steggate_app)
