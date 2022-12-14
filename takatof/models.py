from datetime import datetime
from takatof.config import HIDE_AFTER_ONE_MONTH
from takatof import db, login_manager
from flask_login import UserMixin




class Admin(db.Model, UserMixin):
    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"Admin('{self.id}', '{self.username}')"

    def get_id(self):
        return str(self.username)

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(user_id)


class Building(db.Model):
    id = db.Column(db.String(3), primary_key=True)
    visits = db.Column(db.Integer, nullable=False, default=0)
    posts = db.relationship("Post", backref="location", lazy=True)

    def __repr__(self):
        return f"Building('{self.id}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    building_id = db.Column(db.String(3), db.ForeignKey('building.id'), nullable=False)
    room_number = db.Column(db.String(3), nullable=False)
    content = db.Column(db.String(140), nullable=False)
    reports = db.Column(db.Integer, nullable=False, default=0)
    note = db.Column(db.String(140))

    def __repr__(self):
        return f"Post('{self.id}', '{self.building_id}', '{self.room_number}', '{self.content}')"

def getBuildingList():
    buildingList = list()
    for building in Building.query.order_by(Building.id.asc()).all():
        buildingList.append(building.id)
    return buildingList

def one_month_ago():
    today = datetime.utcnow()
    if today.month == 1:
        one_month_ago = today.replace(year=today.year - 1, month=12)
    else:
        extra_days = 0
        while True:
            try:
                one_month_ago = today.replace(month=today.month - 1, day=today.day - extra_days)
                break
            except ValueError:
                extra_days += 1
    return one_month_ago
            
def getPostsByBuilding(building):
    if HIDE_AFTER_ONE_MONTH:
        buildingPosts = Post.query.filter_by(building_id=building).filter(Post.date_posted>one_month_ago()).order_by(Post.date_posted.desc())
    else:
        buildingPosts = Post.query.filter_by(building_id=building).order_by(Post.date_posted.desc())
    return buildingPosts


def adminMatch(username, password):
    if Admin.query.filter_by(username=username).first() == None:
        return 0
    elif Admin.query.filter_by(username=username).first().password != password:
        return 1
    else:
        return 2

def getAdmin(username):
    return Admin.query.filter_by(username=username).first()

def postExists(id):
    if Post.query.filter_by(id=id).first() == None:
        return False
    return True

def reportPost(id):
    Post.query.filter_by(id=id).first().reports += 1
    db.session.commit()

def getPost(id):
    return Post.query.filter_by(id=id).first()

def getReports():
    return Post.query.filter(Post.reports>0).order_by(Post.reports.asc())

def cancelReports(id):
    Post.query.filter_by(id=id).first().reports = 0
    db.session.commit()

def deletePost(id):
    db.session.delete(Post.query.filter_by(id=id).first())
    db.session.commit()

def addVisit(buildingID):
    Building.query.filter_by(id=buildingID).first().visits += 1
    db.session.commit()
