from flask import Flask,request,url_for,redirect,render_template
import json, urllib2

app=Flask(__name__)

@app.route("/")
def index():
	return "hello"

@app.route("/t/<tag>")
def tag(tag=""):
	url="http://api.tumblr.com/v2/tagged?tag=%s&api_key=aTQcvkZkpZbz7ILTsi8ekrUFE0maSPweft6mM1yyJhQBdnV5eb"
	url = url%(tag)
	request = urllib2.urlopen(url)
	resultstring = request.read()
	result = json.loads(resultstring)
	s = ""
	for item in result['response']:
		print item
		try:
			s= s + "<img src=%s>"%(item['photos'][0]['original_size']['url'])
			print s
		except:
			pass
	return s


if __name__=="__main__":
   app.debug=True
   app.run(host="0.0.0.0",port=8000)
