#!/usr/bin/env python3
from setuptools import find_packages, setup
import sys,os, base64

try:
    from flask import Flask, render_template_string, make_response
    from mystring import string as str
    from flask_frozen import Freezer
    from flask_flatpages import (
        FlatPages, pygmented_markdown)
    from feedgen.feed import FeedGenerator
except:
    for x in [
            'requests',
            'flask==3.0.1',
            'flask_flatpages==0.7.3',
            'frozen_flask==1.0.1',
            'pygments==2.10.0',
            'feedgen==0.9.0',
            'elsa==0.1.6',
            'werkzeug==3.0.0'
        ]:
        os.system(str(sys.executable) + " -m pip install " + str(x))
    from flask import Flask, render_template_string, make_response
    from flask_frozen import Freezer
    from flask_flatpages import (FlatPages, pygmented_markdown)
    from feedgen.feed import FeedGenerator


base_info = {
    'name':"Shakiba Davari",
    'title':"Ph.D.",
    'NAME':"Shakiba Davari",
    'EMAIL':"mailto:sdavari@vt.edu",
    'MENDELEY':"",
    'LINKEDIN_USERNAME': 'sdavari',
    'SCHOLAR_USERNAME': '0C3C2PEAAAAJ',
    'ORCID_ID': '0000-0003-3128-1979',
    'ORCID': 'https://orcid.org/0000-0003-3128-1979',
    'SCHOLAR': 'https://scholar.google.com/citations?user=0C3C2PEAAAAJ',
    'LINKEDIN': 'https://www.linkedin.com/in/sdavari/',
    '3DILAB': 'https://wordpress.cs.vt.edu/3digroup/author/sdavari/',
    'RESUME':'https://s-davari.github.io/Resume-ShakibaDavari.pdf',
    'CV':'https://s-davari.github.io/CV-ShakibaDavari.pdf',
    'DISSERTATION':'https://vtechworks.lib.vt.edu/items/9c1f5ba4-fcb0-4825-b8d3-f4d32c98c576',
    'iARPprArXivDOI': 'https://www.doi.org/10.48550/arXiv.2411.02684',
    'designSpacePprArXivDOI': 'https://doi.org/10.48550/arXiv.2411.02607',
    'iARPaperLnkdInPost': 'https://www.linkedin.com/posts/sdavari_towards-intelligent-augmented-reality-iar-activity-7264261102069280768-ve8X?utm_source=share&utm_medium=member_desktop',
    'designSpacePaperLnkdInPost': 'https://www.linkedin.com/posts/sdavari_towards-context-aware-adaptation-in-extended-activity-7263702382553829376-BWzH?utm_source=share&utm_medium=member_desktop',
    'DissertationLnkdInPost' : 'https://www.linkedin.com/posts/sdavari_intelligent-augmented-reality-iarcontext-aware-activity-7263320768984371201-szww?utm_source=share&utm_medium=member_desktop',
    'WEBSITE': 's-davari.github.io',
    "show_about":True,
    "show_edu":True,
    "show_service":True,
    "show_honors":True,
    "show_proj":True,
    "show_personal":True,
    "show_research":True,
    "show_pubs":True,
    "show_talks":True,
    "show_teachingExp":True,
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

#https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types
def easy_add_page(contents, contenttype='text/html',pullcontent=False):
    if not pullcontent or not os.path.exists(contents):
        return contents, 200, {'Content-Type':contenttype}

    raw_contents = None
    with open(contents,'r') as reader:
        raw_contents = reader.readlines()

    if contents.endswith(".csv"): #Hard Test
        output = make_response(raw_contents)
        output.headers["Content-Disposition"] = "attachment; filename=export.csv"
        output.headers["Content-type"] = "text/csv"
        return output

    return '\n'.join(raw_contents), 200, {'Content-Type':contenttype}

def easy_add_file(file):
    return easy_add_page(open(file).read())

def add_secure_pages(pagepaths):
    from fileinput import FileInput as finput
    with finput(__file__, inplace=True, backup=False) as file:
        for line in file:
            if line.startswith("#Add Secure Pages Here"):
                print(line)
                for pagepath in pagepaths:
                    if pagepath.endswith('.html') or pagepath.endswith('.htm'):
                        secure_page_name = str(pagepath.split("/")[-1]).replace('.html','').replace("*","")
                        print(f"""
@app.route('/secure_{secure_page_name}.html')
def secure_get_{secure_page_name}():
    return easy_add_file('{pagepath}')
""")
                    else:
                        secure_page_name = str(pagepath.split("/")[-1])#.split('.')[0]
                        pull_content=any([secure_page_name.endswith("."+str(x)) for x in [
                            'py','java','rs','csv','json','xml',
                        ]])
                        print(f"""
@app.route('/secure_{secure_page_name.split('.')[0]}.html')
def secure_get_{secure_page_name.split('.')[0]}():
    return easy_add_page('{pagepath}','text/plain',pullcontent={pull_content})
""")
            else:
                print(line, end='')

# === URL Routes === #

@app.route('/')
@app.route('/index.html')
def index():
    for x in base_info.keys():
        if x.startswith('show_'):
            base_info[x] = False
    base_info['show_about'] = True
    base_info['show_edu'] = True
    base_info['show_service'] = True
    base_info['show_honors'] = True
    base_info['show_personal'] = True
    return rendre('index.html')

@app.route('/about')
def index_one():
    return index()

@app.route('/education')
def education():
    for x in base_info.keys():
        if x.startswith('show_'):
            base_info[x] = False
    base_info['show_edu'] = True
    return rendre('index.html')

@app.route('/researchexperience')
def research():
    for x in base_info.keys():
        if x.startswith('show_'):
            base_info[x] = False
    base_info['show_research'] = True
    return rendre('index.html')

@app.route('/projects')
def research_one():
    
    return rendre('index.html')
    #<!------------------------------- @TODO: FIX TALKS AND TEACHING EXP AND UNCOMMENT this bellow:  ---------------------------------------------------------->
    #return research()

@app.route('/research')
def research_two():
    return research()


@app.route('/publicationlist')
def publication():
    for x in base_info.keys():
        if x.startswith('show_'):
            base_info[x] = False
    base_info['show_pubs'] = True
    return rendre('index.html')


@app.route('/publications')
def publication_one():
    return publication()

@app.route('/honors&awards')
def honors():
    for x in base_info.keys():
        if x.startswith('show_'):
            base_info[x] = False
    base_info['show_honors'] = True
    return rendre('index.html')

@app.route('/honors')
def honors_one():
    return honors()
@app.route('/awards')
def honors_two():
    return honors()


@app.route('/leadership')
def serviceAct():
    for x in base_info.keys():
        if x.startswith('show_'):
            base_info[x] = False
    base_info['show_service'] = True
    return rendre('index.html')

@app.route('/service')
def serviceAct_one():
    return serviceAct()
@app.route('/serviceactivities')
def serviceAct_two():
    return serviceAct()
@app.route('/activities')
def serviceAct_three():
    return serviceAct()


@app.route('/videos')
def talks():
    for x in base_info.keys():
        if x.startswith('show_'):
            base_info[x] = False
    base_info['show_talks'] = True
    return rendre('index.html')

@app.route('/demos')
def talks_one():
    return talks()
@app.route('/talks')
def talks_two():
    return talks()
@app.route('/presentations')
def talks_three():
    return talks()
@app.route('/conferences')
def talks_four():
    return talks()


@app.route('/teachingexperience')
def teaching():
    for x in base_info.keys():
        if x.startswith('show_'):
            base_info[x] = False
    base_info['show_teachingExp'] = True
    return rendre('index.html')

@app.route('/teaching')
def teaching_one():
    return teaching()

@app.route('/resume')
def resume_grab():
    return page_redirect(base_info['RESUME'])

@app.route('/email')
def email_grab():
    return page_redirect(base_info['EMAIL'])

@app.route('/cv')
def cv_grab():
    return page_redirect(base_info['CV'])


@app.route('/3dilabpage')
def labpage_grab():
    return page_redirect(base_info['3DILAB'])
@app.route('/3dilab')
def labpage_grab_one():
    return labpage_grab()

@app.route('/linkedin')
def linkedin_grab():
    return page_redirect(base_info['LINKEDIN'])


@app.route('/gscholar')
def scholar_grab():
    return page_redirect(base_info['SCHOLAR'])
@app.route('/scholar')
def scholar_grab_one():
    return scholar_grab()
@app.route('/g-scholar')
def scholar_grab_two():
    return scholar_grab()
@app.route('/googlescholar')
def scholar_grab_three():
    return scholar_grab()

@app.route('/orcid')
def orcid_grab():
    return page_redirect(base_info['ORCID'])

@app.route('/mendeley')
def mendeley_grab():
    return page_redirect(base_info['MENDELEY'])

@app.route('/paperss')
def paperRss():
    """
    # https://www.reddit.com/r/flask/comments/evjcc5/question_on_how_to_generate_a_rss_feed/
    # https://github.com/lkiesow/python-feedgen
    """
    fg = FeedGenerator()
    fg.title('Faper rss feed')
    fg.description('A feed of paper news pulled from the email')
    fg.link(href="https://sdavari.github.io/paperss")

    foil = 'paperss.jsonl'
    if os.path.exists(foil):

        import json
        content = []
        with open(foil, 'r') as reader:
            for line in reader.readlines():
                try:
                    content += [json.loads(line)]
                except:
                    pass

        for article in content:
            fe = fg.add_entry()
            fe.title(article['Title'])
            link = article['Link'].replace('https://s-davari.github.io/','').replace('<','').replace('>','')
            fe.link(href=link)
            fe.description(article['Content'].replace('Twitter] ;LinkedIn] Facebook]','').replace('"',"'"))
            fe.guid(link, permalink=True)
            fe.author(name=article['AuthorName'], email=article['AuthorEmail'])
            if article['PubDate'] != "":
                fe.pubDate(article['PubDate'])

    response = make_response(fg.rss_str())
    response.headers.set('Content-Type', 'application/rss+xml')
    return response

############### PAPERS Pub
@app.route('/ppr_iARarxiv')
@app.route('/ppr_iararxiv')
@app.route('/iARPprArXiv')
@app.route('/PPRiARArXiv')
@app.route('/ppriAR')
def iARPprArXiv_grab():
    return page_redirect(base_info['iARPprArXivDOI'])

@app.route('/ppr_designspace')
@app.route('/designSpacePprArXiv')
@app.route('/PPRdesignSpaceArXiv')
@app.route('/pprDesignSpace')
def designSpacePprArXiv_grab():
    return page_redirect(base_info['designSpacePprArXivDOI'])

@app.route('/dissertation')
def dissertation_grab():
    return page_redirect(base_info['DISSERTATION'])


############### LinkedIn Posts
@app.route('/lnkdin_iARppr')
@app.route('/lnkdin_iar')
@app.route('/lnkdin_iarppr')
@app.route('/lnkdiniAR')
def iARpprLnkdIn_grab():
    return page_redirect(base_info['iARPaperLnkdInPost'])

@app.route('/lnkdin_designspaceppr')
@app.route('/lnkdin_designspace')
@app.route('/lnkdinDesignSpace')
def designSpacePprLnkdIn_grab():
    return page_redirect(base_info['designSpacePaperLnkdInPost'])

@app.route('/lnkdin_dissertation')
@app.route('/lnkdin_dissertation')
@app.route('/lnkdinDissertation')
def dissertationLnkdIn_grab():
    return page_redirect(base_info['DissertationLnkdInPost'])

@app.route('/security.txt')
def security():
    return f"""
# Shakiba Davari Website
Contact: mailto:{base_info['EMAIL']}
Preferred-Languages: en
Expires: 2028-12-31T18:00:00.000Z
""", 200, {'Content-Type':'text/plain'}

@app.route('/robots.txt')
def robots():
    return f"""
# robots.txt - for Shakiba Davari Website

User-agent: *
Disallow: /
""", 200, {'Content-Type':'text/plain'}

@app.route('/qr.html')
def qr_grab():
    svg = open('static/images/VCard.svg').read()
    return svg, 200, {'Content-Type':'image/svg+xml'}

#Add Secure Pages Here

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
        sys.argv) > 1 and sys.argv[0].endswith('setup.py') and str(sys.argv[1]).upper().replace("--",'') == str(string).upper()

if arg('build'):
    freezer.freeze()
    sys.exit(0)
elif arg('addsecurepages'):
    add_secure_pages(sys.argv[2:])
    sys.exit(0)
elif arg('run'):
    port = int(sys.argv[2]) if len(sys.argv) >= 3 else 8899
    app.run(host='0.0.0.0', port=port)
    sys.exit(0)
elif arg('install'):
    sys.exit(os.system('python3 -m pip install -e .'))
elif __name__ == '__main__':
    from elsa import cli
    sys.exit(cli(app, base_url='https://sdavari.github.io'))


setup(name='My Website',
        version='0.0.0',
        description='Python Website',
        author='Shakiba Davari',
        author_email='sdavari@vt.edu',
        url='',
        packages=find_packages(),
        install_requires=[
            'flask==3.0.1',
            'flask_flatpages==0.7.3',
            'frozen_flask==1.0.1',
            'pygments==2.10.0',
            'elsa==0.1.6',
            'feedgen==0.9.0',
            'werkzeug==3.0.0' #https://stackoverflow.com/questions/71661851/typeerror-init-got-an-unexpected-keyword-argument-as-tuple#answer-71662972
        ]
)
