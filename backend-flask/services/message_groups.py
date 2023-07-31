from datetime import datetime, timedelta, timezone
from lib.ddb import Ddb
from lib.db import db
from lib.appsync import AppSync

class MessageGroups:
  def run(cognito_user_id):
    model = {
      'errors': None,
      'data': None
    }
    
    print("cognito_user_id in message_groups.py")
    print(cognito_user_id)
    

    sql = db.template('users','uuid_from_cognito_user_id')
    my_user_uuid = db.query_value(sql,{'cognito_user_id': cognito_user_id})

    print(f"UUID: {my_user_uuid}")
    
    ddb = Ddb.client()
    appsync = AppSync.client()
    # appsync = AppSync()

    # First, create an instance of the AppSync class
    # app_sync = AppSync()

    # This is where as a test we can use AppSync to simply return the results from it
    data=[]
    # data = Ddb.list_message_groups(ddb, my_user_uuid)
    # 4fa2d4e6-11f3-4b39-9ec8-a421d4faaa0a

    # Having to remove this as an error is generated in the GUI unfortunately
    # data = appsync.test_mutation()
    print("Invoking list message groups")
    data = AppSync.list_message_groups(appsync,my_user_uuid)      
    

    print("list_message_groups:", data)
    
    model['data'] = data
    return model