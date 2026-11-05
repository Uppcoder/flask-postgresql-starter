# Flask + PostgreSQL starter

[![Deploy to Uppcoder](deploy-to-uppcoder.svg)](https://portal.uppcoder.com/cust-portal/deploy?starter=flask-postgresql-starter&utm_source=github&utm_medium=repo&utm_campaign=flask-starter)

A small Flask app on PostgreSQL, ready to deploy: a notes API with create,
list and delete, and its table created on startup. The database comes from one
environment variable, `DATABASE_URL`, so no password sits in the code.

| Endpoint | What it does |
|---|---|
| `GET /` | Says whether the database is connected |
| `GET /health` | Runs a query and returns the PostgreSQL version |
| `GET /notes` | Lists the notes |
| `POST /notes` | Adds one: `{"text": "..."}` |
| `DELETE /notes/<id>` | Deletes one |

## Deploy it on Uppcoder (free plan)

[Uppcoder](https://portal.uppcoder.com/developers?utm_source=github&utm_medium=repo&utm_campaign=flask-starter)
runs it on its own HTTPS address with a real PostgreSQL database and VS Code in
the browser beside it.
The free plan (Spark) has no card and no time limit, and the app and its database
are backed up every night to a separate server.

Press the button above: it opens Uppcoder's deploy page with this starter and PostgreSQL filled in. New to Uppcoder? Sign up there, confirm your email, and start the free plan (Spark) in one click on the same page. Or set it up by hand:

1. Sign up at portal.uppcoder.com, confirm your email, then Billing, Spark, Start free.
2. Stacks, Create, Blank stack. Pick **Flask**, then add **PostgreSQL**: it is
   connected to the app automatically.
3. On the Flask card, under Git repository, paste
   `https://github.com/Uppcoder/flask-postgresql-starter` (branch `main`).
4. Deploy. Uppcoder clones the repository, sets `DATABASE_URL` and starts the app
   as `python app.py`; the PostgreSQL driver is already in the app's environment.
   Open the app's address and `/health` shows the database.

The full walk-through, with pictures:
[Deploy a Flask app with PostgreSQL, free](https://portal.uppcoder.com/guides/deploy-flask-postgresql?utm_source=github&utm_medium=repo&utm_campaign=flask-starter).

To start from your own copy, fork this repository first and paste your fork's
address instead.

## Run it on your own machine

With Docker:

```bash
docker compose up
```

Then open http://localhost:8000/notes. Compose starts PostgreSQL 16 beside the
app and sets `DATABASE_URL` for it.

Without Docker, point `DATABASE_URL` at any PostgreSQL database:

```bash
pip install -r requirements.txt
export DATABASE_URL=postgresql://user:password@localhost:5432/mydb
FLASK_DEBUG=1 python app.py
```

The app listens on 127.0.0.1, port 8000, which is where Uppcoder expects it;
`HOST` and `PORT` change that, and `FLASK_DEBUG=1` reloads it when you save.

## Using SQLAlchemy instead

`DATABASE_URL` starts with `postgresql://`, which SQLAlchemy reads as psycopg2.
With psycopg 3 (installed here), give Flask-SQLAlchemy
`DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)`.

MIT licensed. Made by [WEBSSON](https://github.com/websson).
