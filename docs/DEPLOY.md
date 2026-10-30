# Deploying the website

`site/` is a static folder. It loads nothing from other servers, so any web server works. It must stay private until judging: the task fails an entry that is posted publicly first.

## Before judging: password protected (nginx)

```bash
sudo apt install nginx apache2-utils
sudo mkdir -p /var/www/redbelly
sudo cp -r site/* /var/www/redbelly/
sudo htpasswd -c /etc/nginx/.redbelly_htpasswd reviewer
```

`/etc/nginx/sites-available/redbelly`:

```nginx
server {
    listen 80;
    server_name your.domain.example;
    root /var/www/redbelly;
    index index.html;

    auth_basic "Private until judging";
    auth_basic_user_file /etc/nginx/.redbelly_htpasswd;
    add_header X-Robots-Tag "noindex, nofollow" always;

    location / { try_files $uri $uri/ =404; }
    location ~ \.vtt$ { default_type text/vtt; }
    location ~* \.(png|woff2|mp3|css|js)$ { expires 7d; }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/redbelly /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

Add HTTPS with `sudo certbot --nginx -d your.domain.example` if the domain points at the server. Share the password only with the judges.

## Quick preview without nginx

```bash
python3 -m http.server 8080 --bind 127.0.0.1 --directory site
```

Bound to 127.0.0.1, it is reachable only from the server itself. From your own computer, tunnel to it:

```bash
ssh -L 8080:127.0.0.1:8080 user@your-server
```

Then open http://localhost:8080.

## After judging

Remove `auth_basic`, `auth_basic_user_file` and the `X-Robots-Tag` header if the DAO wants the page public, and delete the `robots` meta tag from `scripts/build_site.py`, then rebuild.
