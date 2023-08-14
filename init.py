from flask import Flask, render_template, render_template_string, session, request, redirect, url_for, send_from_directory
from datetime import datetime, timedelta
from pytz import timezone
import db_functions
from os import listdir,path
import json, random
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
 
################################################## Global Content ##################################################
syst_img_path = "/var/www/html/webapp/static/images/template/"
syst_pdf_path = "/var/www/html/webapp/static/pdf/"
# syst_img_path = "static/images/template/"
# syst_pdf_path = "static/pdf/"

image_paths = {}
pdf_paths = {}

folder_paths = []
image_count = 0
template_images = 0
for img_folder_path in listdir(syst_img_path):
	if '.' not in img_folder_path:
		image_paths[img_folder_path] = []
		folder_way = syst_img_path+img_folder_path
		for folder_images in listdir(folder_way):
			folder_way = "static/images/template/"+img_folder_path
			image_paths[img_folder_path].append(str(folder_way+"/"+folder_images))
image_count = [image_count+len(path_counts) for path_counts in image_paths.values()] 
template_images = 0 if image_count == 0 else 1

for pdf_folder_path in listdir(syst_pdf_path):
	if '.' not in pdf_folder_path:
		pdf_paths[pdf_folder_path] = []
		pdf_way = syst_pdf_path+pdf_folder_path
		for folder_pdfs in listdir(pdf_way):
			pdf_line = "static/pdf/"+pdf_folder_path+"/"+folder_pdfs
			pdf_paths[pdf_folder_path].append((pdf_line, folder_pdfs.split('.')[0]))

ist = timezone('Asia/Calcutta')
date_time = datetime.now(ist)
local_date = date_time.strftime("%d-%m-%Y")
db_date = date_time.strftime("%Y-%m-%d")

myapp = Flask(__name__)

@myapp.before_request
def check_session():
	session.permanent = True
	session.modified = True
	myapp.permanent_session_lifetime = timedelta(minutes=60)

sec_use = URLSafeTimedSerializer('wissendtoken')
################################################## Global Content ##################################################

################################################## Login Credentials ##################################################
@myapp.route("/", methods=["GET", "POST"])
def login_page():
	global datetime, timezone
	if request.method == "GET":
		if session.get('wissend_id', 0) != 0:
			if session['wissend_password'] == "0":
				return redirect('change_password')
			else:
				if session['emp_type'] in ['ADMIN','TA','TM','TL', 'TLR', 'TMR','TBH','TBHR','TQA']:
					return redirect('team_lead')
				else:
					return redirect('employee_page')
		else:
			return render_template("login.html", error_status="")
	else:
		ist = timezone('Asia/Calcutta')
		date_time = datetime.now(ist)
		local_date = date_time.strftime("%d-%m-%Y")
		db_date = date_time.strftime("%Y-%m-%d")
		db_month = date_time.month
		form_data = request.form
		session['local_date'] = local_date
		session['db_date'] = db_date
		session['db_month'] = db_month
		session['datetime_format'] = str(date_time.strftime("%Y-%m-%d %H:%M:%S"))
		session['wissend_id'] = form_data.get('user_id')
		session['wissend_password'] = form_data.get('user_pswd')
		if path.isfile("/var/www/html/webapp/static/images/employee_images/{}.jpg".format(session['wissend_id'])):
			session['profile_img'] = "images/employee_images/{}.jpg".format(session['wissend_id'])
		else:
			session['profile_img'] = "images/employee_images/user_logo.jpg"
		session['template_image'] = template_images
		session['template_image_path'] = image_paths
		session['template_pdf_path'] = pdf_paths

		login_data = db_functions.user_login_form(session)
		if isinstance(login_data, int) == False:
			return redirect("change_password")
		elif login_data == 0:
			return render_template("login.html", error_status="Database not connected")
		elif login_data == 1:
			if form_data.get('recover_wiss_id', '') != '':
				dynamic_otp = random.randrange(100000, 999999)
				session['otp'] = dynamic_otp
				session['recover_wissend_id'] = form_data['recover_wiss_id']
				from_mail = 'python-team@wissend.com'
				mail_password = 'W!$$@123'
				mail_data = db_functions.mail_getter_for_id(form_data['recover_wiss_id'])
				if isinstance(mail_data, int) == False:
					if mail_data[0][2] != '' and mail_data[0][2] != None:
						to_mail = mail_data[0][2]
					else:
						to_mail = 'python-team@wissend.com'
					subject_mail = 'Your OTP - Forgot Password Request'
					attachment_cid = db_functions.make_msgid()
					message_data = """
					<html>
					    <body>
					        <div style="max-width: 100%; position: relative; padding: 16px 15px; background-color: #f3f3f1;">
					            <div style="margin-left: 25%; max-width: 50%; flex: 0 0 25%; text-align: center; background-color: #fff; padding-left: 2rem; padding-right: 2rem; border-top: 10px solid #04aa6d; border-bottom: 10px solid #04aa6d;">
					                <form>
										<img src="cid:{0}"/>
					                    <p style="text-align: left; margin-top: 1rem;">Hi {1},</p>
					                    <p style="text-align: left; margin-top: 2rem;">Please use your OTP mentioned below to change your password.</p>
					                    <h2 style="text-align: left; color: #04aa6d; font-size: 32px; margin-top: 15px;">{2}</h2>
					                    <p style="text-align: left; margin-top: 2rem; margin-bottom: 0rem;">Thanks & Regards,</p>
					                    <p style="text-align: left; margin-bottom: 2rem;">Support Team.</p>
					                </form>
					            </div>
					        </div>
					    </body>
					</html>
					""".format(attachment_cid[1:-1], mail_data[0][1],dynamic_otp)
					confirm_msg = "OTP mail sent to - {} - {} - {}".format(to_mail, mail_data[0][1], form_data['recover_wiss_id'])
					db_functions.send_mail(from_mail,mail_password,to_mail,subject_mail,message_data, confirm_msg,attachment_cid)
					######################### Token Content #########################
					token = sec_use.dumps(mail_data, salt='otp-confirm')
					return redirect("/confirm_otp/{}".format(token))
				else:
					return render_template("login.html", error_status="", forgot_code='1')
			else:
				return render_template("login.html", error_status="Please enter valid credentials", forgot_code='0')
		else:
			return render_template("login.html", error_status="Connection error from the server")

@myapp.route("/confirm_otp/<token>", methods=['GET', 'POST'])
def confirm_otp(token):
	try:
		if request.method == "GET":
			token = sec_use.loads(token, salt='otp-confirm', max_age=60)
			return render_template("otp.html", token_data=token, session_otp=str(session['otp']))
		else:
			formy = request.form
			if formy.get('otp_getter', '') != '':
				if str(session['otp']) == str(formy.get('otp_getter')):
					otp_result = db_functions.otp_password_change(session['recover_wissend_id'])
					if isinstance(otp_result, str) == True:
						session['wissend_id'] = session['recover_wissend_id']
						session['wissend_password'] = '0'
						login_data = db_functions.user_login_form(session)
						if isinstance(login_data, int) == False:
							return redirect("/change_password")
						elif login_data == 0:
							return render_template("login.html", error_status="Database not connected")
						else:
							return render_template("login.html", error_status="Please enter valid credentials", forgot_code=login_data)
					else:
						return redirect("/")
				else:
					return render_template("otp.html", token_data=token, session_otp='')
	except SignatureExpired:
		return redirect('/logout')

@myapp.route("/confirm_login", methods=['GET', 'POST'])
def confirm_login():
	try:
		if request.method == "GET":
			return render_template("entry_log.html")
		else:
			formy = request.form
			if formy['login_getter'] == '1':
				json_data = {"log_on": "Success", "log_off":"Yet to submit"}
			else:	
				json_data = {}
			if session.get('wissend_id', 0) != 0:
				emp_storage = db_functions.employee_project_data(session)
				emp_storage = db_functions.insert_attendance(emp_storage, json_data)
				if isinstance(emp_storage, int) == False and emp_storage['log_on_status'] == "Success":
					session['entry_login'] = 1
					if session['emp_type'] in ['ADMIN','TA','TM','TL','TLR','TMR','TBH','TBHR','TQA']:
						return redirect("team_lead")
					else:
						return redirect("employee_page")
				else:
					return render_template("entry_log.html")
			else:
				return redirect('/')
	except:
		return redirect('/logout')
################################################## Login Credentials ##################################################

################################################# Attendance Entries #####################################################
@myapp.route('/attd_mark', methods=['GET','POST'])
def attd_mark():
	try:
		if request.method == "GET":
			return redirect('/')
		else:
			json_data = request.json
			if session.get('wissend_id', 0) != 0:
				emp_storage = db_functions.employee_project_data(session)
				emp_storage = db_functions.insert_attendance(emp_storage, json_data)
				if isinstance(emp_storage, int) == False:
					if session['emp_type'] in ['ADMIN','TA','TM','TL','TLR','TMR','TBH','TBHR','TQA']:
						emp_storage['check_key_lead'] = 0
						if session['wissend_password'] != '0':
							emp_storage['check_team'] = '1'
							emp_storage['check_key_lead'] = 0
							for process_name in emp_storage['employee_projects'].values():
								if process_name['status'] == 'Active':
									for process_data in process_name['process'].values():
										if str(process_data['lead_id']) == str(session['employee_id']) or str(process_data['manager_id']) == str(session['employee_id']) or str(process_data['business_head_id']) == str(session['employee_id']):
											emp_storage['check_key_lead'] = 1
							return render_template("team_lead_page.html", received_data=emp_storage)
						else:
							return redirect("change_password")
					else:
						return render_template("employee_page.html", received_data=emp_storage)
				else:
					return render_template_string("error")
			else:
				return redirect('/')
	except:
		print(db_functions.traceback.format_exc())
		return redirect('/logout')


def attendance_storage(attd_results, emp_storage):
	Attendance_LoginUsers = attd_results[0]
	Attendance_NotLoginUsers = attd_results[1]
	
	Attendance_LogoffUsers = []
	Attendance_Total_Data = {}
	
	Attendance_OverallUsers = attd_results[0]+attd_results[1]
	Attendance_Projects = list(dict.fromkeys([logins['Project'] for logins in Attendance_OverallUsers]))
	
	for overprojects in Attendance_Projects:
		Attendance_Total_Data[overprojects] = {'not_entered_users' : [], 'logoff_users' : []}

	dater = 0
	if emp_storage['attd_from_date'] == emp_storage['attd_to_date']:
		dater = emp_storage['attd_from_date']

	for loggy in attd_results[0]:
		if loggy['Log Off Time'] == None:
			Attendance_LogoffUsers.append(loggy)
			Attendance_Total_Data[loggy['Project']]['logoff_users'].append((loggy['Employee ID'], loggy['Employee Name'], loggy['Business Head'], dater))

	[Attendance_Total_Data[loggy2['Project']]['not_entered_users'].append((loggy2['Employee ID'], loggy2['Employee Name'], loggy2['Business Head'], dater)) for loggy2 in attd_results[1]]

	return len(Attendance_Total_Data), len(Attendance_OverallUsers), len(Attendance_LoginUsers), len(Attendance_LogoffUsers), len(Attendance_NotLoginUsers), Attendance_Total_Data

@myapp.route('/attd_report', methods=['GET','POST'])
def attd_report():
	try:
		if request.method == "GET":
			return redirect('/')
		else:
			form_data = request.form
			if session.get('wissend_id', 0) != 0:
				emp_storage = db_functions.employee_project_data(session)
				if isinstance(emp_storage, int) == False:
					project_id_list = []
					for step_projects in emp_storage['employee_projects'].values():
						if step_projects['status'] == 'Active':
							project_id_list.append(str(step_projects['project_id']))
					project_ids = ", ".join(project_id_list)
					session['team_projects'] = project_ids
					attendance_capacitor = ''
					if session['emp_type'] in ['ADMIN','TA','TM','TL','TLR','TMR','TBH','TBHR']:
						emp_storage['check_key_lead'] = 0
						if session['wissend_password'] != '0':
							emp_storage['check_team'] = '1'
							emp_storage['check_key_lead'] = 0
							for process_name in emp_storage['employee_projects'].values():
								if process_name['status'] == 'Active':
									for process_data in process_name['process'].values():
										if str(process_data['lead_id']) == str(session['employee_id']) or str(process_data['manager_id']) == str(session['employee_id']) or str(process_data['business_head_id']) == str(session['employee_id']):
											emp_storage['check_key_lead'] = 1
							if form_data.get('attd_from_date',0) != 0 and form_data.get('attd_to_date',0) != 0:
								emp_storage['attd_from_date'] = form_data['attd_from_date']
								emp_storage['attd_to_date'] = form_data['attd_to_date']
								attd_results = db_functions.report_attendance(form_data, session)
								attendance_capacitor = attendance_storage(attd_results, emp_storage)
								return render_template("attendance_report.html", received_data=emp_storage, entry_report=attd_results[0], attendance_capacitor=attendance_capacitor)
						else:
							return redirect("change_password")
					elif session['emp_type'] in ['PU','TQA']:
						if session['wissend_password'] != '0':
							if form_data.get('attd_from_date',0) != 0 and form_data.get('attd_to_date',0) != 0:
								emp_storage['attd_from_date'] = form_data['attd_from_date']
								emp_storage['attd_to_date'] = form_data['attd_to_date']
								attd_results = db_functions.report_attendance(form_data, session)
								return render_template("attendance_report.html", received_data=emp_storage, entry_report=attd_results[0], attendance_capacitor=attendance_capacitor)
						else:
							return redirect("change_password")
					else:
						return redirect('/')
				else:
					return redirect('/')
			else:
				return redirect('/')
	except:
		print(db_functions.traceback.format_exc())
		return redirect('/logout')
################################################# Attendance Entries #####################################################

################################################ Shift Block ################################################
@myapp.route("/workshift", methods=['GET', 'POST'])
def workshift():
	try:
		if request.method == "GET":
			if session.get('wissend_id', 0) != 0:
				emp_storage = db_functions.employee_project_data(session)
				if isinstance(emp_storage, int) == False:
					project_list = []
					for projects_key,projects_data in emp_storage['employee_projects'].items():
						if projects_data['status'] == "Active":
							project_list.append(projects_data['project_id'])
					if session['emp_type'] in ['ADMIN','TA','TM','TL','TLR','TMR','TBH','TBHR','TQA']:
						if session['wissend_password'] != '0':
							session['project_list'] = project_list
							workshift_data = db_functions.shift_status_pickup(session)
							return render_template("workshift_page.html", received_data=emp_storage, workshift_data=workshift_data)
						else:
							return redirect("change_password")
					else:
						return redirect('/')
				else:
					return render_template_string("error")
			else:
				return redirect('/')
		else:
			form_data = request.form
			if form_data.get("assign_project_id",0) != 0:
				db_functions.shift_project_user_insert(session,form_data)
			else:
				db_functions.shift_new_user_insert(session,form_data)
			return redirect('/workshift')
	except:
		print(db_functions.traceback.format_exc())
		return redirect('/logout')
################################################ Shift Block ################################################


################################################ Button Setup ################################################
@myapp.route("/addon", methods=['GET', 'POST'])
def addon():
	try:
		if request.method == "GET":
			if session.get('wissend_id', 0) != 0:
				emp_storage = db_functions.employee_project_data(session)
				if isinstance(emp_storage, int) == False:
					if session['emp_type'] in ['ADMIN','TA','TM','TL','TLR','TMR','TBH','TBHR','TQA']:
						if session['wissend_password'] != '0':
							acknowledgement = ''
							status_result = db_functions.shift_status_pickup(session)
							return render_template("addon_page.html", received_data=emp_storage, acknow_status=acknowledgement,shift_data=status_result)
						else:
							return redirect("change_password")
					else:
						return redirect('/')
				else:
					return render_template_string("error")
			else:
				return redirect('/')
		else:
			acknowledgement = ""
			form_data = request.form
			if session.get('wissend_id', 0) != 0:
				emp_storage = db_functions.employee_project_data(session)
				if isinstance(emp_storage, int) == False:
					if form_data.get('addon_project', 0) != 0:
						if form_data['addon_type'] == "Task Creation":
							acknowledgement = db_functions.task_creation_insert(form_data, session)
							acknowledgement['addon_type'] = 'Task Creation Status'
						else:
							acknowledgement = db_functions.process_creation_insert(form_data, emp_storage)
							acknowledgement['addon_type'] = 'Process Creation Status'
						return render_template("addon_page.html", received_data=emp_storage, acknow_status=acknowledgement)
					elif form_data.get("assign_project_id",0) != 0:
						db_functions.shift_data_insert(session,form_data)
					return render_template("addon_page.html", received_data=emp_storage, acknow_status=acknowledgement)
				else:
					return render_template_string("error") 
			else:
				return redirect('/logout')

	except:
		print(db_functions.traceback.format_exc())
		return redirect('/logout')

@myapp.route('/gallery', methods=['GET','POST'])
def gallery():
	try:
		if request.method == "GET":
			if session.get('wissend_id', 0) != 0:
				emp_storage = db_functions.employee_project_data(session)
				if isinstance(emp_storage, int) == False:
					if session['wissend_password'] != '0':
						emp_storage['template_image_path'] = session['template_image_path']
						emp_storage['template_pdf_path'] = session['template_pdf_path']
						return render_template("gallery.html", received_data=emp_storage)
					else:
						return redirect("change_password")
				else:
					return render_template_string("error")
			else:
				return redirect('/')
		else:
			return render_template("gallery.html", received_data=session)
	except:
		print(db_functions.traceback.format_exc())
		return redirect('/logout')

@myapp.route('/leave_request', methods=['GET','POST'])
def leave_request():
	try:
		if request.method == "GET":
			if session.get('wissend_id', 0) != 0:
				emp_storage = db_functions.employee_project_data(session)
				if isinstance(emp_storage, int) == False:
					if session['wissend_password'] != '0':
						leave_status = []
						leave_data = []
						leave_balance_data = {}
						leave_status_result = db_functions.leave_status_pickup(session)
						if leave_status_result != []:
							if leave_status_result[0] != []:
								for each_dict in leave_status_result[0]:
									leave_data.append({
										'Apply Date': str(each_dict['apply_date']),
										'Emp ID': str(each_dict['wiss_employee_id']),
										'Name': str(each_dict['employee_name']),
										'Type': str(each_dict['apply_type']),
										'From Date': str(each_dict['from_date']),
										'To Date': str(each_dict['to_date']),
										'# Days': str(each_dict['num_days']),
										'# Hours': str(each_dict['num_hours']),
										'Status': str(each_dict['status']),
										'Reason': str(each_dict['reason']),
										'Image':f"/static/images/employee_images/{str(each_dict['wiss_employee_id'])}.jpg",
										'Reporting1id': str(each_dict['reporting_id_1']),
										'Reporting2id': str(each_dict['reporting_id_2'])
									})
							if leave_status_result[1] != []:
								leave_balance_data = {'reporting1': {'name':str(leave_status_result[1]['reporting_1']), 'wiss_id':str(leave_status_result[1]['wiss_report_id_1']), 'emp_id':str(leave_status_result[1]['rep_emp_id1']),'Image': f"/static/images/employee_images/{str(leave_status_result[1]['wiss_report_id_1'])}.jpg"},'reporting2': {'name':str(leave_status_result[1]['reporting_2']), 'wiss_id':str(leave_status_result[1]['wiss_report_id_2']), 'emp_id':str(leave_status_result[1]['rep_emp_id2']),'Image': f"/static/images/employee_images/{str(leave_status_result[1]['wiss_report_id_2'])}.jpg"},
								'Balance': {'cl':str(leave_status_result[1]['CL']),'sl':str(leave_status_result[1]['SL']),'lop':str(leave_status_result[1]['LOP']),'perm':str(leave_status_result[1]['permission']),'od':str(leave_status_result[1]['od']),'scl':str(leave_status_result[1]['scl'])}}
							else:
								leave_balance_data = {'reporting1': {'name':'ADMIN', 'wiss_id':'ADMIN', 'emp_id':'2','Image': ""},'reporting2': {'name':'', 'wiss_id':'', 'emp_id':'','Image': ""},
								'Balance': {'cl':'0','sl':'0','lop':'0','perm':'0','od':'0','scl':'0'}}
							leave_status = [leave_data,leave_balance_data]
							
						return render_template("leave.html", received_data=emp_storage, leave_status=leave_status)
					else:
						return redirect("change_password")
				else:
					return render_template_string("error")
			else:
				return redirect('/')
		else:
			form_data = request.form
			leave_status = []
			leave_data = []
			leave_balance_data = {}
			emp_storage = db_functions.employee_project_data(session)
			leave_status_result = db_functions.leave_insert(form_data,session)
			if leave_status_result != []:
				if leave_status_result[0] != []:
					for each_dict in leave_status_result[0]:
						leave_data.append({
							'Apply Date': str(each_dict['apply_date']),
							'Emp ID': str(each_dict['wiss_employee_id']),
							'Name': str(each_dict['employee_name']),
							'Type': str(each_dict['apply_type']),
							'From Date': str(each_dict['from_date']),
							'To Date': str(each_dict['to_date']),
							'# Days': str(each_dict['num_days']),
							'# Hours': str(each_dict['num_hours']),
							'Status': str(each_dict['status']),
							'Reason': str(each_dict['reason']),
							'Image':f"/static/images/employee_images/{str(each_dict['wiss_employee_id'])}.jpg",
							'Reporting1id': str(each_dict['reporting_id_1']),
							'Reporting2id': str(each_dict['reporting_id_2'])
						})
				if leave_status_result[1] != []:
					leave_balance_data = {'reporting1': {'name':str(leave_status_result[1]['reporting_1']), 'wiss_id':str(leave_status_result[1]['wiss_report_id_1']), 'emp_id':str(leave_status_result[1]['rep_emp_id1']),'Image': f"/static/images/employee_images/{str(leave_status_result[1]['wiss_report_id_1'])}.jpg"},'reporting2': {'name':str(leave_status_result[1]['reporting_2']), 'wiss_id':str(leave_status_result[1]['wiss_report_id_2']), 'emp_id':str(leave_status_result[1]['rep_emp_id2']),'Image': f"/static/images/employee_images/{str(leave_status_result[1]['wiss_report_id_2'])}.jpg"},
					'Balance': {'cl':str(leave_status_result[1]['CL']),'sl':str(leave_status_result[1]['SL']),'lop':str(leave_status_result[1]['LOP']),'perm':str(leave_status_result[1]['permission']),'od':str(leave_status_result[1]['od']),'scl':str(leave_status_result[1]['scl'])}}
				leave_status = [leave_data,leave_balance_data]
			return render_template("leave.html", received_data=emp_storage,leave_status=leave_status)
	except:
		print(db_functions.traceback.format_exc())
		return redirect('/logout')

################################################ Employee Entries
def hours_getter(hours,minutes):
	if minutes >= 60:
		quotient = minutes//60
		total_minutes = minutes - 60* quotient
		total_hours = str(hours+quotient)+'h'+' '+str(total_minutes)+'m'
	else:
		total_hours = str(hours)+'h'+' '+str(minutes)+'m'
	return total_hours


def entries_getter(selected_entry_date, bh_projects_list):
	project_list = []
	emp_list = []
	freelancer_project_list = []
	freelancer_list = []
	emp_active = []
	freelancer_active = []
	emp_deactive = []
	freelancer_deactive = []
	emp_pactive = []
	freelancer_pactive = []
	total_report = {'Wissend':[],'Freelancer':[]}
	entry_report = db_functions.emp_entry_report(selected_entry_date)
	if session['emp_type'] in ['TBH','TBHR']:
		entry_report = [entries for entries in entry_report if entries['Project Name'] in bh_projects_list]
		for entries in entry_report:
			x = entries['Wissend ID'].startswith("WFL")
			if x == True:
				freelancer_list.append(entries['Wissend ID'])
				if entries['Status'] == 0:
					freelancer_deactive.append(entries['Wissend ID'])
				elif entries['Status'] >= 480:
					freelancer_active.append(entries['Wissend ID'])
				else:
					freelancer_pactive.append(entries['Wissend ID'])
				if entries['Project Name'] in freelancer_project_list:
					pass
				else:
					freelancer_project_list.append((entries['Project Name']))
			else:
				emp_list.append(entries['Wissend ID'])
				if entries['Status'] == 0:
					emp_deactive.append(entries['Wissend ID'])
				elif entries['Status'] >= 480:
					emp_active.append(entries['Wissend ID'])
				else:
					emp_pactive.append(entries['Wissend ID'])
			if entries['Project Name'] in project_list:
				pass
			else:
				project_list.append(entries['Project Name'])
	else:
		for entries in entry_report:
			x = entries['Wissend ID'].startswith("WFL")
			if x == True:
				freelancer_list.append(entries['Wissend ID'])
				if entries['Status'] == 0:
					freelancer_deactive.append(entries['Wissend ID'])
				elif entries['Status'] >= 480:
					freelancer_active.append(entries['Wissend ID'])
				else:
					freelancer_pactive.append(entries['Wissend ID'])
				if entries['Project Name'] in freelancer_project_list:
					pass
				else:
					freelancer_project_list.append((entries['Project Name']))
			else:
				emp_list.append(entries['Wissend ID'])
				if entries['Status'] == 0:
					emp_deactive.append(entries['Wissend ID'])
				elif entries['Status'] >= 480:
					emp_active.append(entries['Wissend ID'])
				else:
					emp_pactive.append(entries['Wissend ID'])
			if entries['Project Name'] in project_list:
				pass
			else:
				project_list.append(entries['Project Name'])

	total_report['Wissend'].append(len(project_list))
	total_report['Wissend'].append(len(emp_list))
	total_report['Wissend'].append(len(emp_active))
	total_report['Wissend'].append(len(emp_pactive))
	total_report['Wissend'].append(len(emp_deactive))
	total_report['Freelancer'].append(len(freelancer_project_list))
	total_report['Freelancer'].append(len(freelancer_list))
	total_report['Freelancer'].append(len(freelancer_active))
	total_report['Freelancer'].append(len(freelancer_pactive))
	total_report['Freelancer'].append(len(freelancer_deactive))

	if session['emp_type'] in ['TBH','TBHR']:
		entry_report = [entries for entries in entry_report if entries['Project Name'] in bh_projects_list]
		for each_entry in entry_report:
			if 'Business Head' in each_entry.keys():
				del each_entry['Business Head']
	
	entries_dict = {}
	project_list = []
	bh_dict = {}
	for entries in entry_report:
		if session['emp_type'] in ['TBH','TBHR']:
			if entries['Project Name'] in bh_projects_list:
				project_list.append((entries['Project Name'], entries['Wissend ID'], entries['Employee Name'], entries['Status'], entries['Hours'], entries['Minutes']))
				entries_dict[entries['Project Name']] = {'users_entry': [], 'status':[]}
				
		elif session['emp_type'] in ['ADMIN','TA']:
			bh_dict[entries['Business Head']] = []
			project_list.append((entries['Project Name'], entries['Wissend ID'], entries['Employee Name'], entries['Status'], entries['Hours'], entries['Minutes']))
			entries_dict[entries['Project Name']] = {'users_entry': [],'status':[],'business_head':entries['Business Head']}
	
	unique_projects = list(dict.fromkeys(project_list))
	for data_keys, data_values in entries_dict.items():
		actives = []
		pactives = []
		deactives = []
		for project_name in unique_projects:
			if data_keys == project_name[0]:
				if project_name[3] == 0:
					worked_hours = hours_getter(project_name[4],project_name[5])
					deactives.append(project_name[1]+'|'+project_name[2]+'|'+worked_hours)
				elif project_name[3] >= 480:
					worked_hours = hours_getter(project_name[4],project_name[5])
					actives.append(project_name[1]+'|'+project_name[2]+'|'+worked_hours)
				else:
					worked_hours = hours_getter(project_name[4],project_name[5])
					pactives.append(project_name[1]+'|'+project_name[2]+'|'+worked_hours)
		data_values['users_entry'].append((actives, pactives, deactives))
		data_values['status'].append((len(actives), len(pactives), len(deactives), (len(actives)+len(deactives)+len(pactives))))
		if session['emp_type'] in ['ADMIN','TA']:
			bh_dict[data_values['business_head']].append(data_values['status'])
	
	for bh_key,bh_val in bh_dict.items():
		no_emp = 0
		ent_emp = 0
		par_emp = 0
		not_ent_emp = 0
		bh_report = []
		total_project = len(bh_val)
		for bh_data in bh_val:
			no_emp = no_emp + bh_data[0][3]
			ent_emp = ent_emp + bh_data[0][0]
			par_emp = par_emp + bh_data[0][1]
			not_ent_emp = not_ent_emp + bh_data[0][2]
		bh_report.append((total_project,no_emp,ent_emp,par_emp,not_ent_emp))
		bh_dict[bh_key] = bh_report

	
	entry_report = entry_report if entry_report != [] else []
	return entry_report, entries_dict,bh_dict,total_report,freelancer_project_list

@myapp.route("/emp_entry", methods=['GET','POST'])
def emp_entry():
	try:
		if request.method == "GET":
			if session.get('master_wissend_id', 0) == 0:
				if session['wissend_password'] == "0":
					return redirect('change_password')
				else:
					emp_storage = db_functions.employee_project_data(session)
					if isinstance(emp_storage, int) == False:
						if session['emp_type'] in ['ADMIN','TA','TBH','TBHR']:
							bh_projects_list = sorted(list(emp_storage['employee_projects'].keys()))
							get_entries = entries_getter(db_date, bh_projects_list)
							
							formated_date = date_time.strftime("%d-%b-%Y")
							new_dates = [formated_date, date_time.strftime("%d-%m-%Y")]

							return render_template("employee_entry.html", received_data=emp_storage, entry_report=get_entries[0], entries_summary=get_entries[1], entry_date=new_dates,bh_report=get_entries[2],total_report=get_entries[3],freelancer_project_list=get_entries[4])
						else:
							return redirect('/')
					else:
						return redirect('/')
			else:
				return redirect('/')
		else:
			form_data = request.form
			emp_storage = db_functions.employee_project_data(session)
			if isinstance(emp_storage, int) == False:
				bh_projects_list = sorted(list(emp_storage['employee_projects'].keys()))
				ddd = datetime.strptime(form_data['entry_today_date'], "%d-%m-%Y")
				new_date = ddd.strftime("%d-%b-%Y")

				selected_entry_date = form_data['entry_today_date'].split('-')[2]+'-'+form_data['entry_today_date'].split('-')[1]+'-'+form_data['entry_today_date'].split('-')[0]
				get_entries = entries_getter(selected_entry_date, bh_projects_list)
				new_dates = [new_date, form_data['entry_today_date']]

				return render_template("employee_entry.html", received_data=emp_storage, entry_report=get_entries[0], entries_summary=get_entries[1], entry_date=new_dates,bh_report=get_entries[2],total_report=get_entries[3],freelancer_project_list=get_entries[4])
			else:
				return redirect('/')
	except:
		print(db_functions.traceback.format_exc())
		return redirect('logout')
################################################# Employee Entries
################################################ Button Setup ################################################

################################################# Report Content #####################################################
@myapp.route('/employee_process', methods=['GET', 'POST'])
def employee_process():
	try:
		if request.method == 'GET':
			if session.get('wissend_id', 0) != 0:
				if session['wissend_password'] != '0':
					return redirect('employee_page')
				else:
					return redirect("change_password")
			else:
				return redirect('employee_page')
		else:
			form_data = request.form
			if session.get('wissend_id', 0) != 0:
				emp_storage = db_functions.employee_project_data(session)
				if isinstance(emp_storage, int) == False:
					if form_data.get("project_selected", 0) != 0 and form_data.get("process_selected", 0) != 0:
						emp_storage['project_selected'] = form_data['project_selected']
						session['project_selected'] = emp_storage['project_selected']
						if emp_storage['project_selected'] != "" and emp_storage['project_selected'] != "All":
							project_data = emp_storage['employee_projects'][emp_storage['project_selected']]
							emp_storage['project_id'] = project_data['project_id']
							session['project_id'] = project_data['project_id']
						emp_storage['process_selected'] = form_data['process_selected'].split("_")[-1]
						session['process_selected'] = emp_storage['process_selected']
						if emp_storage['process_selected'] != "Quality Check":
							if emp_storage['process_selected'] != "" and emp_storage['process_selected'] != "All":
								process_data = project_data['process'][emp_storage['process_selected']]
								emp_storage['process_id'] = process_data['process_id']
								session['process_id'] = process_data['process_id']
								emp_storage['manager'] = process_data['manager']
								emp_storage['manager_id'] = process_data['manager_id']
								session['manager_id'] = process_data['manager_id']
								emp_storage['lead'] = process_data['lead']
								emp_storage['lead_id'] = process_data['lead_id']
								session['lead_id'] = process_data['lead_id']
								emp_storage['business_head'] = process_data['business_head']
								emp_storage['business_head_id'] = process_data['business_head_id']
								session['business_head_id'] = process_data['business_head_id']
								emp_storage = db_functions.category_list_data(emp_storage, session)
						else:
							return redirect("quality")
					elif form_data.get('target', 0) != 0:
						form_data_list = list(form_data.items())
						notes_target_list = form_data_list[-5:]
						del form_data_list[-5:]
						if len(form_data_list) == 11:
							form_list = [ form_data_list[i:i+11] for i in range(0, len(form_data_list), 11) ]
						else:
							form_list = [ form_data_list[i:i+10] for i in range(0, len(form_data_list), 10) ]
						emp_storage = db_functions.category_list_data(emp_storage, session)
						db_functions.production_data_insert(emp_storage, form_list, notes_target_list, session)
						return redirect("employee_page")
					return render_template("employee_project_page.html", received_data=emp_storage)
				else:
					return render_template_string("error")
			else:
				return redirect('/logout')
	except:
		print(db_functions.traceback.format_exc())
		return redirect('/logout')

@myapp.route('/employee_reports', methods=['GET', 'POST'])
def employee_reports():
	try:
		if request.method == 'GET':
			if session.get('wissend_id', 0) != 0:
				if session['emp_type'] in ['ADMIN','TA','TM','TL', 'TLR', 'TMR','TBH','TBHR','TQA']:
					if session['wissend_password'] != '0':
						return redirect("team_lead")
					else:
						return redirect("change_password")
				else:
					return redirect("employee_page")
			else:
				return redirect('/')
		else:
			form_data = request.form
			if session.get('wissend_id', 0) != 0:
				emp_storage = db_functions.employee_project_data(session)
				if isinstance(emp_storage, int) == False:
					if form_data.get('project_selected', 0) != 0:
						if form_data['project_selected'] != "" and form_data['project_selected'] != "":
							emp_storage['project_selected'] = form_data['project_selected']
							if emp_storage['project_selected'] != "" and emp_storage['project_selected'] != "All":
								project_data = emp_storage['employee_projects'][emp_storage['project_selected']]
								emp_storage['project_id'] = project_data['project_id']
							emp_storage['process_selected'] = form_data['process_selected'].split("_")[-1]
							if emp_storage['process_selected'] != "" and emp_storage['process_selected'] != "All":
								process_data = project_data['process'][emp_storage['process_selected']]
								emp_storage['process_id'] = process_data['process_id']
								emp_storage['manager'] = process_data['manager']
								emp_storage['manager_id'] = process_data['manager_id']
								emp_storage['lead'] = process_data['lead']
								emp_storage['lead_id'] = process_data['lead_id']
								emp_storage['business_head'] = process_data['business_head']
								emp_storage['business_head_id'] = process_data['business_head_id']
							emp_storage = db_functions.get_team_or_user_report(form_data, emp_storage)
							if emp_storage['project_selected'] != "" and emp_storage['project_selected'] != "All":
								emp_storage['employee_project_list'] = emp_storage['project_id']
							else:
								emp_storage['employee_project_list'] = ", ".join([ str(project_val['project_id']) for project_val in emp_storage['employee_projects'].values()])
							if emp_storage['process_selected'] != "" and emp_storage['process_selected'] != "All" and emp_storage['project_selected'] != "All":
								emp_storage['process_id'] = project_data['process'][emp_storage['process_selected']]['process_id']
								emp_storage['employee_project_list'] = emp_storage['process_id']
							else:
								emp_storage['process_id'] = ""
							emp_storage = db_functions.get_report_type(form_data, emp_storage)

							check_report_type = list(form_data.items())
							if check_report_type[0][0] == 'productivity_report':
								emp_storage['report_type'] = 'Productivity'
								emp_storage = db_functions.get_date_range_from_data(form_data, emp_storage, session)
								summary_data = db_functions.data_by_project(emp_storage)
								if isinstance(summary_data, int) == False:
									summary_data = { 'header' : summary_data[0], "data": summary_data[1], "status":"Report Summary" }
									overall_summary = {'summary_status' :"No data found"}
									return render_template("employee_report_page.html", received_data=emp_storage, summary_data=summary_data,overall_summary=overall_summary)
								else:
									summary_data = {'status' :"No data found"}
									overall_summary = {'summary_status' :"No data found"}
									return render_template("employee_report_page.html", received_data=emp_storage, summary_data=summary_data,overall_summary=overall_summary)
							else:
								if check_report_type[0][0] == 'team_quality':
									emp_storage['report_type'] = 'Quality Team'
								elif check_report_type[0][0] == 'user_quality':
									emp_storage['report_type'] = 'Quality User'
								elif check_report_type[0][0] == 'assure_quality':
									emp_storage['report_type'] = 'Quality Assurance'
								emp_storage = db_functions.get_date_range_from_quality(form_data, emp_storage, session)
								quality_data = db_functions.quality_by_project(emp_storage)
								if isinstance(quality_data, int) == False:
									quality_data = { 'user_header' : quality_data[0][0], "user_data": quality_data[0][1], 'file_header' : quality_data[1][0], "file_data": quality_data[1][1], "status":"Report Summary" }
									
								######################################## Quality Tweaking ########################################
									overall_summary = {'overall_users_data' : [], 'overall_files_data' : []}

									users_qc_recived = []
									users_qc_audited = []
									for val_ind, values in enumerate(quality_data['user_data']):
										control_users = []
										for col_ind, column_header in enumerate(quality_data['user_header']):
											if type(values[col_ind]) != str:
												control_users.append(json.dumps(str(values[col_ind])).replace('"', ''))
											else:
												control_users.append(values[col_ind].replace('\n', '').replace('\r', ''))
											if column_header == "Rcvd":
												users_qc_recived.append(int(values[col_ind]))
											elif column_header == "Audit":
												users_qc_audited.append(int(values[col_ind]))
										overall_summary['overall_users_data'].append(tuple(control_users))

									files_qc_recived = []
									files_qc_audited = []
									for val_ind, values in enumerate(quality_data['file_data']):
										control_files = []
										for col_ind, column_header in enumerate(quality_data['file_header']):
											if type(values[col_ind]) != str:
												control_files.append(json.dumps(str(values[col_ind])).replace('"', ''))
											else:
												control_files.append(values[col_ind].replace('\n', '').replace('\r', ''))
											if column_header == "Rcvd":
												files_qc_recived.append(int(values[col_ind]))
											elif column_header == "Audit":
												files_qc_audited.append(int(values[col_ind]))
										overall_summary['overall_files_data'].append(tuple(control_files))
									
									sum_qc_recived = sum(users_qc_recived+files_qc_recived)
									sum_qc_audited = sum(users_qc_audited+files_qc_audited)
									
									overall_summary['overall_qc_recived'] = [sum(users_qc_recived), sum(files_qc_recived)]
									overall_summary['overall_qc_audited'] = [sum(users_qc_audited), sum(files_qc_audited)]
									return render_template("employee_report_page.html", received_data=emp_storage, summary_data=quality_data, overall_summary=overall_summary)
								else:
									quality_data = {'status' :"No data found"}
									overall_summary = {'summary_status' :"No data found"}
									return render_template("employee_report_page.html", received_data=emp_storage, summary_data=quality_data, overall_summary=overall_summary)
								######################################## Quality Tweaking ########################################
						else:
							return redirect("team_lead")
					else:
						revert_form_data = request.form
						db_functions.revert_operation(revert_form_data, session)
						return redirect("employee_reports")
				else:
					return render_template_string("error") 
			else:
				return redirect('/logout')
	except:
		print(db_functions.traceback.format_exc())
		return redirect('/logout')

@myapp.route("/kra_report", methods=['GET','POST'])
def kra_report():
	try:
		if request.method == "GET":
			if session.get('wissend_id', 0) != 0:
				emp_storage = db_functions.employee_project_data(session)
				if isinstance(emp_storage, int) == False:
					if session['emp_type'] in ['ADMIN','TA','TM','TL', 'TLR', 'TMR','TBH','TBHR']:
						if session['wissend_password'] != '0':
							emp_storage['kra_user_id'] = session['kra_user_id']
							emp_storage['kra_report'] = "1"
							emp_storage['kra_year_selected'] = session['kra_year_selected']
							emp_storage['kra_month_selected'] = session['kra_month_selected']
							summary_result = db_functions.kra_report_details(session, emp_storage)
							return render_template("kra_report.html", received_data=emp_storage, summary_result=summary_result)
						else:
							return redirect("change_password")
					else:
						return redirect('/')
				else:
					return render_template_string("error")
			else:
				return redirect('/')
	except:
		print(db_functions.traceback.format_exc())
		return redirect('/logout')
################################################# Report Content #####################################################

################################################ Input Setup ################################################
@myapp.route("/quality", methods=['GET', 'POST'])
def quality_page():
	try:
		if request.method == "GET":
			if session.get('wissend_id', 0) != 0:
				if session['wissend_password'] != '0':
					emp_storage = db_functions.employee_project_data(session)
					if isinstance(emp_storage, int) == False:
						try:
							emp_storage['project_selected'] = session['project_selected']
							emp_storage['process_selected'] = session['process_selected']
							contribute_data = emp_storage['employee_projects'][session['project_selected']]['process'][session['process_selected']]
							emp_storage['business_head'] = contribute_data['business_head']
							emp_storage['manager'] = contribute_data['manager']
							emp_storage['lead'] = contribute_data['lead']
							emp_storage['selected_project_users'] = emp_storage['project_user_data'][session['project_selected']]
							return render_template("quality_input.html", received_data=emp_storage)
						except:
							print(db_functions.traceback.format_exc())
							return redirect("employee_page")
					else:
						return render_template_string("error")
				else:
					return redirect("change_password")
			else:
				return redirect('/')
		else:
			form_data = request.form
			emp_storage = db_functions.employee_project_data(session)
			if isinstance(emp_storage, int) == False:
				db_functions.quality_data_insert(form_data, session)
				if session['employee_designation'] not in ['Data Analyst','Senior Data Analyst']:
					if session['wissend_password'] != '0':
						return redirect("team_lead")
					else:
						return redirect("change_password")
				else:
					return redirect("employee_page")
			else:
				return render_template_string("error")
	except:
		print(db_functions.traceback.format_exc())
		return redirect('/logout')

@myapp.route('/kra_input', methods=['GET','POST'])
def kra_input():
	try:
		if request.method == "GET":
			if session.get('wissend_id', 0) != 0:
				if session['wissend_password'] != '0':
					if session['emp_type'] in ['ADMIN','TA','TM','TL','TLR','TMR','TBH','TBHR']:
						return redirect('team_lead')
					else:
						return redirect('/')
				else:
					return redirect("change_password")
			else:
				return redirect('/')
		else:
			form_data = request.form
			if len(form_data) != 4:
				insert_result = db_functions.kra_input_insert(form_data, session)
				if isinstance(insert_result, int) == False:
					return redirect('kra_report')
				else:
					return render_template_string("error")
			else:
				emp_storage = db_functions.employee_project_data(session)
				user_id = form_data['kra_user_selected']
				user_type = []
				for key1, value1 in emp_storage['project_user_data'].items():
					if key1 != "All":
						for key2, value2 in value1.items():
							[user_type.append(exact_val[6]) for exact_val in value2 if str(exact_val[1]) == str(user_id)]
				session['kra_user_id'] = user_id
				emp_storage['kra_user_id'] = user_id
				kra_input = '1' if form_data.get('kra_input', 0) != 0 else '0'
				kra_report = '1' if form_data.get('kra_report', 0) != 0 else '0'
				emp_storage['kra_input'] = kra_input
				session['kra_input'] = kra_input
				emp_storage['kra_report'] = kra_report
				session['kra_report'] = kra_report
				session['kra_year_selected'] = form_data['kra_year_selected'] if form_data.get('kra_year_selected', 0) != 0 else ''
				session['kra_month_selected'] = form_data['kra_month_selected'] if form_data.get('kra_month_selected', 0) != 0 else ''
				emp_storage['kra_year_selected'] = session['kra_year_selected'] 
				emp_storage['kra_month_selected'] = session['kra_month_selected']
				if kra_input == "1":
					user_name = ""
					user_wiss_id = ""
					for process_name in emp_storage['employee_projects'].values():
						if process_name['status'] == 'Active':
							for process_data in process_name['process'].values():
								if str(process_data['lead_id']) == str(user_id):
									session['bh_id'] = process_data['business_head_id']
									if user_type[0] in ['TL','TLR']:
										user_name = process_data['lead']
										emp_storage['kra_emp_type'] = "Lead"
										emp_storage['kra_report_lead'] = process_data['lead']
										emp_storage['kra_report_manager'] = process_data['manager']
										emp_storage['kra_report_business_head'] = process_data['business_head']
										user_wiss_id = process_data['lead_wiss_id']
										break
									else:
										continue
								elif str(process_data['manager_id']) == str(user_id):
									user_name = process_data['manager']
									emp_storage['kra_emp_type'] = "Manager"
									emp_storage['kra_report_lead'] = process_data['lead']
									emp_storage['kra_report_manager'] = process_data['manager']
									emp_storage['kra_report_business_head'] = process_data['business_head']
									user_wiss_id = process_data['manager_wiss_id']
									session['bh_id'] = process_data['business_head_id']
									break
								elif str(process_data['business_head_id']) == str(user_id):
									user_name = process_data['business_head']
									emp_storage['kra_emp_type'] = "Business Head"
									emp_storage['kra_report_lead'] = process_data['lead']
									emp_storage['kra_report_manager'] = process_data['manager']
									emp_storage['kra_report_business_head'] = process_data['business_head']
									user_wiss_id = process_data['business_head_wiss_id']
									session['bh_id'] = process_data['business_head_id']
									break
					emp_storage['kra_user'] = user_name
					emp_storage['kra_user_wiss_id'] = user_wiss_id
					kra_ques_ans = db_functions.kra_question_data(session,user_id)
					kra_prev_record = db_functions.kra_previous_records(session)
					emp_storage['kra_user_img'] = "images/employee_images/{}.jpg".format(emp_storage['kra_user_wiss_id'])
					return render_template("kra_input.html", received_data=emp_storage, kra_ques_ans=kra_ques_ans, prev_record = kra_prev_record)
				else:
					return redirect('kra_report')
	except:
		print(db_functions.traceback.format_exc())
		return redirect('/logout')
################################################ Input Setup ################################################

################################################## Profile Setup ##################################################
@myapp.route('/team_lead', methods=['GET','POST'])
def team_lead():
	try:
		if request.method == "GET":
			if session.get('wissend_id', 0) != 0:
				if session['entry_login'] == 1:
					try:
						session['template_image'] = str(int(session['template_image'])+1) if session['template_image'] != 0 else 0
					except:
						print("Team Lead - Session Timeout")
						return redirect('/logout')
					emp_storage = db_functions.employee_project_data(session)
					emp_storage['user_shift_time'] = session['user_shift_time']
					if isinstance(emp_storage, int) == False:
						if session['emp_type'] in ['ADMIN','TA','TM','TL','TLR','TMR','TBH','TBHR','TQA']:
							emp_storage['check_key_lead'] = 0
							if session['wissend_password'] != '0':
								emp_storage['check_team'] = '1'
								emp_storage['check_key_lead'] = 0
								for process_name in emp_storage['employee_projects'].values():
									if process_name['status'] == 'Active':
										for process_data in process_name['process'].values():
											if str(process_data['lead_id']) == str(session['employee_id']) or str(process_data['manager_id']) == str(session['employee_id']) or str(process_data['business_head_id']) == str(session['employee_id']):
												emp_storage['check_key_lead'] = 1
								return render_template("team_lead_page.html", received_data=emp_storage, session_storage=session)
							else:
								return redirect("change_password")
						else:
							return redirect('/')
					else:
						return render_template_string("error")
				else:
					return redirect("confirm_login")
			else:
				return redirect('/')
		else:
			return redirect('/')
	except:
		print(db_functions.traceback.format_exc())
		return redirect('/logout')

@myapp.route('/employee_page', methods=['GET', 'POST'])
def employee_page():
	emp_storage = dict()
	try:
		if request.method == 'GET':
			if session.get('wissend_id', 0) != 0:
				if session['entry_login'] == 1:
					try:
						session['template_image'] = str(int(session['template_image'])+1) if session['template_image'] != 0 else 0
					except:
						print("Employee Page - Session Timeout")
						return redirect('/logout')
					emp_storage = db_functions.employee_project_data(session)
					emp_storage['user_shift_time'] = session['user_shift_time']
					if isinstance(emp_storage, int) == False:
						if session['emp_type'] in ['ADMIN','TA','TM','TL', 'TLR', 'TMR','TBH','TBHR','TQA']:
							if session['wissend_password'] != '0':
								return redirect("team_lead")
							else:
								return redirect("change_password")
						else:
							return render_template("employee_page.html", received_data=emp_storage)
					else:
						return render_template_string("error")
				else:
					return redirect("confirm_login")
			else:
				return redirect('/')
		else:
			return render_template("employee_page.html", received_data=emp_storage)
	except:
		print(db_functions.traceback.format_exc())
		return redirect('/logout')
################################################## Profile Setup ##################################################


################################################# Additional Process #####################################################
@myapp.route("/change_password", methods=['GET', 'POST'])
def change_password():
	try:
		if request.method == "GET":
			if session.get('wissend_id', 0) != 0 :
				if session['wissend_password'] == "0":
					return render_template("change_password.html", received_data=session)
				else:
					if session.get('master_wissend_id', 0) != 0 and "/master_login" in request.referrer:
						if session['emp_type'] in ['ADMIN','MA','MU']:
							return redirect("master")
						else:
							session.clear()
							return redirect("master_login")
					else:
						if session['emp_type'] in ['ADMIN','TA','TM','TL', 'TLR', 'TMR','TBH','TBHR','TQA']:
							return redirect('team_lead')
						else:
							return redirect('employee_page')
			else:
				if session.get('master_wissend_id', 0) != 0:
					if session['emp_type'] in ['ADMIN','MA','MU']:
						return redirect("master")
					else:
						session.clear()
						return redirect("master_login")
				else:
					return redirect('/')
		else:
			form_data = request.form
			if form_data.get('new_password', 0) != 0 and form_data.get('confirm_new_password', 0) != 0:
				new_password = form_data['new_password']
				confirm_new_password = form_data['confirm_new_password']
				if new_password == confirm_new_password:
					session['wissend_password'] = db_functions.change_password(new_password, session['wissend_id'])
					if session.get('master_wissend_id', 0) != 0:
						if session['emp_type'] in ['ADMIN','MA','MU']:
							return redirect("master")
						else:
							session.clear()
							return redirect("master_login")
					else:
						if session['emp_type'] in ['ADMIN','TA','TM','TL', 'TLR', 'TMR','TBH','TBHR','TQA']:
							return redirect('team_lead')
						else:
							return redirect('employee_page')
				else:
					return render_template("change_password.html", received_data=session)
			else:
				return render_template("change_password.html", received_data=session)
	except:
		return render_template("change_password.html", received_data=session)

@myapp.route("/master_login", methods=["GET", "POST"])
def master_login_page():
	global datetime, timezone
	try:
		if request.method == "GET":
			if session.get('master_wissend_id', 0) != 0:
				if session['wissend_password'] == "0":
					return redirect('change_password')
				else:
					if session['emp_type'] in ['ADMIN','MA','MU']:
						return redirect("master")
					else:
						session.clear()
						return render_template("login.html", error_status="You cannot access master database")
			else:
				return render_template("login.html", error_status="")
		else:
			ist = timezone('Asia/Calcutta')
			date_time = datetime.now(ist)
			local_date = date_time.strftime("%d-%m-%Y")
			db_date = date_time.strftime("%Y-%m-%d")
			form_data = request.form
			session['local_date'] = local_date
			session['db_date'] = db_date
			session['master_wissend_id'] = form_data.get('user_id')
			session['wissend_password'] = form_data.get('user_pswd')
			session['profile_img'] = "images/employee_images/{}.jpg".format(session['master_wissend_id'])
			login_data = db_functions.user_login_form(session)
			if isinstance(login_data, int) == False:
				return redirect('change_password')
			elif login_data == 0:
				return render_template("login.html", error_status="Database not connected")
			else:
				return render_template("login.html", error_status="Please enter valid credentials")
	except:
		print(db_functions.traceback.format_exc())
		return redirect('/logout')

@myapp.route("/master", methods=["GET", "POST"])
def master_page():
	try:
		if request.method == "GET":
			if session.get('master_wissend_id', 0) != 0:
				if session['wissend_password'] == "0":
					return redirect('change_password')
				else:
					employee_data = db_functions.master_data("o")
					if isinstance(employee_data, int) == False:
						summary_data = { 'header' : employee_data[0], "data": employee_data[1], "summary":employee_data[2], "status":"Report Summary" }
						return render_template("master_page.html", received_data=session, employee_data=summary_data)
					else:
						summary_data = { "status":"No data found" }
						return render_template("master_page.html", received_data=session, employee_data=summary_data)
			else:
				return redirect('master_login')
		else:
			return render_template("master_page.html", received_data=session, employee_data="summary_data")
	except:
		print(db_functions.traceback.format_exc())
		return redirect('/logout')

@myapp.route("/master_data", methods=['GET', 'POST'])
def master_data_page():
	try:
		if request.method == "GET":
			if session.get('master_wissend_id', 0) != 0:
				if session['wissend_password'] == "0":
					return redirect('change_password')
				else:
					try:
						data_id = request.args['id']
						if data_id != "e":
							summary_data = db_functions.master_data(data_id)
							if isinstance(summary_data, int) == False:
								master_results = { 'header' : summary_data[0], "data": summary_data[1], "status":"Report Summary" }
								return render_template("master_report.html", received_data=session, master_result=master_results)
							elif summary_data == 0:
								master_results = {'status' :"No data found"}
								return render_template("master_report.html", received_data=session, master_result=master_results)
							else:
								master_results = {'status' :"No data found"}
								return render_template("master_report.html", received_data=session, master_result=master_results)
						else:
							master_results = {'status' :"No data found"}
							return render_template("master_report.html", received_data=session, master_result=master_results)
					except:
						print(db_functions.traceback.format_exc())
						return redirect('master')
			else:
				return redirect('master_login')
		else:
			return redirect('master')
	except:
		print(db_functions.traceback.format_exc())
		return redirect('/logout')

@myapp.route("/log_report", methods=['GET','POST'])
def log_report():
	try:
		if request.method == "GET":
			if session.get('master_wissend_id', 0) != 0:
				if session['wissend_password'] == "0":
					return redirect('change_password')
				else:
					emp_storage = db_functions.employee_project_data(session)
					if isinstance(emp_storage, int) == False:
						summary_data = { 'header' : "summary_data", "data": [], "status":"Report Summary" }
						log_user_sum = []
						return render_template("log_report.html", received_data=emp_storage, summary_data=summary_data, log_total_summary=log_user_sum)
					else:
						return redirect('/')
			else:
				return redirect('/')
		else:
			form_data = request.form
			emp_storage = db_functions.employee_project_data(session)
			if isinstance(emp_storage, int) == False:
				emp_storage['log_project_selected'] = form_data['project_selected']
				emp_storage['log_user_selected'] = form_data['log_user_selected'].split("_")[-1]
				if form_data['log_from_date'] == "":
					today_date = db_functions.indian_datetime_format(session).strftime("%d-%m-%Y")
					emp_storage['log_from_date'] = today_date
					emp_storage['log_to_date'] = today_date
				else:
					emp_storage['log_from_date'] = form_data['log_from_date']
					emp_storage['log_to_date'] = form_data['log_to_date']
				emp_storage = db_functions.get_user_from_id(form_data['project_selected'], "", emp_storage['log_user_selected'], emp_storage, "log", session)
				report_result = db_functions.get_log_report(form_data, session, emp_storage) if form_data.get("report") != None else db_functions.get_log_summary_report(form_data, session, emp_storage)
				if report_result != 0:
					summary_data = report_result[0]
					log_user_sum = report_result[1]
					log_user_sum['type'] = "Log Report" if form_data.get("report") != None else "Log Summary"
					return render_template("log_report.html", received_data=emp_storage, summary_result=summary_data, log_total_summary=log_user_sum)
				else:
					return redirect('/')
			else:
				return redirect('/')
	except:
		print(db_functions.traceback.format_exc())
		return redirect('/logout')
################################################# Additional Process #####################################################

################################################ Shift Assign ################################################
@myapp.route("/shift/status", methods=['GET', 'POST'])
def shift_status():
	try:
		data_set = {"projects":[],"all_shifts":[],"project_new_users":[]}
		project_dict = []
		
		if request.method == "GET":
			status_result = db_functions.shift_status_pickup(session)
			if status_result != []:
				for each_status_result in status_result:
					user_dict = {
								"employee_name":str(each_status_result["employee_name"]),
								"employee_id":str(each_status_result["employee_id"]),
								"wiss_employee_id":str(each_status_result["wiss_employee_id"]),
								"designation":str(each_status_result["designation"]),
								"shift_name":str(each_status_result["shift_name"]),
								}
					if data_set.get("projects",0) != 0:
						if not any(d['project_name'] == str(each_status_result['project_name']) for d in data_set["projects"]):
							user_list = []
							user_list.append(user_dict)
							data_set["projects"].append({"project_name":str(each_status_result['project_name']),"project_id":str(each_status_result['project_id']),"users":user_list})
						else:
							print("Else Part",data_set["projects"])
			if data_set.get("projects",0) != 0:
				data_set["projects"].append(project_dict)
			return render_template_string(str(data_set))
		else:
			return render_template_string("Shift assign POST")
	except:
		return redirect('/logout')
################################################ Shift Assign ################################################


@myapp.route("/logout")
def logout():
	session.clear()
	return redirect('/')

@myapp.route("/master_logout")
def master_logout_page():
	session.clear()
	return redirect('/master_login')


if __name__ == "__main__":
	myapp.config['SECRET_KEY'] = "\xfc\xacjd\xddKM7\xbcD\xce5\xe40\xe9\xb5*\xb3yi\xd4\x80\x8c\x12"
	myapp.config['SESSION_TYPE'] = 'filesystem'
	myapp.run(debug=True, port=5000)