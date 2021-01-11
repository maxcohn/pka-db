
-- migrations for versions 1.1 (inserting into FTS tables)
INSERT INTO events_fts (event_id, descriptions) SELECT event_id, descriptions FROM events;

INSERT INTO guests_fts (guest_id, name) SELECT guest_id, name FROM guests;



