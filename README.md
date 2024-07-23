# osi.kaist.ac.kr

## Development Guide

1. Clone to local machine
2. Run local Django server (run your own copy of the OSI website on your local machine)
3. Make changes to the code
4. Check if the changes are working as expected
5. Push the changes to the repository
6. Pull the code from the repository to the server
7. Restart the server

### How to clone and run the server

1. Clone and install requirements

```bash
git clone <repository-url>
cd osi.kaist.ac.kr
pip install -r requirements.txt  # consider making a virtual environment before this step
```

2. Copy database and media files from the production server to your local project directory

**WARNING - do not delete the existing database or media files. THERE ARE NO BACKUPS. Especially be careful not to overwrite them by mistake**

- Copy `db.sqlite3` from our production server to your local project root directory. Note that`osi.kaist.ac.kr` is your local project root directory.
- Copy the `media` directory from the server **to your local project root directory**. Note, the production media files are in `/var/www/osi.kaist.ac.kr/media`.
  - Media files are the files uploaded by users, such as profile images, event images, etc. These are not kept in the Git repository.
  - Note that static images (such as the OSI logo) are kept in the Git repository and are not in the `media` directory. Consider the `media` directory as an extension of the database, but for files.

3. Run server

```bash
python manage.py runserver
```

You should see the exact same website as the production server at `localhost:8000`, with the same user credentials.
Try logging into your account!

### What files to change

- **For static text, hyperlinks, etc. in html files**, you can directly change the html files in the `templates` directory.
Note that templates can be extended (we extend all pages from `base.html`) and included (we include the navbar and footer in `base.html`).

- **For dynamic content**, you will need to change the corresponding views in `views.py` and the corresponding models in `models.py`. You should have a good understanding of Django to do this. If you are relying on this guide, you probably need to learn more about Django.

## Deployment Guide

### How to push changes to the production server

1. Push your changes to GitHub
2. SSH into the server
3. Pull the changes from GitHub
4. Restart the server
    ```bash
    source deploy.sh  # run this from the production server!
    ```

### Apache setttings

You only need to do this when setting up a new server.

- According to KAIST security practices, you need to block directory indexing (e.g., viewing list of files in `/media/`). To do this, disable the `Indexes` option in your Apache config at `/etc/apache2/apache2.conf`.
  ```
  <Directory /var/www/>
	  Options -Indexes +FollowSymLinks
	  AllowOverride None
	  Require all granted
  </Directory>
