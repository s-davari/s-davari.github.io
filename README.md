# Base Website

Helpful Items

1. The index.html page is the main and only webpage
2. The setup.py provides any variables and methods used within the html webpage
   1. index.html uses Jinja internally to process the website
3.  Think of the process similar to compilation
    1.  Index is the raw source code
    2.  Python (setup.py) compiles the index.html webpage into the usable format
    3.  Python (setup.py) returns the useable index.html, with all the information sent in as a live dynamic website

However GitHub Actions and GitHub Pages only uses Static Pages.
The Python package [Frozen-Flask](https://github.com/Frozen-Flask/Frozen-Flask) is able to freeze the dynamic website to static webpages.
Essentially the usable index.html file produced by Python (setup.py) gets frozen to a static website.
Methods and variables are transferred from python to html listed below.

> Methods
def get_base():
    .
    .
    .
    return flask.render_template_string(f"""TA DA""")

app.jinja_env.filters['get_base'] = get_base

> Variables
@app.route('/index.html')
def index():
    .
    .
    .
    return render_template_string(get_file(page),mimetype="text/html",variable_one="variable_one")

There are a few cavietes that need to be handled:
1. Redirects cannot be handled using regular flask methods since the dynamic page gets translated to a static webpage. However a static html that redirects is a working redirect that I use. The code is listed below.
```html
<!DOCTYPE HTML>
<html lang="en-US">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="refresh" content="0; url={url}">
        <script type="text/javascript">
             window.location.href = "{url}"
        </script>
        <title>Page Redirection</title>
    </head>
    <body>
        If you are not redirected automatically, follow this <a href='{url}'>link to example</a>.
    </body>
</html>
```

2. The website is completely static, no dynamic handling or webpage redirecting.
