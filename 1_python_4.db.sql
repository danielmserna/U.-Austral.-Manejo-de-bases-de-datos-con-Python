BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "autor" (
	"ID"	INTEGER NOT NULL,
	"NOMBRE"	TEXT NOT NULL,
	"APELLIDO"	TEXT NOT NULL,
	PRIMARY KEY("ID" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "libro" (
	"ID"	INTEGER NOT NULL,
	"ISBN"	TEXT NOT NULL,
	"TITULO"	TEXT NOT NULL,
	"DESCRIPCION"	TEXT NOT NULL,
	"AUTOR"	INTEGER NOT NULL,
	PRIMARY KEY("ID" AUTOINCREMENT)
);
INSERT INTO "autor" VALUES (1,'Joanne','Rowling');
INSERT INTO "autor" VALUES (2,'J','Tolkien');
INSERT INTO "autor" VALUES (3,'Miguel','Cervantes');
INSERT INTO "libro" VALUES (1,'93671837','Harry Potter y la piedra filosofal','El niño que vivió',1);
INSERT INTO "libro" VALUES (2,'7489248949','El señor de los anillos','',2);
INSERT INTO "libro" VALUES (3,'6235327','Don Quijote de la mancha','Sancho panza',3);
CREATE UNIQUE INDEX IF NOT EXISTS "ISBN_IDX" ON "libro" (
	"ISBN"
);
COMMIT;
