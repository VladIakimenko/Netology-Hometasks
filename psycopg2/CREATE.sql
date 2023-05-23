CREATE TABLE clients 
(
    PRIMARY KEY (client_id),
    client_id   SERIAL, 
    first_name  VARCHAR(60)  NOT NULL,
    last_name   VARCHAR(60)  NOT NULL
);


CREATE TABLE phones 
(
    PRIMARY KEY (phone_id),
    phone_id  	  SERIAL,
    phone         VARCHAR(30)  NOT NULL  UNIQUE,
    phone_owner	  INTEGER	   NOT NULL  REFERENCES clients(client_id)
);


CREATE TABLE emails 
(
    PRIMARY KEY (email_id),
    email_id  	  SERIAL,
    email         VARCHAR(60)  NOT NULL  UNIQUE, 
    email_owner	  INTEGER	   NOT NULL  REFERENCES clients(client_id)
);

