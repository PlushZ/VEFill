# Restore the DB
createdb vefill
pg_restore -U youruser -d vefill vefill_backup.dump