from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
import requests
app = Flask(__name__)
data={
    "name" : "vishnupriya" ,
    "password" : "priya144"
}
# request.get_json('')
# r=requests.post('https://blogapp-flask.herokuapp.com/userlogin',json=data)
# print(r.status_code)
# print(r)
# print(r.json())
# requests.get('')
# # print(response)
data2={
    "title": "Blog"
}
r=requests.get('https://blogapp-flask.herokuapp.com/searchblog',json=data2)
print(r.status_code)
print(r)
print(r.json())
# param={
#     "name" : "vishnupriya"
# }
# r=requests.get('https://blogapp-flask.herokuapp.com/userblogs',json=param)
# print(r.status_code)
# print(r)
# print(r.json())
