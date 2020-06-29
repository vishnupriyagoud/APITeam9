from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.user import UserRegister, UserLogin, UserBlogs,InsertBlogs,SearchBlog,DeleteUserPost,FindBlogs,EditBlogs
from resources.admin import AdminRegister, AdminLogin,GetAllBlogs,BlockUser,DeletePost
from datetime import datetime,timedelta

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS']=True
app.config['JWT_SECRET_KEY']='coscskillup'
api = Api(app)
jwt = JWTManager(app)

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'error':'authorization required',
        "description":"Request does not contain an access token"
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'error':'invalid token',
        "description":"Signature verification failed"
    }), 401

api.add_resource(UserRegister, '/userregister')
api.add_resource(AdminRegister, '/adminregister')
api.add_resource(UserLogin, '/userlogin')
api.add_resource(AdminLogin, '/adminlogin')
api.add_resource(GetAllBlogs, '/getblogs')
api.add_resource(UserBlogs,'/userblogs')
api.add_resource(InsertBlogs,'/insertblog')
api.add_resource(SearchBlog,'/searchblog')
api.add_resource(BlockUser,'/blockuser')
api.add_resource(DeletePost,'/deletepost')
api.add_resource(DeleteUserPost,'/deleteuserpost')
api.add_resource(FindBlogs,'/findblog')
api.add_resource(EditBlogs,'/editblog')

if __name__ == '__main__':
    app.run()
