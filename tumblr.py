from flask import Flask,request,url_for,redirect,render_template
import json, urllib2, random, sqlite3

app=Flask(__name__)
random.seed()

@app.route("/")
def index():       
        f = open ("templates/index.html", 'r')
        t = f.read()
        f.close()
        return t + """</div>
        </div>
        </center>
        </body>
        </html>
        """

@app.route("/post")
def post():
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
                r = random.randint(0, len(result['response'])-1)
                #                        print r
                item = result['response'][r]
                t = t + item['title']
                
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

                r = random.randint(0, len(res)-1)
                item = res[r]
                #                                print r
                #                                print item
                tx += tx + "<br>"+item['body']
       
        except:
                pass
                         
        b+=tx
        
        if (b==""):
                return redirect("/error")
                #---Text---
                
        #conn = sqlite3.connect("blog.db")
        #e = "insert into posts values ('"+t+"', '"+b+"');"
        #c = conn.cursor()
        #c.execute(e)
        #conn.commit()
        #e = """
        #select * from posts;
        #"""
        #s = c.execute(e)
        #text = [x for x in s]
        #conn.commit();
        
        f = open ("templates/index.html", 'a')
        #for x in text:
         #       print x[0]
          #      print x[1]
           #     f.write(x[0])
            #    f.write(x[1])
        try:
                c ="""
                <center><div class = 'col-lg-8 col-lg-offset-2 panel panel-default'>
                <div class='panel-heading'>
                <h3 class='panel-title'>"""\
                + t + \
                """
                </h3>
                </div>
                <div class='panel-body'>
                """\
                +b+\
                """</div></div></center>"""
                print c
                f.write (c)
                f.close
                return redirect (url_for ('index'))
        except:
                return redirect (url_for ('error'))
        
@app.route("/error")
def error():
        return render_template("error.html")

@app.route("/restart")
def restart():
        conn = sqlite3.connect("blog.db")
        f = """
        drop table posts;
        """
        p = """
        create table posts(title text, body text); 
        """
        c = conn.cursor()
        #c.execute(f)
        c.execute(e)
        conn.commit();
        return redirect (url_for ('index'))

if __name__=="__main__":
        app.debug=True
        app.run(host="0.0.0.0",port=8000)
