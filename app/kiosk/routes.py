


from flask import render_template, flash, request, redirect, url_for
from flask_login import login_required

from app import db
from app.kiosk import main
from app.kiosk.models import Kiosk
from app.kiosk.forms import CreateKioskForm, EditKioskForm


@main.route('/')
def display_kiosks():

    kiosks = Kiosk.query.all()
    return render_template('home.html', kiosk=kiosks)



@main.route('/kiosk/delete/<kiosk_id>', methods=['GET', 'POST'])
@login_required
def delete_kiosk(kiosk_id):
    kiosk = Kiosk.query.get(kiosk_id)

    if request.method == 'POST':
        db.session.delete(kiosk)
        db.session.commit()
        flash('kiosk deleted successfully')
        return redirect(url_for('main.display_kiosks'))

    return render_template('delete_kiosk.html', kiosk=kiosk, kiosk_id=kiosk_id)


@main.route('/kiosk/edit/<kiosk_id>', methods=['GET', 'POST'])
@login_required
def edit_kiosk(kiosk_id):
    kiosk = Kiosk.query.get(kiosk_id)
    form = EditKioskForm(obj=kiosk)

    if form.validate_on_submit():
        kiosk.network_address = form.network_address.data
        kiosk.location = form.location.data
        db.session.add(kiosk)
        db.session.commit()
        flash('Kiosk updated successfully')
        return redirect(url_for('main.display_kiosks'))

    return render_template('edit_kiosk.html', form=form)


@main.route('/create/kiosk', methods=['GET', 'POST'])
@login_required
def create_kiosk():

    form = CreateKioskForm()

    if form.validate_on_submit():
        kiosk = Kiosk(network_address=form.network_address.data,
                      location=form.location.data)

        db.session.add(kiosk)
        db.session.commit()
        flash('Kiosk added successfully')

        return redirect(url_for('main.display_kiosks'))
    return render_template('create_kiosk.html', form=form)


