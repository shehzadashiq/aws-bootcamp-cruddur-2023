require 'aws-sdk-s3'
require 'json'

workspace_id = ENV['GITPOD_WORKSPACE_ID']
workspace_cluster_host = ENV['GITPOD_WORKSPACE_CLUSTER_HOST']

workspace_url = "https://#{workspace_id}.#{workspace_cluster_host}"

puts "Workspace URL: #{workspace_url}"

def handler(event:, context:)
  puts event
  s3 = Aws::S3::Resource.new
  bucket_name = ENV["UPLOADS_BUCKET_NAME"]
  object_key = 'mock.jpg'

  obj = s3.bucket(bucket_name).object(object_key)
  url = obj.presigned_url(:put, expires_in: 60 * 5)
  url # this is the data that will be returned
  body = {url: url}.to_json
  { statusCode: 200, body: body }
end

puts handler(
  event: {},
  context: {}
)