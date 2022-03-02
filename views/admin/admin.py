from flask import Blueprint, redirect, render_template, url_for,request
from flask_login import current_user
from flask_user import roles_required
from models import User, db,user_manager, Role
from .forms import UserFormCreate, UserFormDelete\
    ,UserFormUpdateChoice, UserFormUpdateCredentials, UserFormUpdatePassword
from datetime import datetime
from .admin_func import get_role_type,RoleType

admin = Blueprint('admin',__name__)

@admin.route("/")
@admin.route("/home")
@roles_required('Admin')
def admin_homepage():
    user = User.query.where(User.id == current_user.id).first()
    return render_template(
        'admin/adminHomepage.html',
        id = user.id,
        email = user.email,
        first_name = user.first_name,
        last_name = user.last_name,
        roles = [role.name for role in user.roles]
        )

@admin.route("/create", methods=["GET","POST"])
@roles_required('Admin')
def admin_create_new_user():
    form = UserFormCreate()
    if request.method == "GET":
        return render_template('admin/adminCreate.html', form=form)

    if form.validate_on_submit():
        user = User()
        user.email=form.email.data
        user.email_confirmed_at=datetime.utcnow()
        user.password=user_manager.hash_password(form.password.data) 
        user.first_name = form.first_name.data  
        user.last_name = form.last_name.data

        role = Role.query.where(Role.name == get_role_type(RoleType(form.roles.data))).first()
        user.roles.append(role)

        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('admin.admin_homepage'))

    return render_template('admin/adminCreate.html', form=form)

@admin.route("/update", methods=["GET","POST"])
@roles_required('Admin')
def admin_update_user_redirect():
    form = UserFormUpdateChoice()
    if request.method == "GET":
        return render_template('admin/adminUpdate.html', form=form)

    if form.validate_on_submit():
        if form.submit_user_update_activity.data:
            user = User.query.where(User.id == form.user_id.data).first()
            user.active = not user.active
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('admin.admin_homepage'))

        if form.submit_user_update_credentials.data:
            return redirect(url_for('admin.admin_update_user_credentials',user_id=form.user_id.data))
        if form.submit_user_update_password.data:
            return redirect(url_for('admin.admin_update_user_password',user_id=form.user_id.data))
        if form.submit_user_update_roles.data:
            return redirect(url_for('admin.admin_update_user_role',user_id=form.user_id.data))
        
        return redirect(url_for('admin.admin_homepage'))

    return render_template('admin/adminUpdate.html', form=form)

@admin.route("/update/password/<user_id>", methods=["GET","POST"])
@roles_required('Admin')
def admin_update_user_password(user_id):

    user = User.query.where(User.id == user_id).first()
    form = UserFormUpdatePassword()
    form.user_id.data = user.id

    if request.method == "GET":
        return render_template('admin/adminUpdatePassword.html', form=form)
    
    if form.validate_on_submit():
        user.password=user_manager.hash_password(form.new_password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('admin.admin_homepage'))

    return render_template('admin/adminUpdatePassword.html',form=form)

@admin.route("/update/credentials/<user_id>", methods=["GET","POST"])
@roles_required('Admin')
def admin_update_user_credentials(user_id):
    user = User.query.where(User.id == user_id).first()
    form = UserFormUpdateCredentials()
    form.user_id.data = user.id

    if request.method == "GET":
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        form.email.data = user.email

        return render_template('admin/adminUpdateCredentials.html', form=form)
    
    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.email = form.email.data 
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('admin.admin_homepage'))

    return render_template('admin/adminUpdateCredentials.html', form=form)

@admin.route("/update/role/<user_id>", methods=["GET","POST"])
@roles_required('Admin')
def admin_update_user_role(user_id):
    user = User.query.where(User.id == user_id).first()
    return render_template('admin/adminUpdateRole.html')


@admin.route("/delete", methods=["GET","POST"])
@roles_required('Admin')
def admin_delete_user():
    form = UserFormDelete()

    if request.method == "GET":
        return render_template('admin/adminDelete.html', form=form)

    if form.validate_on_submit():
        return redirect(url_for('admin.admin_homepage'))

    return render_template('admin/adminDelete.html', form=form)