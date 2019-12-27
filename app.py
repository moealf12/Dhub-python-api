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





if __name__ == '__main__':
    app.run(threaded=True, port=5000)
