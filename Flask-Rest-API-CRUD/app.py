from  flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:okasha@localhost/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False
db=SQLAlchemy(app)
ma=Marshmallow(app)


class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    semester=db.Column(db.String(100))

    def __init__(self,name,semester):
        self.name =name
        self.semester=semester

class UserSchema(ma.Schema):
    class Meta:
        fields=('id','name','semester')


userschema=UserSchema()
usersschema=UserSchema(many=True)

@app.route('/',methods=['GET'])
def get_user():
    allusers=User.query.all()
    result=usersschema.dump(allusers)
    return jsonify(result)

@app.route('/get/<id>',methods=['GET'])
def limit_user(id):
    user= User.query.get(id)
    if user:
        return userschema.jsonify(user)
    else:
        return jsonify({"Hello World":"title"})

@app.route('/post',methods=['POST'])
def set_user():
    name=request.json['name']
    semester=request.json['semester']

    user=User(name,semester)
    db.session.add(user)
    db.session.commit()
    return(userschema.jsonify(user))

@app.route('/update/<id>',methods=['PUT'])
def update(id):
    user=User.query.get(id)
    name=request.json['name']
    semester=request.json['semester']

    user.name=name
    user.semester=semester

    db.session.commit()
    return userschema.jsonify(user)

@app.route('/delete/<id>',methods=['DELETE'])

def delete(id):
    user=User.query.get(id)
    db.session.delete(user) 
    db.session.commit()

    return userschema.jsonify(user)    

if __name__ =="__main__":
    app.run(port=3000,debug=True)