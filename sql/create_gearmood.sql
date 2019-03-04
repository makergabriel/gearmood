CREATE TABLE shake(
 id serial PRIMARY KEY,
 subreddit_id VARCHAR (50),
 submission_id VARCHAR (50),
 title VARCHAR (300),
 data jsonb
);