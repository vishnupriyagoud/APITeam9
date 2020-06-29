from flask_restful import Resource, reqparse
from db import query
from flask_jwt_extended import create_access_token, jwt_required
from resources.user import StudentUser
from datetime import datetime,timedelta

class AdminRegister(Resource):
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('rollno', type = str, required = True, help = 'rollno cannot be left blank')
        parser.add_argument('name', type = str, required = True, help = 'name cannot be left blank')
        parser.add_argument('lastlogin', type = str, required = False, help = '')
        parser.add_argument('password', type = str, required = True, help = 'dept cannot be let blank')

        data = parser.parse_args()

        try:
            isUsernameAlreadyPresent = query(f"""SELECT * FROM ADMINS WHERE name = '{data['name']}'""", return_json = False)
            if len(isUsernameAlreadyPresent) > 0:
                return {"message":"Admin with given username already exists"},400
        except:
            return {"message":"Error inserting into ADMINS"},500


        try:
            query(f"""INSERT INTO ADMINS('rollno','name','lastlogin','password') VALUES (
                                                '{data['rollno']}',
                                                '{data['name']}',
                                                '{datetime.now().replace(microsecond=0, second=0, minute=0) - timedelta(hours=1)}',
                                                '{data['apassword']}'
                                                )"""
                                                )
        except:
            return {"message":"Error inserting into ADMINS"},500

        return {"message":"Admin successfully registered"},201

class AdminUser():
    def __init__(self, rollno, name, lastlogin, password):
        self.rollno = rollno
        self.name = name
        self.lastlogin = lastlogin
        self.password = password

    @classmethod
    def getAdminUserByAusername(cls, name):
        result = query(f"""SELECT * FROM ADMINS WHERE name = '{name}'""",return_json=False)
        if len(result)>0: return AdminUser(result[0]['rollno'], result[0]['name'], result[0]['lastlogin'], result[0]['password'])
        return None


class AdminLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type = str, required = True, help = 'username cannot be left blank')
        parser.add_argument('password', type = str, required = True, help = 'password cannot be left blank')
        data = parser.parse_args()

        try:
            adminuser = AdminUser.getAdminUserByAusername(data['name'])
            if adminuser and data['password']==adminuser.password :
                access_token = create_access_token(identity=adminuser.name, expires_delta = False)
                return {    "rollno":adminuser.rollno,
                            "name":adminuser.name,
                            "access_token":access_token},200
            return {"message":"Invalid credentials!"},401
        except:
            return {"message":"Error while logging in"},500


class GetAllBlogs(Resource):
    # @jwt_required
    def get(self):
        try:
            return query(f"""SELECT * FROM blogs""")
        except:
            return {"message":"Error in fetching data"},500

class BlockUser(Resource):

    def delete(self):
        parser=reqparse.RequestParser()
        parser.add_argument('name',type=str,required=True,help="name cannot be left blank!")
        data=parser.parse_args()
        try:
            check=query(f"""SELECT * FROM Users WHERE name='{data['name']}'""",return_json=False)
            if len(check)==0: return {"message" : "No such User found."}, 404
            query(f"""DELETE FROM Users WHERE name='{data['name']}'""")
        except:
            return {"message" : "An error occurred while deleting."}, 500
        return {"message" : "Deleted successfully."}, 200

class DeletePost(Resource):

    def delete(self):
        parser=reqparse.RequestParser()
        parser.add_argument('sno',type=str,required=True,help="sno cannot be left blank!")
        data=parser.parse_args()
        try:
            check=query(f"""SELECT * FROM blogs WHERE sno='{data['sno']}'""",return_json=False)
            if len(check)==0: return {"message" : "No such Blogs found."}, 404
            query(f"""DELETE FROM blogs WHERE sno='{data['sno']}'""")
        except:
            return {"message" : "An error occurred while deleting."}, 500
        return {"message" : "Deleted successfully."}, 200
