'''
Description - Main and Kiosk routes
@author - John Sentz
@date - 01-Mar-2018
@time - 8:25 PM
'''

import ast

import requests
from flask import render_template, flash, request, redirect, url_for, session, jsonify
from flask_login import login_required

from app import db
from app.kiosk import main
from app.kiosk.forms import CreateKioskForm, EditKioskForm, CreateSchedulerForm, EditSchedulerForm
from app.kiosk.models import Kiosk, Scheduler


@main.route('/')
def display_kiosks():
    return redirect(url_for('authentication.do_the_login'))


@main.route('/kiosks')
@login_required
def kiosk_list():
    kiosks = Kiosk.query.all()
    return render_template('kiosk_list.html', kiosks=kiosks)


@main.route('/kiosk/detail/<kiosk_id>')
@login_required
def kiosk_detail(kiosk_id):
    kiosk = Kiosk.query.get(kiosk_id)

    status = get_kiosk_status(kiosk_id)
    status = ast.literal_eval(status)

    return render_template('kiosk_detail.html', kiosk=kiosk, status=status)


@main.route('/kiosk/delete/<kiosk_id>', methods=['GET', 'POST'])
@login_required
def delete_kiosk(kiosk_id):
    kiosk = Kiosk.query.get(kiosk_id)

    if request.method == 'POST':
        db.session.delete(kiosk)
        db.session.commit()
        flash('kiosk deleted successfully')
        return redirect(url_for('main.kiosk_list'))

    return render_template('delete_kiosk.html', kiosk=kiosk, kiosk_id=kiosk_id)


@main.route('/kiosk/edit/<kiosk_id>', methods=['GET', 'POST'])
@login_required
def edit_kiosk(kiosk_id):
    kiosk = Kiosk.query.get(kiosk_id)

    session["current_address"] = kiosk.network_address  # temp store kiosk ip address in session
    form = EditKioskForm(obj=kiosk)

    if form.validate_on_submit():
        kiosk.network_address = form.network_address.data
        kiosk.location = form.location.data
        db.session.add(kiosk)
        db.session.commit()
        flash('Kiosk updated successfully')
        return redirect(url_for('main.kiosk_list'))

    return render_template('edit_kiosk.html', form=form)


@main.route('/create/kiosk', methods=['GET', 'POST'])
@login_required
def create_kiosk():
    session["current_address"] = ''
    form = CreateKioskForm()

    if form.validate_on_submit():

        Kiosk.create_kiosk(
            network_address=form.network_address.data,
            location=form.location.data
        )
        flash('Kiosk Creation Successful')
        return redirect(url_for('main.kiosk_list'))

    return render_template('create_kiosk.html', form=form)


@main.route('/kiosk/status/<kiosk_id>', methods=['GET', 'POST'])
# @login_required
def get_kiosk_status(kiosk_id):
    kiosk = Kiosk.query.get(kiosk_id)
    url = kiosk.node_url + 'system_stats'
    try:
        r = requests.get(url, timeout=0.5)
        json_content = r.json.im_self.content
        data = json_content
    except:
        data = {"Connection_Error": "Cannot connect to Kiosk at address - {}".format(kiosk.network_address)}
        return str(data)

    return data


@main.route('/kiosk/push_scheduler/<kiosk_id>/<scheduler_id>', methods=['GET', 'POST'])
def push_scheduler(kiosk_id, scheduler_id):
    scheduler = Scheduler.query.get(scheduler_id)
    kiosk = Kiosk.query.get(kiosk_id)
    url = kiosk.node_url + 'receive_scheduler'

    scheduler_json = {
        "name": str(scheduler.name),
        "start_date": str(scheduler.start_date),
        "start_time": str(scheduler.start_time),
        "end_date": str(scheduler.end_date),
        "end_time": str(scheduler.end_date),
        "default": str(scheduler.default),
        "continuous": str(scheduler.continuous)
    }

    try:
        r = requests.post(url, json=scheduler_json, timeout=0.5)
        message = {'message': 'Video scheduler sent'}

    except:
        message = {'message': 'Error sending video scheduler'}

    return redirect(url_for('main.kiosk_detail', kiosk_id=kiosk.id)), message


@main.route('/video/loop/', methods=['GET'])
@login_required
def loop_video():
    kiosk_id = request.args.get('kiosk_id')
    movie_id = request.args.get('movie_id')
    kiosk = Kiosk.query.get(kiosk_id)
    url = kiosk.node_url + 'loop_video'
    payload = {"movie_id": movie_id}
    try:
        r = requests.get(url, params=payload)
        message = {'message': 'Loop video command sent'}

    except:
        message = {'message': 'Error sending loop command'}

    return redirect(url_for('main.kiosk_detail', kiosk_id=kiosk.id)), message


@main.route('/playlist/loop/', methods=['GET'])
@login_required
def loop_playlist():
    kiosk_id = request.args.get('kiosk_id')
    playlist_id = request.args.get('playlist_id')
    kiosk = Kiosk.query.get(kiosk_id)
    url = kiosk.node_url + 'loop_playlist'
    payload = {"playlist_id": playlist_id}

    try:
        r = requests.get(url, params=payload)
        message = {'message': 'Loop playlist command sent'}

    except:
        message = {'message': 'Error sending loop command'}

    return redirect(url_for('main.kiosk_detail', kiosk_id=kiosk.id)), message


@main.route('/playlist/stop_loop/', methods=['GET'])
@login_required
def stop_loop_playlist():
    kiosk_id = request.args.get('kiosk_id')
    kiosk = Kiosk.query.get(kiosk_id)
    url = kiosk.node_url + 'stop_loop_playlist'
    try:
        r = requests.get(url)
        message = {'message': 'Stop loop command sent'}

    except:
        message = {'message': 'Error sending stop loop command'}

    return redirect(url_for('main.kiosk_detail', kiosk_id=kiosk.id)), message


@main.route('/video/play_video_once/', methods=['GET'])
@login_required
def play_video_once():
    kiosk_id = request.args.get('kiosk_id')
    movie_id = request.args.get('movie_id')
    kiosk = Kiosk.query.get(kiosk_id)
    url = kiosk.node_url + 'play_video_once'
    payload = {"movie_id": movie_id}
    try:
        r = requests.get(url, params=payload)
        message = {'message': 'Play command sent'}

    except:
        message = {'message': 'Error sending play command'}

    return redirect(url_for('main.kiosk_detail', kiosk_id=kiosk.id)), message


@main.route('/video/stop_loop/', methods=['GET'])
@login_required
def stop_loop_video():
    kiosk_id = request.args.get('kiosk_id')
    kiosk = Kiosk.query.get(kiosk_id)
    url = kiosk.node_url + 'stop_loop_video'
    try:
        r = requests.get(url)
        message = {'message': 'Stop loop command sent'}

    except:
        message = {'message': 'Error sending stop loop command'}

    return redirect(url_for('main.kiosk_detail', kiosk_id=kiosk.id)), message


@main.route('/sleep_kiosk_display', methods=['GET'])
@login_required
def sleep_kiosk_display():
    kiosk_id = request.args.get('kiosk_id')
    kiosk = Kiosk.query.get(kiosk_id)
    url = kiosk.node_url + 'sleep_kiosk_display'
    try:
        r = requests.get(url)
        message = {'message': 'Sleep display command sent'}

    except:
        message = {'message': 'Error sending sleep display command'}

    return redirect(url_for('main.kiosk_detail', kiosk_id=kiosk.id)), message


@main.route('/wake_kiosk_display', methods=['GET'])
@login_required
def wake_kiosk_display():
    kiosk_id = request.args.get('kiosk_id')
    kiosk = Kiosk.query.get(kiosk_id)
    url = kiosk.node_url + 'wake_kiosk_display'
    try:
        r = requests.get(url)
        message = {'message': 'Wake display command sent'}

    except:
        message = {'message': 'Error sending wake display command'}

    return redirect(url_for('main.kiosk_detail', kiosk_id=kiosk.id)), message


@main.route('/kiosk_display_power_status', methods=['GET'])
@login_required
def kiosk_display_power_status():
    kiosk_id = request.args.get('kiosk_id')
    kiosk = Kiosk.query.get(kiosk_id)
    url = kiosk.node_url + 'kiosk_display_power_status'
    try:
        r = requests.get(url)
        message = {'message': 'Display power status command sent'}

    except:
        message = {'message': 'Error sending display power status command'}

    return redirect(url_for('main.kiosk_detail', kiosk_id=kiosk.id)), message



@main.route('/kiosk/tester', methods=['GET'])
@login_required
def test_remote_login():
    url = "http://10.0.1.13:5100/login"

    payload = "{\n\t\"email\": \"napoleon@dynamite.com\",\n\t\"password\": \"applejack\"\n}"
    headers = {
        'Content-Type': "application/json",
        'Cache-Control': "no-cache",
        'Postman-Token': "40553c1f-4ab5-48c9-906e-165b800bf9d8"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    the_cookie = response.cookies._cookies.values()
    endpoint = url + '/movie_list.html'

    return render_template(response)


@main.route('/scheduler/scheduler_list')
@login_required
def scheduler_list():
    schedulers = Scheduler.query.all()
    return render_template('scheduler_list.html', schedulers=schedulers)


@main.route('/scheduler/detail/<scheduler_id>')
@login_required
def scheduler_detail(scheduler_id):
    scheduler = Scheduler.query.get(scheduler_id)

    return render_template('scheduler_detail.html', scheduler=scheduler)


@main.route('/scheduler/create', methods=['GET', 'POST'])
@login_required
def create_scheduler():
    form = CreateSchedulerForm()
    if form.validate_on_submit():

        Scheduler.create_scheduler(
            name=form.name.data,
            description=form.description.data,
            start_date=form.start_date.data,
            start_time=form.start_time.data,
            end_date=form.end_date.data,
            end_time=form.end_time.data,
            default=form.default.data,
            continuous=form.continuous.data
        )
        flash('Schedule Creation Successful')
        return redirect(url_for('main.scheduler_list'))

    return render_template('create_scheduler.html', form=form)


@main.route('/scheduler/edit/<scheduler_id>', methods=['GET', 'POST'])
@login_required
def edit_scheduler(scheduler_id):
    scheduler = Scheduler.query.get(scheduler_id)

    session["current_scheduler_name"] = scheduler.name  # temp store scheduler name

    form = EditSchedulerForm(obj=scheduler)

    if form.validate_on_submit():
        scheduler.name = form.name.data
        scheduler.description = form.description.data
        scheduler.start_date = form.start_date.data
        scheduler.start_time = form.start_time.data
        scheduler.end_date = form.end_date.data
        scheduler.end_time = form.end_time.data
        scheduler.default = form.default.data
        scheduler.continuous = form.continuous.data

        db.session.add(scheduler)
        db.session.commit()
        flash('Scheduler updated successfully')
        return redirect(url_for('main.scheduler_list'))

    return render_template('edit_scheduler.html', form=form)


@main.route('/scheduler/delete/<scheduler_id>', methods=['GET', 'POST'])
@login_required
def delete_scheduler(scheduler_id):
    scheduler = Scheduler.query.get(scheduler_id)

    if request.method == 'POST':
        db.session.delete(scheduler)
        db.session.commit()
        # Scheduler.delete_scheduler(scheduler)
        flash('Scheduler deleted successfully')
        return redirect(url_for('main.scheduler_list'))

    return render_template('delete_scheduler.html', scheduler=scheduler, scheduler_id=scheduler_id)
