-- this file was manually created
INSERT INTO public.users (display_name, handle, email,bio,cognito_user_id)
VALUES
  ('Shehzad Ali', 'shehzad','shehzadashiq@yahoo.com','NothingSoFar','MOCK'),
  ('Alt Shehzad','shehzad3','shehzadashiq@gmail.com' , 'altShehzad' ,'MOCK'),
  ('Andrew Bayko', 'bayko','bayko@exampro.co','NothingSoFar','MOCK'),
  ('Andrew Brown', 'andrewbrown','andrew@exampro.co','NothingSoFar','MOCK');


INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
  (
    (SELECT uuid from public.users WHERE users.handle = 'shehzad' LIMIT 1),
    'This was imported as seed data!',
    current_timestamp + interval '10 day'
  )
