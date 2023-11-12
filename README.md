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

Then:

```console
docker-start
```
