SELECT
  users.uuid
FROM public.users
WHERE
  users.cognito_user_id='4fa2d4e6-11f3-4b39-9ec8-a421d4faaa0a'
LIMIT 1