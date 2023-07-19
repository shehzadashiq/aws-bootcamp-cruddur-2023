from lib.db import db
# from aws_xray_sdk.core import xray_recorder

class UserActivities:
  def run(user_handle):
    model = {
      'errors': None,
      'data': None
    }
    
    if user_handle == None or len(user_handle) < 1:
      model['errors'] = ['blank_user_handle']
    else:
      print("else:")
      sql = db.template('users','show')
      results = db.query_object_json(sql,{'handle': user_handle})
      model['data'] = results

    return model