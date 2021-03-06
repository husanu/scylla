#!/var/www/scylla/scyllaenv/bin/python
import sys
#sys.path.insert(0, '/var/www/scylla')
#sys.path.insert(0, '/var/www/scylla/scyllaenv/lib/python3.8/site-packages')
from flask import Flask, jsonify, request, render_template, url_for
app = Flask(__name__)
import subprocess
from sh import ls
from sh import head
import json
#from base58 import b58encode
import os
#from functools import wraps
from flask import request, Response
from operator import itemgetter
from json2html import json2html
import glob
import requests
from flask import jsonify
from werkzeug.utils import secure_filename
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


UPLOAD_FOLDER = "/var/www/scylla/user_uploaded_dbs/"

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_PATH"] = 999999999999999999999999999999999999
#https://2e702ecae623463fb72c1fbf5e291bf7.us-west-2.aws.found.io:9243
#2kZN6fjkssx3Jy1fivLrQbcV

SEARCH_HOST = "http://search-scylla-qedo2exnilwadvk3vic7wxmrqy.us-west-2.cloudsearch.amazonaws.com/2013-01-01/search"
DOCUMENT_HOST = "http://doc-scylla-qedo2exnilwadvk3vic7wxmrqy.us-west-2.cloudsearch.amazonaws.com/2013-01-01/documents/batch"

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["2 per second"],
)


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'sammy' and password == 'BasicPassword!'
11;rgb:1313/1919/2626
def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    '''Login Required - email acaceres@0-sec.net for access or DM him @_hyp3ri0n on Twitter. Please do so from a corporate email or
    with some kind of proof that you are a security engineer, academic, or need this data for research purposes (e.g. email from a corporate or .edu email or provide
    a linkedin or twitter account showing as much)
    You have to login with proper credentials''', 401, {'WWW-Authenticate': 'Basic realm="Login Required - email acaceres@0-sec.net for access or DM him @_hyp3ri0n on Twitter. Please do so from a corporate email or with some kind of proof that you are a security engineer, academic, or need this data for research purposes (e.g. email from a corporate or .edu email or provide a linkedin or twitter account showing as much)"'})

#def requires_auth(f):
#    @wraps(f)
#    def decorated(*args, **kwargs):
 #       auth = request.authorization
 #       if not auth or not check_auth(auth.username, auth.password):
 #           return authenticate()
 #       return f(*args, **kwargs)
 #   return decorated

#@app.route("/status")
def check_status():

    _dir = ls("-alhS", "/var/www/")
#    print(_dir)
    return str(_dir)

#@app.route("/grab")
def grab():
    f = open("/var/www/html/results/" + request.args.get("wut"))
    return f.read()

#@app.route("/")
#TODO: TURNED OFF AUTH
#@requires_auth
def index():
    
    user_agent = request.headers.get('User-Agent').lower()

    if "wget" in user_agent or "curl" in user_agent or "aria" in user_agent:
        return "Using cli tools to download all databases is discouraged. You are encouraged to download in browser. If this is not possible I would simply ask that you open up a browser with scylla.sh (to allow cryptomining) while you do so. Note: this is a simple user-agent string check, to bypass this message simply falsify your user-agent header to a common browser." ,409


@app.route("/")
@app.route("/search")
def search():
    size = 50
    q = request.args.get("q") 
    if q:
        #laugh at sheep
        if "'" in q.strip():
            return "You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '\'' at line 1" + "<br />" * 70 + "Just kidding, I don't even use SQL. Single quotes will break your query as Lucene query syntax will interpret it literally. Use double quotes to get exact matches."

        q_lower_list = request.args.get("q").split(":")
        print(q_lower_list)
        q_lower = [q_lower_list[0].lower(), q_lower_list[1]]
        print(q_lower)
        q_param = ":".join(q_lower)
        print(q_param)
        
        _params = {"q" : q_param, "size" : request.args.get("size", default="50"), "start" : request.args.get("start", default=0), "q.parser": "lucene"}
    else:
        _params = {"q" : "*:*", "size" : request.args.get("size", default="50"), "start" : request.args.get("start", default=0), "q.parser": "lucene"}

    print(_params)
    r = requests.get(SEARCH_HOST, params = _params)

    if ":" not in _params["q"]:
        return "<h1> 500 Internal Server Error.</h1> You do not appear to be using Solr/Lucene query syntax.", 500
    
    #print(_params)
    #print(r.url)
    #print("==============================")
    #print(r.text)
 #   print(r.text)
    print(r.json())
    json_hits_num = r.json()["hits"]["found"]
    json_hits_raw = r.json()["hits"]["hit"]
    #print("==============================")

    if 'Accept' in request.headers and request.headers['Accept'] == 'application/json':
        return jsonify(json_hits_raw)
    
    json_hits_filtered = []
    for hit in json_hits_raw:
        json_hits_filtered.append(hit["fields"])
    for _w in json_hits_filtered:
        print(_w)
    #print(json_hits_filtered)
    #print(json.dumps(json_hits_filtered))

    all_keys = []
    for hit in json_hits_filtered:
        all_keys += hit.keys()
    all_keys = list(set(all_keys))

    print("at all keys")

    html = "<table id=\"results\">"
    html += "<tr>"
    for key in all_keys:
        html += "<th>" + key + "</th>"
    html += "</tr>"

    print("over here now muhfukka")
          
    #TODO: this needs a helper function
    c = 0
    for hit in json_hits_filtered:
        c+=1
        if c > 100:
            break
        html += "<tr>"
        for key in all_keys:
            #print(key, hit)            
            try:
                html += "<th>" + hit[key]+ "</th>"
            except:                
                html += "<th>" + "null" + "</th>"
        html += "</tr>"

    html += "</table>"

    print("ok sup bby")

    
    #json_hits_html = json2html.convert(json = json.dumps(json_hits_filtered), table_attributes = 'id="search-table"')

    pages = 0
    if json_hits_num > size:
        pages = int(json_hits_num/size)
        if int(pages) > 99:
            pages = 100
        print("pages: " + str(pages))
    else:
        pages = int(json_hits_num/size)
        print("pages: " + str(pages))
    
#    dbs = glob.glob("/home/ubuntu/bighd/normalized/05Aug_normed/*.jl")
#    domains = []
#    for jl_file in dbs:
#        f = open(jl_file)
#        for line in f:
#            _dic = json.loads(line.strip())
#            if "domain" in _dic:
#                domains.append(_dic["domain"])
#            break
#    dbs = domains

    #return render_template("index.html", params = _params, hits_num = json_hits_num, pages = range(0, pages), es_url = r.url, size = size,
    #                       dbs = dbs, html_results = html)

    print("going to render the page")
    print("===========================rendering ========================")
    return render_template("index.html", params = _params, pages = range(0, pages), size = size,
                           html_results = html, search_host = SEARCH_HOST)

    
@app.route("/claim", methods=["POST"])
def claimed(db_name):

    claimed = ["orrent-invite", "cannabis.", "rambler", "ovh_kimsufi_2", "yande", "forbes", "twitter",
               "MyChemicalRomanc", "BlackMarketReloa", "Plex.tv", "honomaru.", "leetcc.7z",
               "bit.ly_9.3m_social_May", "nulled.io", "R2Games", "gawker_r", "Hostinger_Hacked", "geeks", "Habb", "ne.org.7", "stratfor"]

    for _item in claimed:
        if _item in db_name:
            return True

    return False


@app.route("/progress", methods = ["POST"])
def progress():

    f = secure_filename(request.files['file'])
    
    f.save("/var/www/scylla/user_uploaded_dbs/" + f)
    print(f)
    
    return str("Thanks for the db!")


@app.route("/crowdsource", methods = ["GET", "POST"])
def crowdsource():

    dbs_out = subprocess.run("ls -alhS /var/www/scylla/static/dbs | head -n 100", shell = True, stdout = subprocess.PIPE)
    dbs = dbs_out.stdout.decode("utf-8").split("\n")

    db_name = []
    for db in dbs:
        split = db.split()
        if len(split) > 2:
            if claimed(split[-1]):
                db_name.append((split[-1], split[4], "Claimed"))
            else:
                db_name.append((split[-1], split[4], "Unclaimed"))

    dbs = db_name
    return render_template("crowdsource.html", dbs = dbs)

@app.route("/transparency", methods = ["GET"])
def transparency():
    return render_template("transparency.html")



if __name__ == "__main__":
    app.run(host = "0.0.0.0", threaded=True, port=443, debug=False, ssl_context=('/etc/letsencrypt/live/scylla.sh/cert.pem', '/etc/letsencrypt/live/scylla.sh/privkey.pem'))
