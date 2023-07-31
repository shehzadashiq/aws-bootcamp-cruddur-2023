require 'aws-sdk-s3'
require 'json'
require 'jwt'

# workspace_id = ENV['GITPOD_WORKSPACE_ID']
# workspace_cluster_host = ENV['GITPOD_WORKSPACE_CLUSTER_HOST']

# workspace_url = "https://#{workspace_id}.#{workspace_cluster_host}"

# puts "Workspace URL: #{workspace_url}"

def handler(event:, context:)
  puts event
  # return cors headers for preflight check
  if event['routeKey'] == "OPTIONS /{proxy+}"
    puts({step: 'preflight', message: 'preflight CORS check'}.to_json)
    { 
      headers: {
        "Access-Control-Allow-Headers": "*, Authorization",
        "Access-Control-Allow-Origin": "https://tajarba.com",
        # "Access-Control-Allow-Origin": workspace_url,
        "Access-Control-Allow-Methods": "OPTIONS,GET,POST,PUT"
      },
      statusCode: 200
    }
  else
    token = event['headers']['authorization'].split(' ')[1]
    puts({step: 'presignedurl', access_token: token}.to_json)

    body_hash = JSON.parse(event["body"])
    extension = body_hash["extension"]

    decoded_token = JWT.decode token, nil, false
    cognito_user_uuid = decoded_token[0]['sub']

    s3 = Aws::S3::Resource.new
    bucket_name = ENV["UPLOADS_BUCKET_NAME"]
    object_key = "#{cognito_user_uuid}.#{extension}"

    puts({object_key: object_key}.to_json)

    obj = s3.bucket(bucket_name).object(object_key)
    url = obj.presigned_url(:put, expires_in: 60 * 5)
    url # this is the data that will be returned
    body = {url: url}.to_json
    { 
      headers: {
        "Access-Control-Allow-Headers": "*, Authorization",
        "Access-Control-Allow-Origin": "https://tajarba.com",
        # "Access-Control-Allow-Origin": workspace_url,
        "Access-Control-Allow-Methods": "OPTIONS,GET,POST,PUT"
      },
      statusCode: 200, 
      body: body 
    }
  end # if 
end # def handler