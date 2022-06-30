import json
from flask import redirect, url_for

def decode_json(payload):
  return json.loads(payload.decode('utf-8'))

def commit_or_redirect(db, failure, success=None):
  try:
    db.session.commit()
    if success:
      return redirect(url_for(success))
  except:
    return redirect(url_for(failure))