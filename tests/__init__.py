#!/usr/bin/env python3
from application import app

app.testing = True
test_app = app.test_client()
