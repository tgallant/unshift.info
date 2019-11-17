create or replace function update_timestamp()
	returns trigger as
  $$
begin
  new.updated_at = current_timestamp;
	return new;
end;
$$ language plpgsql;

drop trigger if exists jobs_update_timestamp
  on jobs;
create trigger jobs_update_timestamp
 before update
  on jobs
  for each row
    execute procedure update_timestamp();
