create table d_server_type
(
  id   int auto_increment
    primary key,
  name varchar(255) null,
  constraint name
    unique (name)
);

INSERT INTO monitor.d_server_type (id, name) VALUES (2, 'CentOS');
INSERT INTO monitor.d_server_type (id, name) VALUES (1, 'Windows');