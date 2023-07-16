import uuid
from datetime import datetime, timedelta, timezone
class CreateReply:
  def run(message, cognito_user_id, activity_uuid):
    model = {
      'errors': None,
      'data': None
    }

    if cognito_user_id == None or len(cognito_user_id) < 1:
      model['errors'] = ['cognito_user_id_blank']

    if activity_uuid == None or len(activity_uuid) < 1:
      model['errors'] = ['activity_uuid_blank']

    if message == None or len(message) < 1:
      model['errors'] = ['message_blank'] 
    elif len(message) > 1024:
      model['errors'] = ['message_exceed_max_chars'] 

    if model['errors']:
      # return what we provided
      model['data'] = {
        # 'display_name': 'Andrew Brown',
        'cognito_user_id':  cognito_user_id,
        'message': message,
        'reply_to_activity_uuid': activity_uuid
      }
    else:
      expires_at = (now + ttl_offset)
      uuid = CreateActivity.create_activity(cognito_user_id,message,expires_at)

      object_json = CreateActivity.query_object_activity(uuid)
      model['data'] = object_json    
    return model