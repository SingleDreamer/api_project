from flask import Flask,request,url_for,redirect,render_template
import json, urllib2, random

app=Flask(__name__)
random.seed()

@app.route("/")
def index():
        title = request.args.get("title")
        image = request.args.get("image")
        text = request.args.get("text")
        submit = request.args.get("submit")
        if (submit=="Submit" and title != "" and image != "" and text != ""):
                return redirect("/randomize/"+title+"&"+image+"&"+text)
        return render_template("home.html")

@app.route("/randomize/<title>&<image>&<text>")
def tag(title="",image="",text=""):
        t = ""
        b = ""

        #---Title---
        url="http://api.tumblr.com/v2/tagged?tag=%s&api_key=aTQcvkZkpZbz7ILTsi8ekrUFE0maSPweft6mM1yyJhQBdnV5eb"
        url = url%(title)
        try:
                request = urllib2.urlopen(url)
                resultstring = request.read()
                result = json.loads(resultstring)
                while (t==""):
                        try:
                                r = random.randint(0, len(result['response'])-1)
                                #                        print r
                                item = result['response'][r]
                                t = t + item['title']
                        except:
                                pass
        except:
                pass
        #---Title---

        #---Image---
        url="http://api.tumblr.com/v2/tagged?tag=%s&api_key=aTQcvkZkpZbz7ILTsi8ekrUFE0maSPweft6mM1yyJhQBdnV5eb"
        url = url%(image)
        try:
                request = urllib2.urlopen(url)
                resultstring = request.read()
                result = json.loads(resultstring)

                while (b==""):
                        try:
                                r = random.randint(0, len(result['response'])-1)
                                #                        print r
                                item = result['response'][r]
                                #                        print item
                                b = b + "<img src=%s>"%(item['photos'][0]['original_size']['url'])
                                #                print b
                        except:
                                pass
        except:
                pass
        #---Image---

        tx="" 
        #---Text---
        url="http://api.tumblr.com/v2/tagged?tag=%s&api_key=aTQcvkZkpZbz7ILTsi8ekrUFE0maSPweft6mM1yyJhQBdnV5eb"
        url = url%(text)
                
        try:
                request = urllib2.urlopen(url)
                resultstring = request.read()
                result = json.loads(resultstring)
                res = result['response']

                while (tx==""):
                        try:
                                r = random.randint(0, len(res)-1)
                                item = res[r]
                                #                                print r
                                #                                print item
                                tx += tx + "<br>"+item['body']
                        except:
                                pass
        except:
                pass
                         
        b+=tx
        
        if (b==""):
                return redirect("/error")
                #---Text---

        return render_template("tag.html",title=t,body=b)
        
@app.route("/error")
def error():
        return render_template("error.html")

if __name__=="__main__":
        app.debug=True
        app.run(host="0.0.0.0",port=8000)
