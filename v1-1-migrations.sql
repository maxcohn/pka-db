
-- migrations for versions 1.1 (inserting into FTS tables)
INSERT INTO events_fts (event_id, description) SELECT event_id, description FROM events;

INSERT INTO guests_fts (guest_id, name) SELECT guest_id, name FROM guests;


DROP TABLE pending_events;
