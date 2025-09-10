"""
Raw data preparation pipeline
"""
from __future__ import annotations

import logging

import pandas as pd

logger = logging.getLogger(__name__)

def run_pipeline(cfg: dict):
    logger.debug("Running raw data pipeline with config: %s", cfg)

    # pokracuj pripravou raw dat do cilove pozice a 00 slozky, odkud si to muzou vzit dalsi
    #   - daily, weekly closed price - staci jen 2 akcie !!! (AAPL, MSFT) ???
    #  TODO - co je to adjusted close?
    #   - earnings jsou dulezite
    