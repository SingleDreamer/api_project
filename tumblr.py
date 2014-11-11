from flask import Flask,request,url_for,redirect,render_template
import json, urllib2, random

app=Flask(__name__)
random.seed()

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
	#for item in result['response']:
 		#print item
        try:
                r = random.randint(0, len(result['response'])-1)
                print r
                item = result['response'][r]
                s= s + "<img src=%s>"%(item['photos'][0]['original_size']['url'])
                #print s
        except:
                pass

        if (s==""):
                return redirect("/error")

	return render_template("tag.html",body=s)

@app.route("/error")
def error():
        return render_template("error.html")

if __name__=="__main__":
   app.debug=True
   app.run(host="0.0.0.0",port=8000)
