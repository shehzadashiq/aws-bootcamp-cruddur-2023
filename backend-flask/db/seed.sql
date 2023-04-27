-- this file was manually created
INSERT INTO public.users (display_name, handle, email,cognito_user_id,bio)
VALUES
  ('Shehzad Ali', 'shehzad','shehzad@exampro.co' ,'MOCK',"NothingSoFar"),
  ('Andrew Bayko', 'bayko','bayko@exampro.co' ,'MOCK',"NothingSoFar"),
  ('Andrew Brown', 'andrewbrown','andrew@exampro.co','MOCK',"NothingSoFar");


INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
  (
    (SELECT uuid from public.users WHERE users.handle = 'shehzad' LIMIT 1),
    'This was imported as seed data!',
    current_timestamp + interval '10 day'
  )
