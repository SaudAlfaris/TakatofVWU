from webbrowser import get
from flask import render_template, redirect, url_for, flash, request
from takatof import app, db, login_manager
from takatof.forms import LoginForm, PostForm, SearchForm, ReportForm
from takatof.models import Post, getBuildingList, getPostsByBuilding, adminMatch, addVisit, getAdmin, getPost, postExists, deletePost, reportPost, getReports, cancelReports
from flask_login import login_user, login_required, logout_user, current_user


@app.route("/", methods=("GET", "POST"))
@app.route("/buildings", methods=("GET", "POST"))
def buildingList():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for("building", building=form.building.data))

    return render_template("buildings.html", form=form)

@app.route("/buildings/<building>")
def building(building):
    if building in getBuildingList():
        addVisit(str(building))
        if len(list(getPostsByBuilding(building=building))) == 0:
            return redirect(url_for("addPost",  building=building))
        else:
            return render_template("building.html",  building=building, buildingPosts=getPostsByBuilding(building))
    else:
        return "404: Page Not Found"

@app.route("/buildings/<building>/add", methods=("GET", "POST"))
def addPost(building):
    if len(list(getPostsByBuilding(building=building))) == 0:
        empty = True
    else:
        empty = False
    if building in getBuildingList():
        form = PostForm()
        if form.validate_on_submit():
                db.session.add(Post(building_id=str(building), room_number=form.room_number.data, content=form.content.data, note=form.note.data))
                db.session.commit()
                return redirect(url_for("building", building=building))
        return render_template("addPost.html",  empty=empty, building=building, form=form)
    else:
        return "404: Page Not Found"

@app.route("/report/<postID>", methods=("GET", "POST"))
def report(postID):
    if postExists(postID):
        post = getPost(postID)
        form = ReportForm()
        if form.validate_on_submit():
            reportPost(postID)
            flash("تم إرسال بلاغك وسيتم النظر فيه بأسرع وقت.")
            return redirect(url_for("building", building=post.building_id))
        return render_template("report.html", form=form, post=post)
    return "404: Page Not Found"

@app.route("/login", methods=("GET", "POST"))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('reports'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        matchStatus = adminMatch(username, password)
        if matchStatus != 2 :
            if matchStatus == 1:
                flash("كلمة السر غير صحيحة.")
            else:
                flash("اسم المستخدم غير صحيح.")
            return redirect(url_for("login"))
        else:
            login_user(getAdmin(username))
            return redirect(url_for("reports"))
    return render_template("login.html", form=form)

@app.route("/reports")
@login_required
def reports():
        return render_template("reports.html", posts=getReports())

@app.route("/delete/<postID>")
@login_required
def delete(postID):
    if postExists(postID):
        deletePost(postID)
        flash("تم حذف الخدمة.")
        return redirect(url_for("reports"))
    return "404: Page Not Found"

@app.route("/cancel/<postID>")
@login_required
def cancel(postID):
    if postExists(postID):
        cancelReports(postID)
        flash("تم إلغاء البلاغات على هذه الخدمة.")
        return redirect(url_for("reports"))
    return "404: Page Not Found"


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("buildingList"))