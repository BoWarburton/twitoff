#!/usr/bin/env python
"""
Entry point for the TwitOff Flask web application.
"""
from .app import create_app

APP = create_app()
