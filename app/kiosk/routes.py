'''
Description - Main and Kiosk routes
@author - John Sentz
@date - 01-Mar-2018
@time - 8:25 PM
'''

import requests
from flask import render_template, flash, request, redirect, url_for, session, jsonify, json
from flask_login import login_required
import ast

from app import db
from app.kiosk import main
from app.kiosk.forms import CreateKioskForm, EditKioskForm
from app.kiosk.models import Kiosk


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
        flash('Registration Successful')
        return redirect(url_for('main.kiosk_list'))

    return render_template('create_kiosk.html', form=form)


@main.route('/kiosk/status/<kiosk_id>', methods=['GET', 'POST'])
# @login_required
def get_kiosk_status(kiosk_id):

    kiosk = Kiosk.query.get(kiosk_id)
    network_address = kiosk.network_address
    url = "http://" + network_address + ":5100/system_stats"
    try:
        r = requests.get(url, timeout=3)
        json_content = r.json.im_self.content
        data = json_content
    except:
        data = {"Connection_Error": "Cannot connect to Kiosk at address - {}".format(kiosk.network_address)}
        return str(data)

    return data

