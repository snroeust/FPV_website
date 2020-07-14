from __future__ import division

from datetime import datetime
from flask import flash, redirect, url_for, request, current_app
from flask_login import current_user, login_required

from app import db
from app.main.forms import EditProfileForm, EmptyForm, PostForm, RpiNameForm
from app.models import User, Post, Rpi
from app.main import bp

from flask import Response
from flask import render_template

import cv2
import numpy as np
import struct
import StreamMemory as mem
import time



@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()



@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():

        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title='Home', form=form,
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title='Explore',
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.user', username=user.username,
                       page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.user', username=user.username,
                       page=posts.prev_num) if posts.has_prev else None
    form = EmptyForm()
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url, form=form)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@bp.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('main.index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('main.user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}!'.format(username))
        return redirect(url_for('main.user', username=username))
    else:
        return redirect(url_for('main.index'))


@bp.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('main.index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('main.user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(username))
        return redirect(url_for('main.user', username=username))
    else:
        return redirect(url_for('main.index'))




def generate(name, curr):
    """ Getting image udp frame &
        concate before decode and output image """
    dat = b''
    ip_seg = mem.IP_SEG
    n = name
    count = 0
    addr = [1]
    currentTime = time.time()

    with curr.app_context():
        try:
            ip = ""
            rpis = Rpi.query.all()
            for i in rpis:
                if i.get_Rpi()[2] == n:
                    ip = i.get_Rpi()[1]

            addr[0] = ip
        except:
            print("cant get Adress!!!!!!!!!!!!!!!!!!!!!!")

    t = time.time()
    while True:
        count += 1
        if count > 200:
            currentTime = time.time()

        if currentTime > t + 30:
            t = currentTime

            with curr.app_context():
                try:
                    ip = ""
                    rpis = Rpi.query.all()
                    for i in rpis:
                        if i.get_Rpi()[2] == n:
                            ip = i.get_Rpi()[1]

                    addr[0] = ip
                except:
                    # name ist nicht in datenbank
                    break
            count = 0

        try:
            if ip_seg.get_seg(addr)[1] == False:
                continue

            seg = ip_seg.get_seg(addr)[0]
            ip_seg.dell_seg(addr)

        except:
            continue

        if struct.unpack("B", seg[0:1])[0] > 1:
            dat += seg[1:]

        else:
            dat += seg[1:]
            frame = cv2.imdecode(np.frombuffer(dat, dtype=np.uint8), 1)
            if frame is None:
                dat = b''
                continue

            (flag, encodedImage) = cv2.imencode(".jpg", frame)

            if not flag:
                dat = b''
                continue

            try:
                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                       bytearray(encodedImage) + b'\r\n')
            except:
                break
            dat = b''


@bp.route('/user/video_feed')
@login_required
def video_feed():

    curr = mem.APP_MEM.get_app()

    return Response(generate(current_user.get_rpiname(), curr),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


@bp.route('/enter_RpiName', methods=['GET', 'POST'])
@login_required
def enter_RpiName():

    form = RpiNameForm()
    if form.validate_on_submit():

        current_user.set_rpi_hash(form.rpiname.data)
        db.session.commit()
        flash('Your changes have been saved.')

        return redirect(url_for('main.enter_RpiName'))

    elif request.method == 'GET':

        try:
            form.rpiname.data = current_user.get_rpiname()
        except:
            form.rpiname.data = "your Video Device key"

    return render_template('enter_RpiName.html', title='Enter Video Device Name',
                           form=form)
