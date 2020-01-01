from flask import Flask,jsonify,request
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS
import html5lib
import json
from selenium import webdriver
import threading
from threading import *
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
    class shoping_adv_sooq(Thread):
        def __init__(self,link):
            self.link = link
            self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}



        def get_inf_sooq_phone(self):
            self.temp = []
            self.temp_price = []
            self.temp_img = []
            self.target = requests.get(self.link,headers=self.headers).text
            self.target_name = BeautifulSoup(self.target,'html5lib').findAll("h1", {"class":"itemTitle"})
            self.target_price = BeautifulSoup(self.target,'html5lib').findAll("h3", {"class":"itemPrice"})
            self.target_img = BeautifulSoup(self.target,'html5lib').findAll("img", {"class":"img-size-medium"})
            self.t1 = threading.Thread(target=self.target_name)
            self.t2 = threading.Thread(target=self.target_price)
            self.t3 = threading.Thread(target=self.target_img)
            self.t1.start()
            self.t2.start()
            self.t3.start()


            for i in range(len(self.target_name)):
                clean_result = self.target_name[i].text
                self.temp.append(clean_result)

            for i in range(len(self.target_price)):
                clean_result = self.target_price[i].text
                self.temp_price.append(clean_result)

            for i in range(len(self.target_img)):
                clean_result = self.target_img[i]['data-src']
                self.temp_img.append(clean_result)




            for i in range(len(self.temp)):
                self.temp[i][0].replace('\n\n\t\n \n \n \n\n','')

            self.t1.join()
            self.t2.join()
            self.t3.join()
            try:
                return {"item name":self.temp[0].strip('31 % off Quick View').replace('Quick View',''),"item price":self.temp_price[0],"itemimg":self.temp_img}
            except Exception as e :
                return {"item name":" Try another word ","item price":"Try another word ","itemimg":" Try another word "}

        def get_inf_sooq_phone_2(self):
            self.temp = []
            self.temp_price = []
            self.temp_img = []
            self.target = requests.get(self.link,headers=self.headers).text
            self.target_name = BeautifulSoup(self.target,'html5lib').findAll("h1", {"class":"itemTitle"})
            self.target_price = BeautifulSoup(self.target,'html5lib').findAll("h3", {"class":"itemPrice"})
            self.target_img = BeautifulSoup(self.target,'html5lib').findAll("div", {"class":"col col-image relative discount-wrap"})
            self.t1 = threading.Thread(target=self.target_name)
            self.t2 = threading.Thread(target=self.target_price)
            self.t3 = threading.Thread(target=self.target_img)
            self.t1.start()
            self.t2.start()
            self.t3.start()


            for i in range(len(self.target_name)):
                clean_result = self.target_name[i].text
                self.temp.append(clean_result)

            for i in range(len(self.target_price)):
                clean_result = self.target_price[i].text
                self.temp_price.append(clean_result)

            for i in range(len(self.target_img)):
                clean_result = self.target_img[i].find('img')
                self.temp_img.append(clean_result['data-src'])




            for i in range(len(self.temp)):
                self.temp[i].replace('\n\n\t\n \n \n \n\n','')
                self.t1.join()
                self.t2.join()
                self.t3.join()

            try:
                return {"item name":self.temp[0],"item price":self.temp_price[0],"itemimg":self.temp_img[0]}
            except Exception as e :
                return {"x":'null'}



        def get_inf_sooq(self):
            self.temp = []
            self.temp_price = []
            self.temp_img = []
            self.target = requests.get(self.link,headers=self.headers).text
            self.target_name = BeautifulSoup(self.target,'html5lib').findAll("h1", {"class":"itemTitle"})
            self.target_price = BeautifulSoup(self.target,'html5lib').findAll("h3", {"class":"itemPrice"})
            self.target_img = BeautifulSoup(self.target,'html5lib').findAll("img", {"class":"img-size-medium"})
            self.t1 = threading.Thread(target=self.target_name)
            self.t2 = threading.Thread(target=self.target_price)
            self.t3 = threading.Thread(target=self.target_img)
            self.t1.start()
            self.t2.start()
            self.t3.start()


            for i in range(len(self.target_name)):
                clean_result = self.target_name[i].text
                self.temp.append(clean_result)

            for i in range(len(self.target_price)):
                clean_result = self.target_price[i].text
                self.temp_price.append(clean_result)

            for i in range(len(self.target_img)):
                clean_result = self.target_img[i]['src']
                self.temp_img.append(clean_result)




            for i in range(len(self.temp)):
                self.temp[i][0].replace('\n\n\t\n \n \n \n\n','')
                self.t1.join()
                self.t2.join()
                self.t3.join()

            try:
                return {"item name":self.temp[0].strip('31 % off Quick View').replace('Quick View',''),"item price":self.temp_price[0],"itemimg":self.temp_img[0]}
            except Exception as e :
                return {"item name":self.temp,"item price":self.temp_price,"itemimg":self.temp_img}
            finally:
                pass





    class shoping_adv_jolly(Thread):
        def __init__(self,link):
            self.link = link
            self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        def get_inf_jolly(self):
            self.temp_name_jolly = []
            self.temp_price_jolly = []
            self.temp_img_jolly = []
            self.target = requests.get(self.link,headers=self.headers).text
            self.jolly_name = BeautifulSoup(self.target,'html5lib').find_all("h4" , {"class":"pro_list_msg_1"})
            self.jolly_price = BeautifulSoup(self.target,'html5lib').find_all("div" , {"class":"pro_list_price_1 categoryTwo-loveBox"})
            self.jolly_img = BeautifulSoup(self.target,'html5lib').find_all("img" , {"class":"J-lazy-load firstImg"})
            self.t1 = threading.Thread(target=self.jolly_name)
            self.t2 = threading.Thread(target=self.jolly_price)
            self.t3 = threading.Thread(target=self.jolly_img)
            self.t1.start()
            self.t2.start()
            self.t3.start()


            for i in range(len(self.jolly_name)):
                clean_result = self.jolly_name[i].text
                self.temp_name_jolly.append(clean_result)

            for i in range(len(self.jolly_price)):
                clean_result = self.jolly_price[i].text
                self.temp_price_jolly.append(clean_result)


            for i in range(len(self.jolly_img)):
                clean_result = self.jolly_img[i]['data-original']
                self.temp_img_jolly.append(clean_result)
            self.t1.join()
            self.t2.join()
            self.t3.join()

            try:
                return {'item name':self.temp_name_jolly[0],'item price':self.temp_price_jolly[0],'item img':self.temp_img_jolly[0]}
            except Exception as e :
                pass
    class shoping_adv_extra(Thread):
        def __init__(self,link):
            self.link = link
            self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


        def get_inf_extra(self):
            self.name_holder_extra = []
            self.price_holder_extra = []
            self.img_holder_extra = []
            self.target = requests.get(self.link,headers=self.headers).text
            self.extra_name = BeautifulSoup(self.target,'html5lib').find_all("div" , {"class":"title"})
            self.extra_price = BeautifulSoup(self.target,'html5lib').find_all("div" , {"class":"c_product-price-current"})
            self.extra_img = BeautifulSoup(self.target,'html5lib').findAll("div", {"class":"image-container"})
            self.t1 = threading.Thread(target=self.extra_name)
            self.t2 = threading.Thread(target=self.extra_price)
            self.t3 = threading.Thread(target=self.extra_img)
            self.t1.start()
            self.t2.start()
            self.t3.start()
            for i in range((len(self.extra_name))):
                clean_r = self.extra_name[i].text
                self.name_holder_extra.append(clean_r)


            for i in range(len(self.extra_price)):
                clean_price = self.extra_price[i].text
                self.price_holder_extra.append(clean_price)

            for i in range(len(self.extra_img)):
                clean_result = self.extra_img[i].find('source')['srcset']
                self.img_holder_extra.append(clean_result)

            self.t1.join()
            self.t2.join()
            self.t3.join()
            try:
                return {"item name":self.name_holder_extra[0],"item price":self.price_holder_extra[0],"itemimg":self.img_holder_extra[0]}
            except Exception as e :
                return {"item name":"item not found","item price":"item not found","itemimg":"item not found"}
    class shoping_adv_jareer(Thread):
        def __init__(self,link):
            self.link = link
            self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


        def get_inf_jarrer(self):
            self.name_holder_jarrer = []
            self.price_holder_jarrer = []
            self.img_holder_jarrer = []
            self.target = requests.get(self.link,headers=self.headers).text
            self.jareer_name = BeautifulSoup(self.target,'html5lib').find_all("h3" , {"class":"product-name"})
            self.jareer_price = BeautifulSoup(self.target,'html5lib').find_all("div" , {"class":"price"})
            self.jareer_img = BeautifulSoup(self.target,'html5lib').find_all("li",{"class":"item"})
            self.t1 = threading.Thread(target=self.jareer_name)
            self.t2 = threading.Thread(target=self.jareer_price)
            self.t3 = threading.Thread(target=self.jareer_img)
            self.t1.start()
            self.t2.start()
            self.t3.start()

            for i in range((len(self.jareer_name))):
                clean_r = self.jareer_name[i].text
                self.name_holder_jarrer.append(clean_r)

            for i in range(len(self.jareer_price)):
                clean_price = self.jareer_price[i].text
                self.price_holder_jarrer.append(clean_price)

            for i in range(len(self.jareer_img)):
                cleanSrc = self.jareer_img[i].find_all("img",{"class":"lazyload"})
                self.img_holder_jarrer.append(cleanSrc[0]['data-src'])
            self.t1.join()
            self.t2.join()
            self.t3.join()
            try:
                return {"item name":self.name_holder_jarrer[0],"item price":self.price_holder_jarrer[0],"itemimg":self.img_holder_jarrer[0]}
            except Exception as e :
                pass


    try:
        itemname = itemname.replace(' ','-')
        new_adv = {"sooq":shoping_adv_sooq('https://saudi.souq.com/sa-en/'+itemname+'/s/?as=1').get_inf_sooq_phone(),"jollychic":shoping_adv_jolly('https://www.jollychic.com/s/'+itemname+'?jsort=0111-120&q='+itemname).get_inf_jolly(),"extra":shoping_adv_extra('https://www.extra.com/en-sa/search/?text='+itemname).get_inf_extra(),"jareer":shoping_adv_jareer('https://www.jarir.com/sa-en/catalogsearch/result/?order=priority&dir=asc&q='+itemname).get_inf_jarrer()}
        return {'result':new_adv}
    except :
        itemname = itemname.replace(' ','-')
        new_adv = {"sooq":shoping_adv_sooq('https://saudi.souq.com/sa-en/'+itemname+'/mobile-phones-33/a-t/s/').get_inf_sooq_phone_2(),"jollychic":shoping_adv_jolly('https://www.jollychic.com/s/'+itemname+'?jsort=0111-120&q='+itemname).get_inf_jolly(),"extra":shoping_adv_extra('https://www.extra.com/en-sa/search/?text='+itemname).get_inf_extra(),"jareer":shoping_adv_jareer('https://www.jarir.com/sa-en/catalogsearch/result/?order=priority&dir=asc&q='+itemname).get_inf_jarrer()}
        return {'result':new_adv}
    finally:
        itemname = itemname.replace(' ','-')
        new_adv = {"sooq":shoping_adv_sooq('https://saudi.souq.com/sa-en/'+itemname+'/s/?as=1').get_inf_sooq(),"jollychic":shoping_adv_jolly('https://www.jollychic.com/s/'+itemname+'?jsort=0111-120&q='+itemname).get_inf_jolly(),"extra":shoping_adv_extra('https://www.extra.com/en-sa/search/?text='+itemname).get_inf_extra(),"jareer":shoping_adv_jareer('https://www.jarir.com/sa-en/catalogsearch/result/?order=priority&dir=asc&q='+itemname).get_inf_jarrer()}
        return {'result':new_adv}









if __name__ == '__main__':
    app.run(debug=True,threaded=True, port=5000)
