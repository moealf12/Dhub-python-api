from flask import Flask,jsonify,request
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS
import html5lib
import json
from selenium import webdriver

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
    class shoping_adv:
        def __init__(self,link):
            self.link = link


        def get_inf(self):
            self.temp = []
            self.temp_price = []
            self.temp_img = []
            self.target = requests.get(self.link).text
            self.target_name = BeautifulSoup(self.target,'html5lib').findAll("h6", {"class":"title itemTitle"})
            self.target_price = BeautifulSoup(self.target,'html5lib').findAll("span", {"class":"itemPrice"})
            self.target_img = BeautifulSoup(self.target,'html5lib').findAll("img", {"class":"img-size-medium"})

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
            return {"item name":self.temp[0].strip('31 % off Quick View').replace('Quick View',''),"item price":self.temp_price[0],"itemimg":self.temp_img[0]}







    try:
        new_adv = shoping_adv('https://saudi.souq.com/sa-en/'+itemname+'/s/?as=1').get_inf()
        return {'result':new_adv}
    except Exception as e :
        return {'error':f'Cant finde {e}'}




if __name__ == '__main__':
    app.run(debug=True,threaded=True, port=5000)
