# run.py

#! /usr/bin/env python
from application import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
