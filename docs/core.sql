BEGIN;
--
-- Create model Course
--
CREATE TABLE "courses" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
    "name" varchar(100) NOT NULL, 
    "code" varchar(20) NOT NULL UNIQUE, 
    "created_at" datetime NOT NULL, 
    "updated_at" datetime NOT NULL
    );
--
-- Create model State
--
CREATE TABLE "states" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
    "name" varchar(100) NOT NULL UNIQUE, 
    "created_at" datetime NOT NULL, 
    "updated_at" datetime NOT NULL
    );
--
-- Create model User
--
CREATE TABLE "users" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
    "password" varchar(128) NOT NULL, 
    "last_login" datetime NULL, 
    "is_superuser" bool NOT NULL, 
    "first_name" varchar(150) NOT NULL, 
    "last_name" varchar(150) NOT NULL, 
    "is_staff" bool NOT NULL, 
    "is_active" bool NOT NULL, 
    "date_joined" datetime NOT NULL, 
    "registration_number" varchar(20) NOT NULL UNIQUE, 
    "email" varchar(254) NULL UNIQUE, 
    "voter_id" varchar(36) NULL UNIQUE, 
    "gender" varchar(10) NULL, 
    "role" varchar(20) NOT NULL, 
    "is_verified" bool NOT NULL, 
    "date_verified" datetime NULL, 
    "last_login_ip" char(39) NULL, 
    "course_id" bigint NULL REFERENCES "courses" ("id") DEFERRABLE INITIALLY DEFERRED, 
    "state_id" bigint NULL REFERENCES "states" ("id") DEFERRABLE INITIALLY DEFERRED
    );

CREATE TABLE "users_groups" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
    "user_id" bigint NOT NULL REFERENCES "users" ("id") DEFERRABLE INITIALLY DEFERRED, 
    "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED
    );

CREATE TABLE "users_user_permissions" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
    "user_id" bigint NOT NULL REFERENCES "users" ("id") DEFERRABLE INITIALLY DEFERRED, 
    "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED
    );

--
-- Create model CollegeData
--
CREATE TABLE "college_data" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
    "registration_number" varchar(20) NOT NULL UNIQUE, 
    "first_name" varchar(50) NOT NULL, 
    "last_name" varchar(50) NOT NULL, 
    "email" varchar(254) NOT NULL, 
    "gender" varchar(10) NULL, 
    "voter_id" varchar(36) NULL UNIQUE, 
    "is_used" bool NOT NULL, 
    "created_at" datetime NOT NULL, 
    "status" varchar(20) NOT NULL, 
    "uploaded_by_id" bigint NULL REFERENCES "users" ("id") DEFERRABLE INITIALLY DEFERRED, 
    "course_id" bigint NOT NULL REFERENCES "courses" ("id") DEFERRABLE INITIALLY DEFERRED
    );
--
-- Create index users_registr_4b432d_idx on field(s) registration_number of model user
--
CREATE INDEX "users_registr_4b432d_idx" ON "users" ("registration_number");
--
-- Create index users_role_a93a92_idx on field(s) role, is_verified of model user
--
CREATE INDEX "users_role_a93a92_idx" ON "users" ("role", "is_verified");
--
-- Create index users_state_i_e49108_idx on field(s) state, course of model user
--
CREATE INDEX "users_state_i_e49108_idx" ON "users" ("state_id", "course_id");
--
-- Create index users_email_4b85f2_idx on field(s) email of model user
--
CREATE INDEX "users_email_4b85f2_idx" ON "users" ("email");
--
-- Create index users_gender_c12881_idx on field(s) gender of model user
--
CREATE INDEX "users_gender_c12881_idx" ON "users" ("gender");
--
-- Create index users_voter_i_c1d34a_idx on field(s) voter_id of model user
--
CREATE INDEX "users_voter_i_c1d34a_idx" ON "users" ("voter_id");
CREATE INDEX "courses_code_fa42f1_idx" ON "courses" ("code");
CREATE INDEX "states_name_9db832_idx" ON "states" ("name");
CREATE INDEX "users_course_id_ef7a18fa" ON "users" ("course_id");
CREATE INDEX "users_state_id_0521d641" ON "users" ("state_id");
CREATE UNIQUE INDEX "users_groups_user_id_group_id_fc7788e8_uniq" ON "users_groups" ("user_id", "group_id");
CREATE INDEX "users_groups_user_id_f500bee5" ON "users_groups" ("user_id");
CREATE INDEX "users_groups_group_id_2f3517aa" ON "users_groups" ("group_id");
CREATE UNIQUE INDEX "users_user_permissions_user_id_permission_id_3b86cbdf_uniq" ON "users_user_permissions" ("user_id", "permission_id");
CREATE INDEX "users_user_permissions_user_id_92473840" ON "users_user_permissions" ("user_id");
CREATE INDEX "users_user_permissions_permission_id_6d08dcd2" ON "users_user_permissions" ("permission_id");
CREATE INDEX "college_data_uploaded_by_id_51056561" ON "college_data" ("uploaded_by_id");
CREATE INDEX "college_data_course_id_4ebcfa59" ON "college_data" ("course_id");
CREATE INDEX "college_dat_registr_86e753_idx" ON "college_data" ("registration_number");
CREATE INDEX "college_dat_course__1baf12_idx" ON "college_data" ("course_id", "is_used");
CREATE INDEX "college_dat_status_24a8f1_idx" ON "college_data" ("status");
CREATE INDEX "college_dat_voter_i_fbb903_idx" ON "college_data" ("voter_id");
COMMIT;
