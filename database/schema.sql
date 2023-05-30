CREATE TABLE IF NOT EXISTS blacklist (
  id SERIAL PRIMARY KEY,
  user_id varchar(20) NOT NULL,
  created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS context_message (
  id SERIAL PRIMARY KEY,
  message_id varchar(20) NOT NULL,
  added_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  added_by varchar(20) NOT NULL,
  about varchar(20) NOT NULL
);
