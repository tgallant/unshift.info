create table jobs (
  id serial not null primary key,
  args jsonb,
  processing boolean,
  complete boolean
);
