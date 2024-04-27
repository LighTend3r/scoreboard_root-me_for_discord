BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS "db_version" (
	"id"	INTEGER NOT NULL,
	"version"	INTEGER NOT NULL,
	"timestamp"	REAL NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO db_version (version, timestamp) VALUES (1, 1713233164);

CREATE TABLE IF NOT EXISTS "user_rm" (
	"id"	INTEGER NOT NULL,
	"id_auteur"	INTEGER NOT NULL UNIQUE,
    "nom"	TEXT NOT NULL,
    "score" INTEGER NOT NULL,
    "rang" TEXT NOT NULL,
    "position" INTEGER NOT NULL,
	"timestamp"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS "solve" (
	"id"	INTEGER NOT NULL,
	"id_auteur"	INTEGER NOT NULL,
	"id_challenge"	INTEGER NOT NULL,
	"titre"	TEXT NOT NULL,
	"rubrique" TEXT NOT NULL,
	"score" INTEGER NOT NULL,
	"id_rubrique" INTEGER NOT NULL,
	"url_challenge" TEXT NOT NULL,
	"difficulte" TEXT NOT NULL,
	"timestamp"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);


CREATE UNIQUE INDEX idx_id_auteur_user_rm ON user_rm (id_auteur);
CREATE INDEX idx_nom_user_rm ON user_rm (nom);

CREATE INDEX idx_id_auteur_solve ON solve (id_auteur);
CREATE INDEX idx_id_challenge_solve ON solve (id_challenge);

COMMIT;
