CREATE TABLE IF NOT EXISTS reads(
  read_id VARCHAR(100) NOT NULL,
  exp_group INTEGER(1) NOT NULL,
  sequence VARCHAR NOT NULL,
  read_length INTEGER,
  runid VARCHAR,
  read INTEGER,
  ch INTEGER,
  start_time VARCHAR,
  flowcell VARCHAR,
  protocol_group_id VARCHAR,
  sample_id VARCHAR,
  barcode VARCHAR,
  barcode_alias VARCHAR,
  PRIMARY KEY (read_id)
);

CREATE TABLE IF NOT EXISTS blastn(
  read_id VARCHAR NOT NULL,
  chromosome VARCHAR,
  start_read INTEGER,
  stop_read INTEGER,
  start_reference INTEGER,
  stop_reference INTEGER,
  evalue REAL,
  score INTEGER,
  strand VARCHAR
);

CREATE TABLE IF NOT EXISTS reference_genome(
  chromosome VARCHAR,
  sequence VARCHAR
);

CREATE TABLE IF NOT EXISTS alignments(
  read_id VARCHAR NOT NULL,
  read_sequence VARCHAR,
  alignment VARCHAR,
  ref_sequence VARCHAR,
  alignment_length INT
);

CREATE TABLE IF NOT EXISTS snv(
  read_id VARCHAR,
  snv_type VARCHAR,
  length VARCHAR,
  start VARCHAR,
  read_sequence VARCHAR,
  ref_sequence VARCHAR,
  ignore_snv INTEGER
);
