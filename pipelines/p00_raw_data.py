"""
Raw data preparation pipeline
"""
from __future__ import annotations

import logging

import pandas as pd

logger = logging.getLogger(__name__)

def run_pipeline(cfg: dict):
    logger.debug("Running raw data pipeline with config: %s", cfg)