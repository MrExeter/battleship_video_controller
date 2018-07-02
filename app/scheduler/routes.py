'''
Description - Scheduler Routes
@author - John Sentz
@date - 25-Jun-2018
@time - 4:47 PM
'''
from flask import flash, url_for, redirect, render_template
from flask_login import login_required

from app.scheduler import sched
from app.scheduler.forms import CreateSchedulerForm, EditSchedulerForm
from app.scheduler.models import Scheduler


@sched.route('/scheduler/scheduler_list')
@login_required
def scheduler_list():
    pass


@sched.route('/scheduler/detail/<scheduler_id>')
@login_required
def scheduler_detail(scheduler_id):
    # scheduler = Scheduler.query.get(scheduler_id)
    pass


@sched.route('/scheduler/create', methods=['GET', 'POST'])
@login_required
def create_scheduler():
    form = CreateSchedulerForm()
    if form.validate_on_submit():

        Scheduler.create_scheduler(
            name=form.name.data,
            description=form.description.data,
            start_date_time=form.start_date_time.data,
            end_date_time=form.end_date_time.data,
            repeat=form.repeat.data
        )
        flash('Registration Successful')
        return redirect(url_for('sched.scheduler_list'))

    return render_template('create_kiosk.html', form=form)


@sched.route('/scheduler/edit/<scheduler_id>', methods=['GET', 'POST'])
@login_required
def edit_scheduler(scheduler_id):
    scheduler = Scheduler.query.get(scheduler_id)

    form = EditSchedulerForm(obj=scheduler)

    if form.validate_on_submit():


        db.session.add(scheduler)
        db.session.commit()
        flash('Kiosk updated successfully')
        return redirect(url_for('main.kiosk_list'))

    return render_template('edit_scheduler.html', form=form)



@sched.route('/scheduler/delete/<scheduler_id>', methods=['GET', 'POST'])
@login_required
def delete_scheduler(scheduler_id):
    pass
