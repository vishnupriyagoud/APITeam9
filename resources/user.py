from flask_restful import Resource, reqparse
from db import query
from flask_jwt_extended import create_access_token, jwt_required
from datetime import datetime,timedelta

class UserRegister(Resource):
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('rollno', type = str, required = True, help = 'roll no cannot be left blank')
        parser.add_argument('name', type = str, required = True, help = 'name cannot be left blank')
        parser.add_argument('signup_date', type = str, required = False, help = 'signup_date cannot be left blank')
        parser.add_argument('lastlogin_date', type = str, required = False, help = 'lastlogin_date cannot be left blank')
        parser.add_argument('reported_users', type = str, required = False, help = ' cannot be left blank')
        parser.add_argument('password', type = str, required = True, help = 'password cannot be left blank')
        parser.add_argument('block_status', type = str, required = False, help = 'block_status cannot be left blank')

        data = parser.parse_args()

        try:
            isAlreadyPresent = query(f"""SELECT * FROM users WHERE rollno = '{data['rollno']}'""", return_json = False)
            if len(isAlreadyPresent) > 0:
                return {"message":"Student with given roll no already exists"},400
        except:
            return {"message":"Error inserting into Users"},500

        try:
            query(f"""INSERT INTO coscproj.users (rollno,name,signup_date,lastlogin_date,password) VALUES (
                                                                                                    '{data['rollno']}',
                                                                                                    '{data['name']}',
                                                                                                    '{datetime.now().replace(microsecond=0, second=0, minute=0) - timedelta(hours=1)}',
                                                                                                    '{datetime.now().replace(microsecond=0, second=0, minute=0) - timedelta(hours=1)}',
                                                                                                    '{data['password']}'
                                                                                                    )"""
                                                                                                )
        except:
            return {"message":"Error inserting into USERS"},500

        return {"message":"Student successfully registered"},201

class StudentUser():
    def __init__(self,rollno,name,signup_date,lastlogin_date,password):
        self.rollno = rollno
        self.name = name
        self.signup_date = signup_date
        self.lastlogin_date = lastlogin_date
        self.password = password

    @classmethod
    def getStudentUserBySrollno(cls, sname):
        result = query(f"""SELECT * FROM users WHERE name = '{sname}'""",return_json=False)
        if len(result)>0: return StudentUser(result[0]['rollno'], result[0]['name'], result[0]['signup_date'], result[0]['lastlogin_date'], result[0]['password'])
        return None


class UserLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type = str, required = True, help = 'name cannot be left blank')
        parser.add_argument('password', type = str, required = True, help = 'password cannot be left blank')
        data = parser.parse_args()

        try:
            studentuser = StudentUser.getStudentUserBySrollno(data['name'])
            if studentuser and studentuser.password==data['password'] :
                access_token = create_access_token(identity=studentuser.name, expires_delta = False)
                return {    "rollno":studentuser.rollno,
                            "name":studentuser.name,
                            "access_token":access_token
                        },200
            return {"message":"Invalid credentials!"},401
        except:
            return {"message":"Error while logging in"},500

class InsertBlogs(Resource):
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('rollno', type = str, required = True, help = 'roll no cannot be left blank')
        parser.add_argument('name', type = str, required = True, help = 'name cannot be left blank')
        parser.add_argument('post_date', type = str, required = False, help = 'signup_date cannot be left blank')
        parser.add_argument('post_title', type = str, required = True, help = 'post_title cannot be left blank')
        parser.add_argument('post_content', type = str, required = True, help = ' post_content cannot be left blank')
        parser.add_argument('reported_users', type = str, required = False, help = '')

        data = parser.parse_args()

        try:
            NotPresent = query(f"""SELECT * FROM users WHERE name = '{data['name']}'""", return_json = False)
            if len(NotPresent) == 0:
                return {"message":"Student with given name does not exist in main table"},400
        except:
            return {"message":"Error inserting the blogs"},500

        try:
            NotPresent = query(f"""SELECT * FROM users WHERE rollno = '{data['rollno']}'""", return_json = False)
            if len(NotPresent) == 0:
                return {"message":"Student with given rollno does not exist in main table"},400
        except:
            return {"message":"Error inserting the blogs"},500


        try:
            query(f"""INSERT INTO blogs (rollno,name,post_date,post_title,post_content) VALUES (
                                                                                                    '{data['rollno']}',
                                                                                                    '{data['name']}',
                                                                                                    '{datetime.now().replace(microsecond=0, second=0, minute=0) - timedelta(hours=1)}',
                                                                                                    '{data['post_title']}',
                                                                                                    '{data['post_content']}'
                                                                                                    )"""
                                                                                                    )
        except:
            return {"message":"Error inserting into Blogs"},500

        return {"message":"Blog inserted successfully"},201

class EditBlogs(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('sno',type=str,required=True,help="sno cannot be left blank!")
        parser.add_argument('post_date', type = str, required = False, help = 'signup_date cannot be left blank')
        parser.add_argument('post_title', type = str, required = True, help = 'post_title cannot be left blank')
        parser.add_argument('post_content', type = str, required = True, help = ' post_content cannot be left blank')
        parser.add_argument('reported_users', type = str, required = False, help = '')

        data = parser.parse_args()

        try:
            x=query(f"""SELECT * FROM blogs WHERE sno = '{data["sno"]}'""",return_json=False)
            if len(x)>0:
                query(f"""UPDATE blogs SET
                                                post_date='{datetime.now().replace(microsecond=0, second=0, minute=0) - timedelta(hours=1)}',
                                                post_title='{data['post_title']}',
                                                post_content='{data['post_content']}'
                        WHERE sno = '{data["sno"]}'""")
                return {"message" : "Details are edited successfully!"},200
            return {"message" : "Srollno doesn't exist"},400
        except:
                return{"message" : "Error in editing details"},500

class SearchBlog(Resource):
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('title',type=str,required=True,help="please give title")
        data=parser.parse_args()
        data['title']= '%'+data['title']+'%'
        try:
            return query(f"""SELECT * FROM blogs WHERE post_title like '{data['title']}'""")
        except:
            return {"message":"There was an error displaying the data"},500


class UserBlogs(Resource):
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('name',type=str,required=True,help="please give username")
        data=parser.parse_args()
        try:
            return query(f"""SELECT * FROM blogs WHERE name='{data['name']}'""")
        except:
            return {"message":"There was an error displaying the data"},500

class DeleteUserPost(Resource):
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

class FindBlogs(Resource):
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('sno',type=str,required=True,help="please give sno")
        data=parser.parse_args()
        try:
            return query(f"""SELECT * FROM blogs WHERE sno='{data['sno']}'""")
        except:
            return {"message":"There was an error displaying the data"},500
