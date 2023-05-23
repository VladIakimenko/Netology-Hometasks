GET_NAMES = """\
SELECT *
  FROM clients;"""

GET_PHONES = """\
SELECT phone
  FROM phones
 WHERE phone_owner = <client_id>;"""
 
GET_EMAILS = """\
SELECT email
  FROM emails
 WHERE email_owner = <client_id>;"""
 
FIND_CLIENT = """\
   SELECT c.client_id, c.first_name, c.last_name
     FROM clients c
LEFT JOIN phones ph ON c.client_id = ph.phone_owner
LEFT JOIN emails e  ON c.client_id = e.email_owner
    WHERE c.first_name ILIKE '%<value>%'
 	   OR c.last_name  ILIKE '%<value>%'
 	   OR ph.phone ILIKE '%<value>%'
 	   OR e.email  ILIKE '%<value>%';"""

 	
CHANGE_RECORD = """\
UPDATE <table>
   SET <column> = '<new_value>'
 WHERE <id_column> = '<id>';"""
