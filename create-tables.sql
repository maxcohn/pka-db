BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `shows` (
	`show_id`	INTEGER,
	`name`	TEXT,
	PRIMARY KEY(`show_id`)
);
CREATE TABLE IF NOT EXISTS `guests` (
	`guest_id`	INTEGER,
	`name`	TEXT,
	PRIMARY KEY(`guest_id`)
);
CREATE TABLE IF NOT EXISTS `events` (
	`event_id`	INTEGER,
	`show`	INTEGER,
	`episode`	INTEGER,
	`timestamp`	INTEGER,
	`description`	TEXT,
	FOREIGN KEY(`show`,`episode`) REFERENCES `episodes`(`show`,`episode`),
	PRIMARY KEY(`event_id`)
);
CREATE TABLE IF NOT EXISTS `episodes` (
	`show`	INTEGER,
	`episode`	INTEGER,
	`airdate`	TEXT,
	`runtime`	INTEGER,
	`yt_link`	TEXT,
	FOREIGN KEY(`show`) REFERENCES `shows`(`show_id`),
	PRIMARY KEY(`show`,`episode`)
);
CREATE TABLE IF NOT EXISTS `appearances` (
	`show`	INTEGER,
	`episode`	INTEGER,
	`guest_id`	INTEGER,
	FOREIGN KEY(`show`,`episode`) REFERENCES `episodes`(`show`,`episode`),
	FOREIGN KEY(`guest_id`) REFERENCES `guests`(`guest_id`)
);
CREATE TABLE IF NOT EXISTS `pending_events` (
	`event_id`	INTEGER,
	`show`	INTEGER,
	`episode`	INTEGER,
	`timestamp`	INTEGER,
	`description`	TEXT,
	FOREIGN KEY(`show`,`episode`) REFERENCES `episodes`(`show`,`episode`),
	PRIMARY KEY(`event_id`)
);
COMMIT;
