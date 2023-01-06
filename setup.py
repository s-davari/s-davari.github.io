#!/usr/bin/env python3

from setuptools import find_packages, setup
import sys,os, base64

try:
    from flask import Flask, render_template_string
    from flask_frozen import Freezer
    from flask_flatpages import (
        FlatPages, pygmented_markdown)
except:
    for x in [
            'requests',
            'flask==2.0.1',
            'flask_flatpages==0.7.3',
            'frozen_flask==0.18',
            'pygments==2.10.0',
            'elsa==0.1.6'
        ]:
        os.system(str(sys.executable) + " -m pip install " + str(x))
    from flask import Flask, render_template_string
    from flask_frozen import Freezer
    from flask_flatpages import (
        FlatPages, pygmented_markdown)


base_info = {
    'name':"Miles Frantz",
    'title':"Cyber Security Ph.D. Student",
    'NAME':"Miles Frantz",
    'EMAIL':"g00qhtdbp@relay.firefox.com",
    'GITHUB':"franceme",
    'DOCKER':"frantzme",
    'RESUME':'https://rebrand.ly/frantzme_resume',
    'CV':'https://rebrand.ly/frantzme_cv',
    'GITHUB_USERNAME': 'franceme',
    'LINKEDIN_USERNAME': 'franceme',
    'SCHOLAR_USERNAME': 'RKKj9VgAAAAJ',
    #'MENDELEY_USERNAME': 'myles-f',
    #'ieee': 'MilesFrantz662182',
    #'acm': 'here',
    #'MEDIUM': 'frantzme',
    'ORCID': '0000-0002-7329-6979',
    'ZENODO': '3701552',
    'WEBSITE': 'franceme.github.io',
    'LINKEDIN': 'frantzme',
    # 'phone': '513-480-3169',
    "show_edu":True,
    "show_exp":True,
    "show_proj":True,
    "show_grp":True,
    "show_ment":True,
    "show_sub":True,
    "show_talks":True,
    "show_skills":True,
    "show_docker":True,
    "show_consult":True,
    "show_path":True
}

#https://stackoverflow.com/questions/20646822/how-to-serve-static-files-in-flask
def get_file(filename, base=None):  # pragma: no cover
    try:
        if base:
            src = os.path.join(base,filename)
        else:
            src = filename
        # Figure out how flask returns static files
        # Tried:
        # - render_template
        # - send_file
        # This should not be so non-obvious
        return open(src).read()
    except IOError as exc:
        return str(exc)

prerender_jinja = lambda text: pygmented_markdown(render_template_string(text))
rendre = lambda page:render_template_string(get_file(page),mimetype="text/html",dyct=base_info)
rendre_string = lambda page:render_template_string(page,mimetype="text/html",dyct=base_info)

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FLATPAGES_HTML_RENDERER = prerender_jinja
FLATPAGES_MARKDOWN_EXTENSIONS = ['codehilite']
FREEZER_IGNORE_MIMETYPE_WARNINGS = True

app = Flask(
    __name__,
    static_url_path='',
    static_folder='static',
)
app.config.from_object(__name__)
pages = FlatPages(app)
freezer = Freezer(app)

def page_redirect(url):
    return f"""<!DOCTYPE HTML>
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
""", 200, {'Content-Type':'text/html'}

def easy_add_page(contents):
    return contents, 200, {'Content-Type':'text/html'}

def easy_add_file(file):
    return easy_add_page(open(file).read())

# === URL Routes === #

@app.route('/test_w.html')
def route_test():
    return easy_add_file('static/prototype/test_w.html')

@app.route('/')
@app.route('/index.html')
def index():
    for x in base_info.keys():
        if x.startswith('show_'):
            base_info[x] = True

    for x in ['show_skills','show_ment']:
        base_info[x] = False
    return rendre('index.html')

@app.route('/research.html')
def research():
    for x in base_info.keys():
        if x.startswith('show_'):
            base_info[x] = True

    for x in ['show_skills','show_exp','show_grp','show_docker']:
        base_info[x] = False
    return rendre('index.html')

@app.route('/industry.html')
def industry():
    for x in base_info.keys():
        if x.startswith('show_'):
            base_info[x] = True

    for x in ['show_edu','show_talks','show_sub']:
        base_info[x] = False
    return rendre('index.html')

@app.route('/full.html')
def full():
    for x in base_info.keys():
        if x.startswith('show_'):
            base_info[x] = True
    return rendre('index.html')


@app.route('/diagrams.html')
def diagrams():
    return page_redirect('https://rebrand.ly/graphz')

@app.route('/resume.html')
def resume_grab():
    return page_redirect('https://rebrand.ly/frantzme_resume')

@app.route('/cv.html')
def cv_grab():
    return page_redirect('https://rebrand.ly/frantzme_cv')

@app.route('/sok.html')
def sok_grab():
    return page_redirect('https://oaklandsok.github.io')

@app.route('/rss.html')
def rss_grab():
    return page_redirect('https://zapier.com/engine/rss/8296213/frantzme')

@app.route('/security.txt')
def security():
    return f"""
# Miles Frantz Website
Contact: mailto:{base_info['EMAIL']}
Preferred-Languages: en
Expires: 2025-12-31T18:00:00.000Z
""", 200, {'Content-Type':'text/plain'}

@app.route('/robots.txt')
def robots():
    return f"""
# robots.txt - for Miles Frantz Website

User-agent: *
Disallow: /
""", 200, {'Content-Type':'text/plain'}

@app.route('/qr.html')
def qr_grab():
    svg = open('static/images/VCard.svg').read()
    return svg, 200, {'Content-Type':'image/svg+xml'}


# === Main function  === #
def get_skill(name,amount, isLeft=True):
    ranking = "No Experience"
    if amount == 0:
        ranking = "No Experience"
    if amount >= 25:
        ranking = "Beginner"
    if amount >= 50:
        ranking = "Journeyman"
    if amount >= 75:
        ranking = "Expert"
    if amount >= 100:
        ranking = "Master"

    klass = "bg-info" if isLeft else "bg-secondary"

    return render_template_string(f"""
<div class="mb-3"><span class="fw-bolder">{name}</span>
    <div class="progress my-2 rounded" style="height: 20px">
        <div class="progress-bar {klass}" role="progressbar" data-aos="zoom-in-right" data-aos-delay="100" data-aos-anchor=".skills-section" style="width: {amount}%;" aria-valuenow="{amount}" aria-valuemin="0" aria-valuemax="100">{ranking}</div>
    </div>
</div>
""")

app.jinja_env.filters['get_skill'] = get_skill

def get_base(title, co_name, _from, _to, desc, is_info=True, color=None, html_id=None):
    base_color = "timeline-card-info" if is_info else "timeline-card-success"

    if color is not None:
        color = f"timeline-card-{color}"

    stripi = lambda x:None if x.strip() == '' else x.strip()
    _from = stripi(_from)
    _to = stripi(_to)

    if _from is not None and _to is not None:
        date_string = _from + " - " + _to
    elif _from is None and _to is not None:
        date_string = _to
    elif _from is not None and _to is None:
        date_string = _from
    else:
        date_string = ""

    if co_name is not None and co_name.strip() != "":
        co_name = f" at {co_name}"

    if html_id is not None:
        html_id = f"id='{html_id}'"

    return render_template_string(f"""
<div class="timeline-card {color or base_color}" data-aos="fade-in" data-aos-delay="0" {color} {html_id}>
    <div class="timeline-head px-4 pt-3">
    <div class="h5">{title} <span class="text-muted h6">{co_name}</span></div>
    </div>
    <div class="timeline-body px-4 pb-4">
    <div class="text-muted text-small mb-3">{date_string}</div>
    <div>{desc}</div>
    </div>
</div>
""")

app.jinja_env.filters['get_base'] = get_base

def get_ref(name, title, desc,left_side=True):

    return render_template_string(f"""
          <div class="d-flex mb-2">
            <div class="avatar"><img src="images/reference-image-1.jpg" width="60" height="60"/></div>
            <div class="header-bio m-3 mb-0">
              <h3 class="h6 mb-1" data-aos="fade-left" data-aos-delay="0">{name}</h3>
              <p class="text-muted text-small" data-aos="fade-left" data-aos-delay="100">{title}</p>
            </div>
          </div>
          <div class="d-flex"><i class="text-secondary fas fa-quote-left"></i>
            <p class="lead mx-2" data-aos="fade-left" data-aos-delay="100">{desc}</p>
          </div>
""")

app.jinja_env.filters['get_ref'] = get_ref

def get_main_url(page_name, extra_info=''):
    page_name = str(page_name)
    return render_template_string(f""" <a href="/{page_name.lower()}.html">{page_name.title()}_{extra_info}</a> """)

app.jinja_env.filters['get_main_url'] = get_main_url

def arg(string):
    return __name__ == "__main__" and len(
        sys.argv) > 1 and sys.argv[0].endswith('setup.py') and str(sys.argv[1]).upper() == str(string).upper()

if arg('build'):
    freezer.freeze()
    sys.exit(0)
elif arg('run'):
    port = int(sys.argv[2]) if len(sys.argv) >= 2 else 8899
    app.run(host='0.0.0.0', port=port)
    sys.exit(0)
elif arg('install'):
    sys.exit(os.system('python3 -m pip install -e .'))
elif __name__ == '__main__':
    from elsa import cli
    sys.exit(cli(app, base_url='https://franceme.github.io'))


setup(name='My Website',
        version='0.0.0',
        description='Python Website',
        author='Miles Frantz',
        author_email='frantzme@vt.edu',
        url='',
        packages=find_packages(),
        install_requires=[
            'flask==2.0.1',
            'flask_flatpages==0.7.3',
            'frozen_flask==0.18',
            'pygments==2.10.0',
            'elsa==0.1.6',
            'werkzeug==2.0.3' #https://stackoverflow.com/questions/71661851/typeerror-init-got-an-unexpected-keyword-argument-as-tuple#answer-71662972
        ]
)
