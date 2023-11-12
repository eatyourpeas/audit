# Audit

Not the most inspiring name. It is a thought experiment on the idea of an online survey platform.

Clinical audits tend to have fixed questions so lend themselves to hardcoding the questions so that they are easy to aggregate the answers and produce reports year on year. The vulnerability is that making changes to the questions and scoring as time goes by is difficult.

Surveys, by contrast, are generally only run once (or maybe twice if before and after an intervention), need to be customisable so that users can create questions of different types, and the responses then only have meaning if they can counted and measured to generate reports.

This survey platform therefore is aimed to allow the user to create the questions. Given that the surveys will likely not have that many respondants, are not going to scale, it seems likely a sql backend will be better than a nosql one, but I am open to suggestion here.

## Design

The main elements to a survey will be the questions and the answers, so there will need to be models for each of these entities. There will need to be models too for users and potentially reports.

It is currently a simple django project (4.2) in sqlite3 that is dockerised and runs on python 3.12 as the current latest versions.

To get up and running, clone the repository and then:

```console
chmod +x s/start
```

This is a one off

***Important*** Create a .env file in the env folder, and add this file to .gitignore.

Add these credentials:

```env
# CADDY (WEB SERVER & HTTPS)
SITE_DOMAIN="base-audit.localhost" # this should also be in DJANGO_ALLOWED_HOSTS and DJANGO_CSRF_TRUSTED_ORIGINS
LETSENCRYPT_EMAIL_ADDRESS=************
LETSENCRYPT_ENDPOINT=https://acme-staging-v02.api.letsencrypt.org/directory # LetsEncrypt staging endpoint for testing (https://acme-staging-v02.api.letsencrypt.org/directory) so as not to hit rate limits.
TLS_SOURCE="internal" # or use "acme" for LetsEncrypt
 
# DJANGO
DEBUG="True" # Set DEBUG=True for Local dev and Development, not Staging or Live
DJANGO_ALLOWED_HOSTS="localhost,127.0.0.1,base-audit.localhost"
DJANGO_CSRF_TRUSTED_ORIGINS=https://localhost:8000,https://127.0.0.1,https://base-audit.localhost
DJANGO_SECRET_KEY=******************
```

Then:

```console
s/start
```

In the browser navigate to:

```console
https://base-audit.localhost/base
```