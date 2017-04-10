Nifty-Scraper
=============

This is a small utility written using cherrypy which scrapes data for Nifty50 and displays the values on a web page.

Setup
-----

1. `redis` is required to run this application.

2. Install requirements for the application using:
```sh
    pip install -r requirements.txt
```

3. Create a copy of `server.sample.conf` and name that file `server.conf`. Fill in the required values.

4. Run the application:
```sh
    python app.py
```

5. Go to http://localhost:8080 to view the data.
