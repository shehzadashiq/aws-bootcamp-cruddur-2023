require 'aws-sdk-s3'
require 'json'
require 'jwt'

client = Aws::S3::Client.new(
  region: region_name,
  credentials: credentials,
  # ...
)