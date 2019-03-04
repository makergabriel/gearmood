CREATE TABLE shake(
 submission_id VARCHAR (50) PRIMARY KEY,
 subreddit_id VARCHAR (50),
 title VARCHAR (300),
 data jsonb
);