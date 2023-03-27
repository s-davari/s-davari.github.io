import os,sys
import pyvibe as pv
from pyvibe import HtmlComponent as html

footer = pv.Footer()
with footer.add_footercategory("About") as category:
    category.add_footerlink("About Me", "https://rebrand.ly/frantzme")
    category.add_footerlink("About My Lab", "https://yaogroup.cs.vt.edu/index.html")

with footer.add_footercategory("Tech Used for Website") as category:
    category.add_footerlink("PyVibe", "https://www.pyvibe.com/")
    category.add_footerlink("Pyodide", "https://pyodide.org")
    category.add_footerlink("JSpreadSheet", "https://bossanova.uk/jspreadsheet/v4")
    category.add_footerlink("Ace Code Editor","https://ace.c9.io/")

page = pv.Page("FRAC", navbar=None,footer=footer)
page.href = lambda name,url: f"""<a href="{url}" target="_blank"><strong>{name}</strong></a>"""
page.add_script = lambda content: page.add(html(f"""<script type="text/javascript">{content}</script>"""))

page.add_script("""
var autorun = false;
var content_to_share = [];
""")

with page.add_card() as card:
    card.add_header("Welcome to FRAC (Frantz's Rule Analysis Checker)!")
    card.add_text("by " + page.href("Miles Frantz", "https://rebrand.ly/frantzme"))
    card.add_text("""This is a very rudimentary completely static Python Playground that allows you to analyse your code for common security issues. This process only happens within your browser thanks to the power of Pyodide.""")
    card.add_text("""Why did I do this?
Simply because I am a Ph.D. Security Researcher interested in both Static Code Analysis and I want security tools to be more accessible!""")

    card.add_text("The following Python Security Tools have been included within this playground:")
    card.add_text(f"""
{page.href("Cryptolation", "https://github.com/franceme/cryptolation")} - A state-of-the-art Python security analysis tool I wrote, --currently-- being integrated.
{page.href("Bandit", "https://github.com/PyCQA/bandit")} - A Python security tool designed and created by the fine team PyCQA.
{page.href("DLint", "https://github.com/dlint-py/dlint")} - A security-based Python linter that extends flake8.
""")

    card.add_text("How do you use this?")
    card.add_text(f"""
1) Write your Python code into the text editor or add it as a url (here?code=import os,sys,hashlib;print(hashlib.sha1('This is insecure'))).
2) Wait for the first button on the left to change to "Scan the Code" (loading pyodide).
3) Once you click it, wait for the middle button to change to "View Results".
4) Once you see the results, you can refresh the page to start over or click the "Reset the page" button.
""")


"""
    await micropip.install("semgrep");
"""

page.add_html("""
<link rel="stylesheet" href="https://jsuites.net/v4/jsuites.css" />
<link rel="stylesheet" href="https://bossanova.uk/jspreadsheet/v4/jexcel.css" />
<script src="https://jsuites.net/v4/jsuites.js"></script>
<script src="https://bossanova.uk/jspreadsheet/v4/jexcel.js"></script>
<script src="https://cdn.jsdelivr.net/gh/ajaxorg/ace-builds/src-noconflict/ace.js" type="text/javascript" charset="utf-8"></script>
<script src="https://cdn.jsdelivr.net/pyodide/v0.22.1/full/pyodide.js"></script>
""")

def base_button(id, name, disabledstring, onclick):
    return f"""<button id="{id}" {disabledstring} {onclick} class="relative inline-flex items-center justify-center p-0.5 mb-2 mr-2 overflow-hidden text-sm font-medium text-gray-900 rounded-lg group bg-gradient-to-br from-pink-500 to-orange-400 group-hover:from-pink-500 group-hover:to-orange-400 hover:text-white dark:text-white focus:ring-4 focus:outline-none focus:ring-pink-200 dark:focus:ring-pink-800">
            <span class="relative px-5 py-2.5 transition-all ease-in duration-75 bg-white dark:bg-gray-900 rounded-md group-hover:bg-opacity-0">
                {name}
            </span>
    </button>
"""

def get_submissionbutton(name="Loading...", disabledstring="true",onclick=None):
    return base_button(
        id="scansubmission",
        name=name,
        disabledstring=disabledstring,
        onclick = "" if onclick is None else """onclick="{0}()" """.format(onclick)
    )

def get_viewresultsbutton(name="No Results...", disabledstring="true",onclick=None):
    return base_button(
        id="viewresults",
        name=name,
        disabledstring=disabledstring,
        onclick = "" if onclick is None else """onclick="{0}()" """.format(onclick)
    )

def get_resetbutton(name="Reset the page", disabledstring="false",onclick="resetResults"):
    return base_button(
        id="viewresults",
        name=name,
        disabledstring=disabledstring,
        onclick = "" if onclick is None else """onclick="{0}()" """.format(onclick)
    )

def core_pyodide(extra_commands="", onstart=None):
    call = "main();" if onstart is None else onstart
    return f"""
<script defer type="text/javascript">

var pyodide;
var loaded = false;
var bandit_results = null;
var dlint_results = null;

async function main(){{
    pyodide = await loadPyodide({{fullStdLib:true}});
    await pyodide.loadPackage("micropip");
    const micropip = pyodide.pyimport("micropip");
    await micropip.install("pyvibe");
    await micropip.install("flake8");
    await micropip.install("flake8-csv");
    await micropip.install("dlint");
    await micropip.install("pandas");
    await micropip.install("bandit");
    loaded = true;
    console.log("done");
    document.getElementById("scansubmission").innerHTML = `{get_submissionbutton(name="Scan the code.", disabledstring="false",onclick="scanCode")}`;
    if (autorun) {{
        scanCode()
    }}
}}

function scanCode() {{
    document.getElementById("scansubmission").innerHTML = `{get_submissionbutton(name="Scanning")}`;
    console.log("Scanning");

    editor = document.getElementById("editor").innerText;
    var lines = document.getElementById("editor").innerText.split(/\\r?\\n/);
    var started = false;
    for (var i = 0; i < lines.length; i++) {{
        if (started || isNaN(lines[i])) {{
            started = true;
            content_to_share.push(lines[i]);
        }}
    }}
    console.log(content_to_share.join("\\n"));

    var samplefile = "/sample.py";
    pyodide.FS.writeFile(samplefile, content_to_share.join("\\n"), {{ encoding: "utf8" }});

    pyodide.runPython(`import os,sys,base64`);
    pyodide.runPython(`import pandas as pd`);
    pyodide.runPython(`sys.exit = lambda x: print('Trying to exit with code := '+str(x))`);

    pyodide.runPython(`import bandit.cli.main as banditmain`);
    pyodide.runPython(`sys.argv = "bandit -f csv -o /bandit.csv /sample.py".split()`);
    pyodide.runPython(`banditmain.main()`);
    pyodide.runPython(`bandit_results = pd.read_csv("/bandit.csv")`);
    bandit_results = pyodide.globals.get("bandit_results");

    pyodide.runPython(`import flake8.main.cli as dlintmain`);
    pyodide.runPython(`sys.argv = "flake8 --select=DUO /sample.py --format=csv --output-file=/dlint.csv".split()`);
    pyodide.runPython(`dlintmain.main()`);
    pyodide.runPython(`dlint_results = pd.read_csv("/dlint.csv")`);
    pyodide.runPython(`print(dlint_results)`);
    dlint_results = pyodide.globals.get("dlint_results");

    console.log("Completed");
    document.getElementById("scansubmission").innerHTML = `{get_submissionbutton(name="Scanned", disabledstring="true")}`;
    document.getElementById("viewresults").innerHTML = `{get_viewresultsbutton(name="View the results", disabledstring="false", onclick="viewResults")}`;
    

    var currentLocation = window.location.href;
    document.getElementById("sharecodelink").setAttribute("href", currentLocation.split("?")[0] + "?code=" + content_to_share.join("%0A"));

    if (autorun) {{
        viewResults()
    }}
}}

function viewResults() {{
    document.getElementById("viewresults").innerHTML = `{get_submissionbutton(name="Loading the results", disabledstring="true")}`;
    console.log("Starting to view");

    if (bandit_results != null) {{
        pyodide.runPython(`from js import bandit_results`);
        pyodide.runPython(`
            bandit_raw_arrz = bandit_results.to_dict('tight')['data'];
        `);
        pyodide.runPython(`
        bandit_typez,bandit_titlez,bandit_widthz = [],[],[]
        for kol in bandit_results.columns.tolist():
            bandit_titlez += [kol]
            bandit_typez += ['text']
            bandit_widthz += [40]
        `);
        var bandit_mapping = [];
        var bandit_titlez = pyodide.globals.get("bandit_titlez").toJs();
        var bandit_typez = pyodide.globals.get("bandit_typez").toJs();
        var bandit_widthz = pyodide.globals.get("bandit_widthz").toJs();

        for (var i = 0; i < bandit_titlez.length; i++) {{
            bandit_mapping.push({{
                'title': bandit_titlez[i],
                'type': bandit_typez[i],
                'width': bandit_widthz[i],
            }});
        }}

        jexcel(document.getElementById('bandit_demo'), container = {{
            data: pyodide.globals.get("bandit_raw_arrz").toJs(),
            columns: bandit_mapping,
            allowExport: true,
            allowInsertColumn: false,
            wordWrap: true,
            rowResize: true,
            columnResize: true,
            editable: false,
            search: false,
            fullscreen: false,
            loadingSpin: true,
            tableHeight: '100%',
            tableWidth: '100%',
            columnSorting: true,
            allowDeleteColumn: true,
        }});
        document.getElementsByTagName("table")[0].setAttribute("style","width:100%;");
        document.getElementById("banditresults_container").setAttribute("style","display:block;");
    }}

    if (dlint_results != null) {{
        pyodide.runPython(`from js import dlint_results`);
        pyodide.runPython(`
            dlint_raw_arrz = dlint_results.to_dict('tight')['data'];
        `);
        pyodide.runPython(`
        dlint_typez,dlint_titlez,dlint_widthz = [],[],[]
        for kol in dlint_results.columns.tolist():
            dlint_titlez += [kol]
            dlint_typez += ['text']
            dlint_widthz += [40]
        `);
        var dlint_mapping = [];
        var dlint_titlez = pyodide.globals.get("dlint_titlez").toJs();
        var dlint_typez = pyodide.globals.get("dlint_typez").toJs();
        var dlint_widthz = pyodide.globals.get("dlint_widthz").toJs();

        for (var i = 0; i < dlint_titlez.length; i++) {{
            dlint_mapping.push({{
                'title': dlint_titlez[i],
                'type': dlint_typez[i],
                'width': dlint_widthz[i],
            }});
        }}

        jexcel(document.getElementById('dlint_demo'), container = {{
            data: pyodide.globals.get("dlint_raw_arrz").toJs(),
            columns: dlint_mapping,
            allowExport: true,
            allowInsertColumn: false,
            wordWrap: true,
            rowResize: true,
            columnResize: true,
            editable: false,
            search: false,
            fullscreen: false,
            loadingSpin: true,
            tableHeight: '100%',
            tableWidth: '100%',
            columnSorting: true,
            allowDeleteColumn: true,
        }});
        document.getElementById("dlintresults_container").setAttribute("style","display:block;");
    }}
    var tables = document.getElementsByTagName("table");//
    for (k=0;k < tables.length;k++)
    {{
        tables[k].setAttribute("style","width:100%;");
    }}

    document.getElementById("viewresults").innerHTML = `{get_submissionbutton(name="Loaded the results", disabledstring="true")}`;
    console.log("Finishing");
}}

function resetResults() {{
    var currentLocation = window.location.href;
    window.location.href = currentLocation.split("?")[0];
}}

{call}
{extra_commands}
</script>
"""

page.add_html(core_pyodide())

with page.add_card() as card:
    card.add_header("Scan Code Here")
    card.add(html(""" 
        <iframe name="dummyframe" id="dummyframe" style="display: none;"></iframe>
    """))

    # Have to string break through the action keyword to set the target to the iframe
    with card.add_form(action="""return scanCode();" target="dummyframe" id="setcontent""") as form:        
        form.add(html("""
<style type="text/css" media="screen">
#editorContainer {
    // width: calc( 100vw - 40px );
    height: 500px;
    max-height: calc( 80vh - 60px );
    position: relative;
    background-color: red;
}
#editor { 
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
}
</style>

<div id="editorContainer">
    <div id="editor">
</div> 
</div>
"""))

        form.add(html(get_submissionbutton()))
        form.add(html(get_viewresultsbutton()))
        form.add(html(get_resetbutton()))
    card.add_link(text="Copy the link here to share and auto-scan the code you entered", url=""" " id="sharecodelink""")


with page.add_card(classes = """ " style="visibility:hidden;" id="banditresults_container""") as card:
    card.add_header("Bandit Results")
    card.add(html(""" <div id="bandit_demo" style="width: 100%;"></div> """))

with page.add_card(classes = """ " style="visibility:hidden;" id="dlintresults_container""") as card:
    card.add_header("DLint Results")
    card.add(html(""" <div id="dlint_demo" style="width: 100%;"></div> """))

page.add_script("""
let url = new URL(window.location.href);
let params = new URLSearchParams(url.search);

let current_code = params.get('code');
document.getElementById("editor").innerHTML = current_code;
if (current_code) {
    autorun = true;
}
""")

page.add_script("""
var editor = ace.edit("editor");
editor.setTheme("ace/theme/monokai");
editor.session.setMode("ace/mode/python");
""")

with open(__file__.replace('.py','.html'),"w+") as writer:
    writer.write(page.to_html())