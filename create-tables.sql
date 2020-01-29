BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `shows` (
	`show_id`	INTEGER,
	`name`	TEXT,
	PRIMARY KEY(`show_id`)
);
CREATE TABLE IF NOT EXISTS `people` (
	`person_id`	INTEGER,
	`name`	TEXT,
	PRIMARY KEY(`person_id`)
);
CREATE TABLE IF NOT EXISTS `events` (
	`event_id`	INTEGER,
	`show`	INTEGER,
	`episode`	INTEGER,
	`timestamp`	INTEGER,
	`description`	TEXT,
	PRIMARY KEY(`event_id`),
	FOREIGN KEY(`show`,`episode`) REFERENCES `episodes`(`show`,`episode`)
);
CREATE TABLE IF NOT EXISTS `episodes` (
	`show`	INTEGER,
	`episode`	INTEGER,
	`airdate`	TEXT,
	`runtime`	INTEGER,
	`yt_link`	TEXT,
	PRIMARY KEY(`show`,`episode`),
	FOREIGN KEY(`show`) REFERENCES `shows`(`show_id`)
);
CREATE TABLE IF NOT EXISTS `appearance` (
	`show`	INTEGER,
	`episode`	INTEGER,
	`person_id`	INTEGER,
	FOREIGN KEY(`person_id`) REFERENCES `people`(`person_id`),
	FOREIGN KEY(`show`,`episode`) REFERENCES `episodes`(`show`,`episode`)
);
COMMIT;
