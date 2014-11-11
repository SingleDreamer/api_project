from flask import Flask,request,url_for,redirect,render_template
import json, urllib2

app=Flask(__name__)

@app.route("/")
def index():
        tag = request.args.get("text")
        submit = request.args.get("submit")
        if (submit=="Submit" and tag != ""):
                print "yes"
                return redirect("/t/"+tag)
	return render_template("home.html")

@app.route("/t/<tag>")
def tag(tag=""):
	url="http://api.tumblr.com/v2/tagged?tag=%s&api_key=aTQcvkZkpZbz7ILTsi8ekrUFE0maSPweft6mM1yyJhQBdnV5eb"
	url = url%(tag)
	request = urllib2.urlopen(url)
	resultstring = request.read()
	result = json.loads(resultstring)
	s = ""

#semi-related tags
        rtags = {}

	for item in result['response']:
#                s = s + str(item) + "<br>"
		try:
                        s+="<img src=%s>"%item['photos'][0]['original_size']['url']
                        t = item['tags'][0]
                        if(t!="pokemon" or t!="Pokemon"):
                                rtags[item['tags'][0]]=""
		except:
			pass

#something weird where it goes through more tags and finds more things
        p=""
        for t in rtags.keys():
                url="http://api.tumblr.com/v2/tagged?tag=%s&api_key=aTQcvkZkpZbz7ILTsi8ekrUFE0maSPweft6mM1yyJhQBdnV5eb"
                url = url%(t)
#                print url
                try:
                        request = urllib2.urlopen(url)
                        resultstring = request.read()
                        result = json.loads(resultstring)
                        p+="<br><br>"+t+"<br>"
                        for item in result['response']:
                                try:
                                        p += "<img src=%s>"%item['photos'][0]['original_size']['url']
                                except:
                                        pass
                except:
                        print t

        if (s==""):
                print "hello"
                return redirect("/error")
                
        s += "<br><br><h3>Related Tags</h3><br>" + p 
	return render_template("tag.html",body=s)

@app.route("/error")
def error():
        return render_template("error.html")

if __name__=="__main__":
   app.debug=True
   app.run(host="0.0.0.0",port=8000)
