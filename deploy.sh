# backup db.sqlite3
destination=".db_backup/db.sqlite3.$(date +"%Y_%m_%d_%H_%M_%S")"
mkdir -p .db_backup
cp db.sqlite3 "$destination"
echo "Backing up 'db.sqlite3' to '$destination'"

# deploy
source venv/bin/activate
python manage.py collectstatic
sudo apachectl restart
