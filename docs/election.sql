BEGIN;
--
-- Create model ElectionLevel
--
CREATE TABLE "election_levels" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
    "name" varchar(100) NOT NULL, 
    "code" varchar(50) NOT NULL UNIQUE, 
    "type" varchar(20) NOT NULL, 
    "description" text NOT NULL, 
    "created_at" datetime NOT NULL, 
    "updated_at" datetime NOT NULL, 
    "course_id" bigint NULL REFERENCES "courses" ("id") DEFERRABLE INITIALLY DEFERRED, 
    "state_id" bigint NULL REFERENCES "states" ("id") DEFERRABLE INITIALLY DEFERRED
    );
--
-- Create model Election
--
CREATE TABLE "elections" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
    "title" varchar(200) NOT NULL, 
    "description" text NOT NULL, 
    "start_date" datetime NOT NULL, 
    "end_date" datetime NOT NULL, 
    "is_active" bool NOT NULL, 
    "has_ended" bool NOT NULL, 
    "created_at" datetime NOT NULL, 
    "updated_at" datetime NOT NULL
    );

CREATE TABLE "elections_levels" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
    "election_id" bigint NOT NULL REFERENCES "elections" ("id") DEFERRABLE INITIALLY DEFERRED, 
    "electionlevel_id" bigint NOT NULL REFERENCES "election_levels" ("id") DEFERRABLE INITIALLY DEFERRED
    );
--
-- Create model Position
--
CREATE TABLE "positions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(100) NOT NULL, "description" text NOT NULL, "gender_restriction" varchar(10) NOT NULL, "election_level_id" bigint NOT NULL REFERENCES "election_levels" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Candidate
--
CREATE TABLE "candidates" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "bio" text NOT NULL, "platform" text NOT NULL, "image" varchar(100) NULL, "vote_count" integer unsigned NOT NULL CHECK ("vote_count" >= 0), "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "user_id" bigint NOT NULL REFERENCES "users" ("id") DEFERRABLE INITIALLY DEFERRED, "election_id" bigint NOT NULL REFERENCES "elections" ("id") DEFERRABLE INITIALLY DEFERRED, "position_id" bigint NOT NULL REFERENCES "positions" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model VoterToken
--
CREATE TABLE "voter_tokens" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "token" char(32) NOT NULL UNIQUE, "is_used" bool NOT NULL, "expiry_date" datetime NOT NULL, "created_at" datetime NOT NULL, "used_at" datetime NULL, "election_id" bigint NOT NULL REFERENCES "elections" ("id") DEFERRABLE INITIALLY DEFERRED, "election_level_id" bigint NOT NULL REFERENCES "election_levels" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" bigint NOT NULL REFERENCES "users" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Vote
--
CREATE TABLE "votes" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "timestamp" datetime NOT NULL, "candidate_id" bigint NOT NULL REFERENCES "candidates" ("id") DEFERRABLE INITIALLY DEFERRED, "election_id" bigint NOT NULL REFERENCES "elections" ("id") DEFERRABLE INITIALLY DEFERRED, "election_level_id" bigint NOT NULL REFERENCES "election_levels" ("id") DEFERRABLE INITIALLY DEFERRED, "voter_id" bigint NOT NULL REFERENCES "users" ("id") DEFERRABLE INITIALLY DEFERRED, "token_id" bigint NOT NULL REFERENCES "voter_tokens" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create index election_le_type_29e554_idx on field(s) type of model electionlevel
--
CREATE INDEX "election_le_type_29e554_idx" ON "election_levels" ("type");
--
-- Create index election_le_code_4e1f4d_idx on field(s) code of model electionlevel
--
CREATE INDEX "election_le_code_4e1f4d_idx" ON "election_levels" ("code");
--
-- Create index election_le_course__d77c5a_idx on field(s) course of model electionlevel
--
CREATE INDEX "election_le_course__d77c5a_idx" ON "election_levels" ("course_id");
--
-- Create index election_le_state_i_412196_idx on field(s) state of model electionlevel
--
CREATE INDEX "election_le_state_i_412196_idx" ON "election_levels" ("state_id");
--
-- Create index elections_is_acti_1ae71f_idx on field(s) is_active of model election
--
CREATE INDEX "elections_is_acti_1ae71f_idx" ON "elections" ("is_active");
--
-- Create index elections_start_d_1e140f_idx on field(s) start_date of model election
--
CREATE INDEX "elections_start_d_1e140f_idx" ON "elections" ("start_date");
--
-- Create index elections_end_dat_dec9a5_idx on field(s) end_date of model election
--
CREATE INDEX "elections_end_dat_dec9a5_idx" ON "elections" ("end_date");
--
-- Create index elections_has_end_4d2ca6_idx on field(s) has_ended of model election
--
CREATE INDEX "elections_has_end_4d2ca6_idx" ON "elections" ("has_ended");
--
-- Create index positions_electio_ed7155_idx on field(s) election_level of model position
--
CREATE INDEX "positions_electio_ed7155_idx" ON "positions" ("election_level_id");
--
-- Alter unique_together for position (1 constraint(s))
--
CREATE UNIQUE INDEX "positions_election_level_id_title_gender_restriction_f34808f4_uniq" ON "positions" ("election_level_id", "title", "gender_restriction");
--
-- Create index candidates_electio_728348_idx on field(s) election, position of model candidate
--
CREATE INDEX "candidates_electio_728348_idx" ON "candidates" ("election_id", "position_id");
--
-- Create index candidates_user_id_5d06f1_idx on field(s) user of model candidate
--
CREATE INDEX "candidates_user_id_5d06f1_idx" ON "candidates" ("user_id");
--
-- Alter unique_together for candidate (1 constraint(s))
--
CREATE UNIQUE INDEX "candidates_user_id_election_id_position_id_5b23d648_uniq" ON "candidates" ("user_id", "election_id", "position_id");
--
-- Create index voter_token_token_b5825a_idx on field(s) token of model votertoken
--
CREATE INDEX "voter_token_token_b5825a_idx" ON "voter_tokens" ("token");
--
-- Create index voter_token_electio_efd272_idx on field(s) election, election_level of model votertoken
--
CREATE INDEX "voter_token_electio_efd272_idx" ON "voter_tokens" ("election_id", "election_level_id");
--
-- Create index voter_token_is_used_3b1752_idx on field(s) is_used of model votertoken
--
CREATE INDEX "voter_token_is_used_3b1752_idx" ON "voter_tokens" ("is_used");
--
-- Create index voter_token_expiry__b72f94_idx on field(s) expiry_date of model votertoken
--
CREATE INDEX "voter_token_expiry__b72f94_idx" ON "voter_tokens" ("expiry_date");
--
-- Alter unique_together for votertoken (1 constraint(s))
--
CREATE UNIQUE INDEX "voter_tokens_user_id_election_id_election_level_id_54f7f093_uniq" ON "voter_tokens" ("user_id", "election_id", "election_level_id");
--
-- Create index votes_token_i_f9f50e_idx on field(s) token of model vote
--
CREATE INDEX "votes_token_i_f9f50e_idx" ON "votes" ("token_id");
--
-- Create index votes_candida_da1a33_idx on field(s) candidate of model vote
--
CREATE INDEX "votes_candida_da1a33_idx" ON "votes" ("candidate_id");
--
-- Create index votes_electio_d151b1_idx on field(s) election, election_level of model vote
--
CREATE INDEX "votes_electio_d151b1_idx" ON "votes" ("election_id", "election_level_id");
--
-- Create index votes_timesta_19f1d5_idx on field(s) timestamp of model vote
--
CREATE INDEX "votes_timesta_19f1d5_idx" ON "votes" ("timestamp");
--
-- Alter unique_together for vote (1 constraint(s))
--
CREATE UNIQUE INDEX "votes_token_id_91897528_uniq" ON "votes" ("token_id");
CREATE INDEX "election_levels_course_id_e1bd6928" ON "election_levels" ("course_id");
CREATE INDEX "election_levels_state_id_594e57d3" ON "election_levels" ("state_id");
CREATE UNIQUE INDEX "elections_levels_election_id_electionlevel_id_855c8e38_uniq" ON "elections_levels" ("election_id", "electionlevel_id");
CREATE INDEX "elections_levels_election_id_aab898de" ON "elections_levels" ("election_id");
CREATE INDEX "elections_levels_electionlevel_id_f7727ce5" ON "elections_levels" ("electionlevel_id");
CREATE INDEX "positions_election_level_id_2d2da813" ON "positions" ("election_level_id");
CREATE INDEX "candidates_user_id_38b3e027" ON "candidates" ("user_id");
CREATE INDEX "candidates_election_id_0fe542d7" ON "candidates" ("election_id");
CREATE INDEX "candidates_position_id_b99e8a5d" ON "candidates" ("position_id");
CREATE INDEX "voter_tokens_election_id_f18b2044" ON "voter_tokens" ("election_id");
CREATE INDEX "voter_tokens_election_level_id_b4870bec" ON "voter_tokens" ("election_level_id");
CREATE INDEX "voter_tokens_user_id_4f76fa6d" ON "voter_tokens" ("user_id");
CREATE INDEX "votes_candidate_id_cfd70f5d" ON "votes" ("candidate_id");
CREATE INDEX "votes_election_id_df4ef8dd" ON "votes" ("election_id");
CREATE INDEX "votes_election_level_id_cbf13ba0" ON "votes" ("election_level_id");
CREATE INDEX "votes_voter_id_bb8b944b" ON "votes" ("voter_id");
CREATE INDEX "votes_token_id_91897528" ON "votes" ("token_id");
COMMIT;
