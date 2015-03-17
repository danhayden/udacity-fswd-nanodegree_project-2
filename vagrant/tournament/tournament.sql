-- -----------------------------------------------------------------------------
--
-- Table definitions for the tournament project
--
-- -----------------------------------------------------------------------------


--
-- Connect to tournament database
--

\connect tournament


--
-- Create player table
--

DROP TABLE IF EXISTS player CASCADE;
CREATE TABLE player (
  player_id serial PRIMARY KEY,
  player_name text
);


--
-- Create match table
--

DROP TABLE IF EXISTS match CASCADE;
CREATE TABLE match (
  match_id serial PRIMARY KEY,
  winner INT,
  loser INT,
  FOREIGN KEY (winner) REFERENCES player(player_id),
  FOREIGN KEY (loser) REFERENCES player(player_id)
);


--
-- Create standings view
--

DROP VIEW IF EXISTS standings;
CREATE VIEW standings AS
SELECT
  player_id,
  player_name,
  (SELECT count(*) FROM match WHERE player_id = winner) as wins,
  (SELECT count(*) FROM match WHERE player_id in (winner, loser)) as matches
FROM player
GROUP BY player_id
ORDER BY wins DESC;
