from flask import Flask,jsonify,request
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS
import html5lib
import json
from selenium import webdriver
import threading
from threading import *
import os

app = Flask(__name__)
CORS(app)



@app.route('/',methods=['GET'])
def hello():
    return jsonify({"hello":"Hello moe"})


@app.route('/home',methods=['GET'])
def landepage():
    users = []
    views = []
    sorted_resp = {}
    lookup = requests.get('http://dhubs.herokuapp.com/database').text
    result = BeautifulSoup(lookup,'html5lib')
    result = result.prettify().strip(result.prettify()[1:30])
    result = json.dumps(result,ensure_ascii=False,sort_keys=True)
    result = json.loads(result)
    with open('res.json','w') as e :
        e.write(result)
    with open('res.json','r') as json_file:
        data = json.load(json_file)
        for i in data['posts'] :
            users.append(i['username'])
            views.append(len(i['Views']))
    full_resp = list(zip(users,views))
    sorted_by_second = sorted(full_resp, key=lambda tup: tup[1],reverse=True)
    sorted_resp['res'] = []
    for i in sorted_by_second :
        sorted_resp['res'].append({'name':i[0],'views':i[1]})


    return sorted_resp

@app.route('/say',methods=['POST'])
def hellos():

    name = request.json['name']
    students = {'ahme':20,'majed':2,'abood':3}
    for i in students.keys() :
        if i == name :
            print(i,students[i])
            if students[i] == 0 :
                return jsonify({"hello":f'hello {i} your score is {students[i]}'})
            else:
                return jsonify({"hello":f'hello {i} your score is {students[i]}'})
    else:
        return jsonify({"Error":"User name not Found"})

@app.route('/views/count/<username>',methods=['GET'])
def get_views(username):
    users = []
    views = []
    view_name = []
    sorted_resp = {}
    resp_reduce = {}
    lookup = requests.get(f'http://dhubs.herokuapp.com/shop/{username}').text
    result = BeautifulSoup(lookup,'html5lib')
    result = result.prettify().strip(result.prettify()[1:30])
    result = json.dumps(result,ensure_ascii=False,sort_keys=True)
    result = json.loads(result)
    with open(f'{username}.json','w') as e :
        e.write(result)
    with open(f'{username}.json','r') as json_file:
        data = json.load(json_file)
        for i in data :
            views.append(i['Views'])

    for i in views[0]:
        view_name.append(i['itemname'])

    my_dict = {i:view_name.count(i) for i in view_name}
    print(my_dict)


    return my_dict



@app.route('/item/advisor/<itemname>',methods=['GET'])
def get_advisor(itemname):
    class collecter:
        def __init__(self):

            self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

        def crawl_sooq(self,all=bool()):
            self.link1 = 'https://saudi.souq.com/sa-en/'+itemname+'/s/?as=1'
            self.link2 = 'https://saudi.souq.com/sa-en/'+itemname+'/mobile-phones-33/a-t/s/'
            def sooq(tag1,tag2,tag3,link,pt,imgkey):
                self.tag1 = tag1
                self.tag2 = tag2
                self.tag3 = tag3
                self.link = requests.get(self.link1,headers=self.headers).text
                self.get_result = BeautifulSoup(self.link,'html5lib').find_all(tag1 , {tag2:tag3})
                self.holder = []
                for i in range(len(self.get_result)):
                    self.s_img = self.get_result[i].find('img')[imgkey]
                    self.s_name = self.get_result[i]['data-name']
                    self.holder.append([self.s_img,self.s_name])
                self.price = [int(i.text.split(' ')[0].replace(',','').split('.')[0]) for i in BeautifulSoup(self.link,'html5lib').find_all(pt,{'class':'itemPrice'})]
                return {"item name":self.holder[0][1],"item img":self.holder[0][0],"item price":self.price[0]}

            try :
                return sooq('div','class','column column-block block-list-large single-item',self.link2,'h3','data-src')
            except :
                 return sooq('div','class','column column-block block-grid-large single-item',self.link1,'span','src')




        def crawl_jarrer(self,all=bool()):
            self.link1 = 'https://www.jarir.com/sa-en/catalogsearch/result/?order=priority&dir=asc&q='+itemname


            def jarrer(tag1,tag2,tag3,link,pt,imgkey):
                self.tag1 = tag1
                self.tag2 = tag2
                self.tag3 = tag3
                self.link = requests.get(self.link1,headers=self.headers).text
                self.get_result = BeautifulSoup(self.link,'html5lib').find_all(tag1 , {tag2:tag3})
                self.get_result_price = BeautifulSoup(self.link,'html5lib').find_all('div' , {'class':'price'})

                try:
                    self.price = [int(self.get_result_price[i].text.replace('SR','').split(' ')[0].split(' ')[0]) for i in range(len(self.get_result_price))]
                except:
                    self.price = [int(self.get_result_price[i].text.replace('SR','').split(' ')[0].strip(self.get_result_price[i].text[0]).split('.')[0]) for i in range(len(self.get_result_price))]


                self.name = [ self.get_result[i].find('a')['title'] for i in range(len(self.get_result))]
                self.img = [self.get_result[i].find('img',{"class":"lazyload"})['data-src'] for i in range(len(self.get_result))]

                self.data = [self.name,self.img]


                return {"item name":self.data[0][0],"item img":self.data[1][0],"itme price":self.price[0]}


            try:
                return jarrer('li','class','item last',self.link1,'div','data-src')
            except Exception as e :
                return jarrer('li','class','item last',self.link1,'div',"")


        def crawl_noon(self,all=bool()):
            self.link1 = 'https://www.noon.com/saudi-ar/search?q='+itemname
            self.session = requests.Session()

            def noon(tag1,tag2,tag3,link,pt,imgkey):
                self.tag1 = tag1
                self.tag2 = tag2
                self.tag3 = tag3
                self.link_r = self.session.get(self.link1,headers=self.headers)
                self.link = requests.get(self.link1,headers=self.headers).text
                self.get_result = BeautifulSoup(self.link,'html5lib').find_all(tag1 , {tag2:tag3})
                self.name = [self.get_result[i].find(pt ,{'class':"jsx-1833788615 name"}).text for i in range(len(self.get_result))]
                self.price = [int(self.get_result[i].find('span',{'class':'jsx-4251264678 sellingPrice'}).text.strip('ر.س.‏').split(' ')[0].split('.')[0]) for i in range(len(self.get_result))]
                self.im = BeautifulSoup(self.link,'html5lib').find_all('a',{'class':'jsx-1833788615 product'})

                return {"item name":self.name[0],"item price":self.price[0],'item img':[self.im[i]['href'] for i in range(len(self.im))][0]}




            try:
                return noon('div','class','jsx-1833788615 detailsContainer',self.link1,'p','data-src')
            except :
                return noon('div','class','jsx-1833788615 detailsContainer',self.link1,'div','data-src')




        def crawl_extra(self,all=bool()):
            self.link1 = 'https://www.extra.com/en-sa/search/?text='+itemname


            def extra(tag1,tag2,tag3,link,pt,imgkey):
                self.tag1 = tag1
                self.tag2 = tag2
                self.tag3 = tag3
                self.link = requests.get(self.link1,headers=self.headers).text
                self.get_result = BeautifulSoup(self.link,'html5lib').find_all(tag1 , {tag2:tag3})
                self.name = [ self.get_result[i]['data-name'] for i in range(len(self.get_result))]
                self.price = [int(self.get_result[i]['data-price']) for i in range(len(self.get_result))]
                self.img = [self.get_result[i]['data-imageurl'] for i in range(len(self.get_result))]

                return {"item name":self.name[0],"item price":self.price[0],"item img":self.img[0]}




            return extra('div','class','c_product-tile js-product-tile js-gtm-button',self.link1,'div','data-src')

    return {'result':{'jareer':collecter().crawl_jarrer(),'sooq':collecter().crawl_sooq(),'extra':collecter().crawl_extra(),'noon':collecter().crawl_noon()}}









if __name__ == '__main__':
    app.run(debug=True,threaded=True, port=5000)
