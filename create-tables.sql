BEGIN TRANSACTION;

-- Standard tables

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

-- FTS5 tables

-- https://sqlite.org/fts5.html

CREATE VIRTUAL TABLE IF NOT EXISTS events_fts USING fts5(event_id UNINDEXED, description);

CREATE VIRTUAL TABLE IF NOT EXISTS guests_fts USING fts5(guest_id UNINDEXED, name);

-- Triggers

--TODO test these

-- We need triggers to update the fts tables when their base tables are updated
CREATE TRIGGER IF NOT EXISTS trig_events_after_insert AFTER INSERT ON events
BEGIN
	INSERT INTO events_fts (event_id, description) VALUES (new.event_id, new.description);
END;
CREATE TRIGGER IF NOT EXISTS trig_events_after_delete AFTER DELETE ON events
BEGIN
	DELETE FROM events_fts WHERE event_id = new.event_id;
END;
CREATE TRIGGER IF NOT EXISTS trig_events_after_update AFTER UPDATE ON events
BEGIN
	UPDATE events_fts
	SET
		event_id = new.event_id,
		description = new.description
	WHERE
		event_id = new.event_id;
END;


CREATE TRIGGER IF NOT EXISTS trig_guests_after_insert AFTER INSERT ON guests
BEGIN
	INSERT INTO guests_fts (guest_id, description) VALUES (new.guest_id, new.description);
END;
CREATE TRIGGER IF NOT EXISTS trig_guests_after_delete AFTER DELETE ON guests
BEGIN
	DELETE FROM guests_fts WHERE guest_id = new.guest_id;
END;
CREATE TRIGGER IF NOT EXISTS trig_guests_after_update AFTER UPDATE ON guests
BEGIN
	UPDATE guests_fts
	SET
		guest_id = new.guest_id,
		description = new.description
	WHERE
		guest_id = new.guest_id;
END;

COMMIT;

