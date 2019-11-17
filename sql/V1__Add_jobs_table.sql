create table jobs (
  id serial not null primary key,
  args jsonb,
  status text,
  created_at timestamp with time zone default current_timestamp,
  updated_at timestamp with time zone default current_timestamp
);
