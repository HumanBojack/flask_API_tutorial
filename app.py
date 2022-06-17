# run.py

#! /usr/bin/env python
from api_modele_demo import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
