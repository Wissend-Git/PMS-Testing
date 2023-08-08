from mysql.connector import connect, errorcode, Error
import traceback, re
from datetime import datetime, date, timedelta
import sys, time
####################### Mail Pacakges #######################
import smtplib, os, base64, traceback,os.path, ssl
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import EmailMessage
from email.utils import make_msgid #library used in init file 
from pytz import timezone


try:
	db_test = connect(host="3.21.6.232", user="db_root", password="^^Wi$$$$ROOT$$2022^^", database="wissend_db", port=3306)
	# db_test = connect(host="localhost", user="root", password="", database="wissend_db", port=3306)
	# list_cursor = db_test.cursor()
	# file_test_cursor = db_test.cursor()
	# dict_cursor = db_test.cursor(dictionary=True)
	print("\n********** Connected to Database **********\n")
except Error as conn_err:
	if conn_err.errno == errorcode.ER_BAD_DB_ERROR:
		print("\n********** Database table does not exist **********\n")
	elif conn_err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
		print("\n********** User or Password Credentials Error **********\n")
	else:
		print("\n********** {} **********\n".format(conn_err))
		print("\n********** Database Connection Error **********\n")
finally:
	def database_reconnection(cur='list'):
		global db_test
		result = 0
		try:
			if cur == 'list':
				result = db_test.cursor()
			else:
				result = db_test.cursor(dictionary=True)
		except:
			try:
				db_test = connect(host="3.21.6.232", user="db_root", password="^^Wi$$$$ROOT$$2022^^", database="wissend_db", port=3306)
				# db_test = connect(host="localhost", user="root", password="", database="wissend_db", port=3306)
				print("\n********** Re-connected to Database **********\n")
			except Error as conn_err:
				if conn_err.errno == errorcode.ER_BAD_DB_ERROR:
					print("\n********** Database table does not exist **********\n")
				elif conn_err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
					print("\n********** User or Password Credentials Error **********\n")
				else:
					print("\n********** {} **********\n".format(conn_err))
					print("\n********** Database Re-Connection Error **********\n")
			if cur == 'list':
				result = db_test.cursor()
			else:
				result = db_test.cursor(dictionary=True)
		return result

	def user_login_form(session):
		global db_test
		result = 0
		try:
			wissend_id = session['master_wissend_id'] if session.get('wissend_id', 0) == 0 else session['wissend_id']
			
			query = """
			SELECT emp_tbl.employee_id, emp_tbl.employee_name, dsg_tbl.designation, emp_tbl.employee_password, date_format(emp_tbl.joined_date, '%d-%b-%Y'), emp_typ_tbl.emp_type_shortname, dsg_tbl.desig_role FROM `employees_info` as emp_tbl
			INNER JOIN `designation_info` as dsg_tbl on emp_tbl.designation_id = dsg_tbl.designation_id
			INNER JOIN `employee_type_info` as emp_typ_tbl on emp_typ_tbl.emp_type_id = emp_tbl.employee_type_id	
			WHERE BINARY emp_tbl.wiss_employee_id = '{}' and BINARY emp_tbl.employee_password = '{}' and emp_tbl.status = "Active" limit 1;
			""".format(wissend_id, session['wissend_password'])
			list_cursor = database_reconnection()
			list_cursor.execute(query)
			employee_data = list_cursor.fetchall()

			if employee_data != None and employee_data != []:
				session['employee_id'] = employee_data[0][0]
				session['employee_name'] = employee_data[0][1].title()
				session['employee_designation'] = employee_data[0][2]
				session['wissend_password'] = str(employee_data[0][3])
				session['joined_date'] = employee_data[0][4]
				session['emp_type'] = employee_data[0][5]
				session['desig_role'] = employee_data[0][6]
				session['entry_login'] = 0
				
				attd_query = """
				SELECT * from `attendance_tracker` WHERE employee_id = '{}' and attendance_date = '{}' limit 1;
				""".format(session['employee_id'], session['db_date'])
				dict_cursor = database_reconnection(cur="dict")
				dict_cursor.execute(attd_query)
				attendance_data = dict_cursor.fetchall()
				if attendance_data != None and attendance_data != []:
					if str(attendance_data[0]['in_time'])  != "None":
						session['entry_login'] = 1
					else:	
						session['entry_login'] = 0
				result = session
			else:
				print("{} | User data not found".format(wissend_id))
				result = 1
		except:
			print(traceback.format_exc())
		finally:
			return result

	def send_mail(from_mail,mail_password,to_mail,subject_mail,message_data, confirm_msg, attachment_cid):
		global MIMEMultipart,MIMEText,MIMEBase,encoders,EmailMessage
		# mail_message = MIMEMultipart()
		mail_message = EmailMessage()
		mail_message['From'] = 'Wissend Team'
		mail_message['To'] = to_mail
		mail_message['Subject'] = subject_mail
		
		mail_message.set_content(message_data, 'html', 'utf-8')
		with open("/var/www/html/webapp/static/images/icons/250x100.png", 'rb') as fp:
			mail_message.add_related(fp.read(), 'image', 'png', cid=attachment_cid)
		mail_message.attach(MIMEText(message_data, 'html', 'utf-8'))
		try:
			server = smtplib.SMTP('smtp.gmail.com', 587)
			server.ehlo()
			server.starttls()
			server.login(from_mail, mail_password)
			server.sendmail(from_mail, to_mail, mail_message.as_string())
			print(confirm_msg)
		except Exception as e:
			print(e)
		finally:
			server.close()
		return True

	def mail_getter_for_id(recover_wiss_id):
		global db_test
		result = 0
		try:
			query = 'select wiss_employee_id, employee_name, active_mail from employees_info where wiss_employee_id = "{}" and status = "Active"'.format(recover_wiss_id)
			list_cursor = database_reconnection()
			list_cursor.execute(query)
			mail_getter_data = list_cursor.fetchall()
			if mail_getter_data != []:
				result = mail_getter_data
			else:
				result = 1
		except:
			print(traceback.format_exc())
		return result

	def otp_password_change(rwid):
		global db_test
		result = 0
		try:
			query = """UPDATE `employees_info` SET employee_password = 0 WHERE wiss_employee_id = '{}';""".format(rwid)
			list_cursor = database_reconnection()
			list_cursor.execute(query)
			db_test.commit()
			result = "New password updated"
			print("OTP - Password Changed -",rwid)
		except:
			print(traceback.format_exc())
		return result
	
	def employee_project_data(session_data):
		global db_test
		result = 0
		data = dict()
		date_time_format = indian_datetime_format(session_data)
		data['wissend_id'] = session_data['wissend_id']
		data['employee_id'] = session_data['employee_id']
		data['employee_name'] = session_data['employee_name']
		data['employee_designation'] = session_data['employee_designation']
		data['joined_date'] = session_data['joined_date']
		data['db_date'] = session_data['db_date']
		data['emp_type'] = session_data['emp_type']
		data['profile_img'] = session_data['profile_img']
		data['template_image'] = session_data['template_image']
		data['template_image_path'] = session_data['template_image_path']
		data['template_pdf_path'] = session_data['template_pdf_path']
		data['desig_role'] = session_data['desig_role']
		data['from_date'] = ""
		data['to_date'] = ""
		data['year_selected'] = ""
		data['month_selected'] = ""
		data['result_year'] = ""
		data['result_month'] = ""
		data['result_week'] = ""
		data['result_day'] = ""
		data['project_selected'] = ""
		data['process_selected'] = ""
		data['report_process_selected'] = ""
		data['employee_projects'] = ""
		data['project_user_data'] = ""
		data['kra_year_selected'] = "{}".format(date_time_format.strftime("%Y"))
		data['kra_month_selected'] = "{}".format(int(date_time_format.strftime("%m")))
		data['kra_input'] = ""
		data['kra_report'] = ""
		data['production_date'] = ""
		data['quality_date'] = ""
		data['selected_project_users'] = ""
		data['report_type'] = ""
		data['report_name'] = ""
		data['log_from_date'] = ""
		data['log_to_date'] = ""
		data['log_user_selected'] = ""
		data['log_project_selected'] = ""
		data['log_projectname_selected'] = ""
		data['log_processname_selected'] = ""
		data['log_username_selected'] = ""
		
		data['attd_from_date'] = ""
		data['attd_to_date'] = ""
		data['log_on_status'] = "Yet to submit"
		data['log_off_status'] = "Yet to submit"
		data['log_on_time'] = ""
		data['log_off_time'] = ""
		try:
			if session_data['emp_type'] in ['ADMIN', 'TA', 'MA', 'MU','TQA']:
				emp_query = " WHERE emp_prcs_tbl.status = 'Active' "
			else:
				emp_query = " WHERE emp_prcs_tbl.employee_id = '{}' ".format(session_data['employee_id'])
			attd_query = """
			SELECT * from `attendance_tracker` WHERE employee_id = '{}' and attendance_date = '{}' limit 1;
			""".format(session_data['employee_id'], data['db_date'])
			dict_cursor = database_reconnection(cur="dict")
			dict_cursor.execute(attd_query)
			attendance_data = dict_cursor.fetchall()
			if attendance_data != None and attendance_data != []:
				if str(attendance_data[0]['in_time'])  != "None":
					data['log_on_status'] = "Success"
					data['log_on_time'] = datetime.strftime(attendance_data[0]['in_time'], "%d-%b-%Y | %I:%M:%S %p")
					current_login_date = datetime.strftime(attendance_data[0]['in_time'], "%d-%b-%Y")
					data['log_off_time'] = f"{current_login_date} | 00:00:00 NA"
					data['log_total_hrs'] = "00 : 00"
				if str(attendance_data[0]['out_time']) != "None":
					data['log_off_status'] = "Success"
					data['log_on_time'] = datetime.strftime(attendance_data[0]['in_time'], "%d-%b-%Y | %I:%M:%S %p")
					data['log_off_time'] = datetime.strftime(attendance_data[0]['out_time'], "%d-%b-%Y | %I:%M:%S %p")
					diffg = attendance_data[0]['out_time'] - attendance_data[0]['in_time']
					data['log_total_hrs'] = "0"+str(diffg).split(':')[0]+" : "+str(diffg).split(':')[1] if len(str(diffg).split(':')[0]) == 1 else str(diffg).split(':')[0]+" : "+str(diffg).split(':')[1]
				else:
					data['log_off_status'] = "Yet to submit"
					data['log_total_hrs'] = "00 : 00"

			query = """
			SELECT prj_tbl.project_name, prj_tbl.project_id, prj_tbl.project_short_name, prj_prcs_tbl.process_name, prj_prcs_tbl.project_process_id, prj_prcs_tbl.process_short_name, manager_tbl.employee_name, prj_prcs_tbl.manager_id, lead_tbl.employee_name, prj_prcs_tbl.team_lead_id, business_head_tbl.employee_name, prj_prcs_tbl.business_head_id, emp_prcs_tbl.status, manager_tbl.wiss_employee_id, lead_tbl.wiss_employee_id, business_head_tbl.wiss_employee_id FROM `employee_process_info` as emp_prcs_tbl
			INNER JOIN `project_process_info` as prj_prcs_tbl on prj_prcs_tbl.project_process_id = emp_prcs_tbl.project_process_id
			INNER JOIN `projects_info` as prj_tbl on prj_tbl.project_id = prj_prcs_tbl.project_id
			INNER JOIN `employees_info` as manager_tbl on prj_prcs_tbl.manager_id = manager_tbl.employee_id
			INNER JOIN `employees_info` as lead_tbl on prj_prcs_tbl.team_lead_id = lead_tbl.employee_id
			INNER JOIN `employees_info` as business_head_tbl on prj_prcs_tbl.business_head_id = business_head_tbl.employee_id
			{};
			""".format(emp_query)
			list_cursor = database_reconnection()
			list_cursor.execute(query)
			employee_data = list_cursor.fetchall()
			#list_cursor.close()
			if employee_data != None and employee_data != []:
				data_count = 0
				if employee_data != []:
					project_data = dict()
					log_users_list = []
					for project in employee_data:
						if project_data.get(project[0], 0) == 0:
							log_users_list.append(str(project[1]))
							project_data[project[0]] = { 
								"project_id" : project[1],
								"project_short_name" : project[2],
								"status": project[12],
								"process": { 
									project[3] : {
										"process_id" : project[4],
										"process_short_name" : project[5],
										"manager" : project[6],
										"manager_id" : project[7],
										"manager_wiss_id" : project[13],
										"lead" : project[8],
										"lead_id" : project[9],
										"lead_wiss_id" : project[14],
										"business_head" : project[10],
										"business_head_id" : project[11],
										"business_head_wiss_id" : project[15]
									}
								}
							}
							if data_count == 0:
								data['manager'] = project[6]
								data['manager_id'] = project[7]
								data['manager_wiss_id'] = project[13]
								data['lead'] = project[8]
								data['lead_id'] = project[9]
								data['lead_wiss_id'] = project[14]
								data['business_head'] = project[10]
								data['business_head_id'] = project[11]
								data['business_head_wiss_id'] = project[15]
								data_count = 1
						else:
							project_data[project[0]]["process"][project[3]] = { 
								"process_id" : project[4],
								"process_short_name" : project[5],
								"manager" : project[6],
								"manager_id" : project[7],
								"manager_wiss_id" : project[13],
								"lead" : project[8],
								"lead_id" : project[9],
								"lead_wiss_id" : project[14],
								"business_head" : project[10],
								"business_head_id" : project[11],
								"business_head_wiss_id" : project[15]
							}
					data['employee_projects'] = project_data
				if session_data['emp_type'] in ['TM', 'TL', 'TLR','TMR','TBH','TBHR','PU']:
					project_list = []
					process_list = []
					for prj in data['employee_projects'].values():
						prj_id = "'{}'".format(prj['project_id'])
						project_list.append(prj_id)
						for prcs in prj['process'].values():
							prcs_id = "'{}'".format(prcs['process_id'])
							process_list.append(prcs_id)
					project_id_list = ", ".join(project_list)
					process_id_list = ", ".join(process_list)
					if session_data['emp_type'] in ['TM', 'TMR','TBH','TBHR']:
						project_user_query = """
						select prj_tbl.project_id, prj_tbl.project_name, prj_prcs_tbl.project_process_id, prj_prcs_tbl.process_name, concat(emp_info.employee_name," - ",emp_info.wiss_employee_id), emp_info.employee_id, prj_tbl.project_short_name, prj_prcs_tbl.process_short_name, emp_prcs_tbl.status, emp_typ_tbl.emp_type_shortname, desig_tbl.designation from projects_info as prj_tbl
						inner join project_process_info as prj_prcs_tbl on prj_prcs_tbl.project_id = prj_tbl.project_id
						inner join employee_process_info as emp_prcs_tbl on prj_prcs_tbl.project_process_id = emp_prcs_tbl.project_process_id
						inner join employees_info as emp_info on emp_prcs_tbl.employee_id = emp_info.employee_id
						inner join designation_info as desig_tbl on desig_tbl.designation_id = emp_info.designation_id
						inner join `employee_type_info` as emp_typ_tbl on emp_typ_tbl.emp_type_id = emp_info.employee_type_id
						where prj_tbl.project_id in ({}) and prj_prcs_tbl.project_process_id in ({}) and prj_prcs_tbl.business_head_id != emp_info.employee_id and emp_typ_tbl.emp_type_shortname not in ('ADMIN','TA') and emp_info.status = 'Active' and emp_prcs_tbl.status = 'Active' GROUP by prj_tbl.project_name, emp_info.employee_id order by prj_tbl.project_name asc, prj_prcs_tbl.process_name asc, emp_info.employee_name asc;""".format(project_id_list, process_id_list)
						list_cursor = database_reconnection()
						list_cursor.execute(project_user_query)
						project_user_data_list = list_cursor.fetchall()
						#list_cursor.close()
					else:
						project_user_query = """
						select prj_tbl.project_id, prj_tbl.project_name, prj_prcs_tbl.project_process_id, prj_prcs_tbl.process_name, concat(emp_info.employee_name," - ",emp_info.wiss_employee_id), emp_info.employee_id, prj_tbl.project_short_name, prj_prcs_tbl.process_short_name, emp_prcs_tbl.status, emp_typ_tbl.emp_type_shortname, desig_tbl.designation from projects_info as prj_tbl
						inner join project_process_info as prj_prcs_tbl on prj_prcs_tbl.project_id = prj_tbl.project_id
						inner join employee_process_info as emp_prcs_tbl on prj_prcs_tbl.project_process_id = emp_prcs_tbl.project_process_id
						inner join employees_info as emp_info on emp_prcs_tbl.employee_id = emp_info.employee_id
						inner join designation_info as desig_tbl on desig_tbl.designation_id = emp_info.designation_id
						inner join `employee_type_info` as emp_typ_tbl on emp_typ_tbl.emp_type_id = emp_info.employee_type_id
						where prj_tbl.project_id in ({}) and prj_prcs_tbl.project_process_id in ({}) and prj_prcs_tbl.business_head_id != emp_info.employee_id and emp_typ_tbl.emp_type_shortname not in ('ADMIN','TA') and emp_info.status = 'Active' and emp_prcs_tbl.status = 'Active' GROUP by prj_tbl.project_name, emp_info.employee_id  order by prj_tbl.project_name asc, prj_prcs_tbl.process_name asc, emp_info.employee_name asc;""".format(project_id_list, process_id_list)
						list_cursor = database_reconnection()
						list_cursor.execute(project_user_query)
						project_user_data_list = list_cursor.fetchall()
						#list_cursor.close()
				elif session_data['emp_type'] in ['ADMIN','TA','TQA']:
					project_user_query = """
					select prj_tbl.project_id, prj_tbl.project_name, prj_prcs_tbl.project_process_id, prj_prcs_tbl.process_name, concat(emp_info.employee_name," - ",emp_info.wiss_employee_id), emp_info.employee_id, prj_tbl.project_short_name, prj_prcs_tbl.process_short_name, emp_prcs_tbl.status, emp_typ_tbl.emp_type_shortname, desig_tbl.designation from projects_info as prj_tbl
					inner join project_process_info as prj_prcs_tbl on prj_prcs_tbl.project_id = prj_tbl.project_id
					inner join employee_process_info as emp_prcs_tbl on prj_prcs_tbl.project_process_id = emp_prcs_tbl.project_process_id
					inner join employees_info as emp_info on emp_prcs_tbl.employee_id = emp_info.employee_id
					inner join designation_info as desig_tbl on desig_tbl.designation_id = emp_info.designation_id
					inner join `employee_type_info` as emp_typ_tbl on emp_typ_tbl.emp_type_id = emp_info.employee_type_id
					where prj_prcs_tbl.business_head_id != emp_info.employee_id and emp_info.status = 'Active' and emp_prcs_tbl.status = 'Active'  GROUP by prj_tbl.project_name, emp_info.employee_id  order by prj_tbl.project_name asc, prj_prcs_tbl.process_name asc, emp_info.employee_name asc;
					"""
					list_cursor = database_reconnection()
					list_cursor.execute(project_user_query)
					project_user_data_list = list_cursor.fetchall()
					#list_cursor.close()
				if session_data['emp_type'] in ['ADMIN','TA','TM', 'TL', 'TLR', 'TMR','TBH','TBHR','TQA','PU'] and project_user_data_list != []:
					project_emp_dict = {'All':[]}
					project_emp_list = []
					if project_user_data_list != []:
						for project_user_data in project_user_data_list:
							if project_emp_dict.get(project_user_data[1], 0) == 0:
								project_emp_dict[project_user_data[1]] = {project_user_data[3]:[(project_user_data[4],project_user_data[5], project_user_data[1], project_user_data[6], project_user_data[7], project_user_data[8], project_user_data[9], project_user_data[10])]}
							else:
								if project_emp_dict[project_user_data[1]].get(project_user_data[3], 0) == 0:
									project_emp_dict[project_user_data[1]][project_user_data[3]] = [(project_user_data[4],project_user_data[5], project_user_data[1], project_user_data[6], project_user_data[7], project_user_data[8], project_user_data[9], project_user_data[10])]
								else:
									project_emp_dict[project_user_data[1]][project_user_data[3]].append((project_user_data[4],project_user_data[5], project_user_data[1], project_user_data[6], project_user_data[7], project_user_data[8], project_user_data[9], project_user_data[10]))
							if project_user_data[4] not in project_emp_list:
								project_emp_dict['All'].append((project_user_data[4],project_user_data[5], project_user_data[1], project_user_data[6], project_user_data[1], project_user_data[3], project_user_data[7], project_user_data[8], project_user_data[9], project_user_data[10]))
								project_emp_list.append(project_user_data[4])
					data['project_user_data'] = project_emp_dict
				log_query = """
				SELECT prj_tbl.project_name, emp_tbl.employee_name, emp_tbl.wiss_employee_id, emp_tbl.employee_id FROM `employees_info` as emp_tbl INNER JOIN `projects_info` as prj_tbl on prj_tbl.project_id = emp_tbl.project_id where emp_tbl.project_id in ({})
				""".format(",".join(log_users_list))
				list_cursor = database_reconnection()
				list_cursor.execute(log_query)
				log_user_list = list_cursor.fetchall()
				#list_cursor.close()
				data['log_users'] = log_user_list
				
				result = data
			else:
				print("User data not found")
				result = 2
		except:
			print("Error - {} - {}".format(data['wissend_id'],data['employee_name']))
			print(traceback.format_exc())
		finally:
			return result
	
	def category_list_data(data, session):
		try:
			query = """
			select prj_cat_tbl.category_name, prj_cat_tbl.category_id, prj_task_tbl.task_name, prj_task_tbl.task_id from project_category_level_info as prj_cat_lvl_tbl
			inner join `project_category_info` as prj_cat_tbl on prj_cat_lvl_tbl.end_level_category_id = prj_cat_tbl.category_id
			inner join `project_task_info` as prj_task_tbl on prj_cat_lvl_tbl.project_id = prj_task_tbl.project_id
			where prj_cat_lvl_tbl.project_id = '{0}' and prj_task_tbl.project_id = '{0}';
			""".format(session['project_id'])
			results = get_production_data_by_query(query)
			if results != 0 and results[1] != []:
				data['category_list'] = []
				data['category_id_list'] = []
				data['task_list'] = []
				data['task_id_list'] = []
				for result_data in results[1]:
					if result_data[0] not in data['category_list']:
						data['category_list'].append(result_data[0])
						data['category_id_list'].append((result_data[0], result_data[1]))
					if result_data[2] not in data['task_list']:
						data['task_list'].append(result_data[2])
						data['task_id_list'].append((result_data[2], result_data[3]))
				data['category_list'] = sorted(data['category_list'])
				data['task_list'] = sorted(data['task_list'])
		except:
			print(traceback.format_exc())
		return data

	
	def db_close():
		# #list_cursor.close()
		db_test.close()
		return True

	def regex_findall(regex, content, match_case=0):
		if match_case == 0:
			return re.findall(regex, content)
		else:
			return re.findall(regex, content, flags=match_case)
	
	def get_production_data_by_query(query):
		global db_test
		result = 0
		try:
			list_cursor = database_reconnection()
			list_cursor.execute(query)
			column_names = [i[0] for i in list_cursor.description]
			employee_production = list_cursor.fetchall()
			#list_cursor.close()
			result_status = column_names
			result = [result_status, employee_production]
		except:
			print(traceback.format_exc())
		finally:
			return result
	
	def get_team_or_user_report(form, data):
		if form.get('user_selected', 0) == 0:
			data['user_selected'] = data['employee_id']
		else:
			data['user_selected'] = form['user_selected']
		data['user_selected_all'] = ""
		if form.get('check_project') == "on":
			if form.get('check_process', 0) != 0:
				if form.get('check_user', 0) != 0:
					data['check_project'] = "1"
					data['check_process'] = "1"
					data['check_user'] = "1"
				else:
					data['check_project'] = "1"
					data['check_process'] = "1"
					data['check_user'] = "0"
			else:
				if form.get('check_user', 0) != 0:
					data['check_project'] = "1"
					data['check_process'] = "0"
					data['check_user'] = "1"
				else:
					data['check_project'] = "1"
					data['check_process'] = "0"
					data['check_user'] = "0"
		else:
			data['check_project'] = "0"
			data['check_process'] = "0"
			data['check_user'] = "1"
		if form.get('user_selected', 0) != 0:
			if form['user_selected'] != "All" and form['user_selected'] != "":
				data['user_selected'] = int(form.get('user_selected').split("_")[-1])
			else:
				user_data_list = []
				if data['project_selected'] != "All" and data['project_selected'] != '':
					for project_users in data['project_user_data'][data['project_selected']].values():
						for users_data in project_users:
							if str(users_data[1]) not in user_data_list:
								user_data_list.append(str(users_data[1]))
				else:
					for project_users in data['project_user_data']["All"]:
						if str(project_users[1]) not in user_data_list:
							user_data_list.append(str(project_users[1]))
				data['user_selected_all'] = ", ".join(user_data_list)
		return data

	def get_report_type(form, data):
		if form.get("result_week", 0) != 0:
			data['result_year'] = 0
			data['result_month'] = 0
			data['result_week'] = 1
			data['result_day'] = 0
		elif form.get("result_month", 0) != 0:
			data['result_year'] = 0
			data['result_month'] = 1
			data['result_week'] = 0
			data['result_day'] = 0
		elif form.get("result_day", 0) != 0:
			data['result_year'] = 0
			data['result_month'] = 0
			data['result_week'] = 0
			data['result_day'] = 1
		elif form.get("result_year", 0) != 0:
			data['result_year'] = 1
			data['result_month'] = 0
			data['result_week'] = 0
			data['result_day'] = 0
		return data
		

	def get_date_range_from_data(form, data, session_data):
		data['year_selected'] = form.get("year_selected")
		data['month_selected'] = form.get("month_selected")
		if form.get("from_date") != "":
			data['from_date'] = datetime.strptime(form.get("from_date"), "%d-%m-%Y").strftime("%Y-%m-%d")
		else:
			data['from_date'] = ""
		if form.get("to_date") != "":
			data['to_date'] = datetime.strptime(form.get("to_date"), "%d-%m-%Y").strftime("%Y-%m-%d")
		else:
			data['to_date'] = ""
		today_date = indian_datetime_format(session_data)
		if any([data['year_selected'], data['month_selected'], data['from_date'], data['to_date']]) == False:
			if today_date.day != 1:
				filter_condition = " and year(prod_tbl.production_date) in ('{}') and month(prod_tbl.production_date) in ('{}') ".format(today_date.year, today_date.month)
				data['year_selected'] = "{}".format(today_date.year)
				data['month_selected'] = "{}".format(today_date.month)
			elif today_date.month == 1 and today_date.day == 1:
				filter_condition = " and year(prod_tbl.production_date) in ('{}') and month(prod_tbl.production_date) in ('12') ".format(today_date.year-1)
				data['year_selected'] = "{}".format(today_date.year-1)
				data['month_selected'] = "{}".format(today_date.month)
			elif today_date.day == 1:
				filter_condition = " and year(prod_tbl.production_date) in ('{}') and month(prod_tbl.production_date) in ('{}') ".format(today_date.year, today_date.month)
				data['year_selected'] = "{}".format(today_date.year)
				data['month_selected'] = "{}".format(today_date.month)
			else:
				filter_condition = " and year(prod_tbl.production_date) in ('{}') and month(prod_tbl.production_date) in ('{}') ".format(today_date.year, today_date.month-1)
				data['year_selected'] = "{}".format(today_date.year)
				data['month_selected'] = "{}".format(today_date.month-1)
		elif any([data['year_selected'], data['month_selected']]) == True:
			if data['year_selected'] != "" and data['month_selected'] != "":
				if data['year_selected'] == "All" and data['month_selected'] == "All":
					filter_condition = " and year(prod_tbl.production_date) between '2015' and '{}' ".format(today_date.strftime("%Y"))
				elif data['year_selected'] != "All" and data['month_selected'] != "All":
					filter_condition = " and year(prod_tbl.production_date) in ('{}') and month(prod_tbl.production_date) in ('{}') ".format(data['year_selected'], data['month_selected'])
				elif data['year_selected'] == "All" and data['month_selected'] != "All":
					filter_condition = " and year(prod_tbl.production_date) between '2015' and '{}' and month(prod_tbl.production_date) in ('{}') ".format(today_date.strftime("%Y"), data['month_selected'])
				else:
					filter_condition = " and year(prod_tbl.production_date) in ('{}') and month(prod_tbl.production_date) between '1' and '12' ".format(data['year_selected'])
			elif data['year_selected'] != "" and data['month_selected'] == "":
				if data['year_selected'] == "All":
					filter_condition = " and year(prod_tbl.production_date) between '2015' and '{}' ".format(today_date.strftime("%Y"))
				else:
					filter_condition = " and year(prod_tbl.production_date) in ('{}') ".format(data['year_selected'])
			else:
				if data['month_selected'] == "All":
					filter_condition = " and month(prod_tbl.production_date) between '1' and '12' "
				else:
					filter_condition = " and month(prod_tbl.production_date) in ('{}') ".format(data['month_selected'])
		else:
			if data['from_date'] != "" and data['to_date'] != "":
				filter_condition = " and prod_tbl.production_date between '{}' and '{}' ".format(data['from_date'], data['to_date'])
			elif data['from_date'] != "" and data['to_date'] == "":
				filter_condition = " and prod_tbl.production_date between '{}' and '{}' ".format(data['from_date'], data['from_date'])
			else:
				filter_condition = " and prod_tbl.production_date between '{}' and '{}' ".format(data['to_date'], data['to_date'])
		data['date_range'] = filter_condition
		data['from_date'] = form.get("from_date")
		data['to_date'] = form.get("to_date")
		return data

	def get_date_range_from_quality(form, data, session_data):
		data['year_selected'] = form.get("year_selected")
		data['month_selected'] = form.get("month_selected")

		if form.get("from_date") != "":
			data['from_date'] = datetime.strptime(form.get("from_date"), "%d-%m-%Y").strftime("%Y-%m-%d")
		else:
			data['from_date'] = ""
		if form.get("to_date") != "":
			data['to_date'] = datetime.strptime(form.get("to_date"), "%d-%m-%Y").strftime("%Y-%m-%d")
		else:
			data['to_date'] = ""
		today_date = indian_datetime_format(session_data)


		insert_command_date = 'qlty_tbl.quality_date'
		if data['report_type'] == 'Quality User':
			insert_command_date = 'qlty_tbl.entry_date'

		if any([data['year_selected'], data['month_selected'], data['from_date'], data['to_date']]) == False:
			if today_date.day != 1:
				filter_condition = "year({}) in ('{}') and month({}) in ('{}') ".format(insert_command_date, today_date.year, insert_command_date, today_date.month)
				data['year_selected'] = "{}".format(today_date.year)
				data['month_selected'] = "{}".format(today_date.month)
			elif today_date.month == 1 and today_date.day == 1:
				filter_condition = "year({}) in ('{}') and month({}) in ('12') ".format(insert_command_date, today_date.year-1, insert_command_date)
				data['year_selected'] = "{}".format(today_date.year-1)
				data['month_selected'] = "{}".format(today_date.month)
			elif today_date.day == 1:
				filter_condition = "year({}) in ('{}') and month({}) in ('{}') ".format(insert_command_date, today_date.year, insert_command_date, today_date.month)
				data['year_selected'] = "{}".format(today_date.year)
				data['month_selected'] = "{}".format(today_date.month)
			else:
				filter_condition = "year({}) in ('{}') and month({}) in ('{}') ".format(insert_command_date, today_date.year, insert_command_date, today_date.month-1)
				data['year_selected'] = "{}".format(today_date.year)
				data['month_selected'] = "{}".format(today_date.month-1)
		elif any([data['year_selected'], data['month_selected']]) == True:
			if data['year_selected'] != "" and data['month_selected'] != "":
				if data['year_selected'] == "All" and data['month_selected'] == "All":
					filter_condition = "year({}) between '2015' and '{}' ".format(insert_command_date, today_date.strftime("%Y"))
				elif data['year_selected'] != "All" and data['month_selected'] != "All":
					filter_condition = "year({}) in ('{}') and month({}) in ('{}') ".format(insert_command_date, data['year_selected'], insert_command_date, data['month_selected'])
				elif data['year_selected'] == "All" and data['month_selected'] != "All":
					filter_condition = "year({}) between '2015' and '{}' and month({}) in ('{}') ".format(insert_command_date, today_date.strftime("%Y"), insert_command_date, data['month_selected'])
				else:
					filter_condition = "year({}) in ('{}') and month({}) between '1' and '12' ".format(insert_command_date, data['year_selected'], insert_command_date)
			elif data['year_selected'] != "" and data['month_selected'] == "":
				if data['year_selected'] == "All":
					filter_condition = "year({}) between '2015' and '{}' ".format(insert_command_date, today_date.strftime("%Y"))
				else:
					filter_condition = "year({}) in ('{}') ".format(insert_command_date, data['year_selected'])
			else:
				if data['month_selected'] == "All":
					filter_condition = "month({}) between '1' and '12' ".format(insert_command_date)
				else:
					filter_condition = "month({}) in ('{}') ".format(insert_command_date, data['month_selected'])
		else:
			if data['from_date'] != "" and data['to_date'] != "":
				filter_condition = "{} between '{}' and '{}' ".format(insert_command_date, data['from_date'], data['to_date'])
			elif data['from_date'] != "" and data['to_date'] == "":
				filter_condition = "{} between '{}' and '{}' ".format(insert_command_date, data['from_date'], data['from_date'])
			else:
				filter_condition = "{} between '{}' and '{}' ".format(insert_command_date, data['to_date'], data['to_date'])
		data['date_range'] = filter_condition
		data['from_date'] = form.get("from_date")
		data['to_date'] = form.get("to_date")
		return data

	def data_by_project(data):
		global db_test
		result = 0
		project_selected_header = ""
		if data['check_project'] == '1':
			project_selected_header = ' prj_tbl.project_short_name as Project, '

		if data['check_process'] == '1':
			process_selected_header = ' prj_prcs_tbl.process_short_name as Process, '
		else:
			process_selected_header = ''

		if data['employee_projects'].get(data['project_selected'], 0) != 0:
			process_list = []
			for project_val in data['employee_projects'][data['project_selected']]['process'].values():
				process_list.append(str(project_val['process_id']))
			process_list = ", ".join(process_list)
		else:
			if data['check_process'] == "1":
				process_list = []
				for project_val in data['employee_projects'].values():
					for process_val in project_val['process'].values():
						process_list.append(str(process_val['process_id']))
				process_list = ", ".join(process_list)
			else:
				process_list = ""

		if data['project_selected'] != "All" and data['process_selected'] == "All":
			project_selected_header = ""
			if data['check_process'] == '0':
				process_selected_header = ""
			else:
				process_selected_header = " prj_prcs_tbl.process_short_name as Process, "

		elif data['project_selected'] != "All" and data['process_selected'] != "All":
			project_selected_header = ""
			if data['check_process'] == '0':
				process_selected_header = ""
			else:
				process_selected_header = ""

		if data['project_selected'] == "All" and data['process_selected'] == "All" and data['check_process'] == '0':
			process_selected_list = ""
			process_selected_condition = ", prj_tbl.project_name  "
			if data['check_process'] == "1":
				process_selected_sort = ", prj_tbl.project_name ASC, prj_prcs_tbl.process_name ASC"
			else:
				process_selected_sort = ", prj_tbl.project_name ASC"
			process_selected_sort = "{}, emp_tbl.employee_name ".format(process_selected_sort) if data['check_user'] == "1" else process_selected_sort
		else:
			process_selected_list = ' and prj_prcs_tbl.project_process_id in ({}) '.format(process_list) if data['process_selected'] != "" and data['process_selected'] == "All" else ""
			if data['check_process'] == "1":
				process_selected_condition = ', prj_tbl.project_name, prj_prcs_tbl.process_name  ' if data['process_selected'] == "All" else ""
			else:
				process_selected_condition = ", prj_tbl.project_name"
			if data['check_process'] == "1":
				process_selected_sort = ", prj_tbl.project_name ASC, prj_prcs_tbl.process_name ASC"
			else:
				process_selected_sort = ", prj_tbl.project_name ASC"
			process_selected_sort = "{}, emp_tbl.employee_name ".format(process_selected_sort) if data['check_user'] == "1" else process_selected_sort

		if data['user_selected'] == "All":
			user_name_query = ' emp_tbl.employee_name as User, ' if data['user_selected_all'] != "" else ' count(distinct(prod_tbl.employee_id)) as Users, '
		else:
			user_name_query = ' ' if data['user_selected'] != "" else ' count(distinct(prod_tbl.employee_id)) as Users, '

		if data['check_user'] == '1':
			if data['user_selected'] != "" and data['user_selected'] != "All":
				user_condition = ' prod_tbl.employee_id in ({}) and '.format(data['user_selected'])
			elif data['user_selected'] == "All":
				# user_condition = ' prod_tbl.employee_id in ({}) and '.format(data['user_selected_all'])
				user_condition = " "
			else:
				user_condition = " "
		else:
			if data['user_selected'] != "" and data['user_selected'] != "All":
				user_condition = ' prod_tbl.employee_id in ({}) and '.format(data['user_selected'])
			elif data['user_selected'] == "All":
				# user_condition = ' prod_tbl.employee_id in ({}) and '.format(data['user_selected_all'])
				user_condition = " "
			else:
				user_condition = " "
		comments_notes = ', prod_tbl.notes as Comments ' if data['user_selected'] != "" else ''
		hour_worked_header = " CONCAT(round(FLOOR(sum(prod_tbl.hours_worked)/60), 0),'h ',round(MOD(sum(prod_tbl.hours_worked),60), 0),'m') as Hours, "
		# hour_worked_header = " CONCAT(round(FLOOR(sum(prod_tbl.hours_worked)/60), 0),'h ',round(MOD(sum(prod_tbl.hours_worked),60), 0),'m') as Hours, " if data['user_selected'] != "" else ''
		emp_table_id_join = ' inner join employees_info as emp_tbl on prod_tbl.employee_id = emp_tbl.employee_id ' if data['user_selected'] != "" else ''
		user_selected_sort = ", emp_tbl.employee_name" if data['user_selected'] == "All" and data['check_user'] != '0' else ""
		process_condition = ' prj_tbl.project_id ' if data['process_id'] == "" else "prod_tbl.project_process_id"
		all_year_by_month_condition = ' year(prod_tbl.production_date), ' if data['year_selected'] == 'All' else ""
		all_user_grouping = ', emp_tbl.employee_name' if data['check_user'] == "1" else ""
		try:
			if data['result_year'] == 1:
				query = """
				select Year(prod_tbl.production_date) as Year, {} {} {} SUM(prod_tbl.simple_count) as Simple, SUM(prod_tbl.task_count) as Task, SUM(prod_tbl.parent_count) as Parent, SUM(prod_tbl.child_count) as Child, 
				SUM(prod_tbl.target) as Target, SUM(prod_tbl.achieved) as Achieved, (case when SUM(prod_tbl.target) - SUM(prod_tbl.achieved) < 0 then 0 else SUM(prod_tbl.target) - SUM(prod_tbl.achieved) end) as Bcklg, (case when SUM(prod_tbl.achieved) - SUM(prod_tbl.target) < 0 then 0 else SUM(prod_tbl.achieved) - SUM(prod_tbl.target) end) as Excd, {} 
				round(SUM(prod_tbl.achieved)*100 / SUM(prod_tbl.target), 0) as 'Prod(%)' from projects_info as prj_tbl
				inner join project_process_info as prj_prcs_tbl on prj_tbl.project_id = prj_prcs_tbl.project_id
				inner join daily_productivity_info as prod_tbl on prj_prcs_tbl.project_process_id = prod_tbl.project_process_id
				{} where {} {} in ({}) {}  {} group by year(prod_tbl.production_date){}{}{} order by Year(prod_tbl.production_date) desc {};
				""".format(project_selected_header, process_selected_header, user_name_query, hour_worked_header, emp_table_id_join, user_condition, process_condition, data['employee_project_list'], process_selected_list, data['date_range'], process_selected_condition,user_selected_sort,all_user_grouping,process_selected_sort)
			elif data['result_month'] == 1:
				query = """
				select Year(prod_tbl.production_date) as Year, date_format(prod_tbl.production_date, '%b') as Month, {} {} {} SUM(prod_tbl.simple_count) as Simple, SUM(prod_tbl.task_count) as Task, SUM(prod_tbl.parent_count) as Parent, SUM(prod_tbl.child_count) as Child, 
				SUM(prod_tbl.target) as Target, SUM(prod_tbl.achieved) as Achieved, (case when SUM(prod_tbl.target) - SUM(prod_tbl.achieved) < 0 then 0 else SUM(prod_tbl.target) - SUM(prod_tbl.achieved) end) as Bcklg, (case when SUM(prod_tbl.achieved) - SUM(prod_tbl.target) < 0 then 0 else SUM(prod_tbl.achieved) - SUM(prod_tbl.target) end) as Excd, {}
				round(SUM(prod_tbl.achieved)*100 / SUM(prod_tbl.target), 0) as 'Prod(%)' from projects_info as prj_tbl
				inner join project_process_info as prj_prcs_tbl on prj_tbl.project_id = prj_prcs_tbl.project_id
				inner join daily_productivity_info as prod_tbl on prj_prcs_tbl.project_process_id = prod_tbl.project_process_id
				{} where {} {} in ({}) {} {} group by {} month(prod_tbl.production_date){}{}{} order by Year(prod_tbl.production_date) desc,date_format(prod_tbl.production_date, '%b') desc {};
				""".format(project_selected_header, process_selected_header, user_name_query, hour_worked_header, emp_table_id_join, user_condition, process_condition, data['employee_project_list'], process_selected_list, data['date_range'], all_year_by_month_condition, process_selected_condition,user_selected_sort,all_user_grouping,process_selected_sort)
			elif data['result_week'] == 1:
				query = """
				select Year(prod_tbl.production_date) as Year, date_format(prod_tbl.production_date, '%b') as Month, date_format(prod_tbl.production_date, '%v') as Week, {} {} {} SUM(prod_tbl.simple_count) as Simple, SUM(prod_tbl.task_count) as Task, SUM(prod_tbl.parent_count) as Parent, SUM(prod_tbl.child_count) as Child, 
				SUM(prod_tbl.target) as Target, SUM(prod_tbl.achieved) as Achieved, (case when SUM(prod_tbl.target) - SUM(prod_tbl.achieved) < 0 then 0 else SUM(prod_tbl.target) - SUM(prod_tbl.achieved) end) as Bcklg, (case when SUM(prod_tbl.achieved) - SUM(prod_tbl.target) < 0 then 0 else SUM(prod_tbl.achieved) - SUM(prod_tbl.target) end) as Excd, {}
				round(SUM(prod_tbl.achieved)*100 / SUM(prod_tbl.target), 0) as 'Prod(%)' from projects_info as prj_tbl
				inner join project_process_info as prj_prcs_tbl on prj_tbl.project_id = prj_prcs_tbl.project_id
				inner join daily_productivity_info as prod_tbl on prj_prcs_tbl.project_process_id = prod_tbl.project_process_id
				{} where {} {} in ({}) {} {} group by {} week(prod_tbl.production_date){}{}{} order by Year(prod_tbl.production_date) desc,date_format(prod_tbl.production_date, '%b') desc, date_format(prod_tbl.production_date, '%v') desc {};
				""".format(project_selected_header, process_selected_header, user_name_query, hour_worked_header, emp_table_id_join, user_condition, process_condition, data['employee_project_list'], process_selected_list, data['date_range'], all_year_by_month_condition, process_selected_condition,user_selected_sort,all_user_grouping,process_selected_sort)
			else:
				query = """
				select date_format(prod_tbl.production_date, '%d-%b-%Y') as Date, {} {} {} SUM(prod_tbl.simple_count) as Simple, SUM(prod_tbl.task_count) as Task, SUM(prod_tbl.parent_count) as Parent, SUM(prod_tbl.child_count) as Child, 
				SUM(prod_tbl.target) as Target, SUM(prod_tbl.achieved) as Achieved, (case when SUM(prod_tbl.target) - SUM(prod_tbl.achieved) < 0 then 0 else SUM(prod_tbl.target) - SUM(prod_tbl.achieved) end) as Bcklg, (case when SUM(prod_tbl.achieved) - SUM(prod_tbl.target) < 0 then 0 else SUM(prod_tbl.achieved) - SUM(prod_tbl.target) end) as Excd, {}
				round(SUM(prod_tbl.achieved)*100 / SUM(prod_tbl.target), 0) as 'Prod(%)'{} from projects_info as prj_tbl
				inner join project_process_info as prj_prcs_tbl on prj_tbl.project_id = prj_prcs_tbl.project_id
				inner join daily_productivity_info as prod_tbl on prj_prcs_tbl.project_process_id = prod_tbl.project_process_id
				{} where {} {} in ({}) {} {} group by prod_tbl.production_date{}{} order by prod_tbl.production_date desc {};
				""".format(project_selected_header, process_selected_header, user_name_query, hour_worked_header, comments_notes, emp_table_id_join, user_condition, process_condition, data['employee_project_list'], process_selected_list, data['date_range'], process_selected_condition,user_selected_sort, process_selected_sort)
			list_cursor = database_reconnection()
			list_cursor.execute(query)
			column_names = [i[0] for i in list_cursor.description]
			result_data = list_cursor.fetchall()
			#list_cursor.close()
			if result_data != [] and result_data[0][0] != None:
				result = [column_names, result_data]
			else:
				result = 1
		except:
			print(traceback.format_exc())
		finally:
			return result

	def quality_by_project(data):
		global db_test
		result = 0

		if data['employee_projects'].get(data['project_selected'], 0) != 0:
			project_list = data['employee_projects'][data['project_selected']]['project_id']
		else:
			project_list = []
			for project_val in data['employee_projects'].values():
				project_list.append(str(project_val['project_id']))
			project_list = ", ".join(project_list)

		if data['project_selected'] == "All" and data['process_selected'] == "All":
			project_selected_header = 'prj_tbl.project_short_name as Project, ' if data['check_project'] == '1' else ''
			process_selected_header = 'prj_prcs_tbl.process_short_name as Process, ' if data['check_process'] == '1' else ''
			if data['check_process'] == '1':
				process_condition = 'and prj_tbl.project_id in ({})'.format(project_list)
			else:
				process_condition = 'and prj_tbl.project_id in ({})'.format(project_list)
		if data['project_selected'] != "All" and data['process_selected'] == "All":
			project_selected_header = '' if data['check_project'] == '1' else ''
			process_selected_header = 'prj_prcs_tbl.process_short_name as Process, ' if data['check_process'] == '1' else ''
			if data['check_process'] == '1':
				process_condition = 'and prj_tbl.project_id in ({})'.format(project_list)
			else:
				process_condition = 'and prj_tbl.project_id in ({})'.format(project_list)
		if data['project_selected'] != "All" and data['process_selected'] != "All":
			project_selected_header = '' if data['check_project'] == '1' else ''
			process_selected_header = '' if data['check_process'] == '1' else ''
			if data['check_process'] == '1':
				process_condition = 'and prj_tbl.project_id in ({}) and prj_prcs_tbl.project_process_id in ({})'.format(data['project_id'], data['process_id'])
			else:
				process_condition = 'and prj_tbl.project_id in ({}) and prj_prcs_tbl.project_process_id in ({})'.format(data['project_id'], data['process_id'])

		if data['check_project'] == '1' and data['check_process'] == '0' and data['check_user'] == '0':
			quality_type = ''
			quality_user_name = 'count(distinct(qlty_tbl.quality_user_id)) as Quser, '
			if data['emp_type'] not in ['PU']:
				if data['report_type'] == "Quality Assurance":
					production_user_name_for_user = ''
					production_user_name_for_file = ''
				else:
					production_user_name_for_user = '(case when qlty_tbl.production_user_id <> "0" then count(distinct(qlty_tbl.production_user_id)) else 0 end) as Puser, '
					production_user_name_for_file = '(case when qlty_tbl.production_user_id = "0" then 0 end) as Puser, '
				quality_filename = '(case when qlty_tbl.production_user_id = "0" then count(distinct(qlty_tbl.filename)) else 0 end) as Filename, '
			else:
				if data['report_type'] == "Quality Assurance":
					production_user_name_for_user = ''
					production_user_name_for_file = ''
				else:
					production_user_name_for_user = '(case when qlty_tbl.production_user_id <> "0" then count(distinct(qlty_tbl.production_user_id)) else 0 end) as Puser, ' if data['user_selected'] == "" else 'count(distinct(qlty_tbl.production_user_id)) as Puser, '
					production_user_name_for_file = '(case when qlty_tbl.production_user_id = "0" then 0 end) as Puser, ' if data['user_selected'] == "" else 'count(distinct(qlty_tbl.production_user_id)) as Puser, '
				quality_filename = '(case when qlty_tbl.production_user_id = "0" then qlty_tbl.filename else 0 end) as Filename, ' if data['user_selected'] == "" else 'count(distinct(qlty_tbl.filename)) as Filename, '
			common_table_data = 'SUM(qlty_tbl.received_count) as Rcvd, SUM(qlty_tbl.audit_count) as Audit, SUM(qlty_tbl.missing_error) as Miss, SUM(qlty_tbl.incorrect_error) as Incrt, SUM(qlty_tbl.spelling_error) as Spl, SUM(qlty_tbl.normalize_error) as Norm, SUM(qlty_tbl.total_error) as Total, '
			group_condition = 'prj_tbl.project_name'
			# quality_hours_worked = ""
			quality_hours_worked = "CONCAT(round(FLOOR(SUM(qlty_tbl.quality_hours)/60), 0),'h ',round(MOD(SUM(qlty_tbl.quality_hours),60), 0),'m') as Hours, "
			percentage_formula = " (1 - (SUM(qlty_tbl.total_error)/SUM(qlty_tbl.audit_count)))*100 "
			quality_percentage = '(case when round({}, 2) = 100.00 then round({}, 0) else round({}, 2) end) as Qlty, '.format(percentage_formula, percentage_formula, percentage_formula)
			sampling_percentage = 'round((SUM(qlty_tbl.audit_count)/SUM(qlty_tbl.received_count))*100, 0) as Smpl'
			comments_notes = '' if data['user_selected'] != "" else ''

		elif data['check_project'] == '1' and data['check_process'] == '1' and data['check_user'] == '0':
			quality_type = ''
			if data['emp_type'] not in ['PU']:
				quality_user_name = 'count(distinct(qlty_tbl.quality_user_id)) as Quser, '
				if data['report_type'] == "Quality Assurance":
					production_user_name_for_user = ''
					production_user_name_for_file = ''
				else:
					production_user_name_for_user = '(case when qlty_tbl.production_user_id <> "0" then count(distinct(qlty_tbl.production_user_id)) else 0 end) as Puser, '
					production_user_name_for_file = '(case when qlty_tbl.production_user_id = "0" then 0 end) as Puser, '
				quality_filename = '(case when qlty_tbl.production_user_id = "0" then count(distinct(qlty_tbl.filename)) else 0 end) as Filename, '
				group_condition = 'prj_tbl.project_name, prj_prcs_tbl.process_name'
			else:
				quality_user_name = 'qlty_emp_tbl.employee_name as Quser, '
				if data['report_type'] == "Quality Assurance":
					production_user_name_for_user = ''
					production_user_name_for_file = ''
				else:
					production_user_name_for_user = '(case when qlty_tbl.production_user_id <> "0" then prod_emp_tbl.employee_name else 0 end) as Puser, '
					production_user_name_for_file = '(case when qlty_tbl.production_user_id = "0" then 0 end) as Puser, '
				quality_filename = '(case when qlty_tbl.production_user_id = "0" then qlty_tbl.filename else 0 end) as Filename, '
				group_condition = 'prj_tbl.project_name, prj_prcs_tbl.process_name, qlty_tbl.quality_user_id, qlty_tbl.production_user_id, qlty_tbl.filename'
			common_table_data = 'SUM(qlty_tbl.received_count) as Rcvd, SUM(qlty_tbl.audit_count) as Audit, SUM(qlty_tbl.missing_error) as Miss, SUM(qlty_tbl.incorrect_error) as Incrt, SUM(qlty_tbl.spelling_error) as Spl, SUM(qlty_tbl.normalize_error) as Norm, SUM(qlty_tbl.total_error) as Total, '
			# quality_hours_worked = ""
			quality_hours_worked = "CONCAT(round(FLOOR(SUM(qlty_tbl.quality_hours)/60), 0),'h ',round(MOD(SUM(qlty_tbl.quality_hours),60), 0),'m') as Hours, "
			
			percentage_formula = " (1 - (SUM(qlty_tbl.total_error)/SUM(qlty_tbl.audit_count)))*100 "
			quality_percentage = '(case when round({}, 2) = 100.00 then round({}, 0) else round({}, 2) end) as Qlty, '.format(percentage_formula, percentage_formula, percentage_formula)
			sampling_percentage = 'round((SUM(qlty_tbl.audit_count)/SUM(qlty_tbl.received_count))*100, 0) as Smpl'
			comments_notes = ', qlty_tbl.comments as Cmts ' if data['user_selected'] != "" else ''

		elif data['check_project'] == '1' and data['check_process'] == '0' and data['check_user'] == '1':
			if data['user_selected'] == "All":
				quality_type = 'qlty_tbl.quality_type as "Q-Type", ' if data['check_process'] == '0' else 'count(distinct(qlty_tbl.quality_type)) as "Q-Type", '
				quality_user_name = 'qlty_emp_tbl.employee_name as Quser, ' if data['user_selected_all'] != "" else 'count(distinct(qlty_tbl.quality_user_id)) as Quser, '
				if data['report_type'] == "Quality Assurance":
					production_user_name_for_user = ''
					production_user_name_for_file = ''
				else:
					production_user_name_for_user = '(case when qlty_tbl.production_user_id <> "0" then prod_emp_tbl.employee_name else 0 end) as Puser, ' if data['user_selected_all'] != "" else 'count(distinct(qlty_tbl.production_user_id)) as Puser, '
					production_user_name_for_file = '(case when qlty_tbl.production_user_id = "0" then 0 end) as Puser, ' if data['user_selected_all'] != "" else 'count(distinct(qlty_tbl.production_user_id)) as Puser, '
				quality_filename = '(case when qlty_tbl.production_user_id = "0" then qlty_tbl.filename else 0 end) as Filename, ' if data['user_selected_all'] != "" else 'count(distinct(qlty_tbl.filename)) as Filename, '
				group_condition = 'prj_prcs_tbl.process_name, qlty_tbl.quality_type, qlty_tbl.quality_user_id, qlty_tbl.production_user_id, qlty_tbl.filename'
			else:
				quality_type = 'qlty_tbl.quality_type as "Q-Type", '
				quality_user_name = 'qlty_emp_tbl.employee_name as Quser, ' if data['user_selected_all'] == "" else 'count(distinct(qlty_tbl.quality_user_id)) as Quser, '
				if data['report_type'] == "Quality Team":
					production_user_name_for_user = ''
					production_user_name_for_file = ''
					quality_filename = ''
					group_condition = 'prj_prcs_tbl.process_name, qlty_tbl.quality_type, qlty_tbl.quality_user_id, qlty_tbl.production_user_id, qlty_tbl.filename'
				else:
					production_user_name_for_user = '(case when qlty_tbl.production_user_id <> "0" then prod_emp_tbl.employee_name else 0 end) as Puser, ' if data['user_selected_all'] == "" else 'count(distinct(qlty_tbl.production_user_id)) as Puser, '
					production_user_name_for_file = '(case when qlty_tbl.production_user_id = "0" then 0 end) as Puser, ' if data['user_selected_all'] == "" else 'count(distinct(qlty_tbl.production_user_id)) as Puser, '
					quality_filename = '(case when qlty_tbl.production_user_id = "0" then qlty_tbl.filename else 0 end) as Filename, ' if data['user_selected_all'] == "" else 'count(distinct(qlty_tbl.filename)) as Filename, '
					group_condition = 'prj_prcs_tbl.process_name, qlty_tbl.quality_type, qlty_tbl.quality_user_id, qlty_tbl.production_user_id, qlty_tbl.filename'
			common_table_data = 'SUM(qlty_tbl.received_count) as Rcvd, SUM(qlty_tbl.audit_count) as Audit, SUM(qlty_tbl.missing_error) as Miss, SUM(qlty_tbl.incorrect_error) as Incrt, SUM(qlty_tbl.spelling_error) as Spl, SUM(qlty_tbl.normalize_error) as Norm, SUM(qlty_tbl.total_error) as Total, '
			quality_hours_worked = "CONCAT(round(FLOOR(SUM(qlty_tbl.quality_hours)/60), 0),'h ',round(MOD(SUM(qlty_tbl.quality_hours),60), 0),'m') as Hours, " if data['user_selected'] != "" else ''
			percentage_formula = " (1 - (SUM(qlty_tbl.total_error)/SUM(qlty_tbl.audit_count)))*100 "
			quality_percentage = '(case when round({}, 2) = 100.00 then round({}, 0) else round({}, 2) end) as Qlty, '.format(percentage_formula, percentage_formula, percentage_formula)
			sampling_percentage = 'round((SUM(qlty_tbl.audit_count)/SUM(qlty_tbl.received_count))*100, 0) as Smpl'
			comments_notes = ', qlty_tbl.comments as Cmts ' if data['user_selected'] != "" else ''

		elif data['check_project'] == '1' and data['check_process'] == '1' and data['check_user'] == '1':
			if data['user_selected'] == "All":
				quality_type = 'qlty_tbl.quality_type as "Q-Type", ' if data['check_process'] != '0' else 'count(distinct(qlty_tbl.quality_type)) as "Q-Type", '
				quality_user_name = 'qlty_emp_tbl.employee_name as Quser, ' if data['user_selected_all'] != "" else 'count(distinct(qlty_tbl.quality_user_id)) as Quser, '
				if data['report_type'] == "Quality Assurance":
					production_user_name_for_user = ''
					production_user_name_for_file = ''
				else:
					production_user_name_for_user = '(case when qlty_tbl.production_user_id <> "0" then prod_emp_tbl.employee_name else 0 end) as Puser, ' if data['user_selected_all'] != "" else 'count(distinct(qlty_tbl.production_user_id)) as Puser, '
					production_user_name_for_file = '(case when qlty_tbl.production_user_id = "0" then 0 end) as Puser, ' if data['user_selected_all'] != "" else 'count(distinct(qlty_tbl.production_user_id)) as Puser, '
				quality_filename = '(case when qlty_tbl.production_user_id = "0" then qlty_tbl.filename else 0 end) as Filename, ' if data['user_selected_all'] != "" else 'count(distinct(qlty_tbl.filename)) as Filename, '
				group_condition = 'prj_prcs_tbl.process_name, qlty_tbl.quality_type, qlty_tbl.quality_user_id, qlty_tbl.production_user_id, qlty_tbl.filename'
			else:
				quality_type = 'qlty_tbl.quality_type as "Q-Type", ' if data['check_process'] != '0' else 'count(distinct(qlty_tbl.quality_type)) as "Q-Type", '
				quality_user_name = 'qlty_emp_tbl.employee_name as Quser, ' if data['user_selected_all'] == "" else 'count(distinct(qlty_tbl.quality_user_id)) as Quser, '
				if data['report_type'] == "Quality Team":
					production_user_name_for_user = ''
					production_user_name_for_file = ''
					quality_filename = ''
					group_condition = 'prj_prcs_tbl.process_name, qlty_tbl.quality_type, qlty_tbl.quality_user_id, qlty_tbl.production_user_id, qlty_tbl.filename'
				else:
					production_user_name_for_user = '(case when qlty_tbl.production_user_id <> "0" then prod_emp_tbl.employee_name else 0 end) as Puser, ' if data['user_selected_all'] == "" else 'count(distinct(qlty_tbl.production_user_id)) as Puser, '
					production_user_name_for_file = '(case when qlty_tbl.production_user_id = "0" then 0 end) as Puser, ' if data['user_selected_all'] == "" else 'count(distinct(qlty_tbl.production_user_id)) as Puser, '
					quality_filename = '(case when qlty_tbl.production_user_id = "0" then qlty_tbl.filename else 0 end) as Filename, ' if data['user_selected_all'] == "" else 'count(distinct(qlty_tbl.filename)) as Filename, '
					group_condition = 'prj_prcs_tbl.process_name, qlty_tbl.quality_type, qlty_tbl.quality_user_id, qlty_tbl.production_user_id, qlty_tbl.filename'
			common_table_data = 'SUM(qlty_tbl.received_count) as Rcvd, SUM(qlty_tbl.audit_count) as Audit, SUM(qlty_tbl.missing_error) as Miss, SUM(qlty_tbl.incorrect_error) as Incrt, SUM(qlty_tbl.spelling_error) as Spl, SUM(qlty_tbl.normalize_error) as Norm, SUM(qlty_tbl.total_error) as Total, '
			quality_hours_worked = "CONCAT(round(FLOOR(SUM(qlty_tbl.quality_hours)/60), 0),'h ',round(MOD(SUM(qlty_tbl.quality_hours),60), 0),'m') as Hours, " if data['user_selected'] != "" else ''
			percentage_formula = " (1 - (SUM(qlty_tbl.total_error)/SUM(qlty_tbl.audit_count)))*100 "
			quality_percentage = '(case when round({}, 2) = 100.00 then round({}, 0) else round({}, 2) end) as Qlty, '.format(percentage_formula, percentage_formula, percentage_formula)
			sampling_percentage = 'round((SUM(qlty_tbl.audit_count)/SUM(qlty_tbl.received_count))*100, 0) as Smpl'
			comments_notes = ', qlty_tbl.comments as Cmts ' if data['user_selected'] != "" else ''

		quality_user_join = 'inner join employees_info as qlty_emp_tbl on qlty_tbl.quality_user_id = qlty_emp_tbl.employee_id'
		if data['check_user'] == "0":
			if data['user_selected'] != "":
				if data['emp_type'] == 'PU':
					quality_user_join = 'inner join employees_info as qlty_emp_tbl on qlty_tbl.quality_user_id = qlty_emp_tbl.employee_id'
					production_user_join = 'inner join employees_info as prod_emp_tbl on qlty_tbl.production_user_id = prod_emp_tbl.employee_id'
				else:
					production_user_join = ''
			else:
				production_user_join = 'inner join employees_info as prod_emp_tbl on qlty_tbl.production_user_id = prod_emp_tbl.employee_id'
		else:
			if data['user_selected'] != "":
				production_user_join = 'inner join employees_info as prod_emp_tbl on qlty_tbl.production_user_id = prod_emp_tbl.employee_id'
			else:
				production_user_join = ''

		date_condition = data['date_range']

		selected_split_date = 'qlty_tbl.quality_date'
		if data['report_type'] == 'Quality User':
			selected_split_date = 'qlty_tbl.entry_date'

		if data['report_type'] == 'Quality Assurance':
			mode_condition = 'and qlty_tbl.quality_mode = "QA" '
		else:
			mode_condition = 'and qlty_tbl.quality_mode = "QC" '

		if data['project_selected'] == "All" and data['process_selected'] == "All":
			if data['report_type'] == 'Quality User':
				if data['emp_type'] == 'PU':
					quser_condition = 'and qlty_tbl.quality_user_id in ({}) '.format(data['employee_id']) if data['check_user'] == '0' else ''
					puser_condition = ''
				else:
					if data['check_user'] == '1':
						quser_condition = 'and qlty_tbl.quality_user_id in ({}) '.format(data['user_selected']) if data['user_selected'] != "All" else ''
						puser_condition = ''
					else:
						quser_condition = ''
						puser_condition = ''
			elif data['report_type'] == 'Quality Team':
				if data['emp_type'] == 'PU':
					quser_condition = ''
					puser_condition = 'and qlty_tbl.production_user_id in ({}) '.format(data['employee_id']) if data['check_user'] == '0' else ''
				else:
					if data['check_user'] == '1':
						quser_condition = ''
						puser_condition = 'and qlty_tbl.production_user_id in ({}) '.format(data['user_selected']) if data['user_selected'] != "All" else ''
					else:
						quser_condition = ''
						puser_condition = ''
			else:
				if data['check_user'] == '1':
					quser_condition = 'and qlty_tbl.quality_user_id in ({}) '.format(data['user_selected']) if data['user_selected'] != "All" else ''
					puser_condition = ''
				else:
					quser_condition = ''
					puser_condition = ''
		elif data['project_selected'] != "All" and data['process_selected'] == "All":
			if data['report_type'] == 'Quality User':
				if data['emp_type'] == 'PU':
					quser_condition = 'and qlty_tbl.quality_user_id in ({}) '.format(data['employee_id']) if data['check_user'] == '0' else ''
					puser_condition = ''
				else:
					if data['check_user'] == '1':
						quser_condition = 'and qlty_tbl.quality_user_id in ({}) '.format(data['user_selected']) if data['user_selected'] != "All" else ''
						puser_condition = ''
					else:
						quser_condition = ''
						puser_condition = ''
			elif data['report_type'] == 'Quality Team':
				if data['emp_type'] == 'PU':
					quser_condition = ''
					puser_condition = 'and qlty_tbl.production_user_id in ({}) '.format(data['employee_id']) if data['check_user'] == '0' else ''
				else:
					if data['check_user'] == '1':
						quser_condition = ''
						puser_condition = 'and qlty_tbl.production_user_id in ({}) '.format(data['user_selected']) if data['user_selected'] != "All" else ''
					else:
						quser_condition = ''
						puser_condition = ''
			else:
				if data['check_user'] == '1':
					quser_condition = 'and qlty_tbl.quality_user_id in ({}) '.format(data['user_selected']) if data['user_selected'] != "All" else ''
					puser_condition = ''
				else:
					quser_condition = ''
					puser_condition = ''
		else:
			if data['report_type'] == 'Quality User':
				if data['emp_type'] == 'PU':
					quser_condition = 'and qlty_tbl.quality_user_id in ({}) '.format(data['employee_id']) if data['check_user'] == '0' else ''
					puser_condition = ''
				else:
					if data['check_user'] == '1':
						quser_condition = 'and qlty_tbl.quality_user_id in ({}) '.format(data['user_selected']) if data['user_selected'] != "All" else ''
						puser_condition = ''
					else:
						quser_condition = ''
						puser_condition = ''
			elif data['report_type'] == 'Quality Team':
				if data['emp_type'] == 'PU':
					quser_condition = ''
					puser_condition = 'and qlty_tbl.production_user_id in ({}) '.format(data['employee_id']) if data['check_user'] == '0' else ''
				else:
					if data['check_user'] == '1':
						quser_condition = ''
						puser_condition = 'and qlty_tbl.production_user_id in ({}) '.format(data['user_selected']) if data['user_selected'] != "All" else ''
					else:
						quser_condition = ''
						puser_condition = ''
			else:
				if data['check_user'] == '1':
					quser_condition = 'and qlty_tbl.quality_user_id in ({}) '.format(data['user_selected']) if data['user_selected'] != "All" else ''
					puser_condition = ''
				else:
					quser_condition = ''
					puser_condition = ''

		try:
			if data['result_year'] == 1:
				group_date = 'Year({}), '.format(selected_split_date)
				username_query = """select Year({}) as Year, {} {} {} {} {} {} {} {} {} from quality_info as qlty_tbl
				inner join projects_info as prj_tbl on prj_tbl.project_id = qlty_tbl.project_id
				inner join project_process_info as prj_prcs_tbl on prj_prcs_tbl.project_process_id = qlty_tbl.project_process_id {} {} where {} {} {} {} {} group by {} {} order by {} desc, prj_tbl.project_name ASC, prj_prcs_tbl.process_name ASC, qlty_tbl.quality_type ASC;
				""".format(selected_split_date, project_selected_header, process_selected_header, quality_type, quality_user_name, production_user_name_for_user, common_table_data, quality_hours_worked, quality_percentage, sampling_percentage, quality_user_join, production_user_join, date_condition, mode_condition, process_condition, quser_condition, puser_condition, group_date, group_condition, selected_split_date)
				filename_query = """select Year({}) as Year, {} {} {} {} {} {} {} {} {} from quality_info as qlty_tbl
				inner join projects_info as prj_tbl on prj_tbl.project_id = qlty_tbl.project_id
				inner join project_process_info as prj_prcs_tbl on prj_prcs_tbl.project_process_id = qlty_tbl.project_process_id {} where {} {} {} {} {} and qlty_tbl.filename <> "" group by {} {} order by {} desc, prj_tbl.project_name ASC, prj_prcs_tbl.process_name ASC, qlty_tbl.quality_type ASC;
				""".format(selected_split_date, project_selected_header, process_selected_header, quality_type, quality_user_name, quality_filename, common_table_data, quality_hours_worked, quality_percentage, sampling_percentage, quality_user_join, date_condition, mode_condition, process_condition, quser_condition, puser_condition, group_date, group_condition, selected_split_date)
			elif data['result_month'] == 1:
				group_date = "date_format({}, '%b'), ".format(selected_split_date)
				username_query = """select Year({}) as Year, date_format({}, '%b') as Month, {} {} {} {} {} {} {} {} {} from quality_info as qlty_tbl
				inner join projects_info as prj_tbl on prj_tbl.project_id = qlty_tbl.project_id
				inner join project_process_info as prj_prcs_tbl on prj_prcs_tbl.project_process_id = qlty_tbl.project_process_id {} {} where {} {} {} {} {} group by {} {} order by {} desc, prj_tbl.project_name ASC, prj_prcs_tbl.process_name ASC, qlty_tbl.quality_type ASC;
				""".format(selected_split_date, selected_split_date, project_selected_header, process_selected_header, quality_type, quality_user_name, production_user_name_for_user, common_table_data, quality_hours_worked, quality_percentage, sampling_percentage, quality_user_join, production_user_join, date_condition, mode_condition, process_condition, quser_condition, puser_condition, group_date, group_condition, selected_split_date)
				filename_query = """select Year({}) as Year, date_format({}, '%b') as Month, {} {} {} {} {} {} {} {} {} from quality_info as qlty_tbl
				inner join projects_info as prj_tbl on prj_tbl.project_id = qlty_tbl.project_id
				inner join project_process_info as prj_prcs_tbl on prj_prcs_tbl.project_process_id = qlty_tbl.project_process_id {} where {} {} {} {} {} and qlty_tbl.filename <> "" group by {} {} order by {} desc, prj_tbl.project_name ASC, prj_prcs_tbl.process_name ASC, qlty_tbl.quality_type ASC;
				""".format(selected_split_date, selected_split_date, project_selected_header, process_selected_header, quality_type, quality_user_name, quality_filename, common_table_data, quality_hours_worked, quality_percentage, sampling_percentage, quality_user_join, date_condition, mode_condition, process_condition, quser_condition, puser_condition, group_date, group_condition, selected_split_date)
			elif data['result_week'] == 1:
				group_date = "date_format({}, '%v'), ".format(selected_split_date)
				username_query = """select Year({}) as Year, date_format({}, '%b') as Month, date_format({}, '%v') as Week, {} {} {} {} {} {} {} {} {} from quality_info as qlty_tbl
				inner join projects_info as prj_tbl on prj_tbl.project_id = qlty_tbl.project_id
				inner join project_process_info as prj_prcs_tbl on prj_prcs_tbl.project_process_id = qlty_tbl.project_process_id {} {} where {} {} {} {} {} group by {} {} order by {} desc, prj_tbl.project_name ASC, prj_prcs_tbl.process_name ASC, qlty_tbl.quality_type ASC;
				""".format(selected_split_date, selected_split_date, selected_split_date, project_selected_header, process_selected_header, quality_type, quality_user_name, production_user_name_for_user, common_table_data, quality_hours_worked, quality_percentage, sampling_percentage, quality_user_join, production_user_join, date_condition, mode_condition, process_condition, quser_condition, puser_condition, group_date, group_condition, selected_split_date)
				filename_query = """select Year({}) as Year, date_format({}, '%b') as Month, date_format({}, '%v') as Week, {} {} {} {} {} {} {} {} {} from quality_info as qlty_tbl
				inner join projects_info as prj_tbl on prj_tbl.project_id = qlty_tbl.project_id
				inner join project_process_info as prj_prcs_tbl on prj_prcs_tbl.project_process_id = qlty_tbl.project_process_id {} where {} {} {} {} {} and qlty_tbl.filename <> "" group by {} {} order by {} desc, prj_tbl.project_name ASC, prj_prcs_tbl.process_name ASC, qlty_tbl.quality_type ASC;
				""".format(selected_split_date, selected_split_date, selected_split_date, project_selected_header, process_selected_header, quality_type, quality_user_name, quality_filename, common_table_data, quality_hours_worked, quality_percentage, sampling_percentage, quality_user_join, date_condition, mode_condition, process_condition, quser_condition, puser_condition, group_date, group_condition, selected_split_date)
			else:
				group_date = "{}, ".format(selected_split_date)
				username_query = """select date_format(qlty_tbl.entry_date, '%d-%b-%Y') as "Entry-Date", date_format(qlty_tbl.quality_date, '%d-%b-%Y') as "Quality-Date", {} {} {} {} {} {} {} {} {} {} from quality_info as qlty_tbl
				inner join projects_info as prj_tbl on prj_tbl.project_id = qlty_tbl.project_id
				inner join project_process_info as prj_prcs_tbl on prj_prcs_tbl.project_process_id = qlty_tbl.project_process_id {} {} where {} {} {} {} {} group by {} {} order by {} desc, prj_tbl.project_name ASC, prj_prcs_tbl.process_name ASC, qlty_tbl.quality_type ASC;
				""".format(project_selected_header, process_selected_header, quality_type, quality_user_name, production_user_name_for_user, common_table_data, quality_hours_worked, quality_percentage, sampling_percentage, comments_notes, quality_user_join, production_user_join, date_condition, mode_condition, process_condition, quser_condition, puser_condition, group_date, group_condition, selected_split_date)
				filename_query = """select date_format(qlty_tbl.entry_date, '%d-%b-%Y') as "Entry-Date", date_format(qlty_tbl.quality_date, '%d-%b-%Y') as "Quality-Date", {} {} {} {} {} {} {} {} {} {} from quality_info as qlty_tbl
				inner join projects_info as prj_tbl on prj_tbl.project_id = qlty_tbl.project_id
				inner join project_process_info as prj_prcs_tbl on prj_prcs_tbl.project_process_id = qlty_tbl.project_process_id {} where {} {} {} {} {} and qlty_tbl.filename <> "" group by {} {} order by {} desc, prj_tbl.project_name ASC, prj_prcs_tbl.process_name ASC, qlty_tbl.quality_type ASC;
				""".format(project_selected_header, process_selected_header, quality_type, quality_user_name, quality_filename, common_table_data, quality_hours_worked, quality_percentage, sampling_percentage, comments_notes, quality_user_join, date_condition, mode_condition, process_condition, quser_condition, puser_condition, group_date, group_condition, selected_split_date)
			
			list_cursor = database_reconnection()
			list_cursor.execute(username_query)
			username_result = list_cursor.fetchall()
			user_column_names = [i[0] for i in list_cursor.description]
			#list_cursor.close()
			list_cursor = database_reconnection()
			list_cursor.execute(filename_query)
			filename_result = list_cursor.fetchall()
			#list_cursor.close()
			file_column_names = [i[0] for i in list_cursor.description]

			if (username_result != [] and username_result[0][0] != None) or (filename_result != [] and filename_result[0][0] != None):
				result = [[user_column_names, username_result], [file_column_names, filename_result]]
			else:
				result = 1
		except:
			print(traceback.format_exc())
		finally:
			return result
	############################################################################## [ Quality Modified Conditon ] ######################################################

	def revert_operation(revert_form_data, session):
		global db_test
		try:
			old_revert_date = datetime.strptime(revert_form_data['Quality-Date'],"%d-%b-%Y").strftime("%Y-%m-%d")
			project_added = 'prj_tbl.project_id, ' if 'Project' in revert_form_data.keys() else ''
			project_inner_join = "inner join projects_info as prj_tbl on prj_tbl.project_short_name = '{}'".format(revert_form_data['Project']) if 'Project' in revert_form_data.keys() else ''
			process_added = 'prj_process_tbl.project_process_id, ' if 'Process' in revert_form_data.keys() else ''
			process_inner_join = "inner join project_process_info as prj_process_tbl on prj_process_tbl.process_short_name = '{}'".format(revert_form_data['Process']) if 'Process' in revert_form_data.keys() else ''
			collected_query = """select {} {} qlty_emp_tbl.employee_id from employees_info as qlty_emp_tbl {} {} where qlty_emp_tbl.employee_name = '{}';""".format(project_added, process_added, project_inner_join, process_inner_join, revert_form_data['Quser'])
			list_cursor = database_reconnection()
			list_cursor.execute(collected_query)
			collected_data = list_cursor.fetchall()
			#list_cursor.close()
			project_entered = "and `project_id` = '{}' ".format(collected_data[0][0]) if 'Project' in revert_form_data.keys() else ''
			if 'Project' in revert_form_data.keys():
				process_entered = "and `project_process_id` = '{}' ".format(collected_data[0][1]) if 'Process' in revert_form_data.keys() else ''
			else:
				process_entered = "and `project_process_id` = '{}' ".format(collected_data[0][0]) if 'Process' in revert_form_data.keys() else ''

			missing_error = int(revert_form_data['Miss'])
			incorrect_error = int(revert_form_data['Incrt'])
			spelling_error = int(revert_form_data['Spl'])
			normalize_error = int(revert_form_data['Norm'])
			total_error = missing_error + incorrect_error + spelling_error + normalize_error
			quality_percentage = round((1 - (int(total_error)/int(revert_form_data['Audit'])))*100, 0)

			update_query = """
			UPDATE `quality_info` SET `missing_error` = {}, `incorrect_error` = {}, `spelling_error` = {}, `normalize_error` = {}, `total_error` = {}, `quality_percentage` = {}
			WHERE `quality_date` = '{}' {}{} and `quality_user_id` = '{}' and `quality_mode` = 'QA' and `quality_type` = '{}' and `filename` = '{}' and `received_count` = '{}' and `audit_count` = '{}' limit 1;
			""".format(missing_error, incorrect_error, spelling_error, normalize_error, total_error, quality_percentage, old_revert_date, project_entered, process_entered, collected_data[0][-1], revert_form_data['Q-Type'], revert_form_data['Filename'], revert_form_data['Rcvd'], revert_form_data['Audit'])
			
			list_cursor = database_reconnection()
			list_cursor.execute(update_query)
			db_test.commit()
			#list_cursor.close()
			print("{} - {} | Revert Data Updated".format(session['wissend_id'], session['employee_name']))
		except:
			print(traceback.format_exc())
		finally:
			return True

	def current_month_date_range():
		today_date = datetime.now()
		if today_date.day != 1:
			current_month_date = today_date.replace(day=1)
			next_month_date = current_month_date.replace(month=current_month_date.month+1)
			days_per_month = (next_month_date - current_month_date).days
			index_date = current_month_date.strftime("%Y-%m-%d")
			end_date = current_month_date.replace(day=days_per_month).strftime("%Y-%m-%d")
		else:
			current_month_date = today_date.replace(month=today_date.month-1, day=1)
			next_month_date = current_month_date.replace(month=current_month_date.month+1)
			days_per_month = (next_month_date - current_month_date).days
			index_date = current_month_date.strftime("%Y-%m-%d")
			end_date = current_month_date.replace(day=days_per_month).strftime("%Y-%m-%d")
		return " and prod_tbl.production_date between '{}' and '{}' ".format(index_date, end_date)
	
	def image_to_binary(image_name):
		with open(image_name, 'rb') as file:
			binary_data = file.read()
		return binary_data

	def production_data_insert(data, form_list, notes_target_list, session):
		global db_test
		try:
			insert_data_list = []
			i = 0
			for form_data_list in form_list:
				new_data_list = []
				if len(form_data_list) == 11:
					input_date = form_data_list[0][1]
					if input_date == '':
						input_date = session['db_date']
					else:
						input_date = datetime.strptime(input_date,"%d-%m-%Y").strftime("%Y-%m-%d")
					del form_data_list[0]
				else:
					input_date = session['db_date']
				new_data_list.append(input_date)
				new_data_list.append(session['employee_id'])
				new_data_list.append(session['project_id'])
				new_data_list.append(session['process_id'])
				new_data_list.append(session['business_head_id'])
				new_data_list.append(session['manager_id'])
				new_data_list.append(session['lead_id'])
				cat_val = form_data_list[1][1]
				cat_id = form_data_list[1][0].split("_")[-1]
				if cat_val == "":
					cat_val = form_data_list[3][1]
					cat_id = form_data_list[3][0].split("_")[-1]
					if cat_val == "":
						cat_val = form_data_list[4][1]
						cat_id = form_data_list[4][0].split("_")[-1]
				new_data_list.append(cat_id)
				task_id = form_data_list[2][0].split("_")[-1]
				new_data_list.append(task_id)
				simple_count = form_data_list[5][1] if form_data_list[0][1].split('_')[0] == 'simple' and form_data_list[5][1] != "" else 0
				task_count = form_data_list[5][1] if form_data_list[0][1].split('_')[0] == 'task' and form_data_list[5][1] != "" else 0
				parent_count = form_data_list[6][1] if form_data_list[6][1] != "" else 0
				child_count = form_data_list[7][1] if form_data_list[7][1] != "" else 0
				if parent_count != 0 and child_count != 0:
					simple_count = 0
					task_count = 0
				new_data_list.append(simple_count)
				new_data_list.append(task_count)
				new_data_list.append(parent_count)
				new_data_list.append(child_count)
				achieved_count = notes_target_list[2][1] if i == 0 else 0
				new_data_list.append(achieved_count)
				target_count = notes_target_list[1][1] if i == 0 else 0
				new_data_list.append(target_count)		
				hours_count = form_data_list[8][1] if form_data_list[8][1] != "" else 0
				new_data_list.append(hours_count)
				minutes_count = form_data_list[9][1] if form_data_list[9][1] != "" else 0
				new_data_list.append(minutes_count)
				time_minutes_count = (int(hours_count)*60)+(int(minutes_count))
				new_data_list.append(time_minutes_count)
				productivity = round((int((achieved_count))/int((target_count)))*100, 0) if i == 0 else 0
				new_data_list.append(productivity)
				backlog_count = notes_target_list[3][1] if i == 0 else 0
				new_data_list.append(backlog_count)
				exceed_count = notes_target_list[4][1] if i == 0 else 0
				new_data_list.append(exceed_count)
				notes = notes_target_list[0][1] if i == 0 else ""
				new_data_list.append(notes)
				new_data_list.append(session['employee_id'])
				i =+ 1
				insert_data_list.append(str(tuple(new_data_list)))
			
			select_query = """
			SELECT production_date FROM `daily_productivity_info` WHERE `production_date` = '{0}' and `employee_id` = '{1}' and `project_id` = '{2}' and `project_process_id` = '{3}' and `category_id` = '{4}' and `task_id` = '{5}' and `simple_count` = '{6}' and `task_count` = '{7}' and `parent_count` = '{8}' and `child_count` = '{9}' and `achieved` = '{10}' and `target` = '{11}' and `hours` = '{12}' and `minutes` = '{13}' and `hours_worked` = '{14}' limit 1;
			""".format(input_date, session['employee_id'], session['project_id'], session['process_id'], cat_id, task_id, simple_count, task_count, parent_count, child_count, achieved_count, target_count, hours_count, minutes_count, time_minutes_count)
			get_data = get_production_data_by_query(select_query)
			if get_data[1] == []:
				query = """
				INSERT INTO `daily_productivity_info` (`production_date`,`employee_id`,`project_id`,`project_process_id`,`business_head_id`,`manager_id`,`team_lead_id`,`category_id`,`task_id`,`simple_count`,`task_count`,`parent_count`,`child_count`,`achieved`,`target`,`hours`,`minutes`,`hours_worked`,`productivity_percentage`,`backlog`,`exceed`,`notes`,`employee_id_modified`) VALUES {0};
				""".format((", ".join(insert_data_list)))
				
				list_cursor = database_reconnection()
				list_cursor.execute(query)
				db_test.commit()
				#list_cursor.close()
				print("{} - {} | Production Data inserted".format(session['wissend_id'], session['employee_name']))
			else:
				print("{} - {} | Production Data Repeated".format(session['wissend_id'], session['employee_name']))
		except:
			print(traceback.format_exc())
		return True

	def change_password(new_password, wiss_emp_id):
		global db_test
		try:
			query = """UPDATE `employees_info` SET employee_password='{}' WHERE wiss_employee_id = '{}';""".format(new_password, wiss_emp_id)
			list_cursor = database_reconnection()
			list_cursor.execute(query)
			db_test.commit()
			#list_cursor.close()
			print("Password Changed")
		except:
			print(traceback.format_exc())
		return new_password

	def quality_data_insert(inp_form_data, session):
		global db_test
		try:
			form_data_list = list(inp_form_data.items())

			quality_data = []
			input_date = form_data_list[0][1]
			if input_date == '':
				input_date = session['db_date']
			else:
				input_date = datetime.strptime(input_date,"%d-%m-%Y").strftime("%Y-%m-%d")
			quality_date = input_date
			qlty_entry_date = session['db_date']
			del form_data_list[0]
			project_report_list = form_data_list[:5]
			del form_data_list[:5]
			form_list = [ form_data_list[i:i+12] for i in range(0, len(form_data_list), 12) ]
			for form_data in form_list:
				split_list = []
				split_list.append(quality_date)
				split_list.append(qlty_entry_date)
				split_list.append(session['employee_id'])
				split_list.append(project_report_list[1][1])
				process_id = project_report_list[3][1]
				if process_id != "All" and process_id != "":
					split_list.append(process_id)
				else:
					process_id = ""

				quality_mode = 'QA' if session['emp_type'] == 'TQA' else 'QC'
				split_list.append(quality_mode)
				quality_type = form_data[0][1] if form_data[0][1] != "" else ""
				split_list.append(quality_type)
				production_user = form_data[1][1].split("_")[-1] if form_data[1][1] != "" else ""
				if production_user != "":
					split_list.append(production_user)
				file_name = form_data[2][1] if form_data[2][1] != "" else ""
				split_list.append(file_name)
				received_count = form_data[3][1] if form_data[3][1] != "0" else "0"
				split_list.append(received_count)
				audit_count = form_data[4][1] if form_data[4][1] != "0" else "0"
				split_list.append(audit_count)
				missing_count = form_data[5][1] if form_data[5][1] != "0" else "0"
				split_list.append(missing_count)
				incorrect_count = form_data[6][1] if form_data[6][1] != "0" else "0"
				split_list.append(incorrect_count)
				spelling_count = form_data[7][1] if form_data[7][1] != "0" else "0"
				split_list.append(spelling_count)
				normalize_count = form_data[8][1] if form_data[8][1] != "0" else "0"
				split_list.append(normalize_count)
				hours = form_data[9][1] if form_data[9][1] != "0" else "0"
				split_list.append(hours)
				minutes = form_data[10][1] if form_data[10][1] != "0" else "0"
				split_list.append(minutes)
				quality_hours = (int(hours)*60)+(int(minutes))
				split_list.append(quality_hours)
				quality_comments = form_data[11][1] if form_data[11][1] != "" else ""
				split_list.append(quality_comments)
				total_error = int(missing_count)+int(incorrect_count)+int(spelling_count)+int(normalize_count)
				split_list.append(total_error)
				quality_count = round((((1 - (int(total_error)/int(audit_count))) * 100)), 0)
				sampling_count = round(((int(audit_count)/int(received_count)) * 100), 0)
				split_list.append(quality_count)
				split_list.append(sampling_count)
				split_list.append(session['employee_id'])
				quality_data.append(str(tuple(split_list)))
				
			if production_user != "":
				production_user_header = "and `production_user_id` = "
			else:
				production_user_header = ""
			if process_id != "":
				process_id_header = " and `project_process_id` = "
			else:
				process_id_header = ""
			select_query = """
			SELECT quality_date FROM `quality_info` WHERE `quality_date` = '{}' and `entry_date` = '{}' and `quality_user_id` = '{}' and `project_id` = '{}' {}{} and `quality_mode` = '{}' and `quality_type` = '{}' {}{} and `filename` = '{}' and `received_count` = '{}' and `audit_count` = '{}' and `hours` = '{}' and `minutes` = '{}' limit 1;
			""".format(input_date, qlty_entry_date, session['employee_id'], project_report_list[1][1], process_id_header, process_id, quality_mode, quality_type, production_user_header, production_user, file_name, received_count, audit_count, hours, minutes)
			get_data = get_production_data_by_query(select_query)
			if get_data[1] == []:
				if process_id != "":
					process_id_column = ", `project_process_id`"
				else:
					process_id_column = ""
				if production_user != "":
					user_column = ",`production_user_id`"
				else:
					user_column = ""
				query = """
					INSERT INTO `quality_info` (`quality_date`,`entry_date`,`quality_user_id`,`project_id`{},`quality_mode`,`quality_type`{},`filename`,`received_count`,`audit_count`,`missing_error`,`incorrect_error`,`spelling_error`,`normalize_error`,`hours`,`minutes`,`quality_hours`,`comments`,`total_error`,`quality_percentage`,`sampling_percentage`,`employee_id_modified`) VALUES {};
					""".format(process_id_column, user_column, (", ".join(quality_data)))
				
				list_cursor = database_reconnection()
				list_cursor.execute(query)
				db_test.commit()
				#list_cursor.close()
				print("{} - {} | Quality Data Inserted".format(session['wissend_id'], session['employee_name']))
		except:
			print(traceback.format_exc())
		return True

	def task_creation_insert(form_data, session_data):
		global db_test
		aknowledgement = {}
		try:
			task_creation_major_list = []
			prev_task_list = []
			new_task_list = []

			form_data_list = list(form_data.items())
			if form_data_list[2][1] == 'Task Creation':
				task_creation_project_id = form_data_list[1][1]
				for form_values in form_data_list:
					task_value_data = []
					if form_values[1] != '':
						if 'task_creation' in form_values[0]:
							task_value_data.append(int(task_creation_project_id))
							task_value_data.append(form_values[1].title())

							select_query = """select task_name from `project_task_info` where `project_id` = '{}' and `task_name` = '{}' limit 1;""".format(task_creation_project_id, form_values[1].title())
							result_data = get_dict_results(select_query)

							if result_data == []:
								task_creation_major_list.append(str(tuple(task_value_data)))
								new_task_list.append(form_values[1].title())
							else:
								prev_task_list.append(result_data[0]['task_name'])


			if task_creation_major_list != []:
				task_insert_query = """insert into `project_task_info` (`project_id`,`task_name`) VALUES {};
				""".format((", ".join(task_creation_major_list)))
				list_cursor = database_reconnection()
				list_cursor.execute(task_insert_query)
				db_test.commit()
				#list_cursor.close()
				print("{} - {} | New Task Inserted".format(session_data['wissend_id'], session_data['employee_name']))

			if prev_task_list == [] and new_task_list != []:
				aknowledgement['new_task_list'] = new_task_list
				aknowledgement['prev_task_list'] = []
			elif prev_task_list != [] and new_task_list == []:
				aknowledgement['new_task_list'] = []
				aknowledgement['prev_task_list'] = prev_task_list
			elif prev_task_list != [] and new_task_list != []:
				aknowledgement['new_task_list'] = new_task_list
				aknowledgement['prev_task_list'] = prev_task_list
		except:
			print(traceback.format_exc())
		return aknowledgement

	def short_name(text):
		l = text.split()
		return_short_name = ''
		if len(l) >= 3:
			new = ""
			for i in range(0, len(l)-1):
				text = l[i]
				new += text[0].upper()+''
			return_short_name = new+' '+l[-1].title()
		else:
			return_short_name = text.title()
		return return_short_name

	def process_creation_insert(form_data, emp_storage):
		global db_test
		aknowledgement = {}
		try:
			process_creation_major_dict = {}
			heads_list = []
			final_process_creation_data = []
			process_creation_major_dict['project_process_id'] = []
			limited_checklist = []
			prev_process_list = []
			new_process_list = []

			form_data_list = list(form_data.items())
			common_db_values = [common_db_values for common_db_values in emp_storage['employee_projects'][form_data['addon_project']]['process'].values()]
			heads_list.append(common_db_values[0]['business_head_id'])
			heads_list.append(common_db_values[0]['manager_id'])
			heads_list.append(common_db_values[0]['lead_id'])

			if form_data_list[2][1] == 'Process Creation':
				process_creation_project_id = form_data_list[1][1]
				del form_data_list[:3]

				process_map_dict = {}
				key_numbers = {}
				for form_values in form_data_list:
					if form_values[1] != '':
						if 'process_creation' in form_values[0]:
							key_numbers[form_values[0].split('_')[-1]] = form_values[1]
							process_map_dict[form_values[1]] = []
						if '_name_' in form_values[0]:
							for key_id, key_value in key_numbers.items():
								if form_values[0].split('_')[-2] == key_id:
									process_map_dict[key_value].append(form_values[1].split('_')[1])
				process_creation_major_dict['project_id'] = process_creation_project_id
				process_creation_major_dict['heads_list'] = heads_list
				process_creation_major_dict['process_mapped_users'] = process_map_dict

			for exact_process_name in process_map_dict.keys():
				process_values_data = []
				return_short_name = short_name(exact_process_name.title())
				process_values_data.append(exact_process_name.title())
				process_values_data.append(process_creation_major_dict['project_id'])
				process_values_data.append(return_short_name)
				process_values_data.append(process_creation_major_dict['heads_list'][0])
				process_values_data.append(process_creation_major_dict['heads_list'][1])
				process_values_data.append(process_creation_major_dict['heads_list'][2])
				process_values_data.append(emp_storage['employee_id'])

				select_query = """select project_process_id from `project_process_info` where `process_name` = '{}' and `project_id` = '{}' and `business_head_id` = '{}' and `manager_id` = '{}' and `team_lead_id` = '{}' limit 1;
				""".format(exact_process_name, process_creation_major_dict['project_id'], process_creation_major_dict['heads_list'][0], process_creation_major_dict['heads_list'][1], process_creation_major_dict['heads_list'][2])
				result_data = get_dict_results(select_query)
				if result_data == []:
					final_process_creation_data.append(str(tuple(process_values_data)))
					limited_checklist.append('New process')
					new_process_list.append(exact_process_name.title())
				else:
					limited_checklist.append(result_data[0]['project_process_id'])
					prev_process_list.append(exact_process_name.title())

			if final_process_creation_data != []:
				process_insert_query = """insert into `project_process_info` (`process_name`,`project_id`,`process_short_name`,`business_head_id`,`manager_id`,`team_lead_id`,`employee_id_modified`) VALUES {};
				""".format((", ".join(final_process_creation_data)))
				list_cursor = database_reconnection()
				list_cursor.execute(process_insert_query)
				db_test.commit()
				#list_cursor.close()
				print("{} - {} | New Process Inserted".format(emp_storage['wissend_id'], emp_storage['employee_name']))

			for exact_process_name, exact_process_values in process_map_dict.items():
				select_query = """select project_process_id from `project_process_info` where `process_name` = '{}' and `project_id` = '{}' and `business_head_id` = '{}' and `manager_id` = '{}' and `team_lead_id` = '{}' limit 1;
				""".format(exact_process_name, process_creation_major_dict['project_id'], process_creation_major_dict['heads_list'][0], process_creation_major_dict['heads_list'][1], process_creation_major_dict['heads_list'][2])
				result_data = get_dict_results(select_query)
				if result_data != []:
					process_creation_major_dict['project_process_id'].append(result_data[0]['project_process_id'])

					if 'New process' in limited_checklist:
						process_creation_major_dict[result_data[0]['project_process_id']] = exact_process_values
					else:
						process_creation_major_dict[result_data[0]['project_process_id']] = []

			if 'New process' in limited_checklist:
				highers_in = []
				final_employee_process_creation_data = []
				for new_process_id in process_creation_major_dict['project_process_id']:
					for checked_process_keys, checked_process_values in process_creation_major_dict.items():
						if new_process_id == checked_process_keys:
							for freezed_users_id in checked_process_values:
								employees_process_values = []
								employees_process_values.append(int(freezed_users_id))
								employees_process_values.append(int(checked_process_keys))
								employees_process_values.append(int(process_creation_major_dict['project_id']))
								employees_process_values.append('Active')

								for higher_officials in process_creation_major_dict['heads_list']:
									highers_list = []
									if freezed_users_id != str(higher_officials):
										done = str(higher_officials)+'_'+str(new_process_id)
										if done not in highers_in and str(higher_officials) not in checked_process_values:
											highers_list.append(higher_officials)
											highers_list.append(new_process_id)
											highers_list.append(int(process_creation_major_dict['project_id']))
											highers_list.append('Active')
											highers_in.append(done)

									select_query = """select employee_process_id from `employee_process_info` where `employee_id` = '{}' and `project_process_id` = '{}' and `project_id` = '{}' and `status` = '{}' limit 1;
									""".format(higher_officials, new_process_id, process_creation_major_dict['project_id'], 'Active')
									result_data = get_dict_results(select_query)
									if result_data == []:
										if highers_list != []:
											final_employee_process_creation_data.append(str(tuple(highers_list)))

								select_query = """select employee_process_id from `employee_process_info` where `employee_id` = '{}' and `project_process_id` = '{}' and `project_id` = '{}' and `status` = '{}' limit 1;
								""".format(freezed_users_id, checked_process_keys, process_creation_major_dict['project_id'], 'Active')
								result_data = get_dict_results(select_query)
								if result_data == []:
									final_employee_process_creation_data.append(str(tuple(employees_process_values)))

				if final_employee_process_creation_data != []:
					employees_insert_query = """insert into `employee_process_info` (`employee_id`,`project_process_id`,`project_id`,`status`) VALUES {};
					""".format((", ".join(final_employee_process_creation_data)))
					list_cursor = database_reconnection()
					list_cursor.execute(employees_insert_query)
					db_test.commit()
					#list_cursor.close()
					print("{} - {} | Employees mapped successfully".format(emp_storage['wissend_id'], emp_storage['employee_name']))
					aknowledgement['process_employees_list'] = 'employees mapped successfully'
			
			if prev_process_list == [] and new_process_list != []:
				aknowledgement['new_process_list'] = new_process_list
				aknowledgement['prev_process_list'] = []
			elif prev_process_list != [] and new_process_list == []:
				aknowledgement['new_process_list'] = []
				aknowledgement['prev_process_list'] = prev_process_list
			elif prev_process_list != [] and new_process_list != []:
				aknowledgement['new_process_list'] = new_process_list
				aknowledgement['prev_process_list'] = prev_process_list
		except:
			print(traceback.format_exc())
		return aknowledgement
	
	def master_data(data_id):
		global db_test
		result = 0
		try:
			if data_id != "e":
				if data_id == "o":
					condition_data = ""
				elif data_id == "a":
					condition_data = "and emp_tbl.status in ('Active')"
				elif data_id == "ia":
					condition_data = "and emp_tbl.status in ('Inactive')"
				elif data_id == "pf":
					condition_data = "and emp_tbl.pf in ('Y')"
				else:
					condition_data = ""
				query = """
				SELECT emp_tbl.employee_name as Name, emp_tbl.wiss_employee_id as ID, prj_tbl.project_name as Project, desig_tbl.designation as Desig, date_format(emp_tbl.joined_date, '%d-%b-%Y') as DOJ, emp_tbl.contact_number as Contact_No, date_format(emp_tbl.date_of_birth, '%d-%b-%Y') as DOB, emp_tbl.age as Age, emp_tbl.personal_mail as Personal_Mail, emp_tbl.wissend_mail as Wissend_Mail, date_format(emp_tbl.previous_appraisal_date, '%d-%b-%Y') as Prev_Appraisal, date_format(emp_tbl.next_appraisal_date, '%d-%b-%Y') as Next_Appraisal, qlfy_tbl.qualification as Qualify, emp_tbl.overall_experience as Work_Exp, emp_tbl.relevant_experience as Rel_Exp, emp_tbl.wissend_experience as Wiss_Exp, emp_tbl.present_address as Present_Address, emp_tbl.permanent_address as Permanent_Address, emp_tbl.place as Location, emp_tbl.father as Father, emp_tbl.mother as Mother, emp_tbl.marital_status Marital, emp_tbl.spouse as Spouse, emp_tbl.children as Children, emp_tbl.alternate_contact as Alt_Contact, emp_tbl.emergency_contact as Emer_Contact, emp_tbl.emergency_name_relationship as Emer_Name_Relationship, emp_tbl.blood_group as Blood, emp_tbl.bank_account as Bank_Acc, emp_tbl.pan as PAN, emp_tbl.aadhar as Aadhar, emp_tbl.passport as Passport, emp_tbl.grade as Grade, emp_tbl.ctc_per_month as Month_CTC, emp_tbl.ctc_per_year as Year_CTC, emp_tbl.pf as PF, emp_tbl.esi as ESI, emp_tbl.status as Status, date_format(emp_tbl.relieved_date, '%d-%b-%Y') as Relieved from `employees_info` as emp_tbl
				INNER JOIN `designation_info` as desig_tbl ON desig_tbl.designation_id = emp_tbl.designation_id
				INNER JOIN `qualification_info` as qlfy_tbl ON qlfy_tbl.qualification_id = emp_tbl.qualification_id
				INNER JOIN `employee_process_info` as emp_prcs_tbl ON emp_prcs_tbl.employee_id = emp_tbl.employee_id
				INNER JOIN `project_process_info` as prj_prcs_tbl ON prj_prcs_tbl.project_process_id = emp_prcs_tbl.project_process_id
				INNER JOIN `projects_info` as prj_tbl ON prj_tbl.project_id = prj_prcs_tbl.project_id
				WHERE `wiss_employee_id` not in ("ADMIN","Vellai")  {} GROUP BY emp_tbl.employee_id ORDER BY emp_tbl.wiss_employee_id ;
				""".format(condition_data)
				list_cursor = database_reconnection()
				list_cursor.execute(query)
				column_names = [i[0] for i in list_cursor.description]
				result_data = list_cursor.fetchall()
				#list_cursor.close()
				if result_data != [] and result_data[0][0] != None:
					active_user = 0
					inactive_user = 0
					pf_user = 0
					fresher_user = 0
					intermediate_user = 0
					experienced_user = 0
					for employee_data in result_data:
						if employee_data[37] == "Active":
							active_user += 1
							if employee_data[35] == "Y":
								pf_user += 1
							if employee_data[15] <= 1:
								fresher_user += 1
							elif employee_data[15] <= 5:
								intermediate_user += 1
							else:
								experienced_user += 1
						else:
							inactive_user += 1
					result = [column_names, result_data, [len(result_data), active_user, inactive_user, pf_user, fresher_user, intermediate_user, experienced_user]]
		except:
			print(traceback.format_exc())
			pass
		return result
	
	def master_page_data():
		global db_test
		result = 0
		try:
			query = """
			SELECT emp_tbl.employee_name as Name, emp_tbl.wiss_employee_id as ID, desig_tbl.designation as Designation, date_format(emp_tbl.joined_date, '%d-%b-%Y') as DOJ, emp_tbl.contact_number as Contact_No, date_format(emp_tbl.date_of_birth, '%d-%b-%Y') as DOB, emp_tbl.age as Age, emp_tbl.personal_mail as Personal_Mail, emp_tbl.wissend_mail as Wissend_Mail, date_format(emp_tbl.previous_appraisal_date, '%d-%b-%Y') as Prev_Appraisal, date_format(emp_tbl.next_appraisal_date, '%d-%b-%Y') as Next_Appraisal, qlfy_tbl.qualification as Qualify, emp_tbl.overall_experience as Work_Exp, emp_tbl.relevant_experience as Rel_Exp, emp_tbl.wissend_experience as Wiss_Exp, emp_tbl.present_address as Present_Address, emp_tbl.permanent_address as Permanent_Address, emp_tbl.place as Location, emp_tbl.father as Father, emp_tbl.mother as Mother, emp_tbl.marital_status Marital, emp_tbl.spouse as Spouse, emp_tbl.children as Children, emp_tbl.alternate_contact as Alt_Contact, emp_tbl.emergency_contact as Emer_Contact, emp_tbl.emergency_name_relationship as Emer_Name_Relationship, emp_tbl.blood_group as Blood, emp_tbl.bank_account as Bank_Acc, emp_tbl.pan as PAN, emp_tbl.aadhar as Aadhar, emp_tbl.passport as Passport, emp_tbl.grade as Grade, emp_tbl.ctc_per_month as Month_CTC, emp_tbl.ctc_per_year as Year_CTC, emp_tbl.pf as PF, emp_tbl.esi as ESI, emp_tbl.status as Status, date_format(emp_tbl.relieved_date, '%d-%b-%Y') as Relieved from `employees_info` as emp_tbl
			INNER JOIN `designation_info` as desig_tbl ON desig_tbl.designation_id = emp_tbl.designation_id
			INNER JOIN `qualification_info` as qlfy_tbl ON qlfy_tbl.qualification_id = emp_tbl.qualification_id  WHERE `wiss_employee_id` not in ("ADMIN","Vellai") ORDER BY emp_tbl.wiss_employee_id;
			"""
			list_cursor = database_reconnection()
			list_cursor.execute(query)
			column_names = [i[0] for i in list_cursor.description]
			result_data = list_cursor.fetchall()
			#list_cursor.close()
			if result_data != [] and result_data[0][0] != None:
				active_user = 0
				inactive_user = 0
				pf_user = 0
				fresher_user = 0
				intermediate_user = 0
				experienced_user = 0
				for employee_data in result_data:
					if employee_data[36] == "Active":
						active_user += 1
						if employee_data[34] == "yes":
							pf_user += 1
						if employee_data[14] <= 1:
							fresher_user += 1
						elif employee_data[14] <= 4:
							intermediate_user += 1
						else:
							experienced_user += 1
					else:
						inactive_user += 1
				result = [column_names, result_data, [len(result_data), active_user, inactive_user, pf_user, fresher_user, intermediate_user, experienced_user]]
		except:
			print(traceback.format_exc())
			pass
		return result
	
	def kra_input_insert(form_data, session_data):
		global db_test
		result = 0
		try:
			kra_for_emp_id = form_data['kra_for_employee_id'] if form_data.get('kra_for_employee_id', 0) != 0 and form_data.get('kra_for_employee_id', 0) != "" else ""
			comments = form_data['comments'] if form_data.get('comments', 0) != 0 else ""
			stakeholder_rating = form_data['achieved_rating'] if form_data.get('achieved_rating', 0) != 0 else "0"
			kra_date = session_data['db_date']
			date_time = indian_datetime_format(session_data)
			month = date_time.month - 1 if session_data['emp_type'] not in ['ADMIN','TA','TBH','TBHR'] else int(session_data['kra_month_selected'])
			if month == 0:
				month = 12
				year = date_time.year - 1
			else:
				year = date_time.year

			if session_data['emp_type'] in ['ADMIN','TA','TBH','TBHR']:
				modified_month_dbcheck = "and month(review_for_month) = {}".format(session_data['kra_month_selected'])
			else:
				session_data['kra_year_selected'] = str(year)
				session_data['kra_month_selected'] = str(month)
				modified_month_dbcheck = ""
			review_for_month = date_time.replace(day=1,month=month,year=year).strftime("%Y-%m-%d")

			if session_data['emp_type'] in ['TL', 'TLR']:
				kra_by_id = ",lead_id"
				kra_by_rating = ",lead_rating"
				kra_by_score = ",lead_score"
				comments_header = ",lead_comments"
				other_comments_header = ",manager_comments,business_head_comments"
				other_comments = ",'',''"
				achieved_rating = "0"
			elif session_data['emp_type'] in ['TM', 'TMR']:
				kra_by_id = ",manager_id"
				kra_by_rating = ",manager_rating"
				kra_by_score = ",manager_score"
				comments_header = ",manager_comments"
				other_comments_header = ",lead_comments,business_head_comments"
				other_comments = ",'',''"
				if session_data['bh_id'] == session_data['employee_id']:
					kra_by_id = ",business_head_id"
					kra_by_rating = ",business_head_rating"
					kra_by_score = ",business_head_score"
					comments_header = ",business_head_comments"
					other_comments_header = ",lead_comments,manager_comments"
					other_comments = ",'',''"
					achieved_rating = form_data['achieved_rating'] if form_data.get('achieved_rating', 0) != 0 else "0"
				else:
					achieved_rating = "0"
			else:
				kra_by_id = ",business_head_id"
				kra_by_rating = ",business_head_rating"
				kra_by_score = ",business_head_score"
				comments_header = ",business_head_comments"
				other_comments_header = ",lead_comments,manager_comments"
				other_comments = ",'',''"
				achieved_rating = form_data['achieved_rating'] if form_data.get('achieved_rating', 0) != 0 else "0"
			form_data_list = list(form_data.items())

			query = """select date_format(review_date, '%Y-%m-%d') as review_date from `kra_input` where kra_for_employee_id = '{0}' and is_active = 'Y' {1} order by review_date desc limit 1;""".format(kra_for_emp_id, modified_month_dbcheck)
			results = get_dict_results(query)

			data_list = []
			for list_data in form_data_list[:-3]:
				key_list = []
				key_split = list_data[0].split("_")
				key_list.append(kra_date)
				key_list.append(review_for_month)
				key_list.append(kra_for_emp_id)
				key_list.append(key_split[0])
				key_list.append(list_data[1])
				key_list.append(str(int(key_split[1])*int(list_data[1])))
				key_list.append(session_data['employee_id'])
				data_list.append(str(tuple(key_list)))

			if results == []:
				query = """
				insert into `kra_input` (review_date,review_for_month,kra_for_employee_id,ques_ans_id {0} {1} {3}) values {2}
				""".format(kra_by_rating,kra_by_score,(", ".join(data_list)),kra_by_id)
			else:
				current_month = datetime.strptime(kra_date, "%Y-%m-%d").month
				db_month = datetime.strptime(results[0]['review_date'], "%Y-%m-%d").month

				if current_month == db_month:
					rating_list = []
					score_list = []
					for list_data in form_data_list[:-3]:
						key_split = list_data[0].split("_")
						rating_list.append("when {} then {}".format(int(key_split[0]), int(list_data[1])))
						score_list.append("when {} then {}".format(int(key_split[0]), int(key_split[1])*int(list_data[1])))
					query="""
					update kra_input set {0} = case ques_ans_id
					{1}
					end, {2} = case ques_ans_id
					{3}
					end, {6} = {7}
					where kra_for_employee_id = {4} and month('{5}') = month(review_date) and year('{5}') = year(review_date) and is_active = 'Y';
					""".format(kra_by_rating.strip(","),(" ".join(rating_list)),kra_by_score.strip(","),(" ".join(score_list)),kra_for_emp_id,kra_date,kra_by_id.strip(","),session_data['employee_id'])
				else:
					if session_data['emp_type'] in ['ADMIN','TA','TBH','TBHR']:
						rating_list = []
						score_list = []
						for list_data in form_data_list[:-3]:
							key_split = list_data[0].split("_")
							rating_list.append("when {} then {}".format(int(key_split[0]), int(list_data[1])))
							score_list.append("when {} then {}".format(int(key_split[0]), int(key_split[1])*int(list_data[1])))
						query="""
						update kra_input set {0} = case ques_ans_id {1} end, {2} = case ques_ans_id {3} end, {6} = {7}
						where kra_for_employee_id = {4} and month('{5}') = month(review_date) and year('{5}') = year(review_date) and is_active = 'Y';
						""".format(kra_by_rating.strip(","), (" ".join(rating_list)), kra_by_score.strip(","), (" ".join(score_list)), kra_for_emp_id, results[0]['review_date'], kra_by_id.strip(","), session_data['employee_id'])
					else:
						query = """
						insert into `kra_input` (review_date,review_for_month,kra_for_employee_id,ques_ans_id {0} {1} {3}) values {2}
						""".format(kra_by_rating,kra_by_score, (", ".join(data_list)), kra_by_id)
			list_cursor = database_reconnection()
			list_cursor.execute(query)
			db_test.commit()
			#list_cursor.close()
			query = """
			select date_format(review_date, '%Y-%m-%d') as review_date, date_format(review_for_month, '%Y-%m-%d') as review_for_month, achieved_rating, last_review_date, last_review_rating from `kra_summary_report` where kra_for_employee_id = '{0}' and is_active = 'Y' order by review_date desc limit 1;
			""".format(kra_for_emp_id)
			results = get_dict_results(query)

			selected_month_query = """
			select date_format(review_date, '%Y-%m-%d') as review_date, date_format(review_for_month, '%Y-%m-%d') as review_for_month, achieved_rating, last_review_date, last_review_rating from `kra_summary_report` where kra_for_employee_id = '{0}' and is_active = 'Y' and {1} >= month(review_for_month) and {2} = year(review_for_month) order by review_date desc;
			""".format(kra_for_emp_id, str(int(session_data['kra_month_selected'])+1), session_data['kra_year_selected'])
			selected_month_results = get_dict_results(selected_month_query)

			if results == []:
				query = """
				insert into `kra_summary_report` (review_date,review_for_month,kra_for_employee_id {0},achieved_rating,last_review_date,last_review_rating {5} {8}) values ('{1}','{2}','{3}','{7}','{4}','{2}','{4}','{6}' {9})
				""".format(kra_by_rating,kra_date,review_for_month,kra_for_emp_id,achieved_rating,comments_header,comments,stakeholder_rating,other_comments_header,other_comments)
			else:
				current_month = datetime.strptime(session_data['db_date'], "%Y-%m-%d").month
				db_month = ''

				exact_month_results = []
				bh_last_review_data = []
				if session_data['emp_type'] in ['ADMIN','TA','TBH','TBHR']:
					if selected_month_results != []:
						db_month = datetime.strptime(selected_month_results[0]['review_for_month'], "%Y-%m-%d").month
						for exact_month in selected_month_results:
							if datetime.strptime(exact_month['review_for_month'], "%Y-%m-%d").month < int(session_data['kra_month_selected']):
								bh_last_review_data.append(exact_month['achieved_rating'])
								bh_last_review_data.append(exact_month['review_for_month'])
								break
							if str(datetime.strptime(exact_month['review_for_month'], "%Y-%m-%d").month) == str(int(session_data['kra_month_selected'])):
								db_month = datetime.strptime(exact_month['review_for_month'], "%Y-%m-%d").month
								exact_month_results.append(exact_month)
					else:
						db_month = datetime.strptime(results[0]['review_for_month'], "%Y-%m-%d").month
				else:
					db_month = datetime.strptime(results[0]['review_date'], "%Y-%m-%d").month

				if bh_last_review_data == []:
					# bh_last_review_data.append(selected_month_results[-1]['achieved_rating'])
					# bh_last_review_data.append(selected_month_results[-1]['review_for_month'])
					bh_last_review_data.append(results[0]['achieved_rating'])
					bh_last_review_data.append(results[0]['review_for_month'])

				if current_month == db_month:
					if session_data['emp_type'] in ['TL', 'TLR', 'TM', 'TMR']:
						if session_data['bh_id'] != session_data['employee_id']:
							achieved_rating = results[0]['achieved_rating']
					query="""
					update `kra_summary_report` set {0} = case kra_for_employee_id
					when {1} then {6}
					end, achieved_rating = {2},
					{3} = case kra_for_employee_id
					when {1} then '{4}'
					end where kra_for_employee_id = {1} and month('{5}') = month(review_date) and year('{5}') = year(review_date) and is_active = 'Y';
					""".format(kra_by_rating.strip(","),kra_for_emp_id,achieved_rating,comments_header.strip(","),comments,kra_date,stakeholder_rating)
				else:
					if session_data['emp_type'] in ['ADMIN','TA','TBH','TBHR']:
						if exact_month_results == []:
							last_review_date = results[0]['review_for_month']
							last_review_rating = results[0]['achieved_rating']
							query = """
							insert into `kra_summary_report` (review_date,kra_for_employee_id,achieved_rating {0},last_review_date,last_review_rating {4}, review_for_month {10}) values ('{1}','{2}','{3}','{9}','{6}','{7}','{5}','{8}' {11})
							""".format(kra_by_rating,kra_date,kra_for_emp_id,achieved_rating,comments_header,comments,last_review_date,last_review_rating,review_for_month,stakeholder_rating,other_comments_header,other_comments)
						else:
							last_review_rating = ", last_review_rating = '{}'".format(bh_last_review_data[0])
							last_review_date = ", last_review_date = '{}'".format(bh_last_review_data[1])
							query="""
							update `kra_summary_report` set {0} = case kra_for_employee_id
							when {1} then {6}
							end, achieved_rating = {2},
							{3} = case kra_for_employee_id
							when {1} then '{4}'
							end {7} {8}
							where kra_for_employee_id = {1} and month('{5}') = month(review_for_month) and year('{5}') = year(review_for_month) and is_active = 'Y';
							""".format(kra_by_rating.strip(","),kra_for_emp_id,achieved_rating,comments_header.strip(","),comments,review_for_month,stakeholder_rating, last_review_date, last_review_rating)

							prev_last_rviewupdate = """
							update `kra_summary_report` set last_review_rating = {2}
							where kra_for_employee_id = '{0}' and is_active = 'Y' and month(review_for_month) = {1} and year(review_for_month) = {1}
							""".format(kra_for_emp_id, str(int(session_data['kra_month_selected'])+1), achieved_rating)
							execute_query(prev_last_rviewupdate)
					else:
						last_review_date = results[0]['review_for_month']
						last_review_rating = results[0]['achieved_rating']
						query = """
						insert into `kra_summary_report` (review_date,kra_for_employee_id,achieved_rating {0},last_review_date,last_review_rating {4}, review_for_month {10}) values ('{1}','{2}','{3}','{9}','{6}','{7}','{5}','{8}' {11})
						""".format(kra_by_rating,kra_date,kra_for_emp_id,achieved_rating,comments_header,comments,last_review_date,last_review_rating,review_for_month,stakeholder_rating,other_comments_header,other_comments)
			
			list_cursor = database_reconnection()
			list_cursor.execute(query)
			db_test.commit()
			#list_cursor.close()
			result = "Kra Data Inserted"
			print("{} - {} | KRA Data Submitted".format(session_data['wissend_id'], session_data['employee_name']))
		except:
			print(traceback.format_exc())
			pass
		return result

	def kra_report_details(session_data, data):
		global db_test
		result = 0
		try:
			kra_user_id = session_data['kra_user_id']
			if kra_user_id == "All":
				user_list = []
				if data['emp_type'] in ['TL', 'TLR', 'TM', 'TMR']:
					for proj_data in data['employee_projects'].values():
						for process_data in proj_data['process'].values():
							if process_data['lead_id'] == data['employee_id'] and str(process_data['lead_id']) not in user_list:
								user_list.append(str(process_data['lead_id']))
							elif process_data['manager_id'] == data['employee_id'] and str(process_data['lead_id']) not in user_list:
								user_list.append(str(process_data['lead_id']))
								user_list.append(str(process_data['manager_id']))
							else:
								user_list.append(str(process_data['lead_id']))
								user_list.append(str(process_data['manager_id']))
				else:
					for proj_data in data['employee_projects'].values():
						for process_data in proj_data['process'].values():
							if str(process_data['lead_id']) not in user_list:
								user_list.append(str(process_data['lead_id']))
							if str(process_data['manager_id']) not in user_list:
								user_list.append(str(process_data['manager_id']))
							if str(process_data['business_head_id']) not in user_list:
								user_list.append(str(process_data['business_head_id']))
				kra_user_id = ", ".join(user_list)
			date_range_condition = kra_year_month_query(session_data, "R")
			query = """
			select date_format(report.review_for_month, '%b%y') as Month, date_format(report.review_date, '%d-%b-%Y') as `Review Date`,  emp_tbl.employee_name as Name, desig.designation as Designation,  report.lead_rating as `Lead`, report.manager_rating as `Manager`, report.business_head_rating as `BHead`, report.achieved_rating as `Achieved`, report.last_review_rating as `Prev Rating`, date_format(report.last_review_date, '%b%y') as `Prev Review`, CONCAT("<b>Lead :</b> ",report.lead_comments, "<br/><b>Manager :</b> ", report.manager_comments, "<br/><b>BHead :</b> ",report.business_head_comments) as Comments from kra_summary_report as report
			inner join employees_info as emp_tbl on report.kra_for_employee_id = emp_tbl.employee_id
			inner join designation_info as desig on emp_tbl.designation_id = desig.designation_id
			where report.kra_for_employee_id in ({0}) {1} and report.is_active = "Y" order by month(report.review_for_month) desc, emp_tbl.employee_name asc;
			""".format(kra_user_id, date_range_condition)
			result = get_dict_results(query)
		except:
			print(traceback.format_exc())
			pass
		return result
	
	def get_dict_results(query):
		global db_test
		result = 0
		try:
			dict_cursor = database_reconnection(cur='dict')
			dict_cursor.execute(query)
			result = dict_cursor.fetchall()
			dict_cursor.close()
		except:
			print(traceback.format_exc())
		finally:
			return result

	def execute_query(query):
		global db_test
		try:
			list_cursor = database_reconnection()
			list_cursor.execute(query)
			db_test.commit()
			#list_cursor.close()
		except:
			print(traceback.format_exc())
		return True
	
	def kra_question_data(session_data, user_id):
		global db_test
		result = 0
		try:
			query = """
			SELECT ques_ans_id, header, question, question_percent, answer, ans_rating FROM employees_info as emp_info
			INNER JOIN designation_info as desig_info ON desig_info.designation_id = emp_info.designation_id
			INNER JOIN kra_question_answer as kra_qa ON kra_qa.desig_role = desig_info.desig_role
			WHERE emp_info.employee_id = {} and kra_qa.is_active = "Y";
			""".format(user_id)
			results = get_dict_results(query)
			data = dict()
			for result_dict in results:
				if data.get(result_dict['question'], 0) == 0:
					data[result_dict['question']] = {"qa_id":result_dict['ques_ans_id'], "percent":result_dict['question_percent'], "header":result_dict['header'],"lead_rating":"","lead_score":"","manager_rating":"","manager_score":"","bh_rating":"","bh_score":"","keys":{result_dict['answer']:{"rating":result_dict['ans_rating']}}}
				else:
					data[result_dict['question']]['keys'][result_dict['answer']] = {"rating":result_dict['ans_rating']}
			result = data
		except:
			print(traceback.format_exc())
			pass
		return result
	
	def kra_year_month_query(session_data, type):
		result = 0
		if type == "R":
			review_month = "review_for_month"
		else:
			if session_data['emp_type'] in ['ADMIN','TA','TBH','TBHR']:
				review_month = "review_for_month"
			else:	
				review_month = "review_date"
		from_date = session_data['kra_year_selected']
		to_date = session_data['kra_month_selected']
		date_time = indian_datetime_format(session_data)
		try:
			if from_date != "" and to_date != "":
				if from_date == "All" and to_date == "All":
					filter_condition = " and year(report.{0}) between '2015' and '{1}' ".format(review_month,date_time.strftime("%Y"))
				elif from_date != "All" and to_date != "All":
					filter_condition = " and year(report.{0}) in ('{1}') and month(report.{0}) in ('{2}') ".format(review_month,from_date, to_date)
				elif from_date == "All" and to_date != "All":
					filter_condition = " and year(report.{0}) between '2015' and '{2}' and month(report.{0}) in ('{1}') ".format(review_month,to_date, date_time.strftime("%Y"))
				else:
					filter_condition = " and year(report.{0}) in ('{1}') and month(report.{0}) between '1' and '12' ".format(review_month,from_date)
			else:
				filter_condition = " and year(report.{0}) in ('{1}') and month(report.{0}) in ('{2}') ".format(review_month,date_time.strftime("%Y"), int(date_time.strftime("%m")))
			result = filter_condition
		except:
			print(traceback.format_exc())
			pass
		return result
	
	def kra_previous_records(session_data):
		result = 0
		try:
			date_range_condition = kra_year_month_query(session_data, "P")
			if session_data['emp_type'] in ['ADMIN','TA','TBH','TBHR']:
				modified_month = "and year(inp.review_for_month) = {} and month(inp.review_for_month) = {}".format(session_data['kra_year_selected'], session_data['kra_month_selected'])
			else:
				previous_month = (datetime.strptime(session_data['db_date'], "%Y-%m-%d").month) - 1
				if previous_month == 0:
					previous_year = (datetime.strptime(session_data['db_date'], "%Y-%m-%d").year) - 1
					modified_month = "and year(inp.review_for_month) = {} and month(inp.review_for_month) = 12".format(previous_year)
				else:
					current_year = datetime.strptime(session_data['db_date'], "%Y-%m-%d").year
					modified_month = "and year(inp.review_for_month) = {} and month(inp.review_for_month) = {}".format(current_year, previous_month)

			query = """
			select emp_tbl.employee_id, emp_tbl.employee_name, report.lead_rating, report.manager_rating, report.business_head_rating, report.achieved_rating, inp.lead_rating, inp.manager_rating, inp.business_head_rating, inp.ques_ans_id, date_format(report.review_date, '%d-%b-%Y') from kra_summary_report as report
			inner join employees_info as emp_tbl on report.kra_for_employee_id = emp_tbl.employee_id
			inner join kra_input as inp on report.kra_for_employee_id = inp.kra_for_employee_id
			inner join kra_question_answer as qa on inp.ques_ans_id = qa.ques_ans_id
			where report.kra_for_employee_id in ({0}) {1} {2};
			""".format(session_data['kra_user_id'], date_range_condition, modified_month)
			result = get_dict_results(query)
		except:
			print(traceback.format_exc())
			pass
		return result
	
	def indian_datetime_format(session_data):
		return datetime.strptime(session_data['datetime_format'], "%Y-%m-%d %H:%M:%S")
	
	def get_log_report(form_data, session_data, data):
		global datetime, db_test
		result = 0
		try:
			crnt_dt = datetime.now()
			zero_t = datetime.strptime("00:00:00", "%H:%M:%S")
			date_range_condition = log_year_month_query(form_data, session_data)
			if form_data.get('project_selected') == "All":
				prj_condition = ""
			else:
				prj_id = 0
				prj_name = str(form_data['project_selected'])
				for prj, prj_val in data['employee_projects'].items():
					if str(prj) == prj_name:
						prj_id = prj_val['project_id']
						break
				prj_condition = " and emp.project_id in ('{}')".format(prj_id)
			if form_data.get('log_user_selected') == "All":
				emp_condition = ""
			else:
				user_id = str(form_data['log_user_selected'].split("_")[-1])
				for user_data in data['project_user_data']['All']:
					if str(user_data[1]) == user_id:
						user_id = user_data[0].split(' - ')[-1]
						break
				emp_condition = " and user_id in ('{}')".format(user_id)
			query = """
			SELECT date_format(log.log_date, "%d_%b_%Y") as Date, log.system_name as SystemName, emp.wiss_employee_id as `EmpID`, emp.employee_name as Employee, desig.desig_short as `Designation`, prj.project_short_name as Project, log.log_on as `Log In`, log.log_off as `Log Off`, IF(time(log.log_off) = "00:00:00","00:00:00",timediff(log.log_off,log.log_on))  as `Time Diff`, log.idle_hours as `Idle Hours`  FROM `system_log_info` as log   
			INNER JOIN `employees_info` as emp on emp.wiss_employee_id = log.user_id
			inner join `designation_info` as desig on desig.designation_id = emp.designation_id
			inner join `projects_info` as prj on prj.project_id = emp.project_id
			where {} {} {} and emp.status = "Active"
			group by log.log_date, log.log_on
			ORDER by log.log_date desc, log.log_on asc, emp.employee_name asc ;
			""".format(date_range_condition, prj_condition, emp_condition)
			summary_data = get_dict_log_results(query)

			log_user_sum = {"Total":0,"Active":0,"Inactive":0}
			tot_list = []
			act_list = []
			inact_list = []
			new_sum_list = []
			new_sum_dict = {}
			lout_dict = {}

			for ind_no, sep_data in enumerate(summary_data):
				id_date = "{}_{}".format(sep_data['EmpID'], sep_data['Date'])
				new_sum = dict()
				new_sum['Date'] = sep_data['Date']
				new_sum['SystemName'] = sep_data['SystemName']
				new_sum['EmpID'] = sep_data['EmpID']
				new_sum['Employee'] = sep_data['Employee']
				new_sum['Designation'] = sep_data['Designation']
				new_sum['Project'] = sep_data['Project']
				new_sum['Log In'] = sep_data['Log In']
				new_sum['Log Off'] = sep_data['Log Off']

				############################################### Seperate Work ###############################################
				if new_sum_dict.get(id_date, 0) == 0:
					new_sum_dict[id_date] = {}
					new_sum_dict[id_date]['index'] = ind_no
					new_sum_dict[id_date]['wiss_id'] = sep_data['EmpID']
					new_sum_dict[id_date]['previous_logoff'] = sep_data['Log Off']
					new_sum_dict[id_date]['previous_login'] = sep_data['Log In']
				else:
					if form_data.get('log_user_selected') != "All":
						if "{}".format(new_sum_dict[id_date]['previous_logoff']) not in ['0:00:00', '00:00:00']:
							new_sum['Log Off'] = sep_data['Log Off']
							new_sum_dict[id_date]['index'] = ind_no
						else:
							new_sum_list[int(new_sum_dict[id_date]['index'])]['Log Off'] = sep_data['Log In']
							new_sum_list[int(new_sum_dict[id_date]['index'])]['Worked Hrs'] = sep_data['Log In'] - new_sum_list[int(new_sum_dict[id_date]['index'])]['Log In']
							if new_sum_dict[id_date]['wiss_id'] == new_sum_list[int(new_sum_dict[id_date]['index'])]['EmpID']:
								new_sum_dict[id_date]['index']+=1
							new_sum_dict[id_date]['index'] = ind_no
					else:
						if "{}".format(new_sum_dict[id_date]['previous_logoff']) not in ['0:00:00', '00:00:00']:
							new_sum['Log Off'] = sep_data['Log Off']
							new_sum_dict[id_date]['index'] = ind_no
						else:
							new_sum_list[int(new_sum_dict[id_date]['index'])]['Log Off'] = sep_data['Log In']
							new_sum_list[int(new_sum_dict[id_date]['index'])]['Worked Hrs'] = sep_data['Log In'] - new_sum_list[int(new_sum_dict[id_date]['index'])]['Log In']
							if new_sum_dict[id_date]['wiss_id'] == new_sum_list[int(new_sum_dict[id_date]['index'])]['EmpID']:
								new_sum_dict[id_date]['index']+=1
							new_sum_dict[id_date]['index'] = ind_no
				############################################### Seperate Work ###############################################

				if "{}".format(sep_data['Log Off']) in ['0:00:00', '00:00:00']:
					new_sum['Worked Hrs'] = time_delta(zero_t)
					if sep_data['EmpID'] not in act_list:
						act_list.append(sep_data['EmpID'])
					if sep_data['EmpID'] in inact_list:
						inact_list.remove(sep_data['EmpID'])
				else:
					new_sum['Worked Hrs'] = sep_data['Log Off'] - sep_data['Log In']
					if sep_data['EmpID'] in act_list:
						act_list.remove(sep_data['EmpID'])
					if sep_data['EmpID'] not in inact_list:
						inact_list.append(sep_data['EmpID'])

				if lout_dict.get(id_date, 0) == 0:
					if sep_data['EmpID'] not in tot_list:
						tot_list.append(sep_data['EmpID'])
					lout_dict[id_date] = {}
					new_sum['Idle Hrs'] = time_delta(zero_t)
					lout_dict[id_date]['Pre_lout'] = sep_data['Log Off']
				else:
					if "{}".format(lout_dict[id_date]['Pre_lout']) in ['0:00:00', '00:00:00']:
						new_sum['Idle Hrs'] = time_delta(zero_t)
					else:
						new_sum['Idle Hrs'] = sep_data['Log In'] - lout_dict[id_date]['Pre_lout']
				lout_dict[id_date]['Pre_lout'] = sep_data['Log Off']
				new_sum_dict[id_date]['previous_logoff'] = sep_data['Log Off']
				new_sum_list.append(new_sum)

			log_user_sum['Total'] = len(tot_list)
			log_user_sum['Active'] = len(act_list)
			log_user_sum['Inactive'] = len(inact_list)
			result = [new_sum_list,log_user_sum]
		except:
			print(traceback.format_exc())
			pass
		return result
	
	def time_delta(data):
		return timedelta(hours=data.hour,minutes=data.minute,seconds=data.second)
	
	def get_log_summary_report(form_data, session_data, data):
		global datetime
		result = 0
		try:
			crnt_dt = datetime.now()
			crnt_ts = datetime.strftime(crnt_dt, "%H:%M:%S")
			crnt_tdt = datetime.strptime(crnt_ts, "%H:%M:%S")
			shift_st = datetime.strptime("10:00:00", "%H:%M:%S")
			shift_et = datetime.strptime("19:00:00", "%H:%M:%S")
			zero_t = datetime.strptime("00:00:00", "%H:%M:%S")
			tot_list = []
			act_list = []
			inact_list = []
			report_result = get_log_report(form_data, session_data, data)
			summary_data = report_result[0]
			log_user_sum = report_result[1]
			new_sum_list = []
			new_sum_dict = {}
			lout_dict = {}
			for sep_data in summary_data:
				id_date = "{}_{}".format(sep_data['EmpID'], sep_data['Date'])
				new_sum = dict()
				new_sum['Date'] = sep_data['Date']
				new_sum['EmpID'] = sep_data['EmpID']
				new_sum['Employee'] = sep_data['Employee']
				new_sum['Designation'] = sep_data['Designation']
				new_sum['Project'] = sep_data['Project']
				new_sum['Log In'] = sep_data['Log In']
				new_sum['Log Off'] = sep_data['Log Off']
				if new_sum_dict.get(id_date, 0) == 0:
					if sep_data['EmpID'] not in tot_list:
						tot_list.append(sep_data['EmpID'])
					new_sum_dict[id_date] = {}
					lout_dict[id_date] = {}
					if "{}".format(sep_data['Log Off']) in ['0:00:00', '00:00:00']:
						log_et = "{}".format(sep_data['Log In'])
						if sep_data['EmpID'] not in act_list:
							act_list.append(sep_data['EmpID'])
					else:
						log_et = "{}".format(sep_data['Log Off'])
						if sep_data['EmpID'] not in inact_list:
							inact_list.append(sep_data['EmpID'])
					log_et = datetime.strptime(log_et, "%H:%M:%S")
					hours_logged = time_delta(log_et) - sep_data['Log In']
					new_sum['Total Hrs'] = hours_logged
					hrs_wrk = time_delta(log_et) - sep_data['Log In']
					new_sum['Worked'] = hrs_wrk
					new_sum['Idle Hrs'] = time_delta(zero_t)
					new_sum['#Log'] = 1
					log_st = datetime.strptime("{}".format(sep_data['Log In']), "%H:%M:%S")
					new_sum['In Time'] = '+ {}'.format(shift_st-log_st) if shift_st >= log_st else '- {}'.format(log_st - shift_st)
					new_sum['Out Time'] = '+ {}'.format(log_et-shift_et) if log_et >= shift_et else '- {}'.format(shift_et - log_et)
					lout_dict[id_date]['Pre_lout'] = sep_data['Log Off']
					new_sum_dict[id_date] = new_sum
					new_sum_list.append(new_sum)
				else:
					list_index = list(new_sum_dict.keys()).index(id_date)
					exist_dict = new_sum_list[list_index]
					if "{}".format(sep_data['Log Off']) in ['0:00:00', '00:00:00']:
						if "{}".format(lout_dict[id_date]['Pre_lout']) in ['0:00:00', '00:00:00']:
							idle_hrs = exist_dict['Idle Hrs'] + time_delta(zero_t)
							hrs_idle = time_delta(zero_t)
						else:
							idle_hrs = exist_dict['Idle Hrs'] + (sep_data['Log In'] - exist_dict['Log Off'])
							hrs_idle = sep_data['Log In'] - exist_dict['Log Off']
						if "{}".format(exist_dict['Log Off']) in ['0:00:00', '00:00:00']:
							hrs_wrk = exist_dict['Worked'] + (sep_data['Log In'] - exist_dict['Log In']) - hrs_idle
						else:
							hrs_wrk = exist_dict['Worked'] + (sep_data['Log In'] - exist_dict['Log Off']) - hrs_idle
						log_et = "{}".format(sep_data['Log In'])
						if sep_data['EmpID'] not in act_list:
							act_list.append(sep_data['EmpID'])
						if sep_data['EmpID'] in inact_list:
							inact_list.remove(sep_data['EmpID'])
					else:
						if "{}".format(lout_dict[id_date]['Pre_lout']) in ['0:00:00', '00:00:00']:
							idle_hrs = exist_dict['Idle Hrs'] + time_delta(zero_t)
							hrs_idle = sep_data['Log In'] - exist_dict['Log Off']
						else:
							idle_hrs = exist_dict['Idle Hrs'] + (sep_data['Log In'] - exist_dict['Log Off'])
							hrs_idle = time_delta(zero_t)
						if "{}".format(exist_dict['Log Off']) in ['0:00:00', '00:00:00']:
							hrs_wrk = exist_dict['Worked'] + (sep_data['Log In'] - exist_dict['Log In']) + (sep_data['Log Off'] - sep_data['Log In'])
						else:
							hrs_wrk = exist_dict['Worked'] + (sep_data['Log Off'] - sep_data['Log In']) + hrs_idle
						log_et = "{}".format(sep_data['Log Off'])
						if sep_data['EmpID'] in act_list:
							act_list.remove(sep_data['EmpID'])
						if sep_data['EmpID'] not in inact_list:
							inact_list.append(sep_data['EmpID'])
					log_et = datetime.strptime(log_et, "%H:%M:%S")
					new_sum['Log In'] = exist_dict['Log In']
					new_sum['Log Off'] = time_delta(log_et)
					hours_logged = time_delta(log_et) - exist_dict['Log In']
					new_sum['Total Hrs'] = hours_logged
					new_sum['Worked'] = hrs_wrk
					new_sum['Idle Hrs'] = idle_hrs
					new_sum['#Log'] = exist_dict['#Log']+1
					new_sum['In Time'] = exist_dict['In Time']
					new_sum['Out Time'] = '+ {}'.format(log_et-shift_et) if log_et >= shift_et else '- {}'.format(shift_et - log_et)
					lout_dict[id_date]['Pre_lout'] = sep_data['Log Off']
					new_sum_dict[id_date] = new_sum
					new_sum_list[list_index] = new_sum
			log_user_sum['Total'] = len(tot_list)
			log_user_sum['Active'] = len(act_list)
			log_user_sum['Inactive'] = len(inact_list)
			result = [new_sum_list,log_user_sum]
		except:
			print(traceback.format_exc())
			pass
		return result
	
	def log_year_month_query(form_data, session_data):
		result = 0
		try:
			from_date = form_data['log_from_date']
			to_date = form_data['log_to_date']
			date_time = indian_datetime_format(session_data)
			from_date = datetime.strptime(from_date, "%d-%m-%Y").strftime("%Y-%m-%d") if from_date != "" else date_time.strftime("%Y-%m-%d")
			to_date = datetime.strptime(to_date, "%d-%m-%Y").strftime("%Y-%m-%d") if to_date != "" else date_time.strftime("%Y-%m-%d")
			result = " log.log_date between '{}' and '{}' ".format(from_date, to_date)
		except:
			print(traceback.format_exc())
			pass
		return result

	def get_user_from_id(project, process, user, data, key, session_data):
		result = 0
		process = 'All' if process == "" else process
		try:
			user_name = ""
			if project != "All" and process != "All" and user != "All":
				for user_data in data['project_user_data'][project][process]:
					if str(user_data[1]) == str(user):
						user_name = user_data[0]
						break
			elif user != "All" and project != "All" or process != "All":
				if project == "All" and process == "All":
					for prj_val in data['project_user_data'].values():
						for prcs_val in prj_val.values():
							for user_data in prcs_val:
								if str(user_data[1]) == str(user):
									user_name = user_data[0]
									break
				elif project == "All" and process != "All":
					for prj_val in data['project_user_data'].values():
						for user_data in prj_val[process]:
							if str(user_data[1]) == str(user):
								user_name = user_data[0]
								break
				elif project != "All" and process == "All":
					for prcs_val in data['project_user_data'][project].values():
						for user_data in prcs_val:
							if str(user_data[1]) == str(user):
								user_name = user_data[0]
								break
			data['{}_projectname_selected'.format(key)] = project
			session_data['{}_projectname_selected'.format(key)] = project
			data['{}_processname_selected'.format(key)] = process
			session_data['{}_processname_selected'.format(key)] = process
			data['{}_username_selected'.format(key)] = user_name
			session_data['{}_username_selected'.format(key)] = user_name
			result = data
		except:
			print(traceback.format_exc())
			pass
		return result

	def get_dict_log_results(query):
		result = 0
		try:
			try:
				log_test = connect(host="3.21.6.232", user="db_root", password="^^Wi$$$$ROOT$$2022^^", database="wissend_db", port=3306)
				# log_test = connect(host="localhost", user="root", password="", database="wissend_db", port=3306)
				# log_cursor = db_test.cursor()
				log_dict_cursor = log_test.cursor(dictionary=True)
				print("\n********** Connected to Database **********\n")
			except Error as conn_err:
				if conn_err.errno == errorcode.ER_BAD_DB_ERROR:
					print("\n********** Database table does not exist **********\n")
				elif conn_err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
					print("\n********** User or Password Credentials Error **********\n")
				else:
					print("\n********** {conn_err} **********\n")
					print("\n********** Database Connection Error **********\n")
			log_dict_cursor.execute(query)
			result = log_dict_cursor.fetchall()
			log_dict_cursor.close()
		except:
			print(traceback.format_exc())
		finally:
			return result

	def emp_entry_report(selected_entry_date):
		result = 0
		try:
			# current_date = selected_entry_date.strftime("%Y-%m-%d")
			entry_date = '= "{}"'.format(selected_entry_date)

			query = """
			SELECT business_head_tbl.employee_name AS 'Business Head', employees_info.wiss_employee_id AS `Wissend ID`,employees_info.employee_name AS `Employee Name`,projects_info.project_name AS `Project Name`, COALESCE(tbl.Hours,0)+COALESCE(tb.Quality,0) AS Status,COALESCE(tbl.pth,0)+COALESCE(tb.qh,0) AS Hours, COALESCE(tbl.ptm,0)+COALESCE(tb.qm,0) AS Minutes FROM employees_info 
			LEFT JOIN (SELECT dpi.employee_id, SUM(dpi.hours_worked) AS Hours, SUM(dpi.hours) AS pth, SUM(dpi.minutes) AS ptm FROM daily_productivity_info AS dpi WHERE dpi.production_date {0} GROUP BY dpi.employee_id) AS tbl ON tbl.employee_id = employees_info.employee_id 
			LEFT JOIN (SELECT qi.quality_user_id, SUM(qi.quality_hours) AS Quality , SUM(qi.hours) AS qh, SUM(qi.minutes) AS qm FROM quality_info AS qi WHERE qi.entry_date {0} GROUP BY qi.quality_user_id) AS tb ON tb.`quality_user_id` = employees_info.employee_id 
			INNER JOIN employee_process_info AS epi ON epi.employee_id = employees_info.employee_id 
			INNER JOIN projects_info ON projects_info.project_id = employees_info.project_id 
            INNER JOIN project_process_info as prj_prcs_tbl on projects_info.project_id = prj_prcs_tbl.project_id
			INNER JOIN `employees_info` as business_head_tbl on prj_prcs_tbl.business_head_id = business_head_tbl.employee_id
			WHERE employees_info.status = 'Active' AND epi.status = 'Active' AND employees_info.employee_type_id NOT IN (1,10) and employees_info.wiss_employee_id NOT IN ("WFL0001","WFL0008") GROUP BY employees_info.employee_id ORDER BY business_head_tbl.employee_name, projects_info.project_name,employees_info.employee_name;
			""".format(entry_date)
			result = get_dict_results(query)
		except:
			print(traceback.format_exc())
			pass
		return result

	def insert_attendance(employee_data, json_data):
		result = employee_data
		try:
			ist = timezone('Asia/Calcutta')
			crnt_time = datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S")
			if json_data.get('log_on',0) != 0 and json_data.get('log_off',0) != 0:
				if json_data['log_on'] == "Success" and json_data['log_off'] != "Success":
					query = """
					INSERT INTO `attendance_tracker` (attendance_date, employee_id, in_time) VALUES ('{}','{}','{}');
					""".format(employee_data['db_date'], employee_data['employee_id'], crnt_time)
					employee_data['log_on_status'] = "Success"
					employee_data['log_off_status'] = "Yet to submit"
				else:
					query = """
					UPDATE `attendance_tracker` set out_time='{}' WHERE attendance_date='{}' and employee_id = '{}'; 
					""".format(crnt_time, employee_data['db_date'], employee_data['employee_id'])
					employee_data['log_on_status'] = "Success"
					employee_data['log_off_status'] = "Success"
			list_cursor = database_reconnection()
			list_cursor.execute(query)
			db_test.commit()
			result = employee_data
		except:
			print(traceback.format_exc())
			pass
		return result

	def attendance_year_month_query(form_data, session_data):
		result = 0
		try:
			from_date = form_data['attd_from_date']
			to_date = form_data['attd_to_date']
			date_time = indian_datetime_format(session_data)
			from_date = datetime.strptime(from_date, "%d-%m-%Y").strftime("%Y-%m-%d") if from_date != "" else date_time.strftime("%Y-%m-%d")
			to_date = datetime.strptime(to_date, "%d-%m-%Y").strftime("%Y-%m-%d") if to_date != "" else date_time.strftime("%Y-%m-%d")
			if session_data['emp_type'] in ['ADMIN','TA']:
				result = (" attd_track.attendance_date between '{}' and '{}' group by attd_track.attendance_date,emp_name.wiss_employee_id order by attd_track.in_time desc".format(from_date, to_date), " att.attendance_date between '{}' and '{}'".format(from_date, to_date))
			elif session_data['emp_type'] in ['TLR','TMR','TL','TM', 'TBHR', 'TBH']:
				result = (" attd_track.attendance_date between '{}' and '{}' and emp_prj.project_id in ({}) group by attd_track.attendance_date,emp_name.wiss_employee_id order by attd_track.in_time desc".format(from_date, to_date, session_data['team_projects']), " att.attendance_date between '{}' and '{}' and pro_info.project_id in ({})".format(from_date, to_date, session_data['team_projects']))
			else:
				result = (" attd_track.attendance_date between '{}' and '{}' and emp_name.employee_id = {} group by attd_track.attendance_date,emp_name.wiss_employee_id order by attd_track.in_time desc".format(from_date, to_date, session_data['employee_id']), "")
		except:
			print(traceback.format_exc())
			pass
		return result
	
	def report_attendance(form_data, session_data):
		result = []
		try:
			if form_data.get('attd_from_date',0) != 0 and form_data.get('attd_to_date',0) != 0:
				date_range_condition = attendance_year_month_query(form_data, session_data)
				#################################### Only Login Query ####################################
				att_report_query = """
				SELECT date_format(attd_track.attendance_date, "%d-%b-%y") as `Date`, emp_name.wiss_employee_id as `Employee ID`, emp_name.employee_name as `Employee Name`, emp_prj.project_name as `Project`, emp_bh.employee_name as `Business Head`, date_format(attd_track.in_time, "%d-%b %H:%i:%S") as `Log On Time`, date_format(attd_track.out_time, "%d-%b %H:%i:%S") as `Log Off Time`,IF(time(attd_track.out_time) = "00:00:00","00:00:00", timediff(attd_track.out_time,attd_track.in_time)) as `Log Hours`,IF(timediff(attd_track.out_time,attd_track.in_time)<"09:00:00",timediff(time("09:00:00"),timediff(attd_track.out_time,attd_track.in_time)),"00:00:00") as `Short Fall` , CASE WHEN timediff(attd_track.out_time,attd_track.in_time) < "04:30:00" THEN "A" WHEN timediff(attd_track.out_time,attd_track.in_time) >= "08:55:00" THEN "P" WHEN timediff(attd_track.out_time,attd_track.in_time) > "04:30:00" AND timediff(attd_track.out_time,attd_track.in_time) < "08:55:00" THEN "HD" ELSE "A" END as `Status` FROM `attendance_tracker` as attd_track
                                INNER JOIN employees_info as emp_name on emp_name.employee_id = attd_track.employee_id
                                INNER JOIN project_process_info as emp_prj_prcs on emp_prj_prcs.project_id = emp_name.project_id
                                INNER JOIN projects_info as emp_prj on emp_prj.project_id = emp_prj_prcs.project_id
                                INNER JOIN employees_info as emp_bh on emp_bh.employee_id = emp_prj_prcs.business_head_id WHERE {};
				""".format(date_range_condition[0])
				dict_cursor = database_reconnection(cur="dict")
				dict_cursor.execute(att_report_query)
				att_report_result = dict_cursor.fetchall()

				#################################### Only Login Query ####################################
				if session_data['emp_type'] in ["ADMIN", 'TA', 'TLR','TMR','TL','TM', 'TBHR', 'TBH']:
					if session_data['emp_type'] in ["ADMIN", 'TA']:
						where_condition = f"WHERE (NOT EXISTS (SELECT att.in_time FROM `attendance_tracker` as att where emp_in.employee_id = att.employee_id and {date_range_condition[1]} group by att.attendance_date and att.employee_id)) and emp_in.status = 'Active' GROUP by emp_in.wiss_employee_id"
					else:
						where_condition = f"WHERE (NOT EXISTS (SELECT att.in_time FROM `attendance_tracker` as att where emp_in.employee_id = att.employee_id and {date_range_condition[1]} group by att.attendance_date and att.employee_id)) and emp_in.status = 'Active' and emp_in.project_id in ({session_data['team_projects']}) GROUP by emp_in.wiss_employee_id"
					att_notquery = """
						SELECT  emp_in.wiss_employee_id as "Employee ID", emp_in.employee_name as "Employee Name", pro_info.project_name as `Project`, business_head_tbl.employee_name AS 'Business Head', "" as "Log On Time", "" as "Log Off Time", "00:00:00" as "Log Hours" FROM `employees_info` as emp_in
						INNER JOIN projects_info as pro_info on pro_info.project_id = emp_in.project_id 
						INNER JOIN project_process_info as prj_prcs_tbl on pro_info.project_id = prj_prcs_tbl.project_id
						INNER JOIN `employees_info` as business_head_tbl on prj_prcs_tbl.business_head_id = business_head_tbl.employee_id {};
						""".format(where_condition)

					dict_cursor = database_reconnection(cur="dict")
					dict_cursor.execute(att_notquery)
					att_notlogin_result = dict_cursor.fetchall()
					result = [att_report_result, att_notlogin_result]
				else:
					result = [att_report_result]
		except:
			print(traceback.format_exc())
			pass
		return result
	def leave_status_pickup(session_data):
		result = []
		# report_result = []
		try:
			print(session_data)
			employee_id = session_data['employee_id']
			emp_type_id = session_data['emp_type']
			print(type(emp_type_id))
			print(employee_id)
			print(emp_type_id)
			if str(emp_type_id) in ('TA','ADMIN'):
				print('Yes')
				att_status_query = f"""SELECT leave_requests.`apply_date`,leave_requests.`apply_type`,leave_requests.`from_date`,	leave_requests.`to_date`,leave_requests.`num_days`,leave_requests.`num_hours`,leave_requests.`status`,leave_requests.`reason`,leave_requests.`reporting_id_1`,leave_requests.`reporting_id_2`,leave_requests.`approver_id`,employees_info.	wiss_employee_id,employees_info.employee_name FROM leave_requests
				INNER JOIN employees_info ON employees_info.employee_id = leave_requests.employee_id
				WHERE leave_requests.modified_status = 'N' AND month(leave_requests.`apply_date`) = month('{session_data['db_date']}') AND year(leave_requests.`apply_date`) = year('{session_data['db_date']}')"""
			else:
				att_status_query = f"""SELECT leave_requests.`apply_date`,leave_requests.`apply_type`,leave_requests.`from_date`,leave_requests.`to_date`,leave_requests.`num_days`,leave_requests.`num_hours`,leave_requests.`status`,leave_requests.`reason`,leave_requests.`reporting_id_1`,leave_requests.`reporting_id_2`,leave_requests.`approver_id`,employees_info.wiss_employee_id,employees_info.employee_name FROM leave_requests
				INNER JOIN employees_info ON employees_info.employee_id = leave_requests.employee_id
				WHERE (leave_requests.employee_id = {employee_id} OR leave_requests.reporting_id_1 = {employee_id} OR leave_requests.reporting_id_2 = {employee_id}) AND leave_requests.modified_status = 'N' AND month(leave_requests.`apply_date`) = month('{session_data['db_date']}') AND year(leave_requests.`apply_date`) = year('{session_data['db_date']}')"""
			reporting_query = f"""SELECT emp_tbl.employee_name,emp_tbl.wiss_employee_id,rep_tbl1.employee_name as reporting_1,rep_tbl1.	employee_id as rep_emp_id1,rep_tbl1.wiss_employee_id as wiss_report_id_1,rep_tbl2.employee_name as reporting_2,rep_tbl2.employee_id AS rep_emp_id2,rep_tbl2.wiss_employee_id as wiss_report_id_2,lv_trc.casual_leave as CL,lv_trc.sick_leave as SL,lv_trc.permission,lv_trc.loss_of_pay as LOP,lv_trc.on_duty AS od,lv_trc.spl_cat_leave AS scl FROM leave_tracker AS lv_trc 
				INNER JOIN employees_info as emp_tbl ON emp_tbl.employee_id = lv_trc.employee_id
				INNER JOIN employees_info AS rep_tbl1 ON rep_tbl1.employee_id = lv_trc.reporting_id_1
				INNER JOIN employees_info AS rep_tbl2 ON rep_tbl2.employee_id = lv_trc.reporting_id_2
				WHERE lv_trc.employee_id = {employee_id} AND emp_tbl.status = 'Active' AND month(lv_trc.updated_date) = month('{session_data['db_date']}') AND year(lv_trc.updated_date) = year('{session_data['db_date']}')"""
			dict_cursor = database_reconnection(cur="dict")
			dict_cursor.execute(att_status_query)
			leave_result = dict_cursor.fetchall()
			dict_cursor = database_reconnection(cur="dict")
			dict_cursor.execute(reporting_query)
			report_result = dict_cursor.fetchall()
			if report_result != []:
				result = [leave_result, report_result[0]]
			else:
				result = [leave_result, report_result]
		except:
			print(traceback.format_exc())
			pass
		return result

	def leave_calculation(employee_id,num_days,permission_hours,apply_date,apply_type):
		leave_select_query = f"""SELECT `casual_leave`, `sick_leave`, `permission`, `spl_cat_leave`, `loss_of_pay`, `on_duty` FROM `leave_tracker` WHERE `employee_id` = "{employee_id}" AND month(`updated_date`)= month('{apply_date}') AND year(`updated_date`)=year('{apply_date}')"""
		dict_cursor = database_reconnection(cur="dict")
		dict_cursor.execute(leave_select_query)
		leave_result = dict_cursor.fetchall()
		if leave_result != []:
			leave_result_data = leave_result[0]
			update_query = ''
			if apply_type == 'CL':
				num_cl = float(leave_result_data['casual_leave']) - float(num_days)
				update_query = f"""UPDATE `leave_tracker` SET `casual_leave` = "{num_cl}" WHERE `employee_id` = "{employee_id}" AND month(`updated_date`)= month('{apply_date}') AND year(`updated_date`)=year('{apply_date}')"""
			elif apply_type == 'SL':
				num_sl = float(leave_result_data['sick_leave']) - float(num_days)
				update_query = f"""UPDATE `leave_tracker` SET `sick_leave` = "{num_sl}" WHERE `employee_id` = "{employee_id}" AND month(`updated_date`)= month('{apply_date}') AND year(`updated_date`)=year('{apply_date}')"""
			elif apply_type == 'LOP':
				num_lop = float(leave_result_data['loss_of_pay']) + float(num_days)
				update_query = f"""UPDATE `leave_tracker` SET `loss_of_pay` = "{num_lop}" WHERE `employee_id` = "{employee_id}" AND month(`updated_date`)= month('{apply_date}') AND year(`updated_date`)=year('{apply_date}')"""
			elif apply_type == 'OD':
				num_onduty = float(leave_result_data['on_duty']) + float(num_days)
				update_query = f"""UPDATE `leave_tracker` SET `on_duty` = "{num_onduty}" WHERE `employee_id` = "{employee_id}" AND month(`updated_date`)= month('{apply_date}') AND year(`updated_date`)=year('{apply_date}')"""
			elif apply_type == 'P':
				num_permission = float(leave_result_data['permission']) - float(permission_hours)
				update_query = f"""UPDATE `leave_tracker` SET `permission` = "{num_permission}" WHERE `employee_id` = "{employee_id}" AND month(`updated_date`)= month('{apply_date}') AND year(`updated_date`)=year('{apply_date}')"""
			if update_query != '':
				dict_cursor = database_reconnection(cur="dict")
				dict_cursor.execute(update_query)
				db_test.commit()

	def leave_insert(form_data,session_data):
		result = []
		check_exist_data = 0
		try:
			employee_id = session_data['employee_id']
			apply_date = session_data['db_date']
			num_days = 0
			permission_hours = 0
			check_val = 0
			od_date = 0
			if form_data.get('apply_type',0) != 0:
				check_val = 1
				from_session = form_data['from_session_type']
				if form_data.get('to_session_type',0) != 0:
					to_session = form_data['to_session_type']
				else:
					to_session = from_session
				apply_type = form_data['apply_type'].upper()
				if apply_type == 'CL' or apply_type == 'SCL' or apply_type == 'SL':
					from_date_next = datetime.strptime(str(form_data['leave_from_date']).replace('/','-'), "%m-%d-%Y")
					to_date_next = datetime.strptime(str(form_data['leave_to_date']).replace('/','-'), "%m-%d-%Y")
					from_date = from_date_next.strftime("%Y-%m-%d")
					to_date = to_date_next.strftime("%Y-%m-%d")
					num_days = form_data['num_of_days']
				elif apply_type == 'P':
					from_date_next = datetime.strptime(str(form_data['permission_date']).replace('/','-'), "%m-%d-%Y")
					to_date_next = datetime.strptime(str(form_data['permission_date']).replace('/','-'), "%m-%d-%Y")
					from_date = from_date_next.strftime("%Y-%m-%d")
					to_date = to_date_next.strftime("%Y-%m-%d")
					permission_hours = form_data['perm_hours_type']
				elif apply_type == 'OD':
					from_date_next = datetime.strptime(str(form_data['od_date']).replace('/','-'), "%m-%d-%Y")
					to_date_next = datetime.strptime(str(form_data['od_date']).replace('/','-'), "%m-%d-%Y")
					from_date = from_date_next.strftime("%Y-%m-%d")
					to_date = to_date_next.strftime("%Y-%m-%d")
			else:
				from_date = form_data['from_date']
				to_date = form_data['to_date']
				empid_query = f"""SELECT `employee_id` FROM `employees_info` WHERE `wiss_employee_id` = '{form_data['emp_id']}';"""
				dict_cursor = database_reconnection(cur="dict")
				dict_cursor.execute(empid_query)
				empid_result = dict_cursor.fetchall()
				if empid_result != []:
					employee_id = empid_result[0]['employee_id']
				apply_type = form_data['type'].upper()
			if check_val == 1:
				leave_select_query = f"""SELECT `apply_id`,`from_session`,`to_session` FROM `leave_requests` WHERE `apply_type` = '{form_data['apply_type']}' AND `from_date` = '{from_date}' AND `from_session` = '{from_session}' AND `to_date` = '{to_date}' AND `to_session` = '{to_session}' AND `employee_id` = {employee_id}"""
				dict_cursor = database_reconnection(cur="dict")
				dict_cursor.execute(leave_select_query)
				leave_result = dict_cursor.fetchall()
				if leave_result != []:
					check_exist_data = 1
					modified_status = 'Y'
					from_sess_type = leave_result[0]['from_session']
					if leave_result[0].get('to_session',0) != 0:
						to_sess_type = leave_result[0]['to_session']
					else:
						to_sess_type = from_sess_type
					apply_id = leave_result[0]['apply_id']
				else:
					modified_status = 'N'
					from_sess_type = form_data['from_session_type']
					if form_data.get('to_session',0) != 0:
						to_sess_type = form_data['to_session_type']
					else:
						to_sess_type = from_sess_type
				insert_query = f"""INSERT INTO `leave_requests`(`employee_id`, `apply_date`, `apply_type`, `from_date`, `from_session`, `to_date`, `to_session`, `reason`, `reporting_id_1`, `reporting_id_2`, `modified_status`, `num_days`,`num_hours`)VALUES ({employee_id},'{apply_date}','{apply_type}','{from_date}','{from_sess_type}','{to_date}','{to_sess_type}','{form_data['leave_reason']}','{form_data['reporting1']}','{form_data['reporting2']}','{modified_status}','{num_days}','{permission_hours}')"""
			else:
				reportid_query = f"""SELECT `apply_id`,`reporting_id_1`,`reporting_id_2`,`from_session`,`to_session`,`status` FROM `leave_requests` WHERE `apply_type` = '{apply_type}' AND `from_date` = '{from_date}' AND `to_date` = '{to_date}' AND `employee_id` = {employee_id} AND `modified_status`='N'"""
				dict_cursor = database_reconnection(cur="dict")
				dict_cursor.execute(reportid_query)
				report_result = dict_cursor.fetchall()
				if report_result != []:
					apply_id = report_result[0]['apply_id']
					leave_status = report_result[0]['status']
					if leave_status == form_data['final_confirm']:
						check_exist_data = 1
					else:
						update_query = f"UPDATE `leave_requests` SET `modified_status`='Y' WHERE `apply_id` = {apply_id}"
						dict_cursor.execute(update_query)
						db_test.commit()
					report1_id = report_result[0]['reporting_id_1']
					report2_id = report_result[0]['reporting_id_2']
					from_sess_type = report_result[0]['from_session']
					if report_result[0].get('to_session',0) != 0:
						to_sess_type = report_result[0]['to_session']
					else:
						to_sess_type = report_result[0]['from_session']
				else:
					from_sess_type = "NULL"
					to_sess_type = "NULL"
				insert_query = f"""INSERT INTO `leave_requests`(`employee_id`, `apply_date`, `apply_type`, `from_date`, `to_date`, `reason`, `modified_status`, `num_days`,`num_hours`,`status`,`approver_id`,`reporting_id_1`,`reporting_id_2`,`from_session`,`to_session`)VALUES ({employee_id},'{form_data['apply_date']}','{apply_type}','{from_date}','{to_date}','{form_data['reason']}','N','{form_data['#_days']}','{form_data['#_hours']}','{form_data['final_confirm']}','{session_data['employee_id']}','{report1_id}','{report2_id}','{from_sess_type}','{to_sess_type}')"""
			print(insert_query)
			if check_exist_data == 0:
				dict_cursor = database_reconnection(cur="dict")
				dict_cursor.execute(insert_query)
				db_test.commit()
			if form_data.get('final_confirm',0) != 0:
				if form_data['final_confirm'].lower() == 'approved':
					num_days = form_data['#_days']
					permission_hours = form_data['#_hours']
					if check_exist_data == 0:
						leave_calculation(employee_id,num_days,permission_hours,apply_date,apply_type)
			result = leave_status_pickup(session_data)
		except:
			print(traceback.format_exc())
			pass
		return result
	
	def shift_status_pickup(session):
		data_set = {}
		try:
			data_set = {"projects":[],"all_shifts":[],"project_new_users":[],'project_shifts':[]}
			project_dict = []
			proj_list = []
			emp_type = session['emp_type']
			emp_id  = session['employee_id']
			if emp_type not in ['ADMIN','TA']:
				shift_query = f'''SELECT shift_assign_records.`employee_id`, shift_assign_records.`designation_id`, shift_assign_records.`project_id`, shift_assign_records.`manager_id`, shift_assign_records.`bh_head_id`, shift_assign_records.`shift_id`,projects_info.project_name,employees_info.wiss_employee_id,employees_info.employee_name,designation_info.designation,shift_timings_info.shift_name,shift_timings_info.shift_time_in,shift_timings_info.shift_time_off,CONCAT(
					DATE_FORMAT(shift_time_in, '%h:%i %p'),
					' - ',
					DATE_FORMAT(shift_time_off, '%h:%i %p')
				) as shift_timings
				FROM `shift_assign_records`
				INNER JOIN projects_info ON projects_info.project_id = shift_assign_records.project_id
				INNER JOIN employees_info ON employees_info.employee_id = shift_assign_records.employee_id
				INNER JOIN designation_info ON designation_info.designation_id = shift_assign_records.designation_id
				INNER JOIN shift_timings_info ON shift_timings_info.shift_id = shift_assign_records.shift_id
				WHERE (shift_assign_records.manager_id = {emp_id} OR shift_assign_records.bh_head_id = {emp_id}) AND projects_info.project_status = "Active" and shift_assign_records.is_updated = "N" order by projects_info.project_name,employees_info.employee_name'''
			else:
				shift_query = '''SELECT shift_assign_records.`employee_id`, shift_assign_records.`designation_id`, shift_assign_records.`project_id`, shift_assign_records.`manager_id`, shift_assign_records.`bh_head_id`, shift_assign_records.`shift_id`,projects_info.project_name,employees_info.wiss_employee_id,employees_info.employee_name,designation_info.designation,shift_timings_info.shift_name,shift_timings_info.shift_time_in,shift_timings_info.shift_time_off,CONCAT(
					DATE_FORMAT(shift_time_in, '%h:%i %p'),
					' - ',
					DATE_FORMAT(shift_time_off, '%h:%i %p')
				) as shift_timings
				FROM `shift_assign_records`
				INNER JOIN projects_info ON projects_info.project_id = shift_assign_records.project_id
				INNER JOIN employees_info ON employees_info.employee_id = shift_assign_records.employee_id
				INNER JOIN designation_info ON designation_info.designation_id = shift_assign_records.designation_id
				INNER JOIN shift_timings_info ON shift_timings_info.shift_id = shift_assign_records.shift_id
				WHERE projects_info.project_status = "Active" and shift_assign_records.is_updated = "N" order by projects_info.project_name,employees_info.employee_name'''
			dict_cursor = database_reconnection(cur="dict")
			dict_cursor.execute(shift_query)
			shift_result = dict_cursor.fetchall()
			new_set_dict = {}
			if shift_result != []:
				proj_shift_dict = {}
				for each_status_result in shift_result:
					user_dict = {
								"employee_name":str(each_status_result["employee_name"]),
								"employee_id":str(each_status_result["employee_id"]),
								"wiss_employee_id":str(each_status_result["wiss_employee_id"]),
								"designation":str(each_status_result["designation"]),
								"designation_id":str(each_status_result["designation_id"]),
								"shift_name":str(each_status_result["shift_name"]),
								"shift_id":str(each_status_result["shift_id"]),
								"shift_timings":str(each_status_result["shift_timings"]),
								}
					project_name = each_status_result['project_name']
					if project_name not in new_set_dict:
						user_list = []
						user_list.append(user_dict)
						new_set_dict[project_name] = {
							"project_name":str(each_status_result['project_name']),
							"project_id":str(each_status_result['project_id']),
							"manager_id":each_status_result['manager_id'],
							"head_id":each_status_result['bh_head_id'],
							"users":[],
							"project_shifts":[]
						}
						# data_set['projects'].append(data_set_dict)
						proj_list.append(str(each_status_result['project_id']))
					new_set_dict[project_name]['users'].append(user_dict)
					if project_name not in proj_shift_dict:
						proj_shift_dict[project_name]= {each_status_result["shift_name"]:{"shift_name":str(each_status_result["shift_name"]),"shift_id":str(each_status_result["shift_id"]),"shift_timings":str(each_status_result["shift_timings"])}}
						new_set_dict[project_name]['project_shifts'].append({"shift_name":str(each_status_result["shift_name"]),"shift_id":str(each_status_result["shift_id"]),"shift_timings":str(each_status_result["shift_timings"])})
					else:
						if each_status_result["shift_name"] not in proj_shift_dict[project_name]:
							proj_shift_dict[project_name][each_status_result["shift_name"]] = {"shift_name":str(each_status_result["shift_name"]),"shift_id":str(each_status_result["shift_id"]),"shift_timings":str(each_status_result["shift_timings"])}
							new_set_dict[project_name]['project_shifts'].append({"shift_name":str(each_status_result["shift_name"]),"shift_id":str(each_status_result["shift_id"]),"shift_timings":str(each_status_result["shift_timings"])})
					# if data_set['projects'] == []:
						
					# 	user_list = []
					# 	print("aaaa",each_status_result['shift_timings'], each_status_result["employee_name"])
					# 	user_list.append(user_dict)
					# 	data_set_dict = {
					# 		"project_name":str(each_status_result['project_name']),
					# 		"project_id":str(each_status_result['project_id']),
					# 		"manager_id":each_status_result['manager_id'],
					# 		"head_id":each_status_result['bh_head_id'],
					# 		"users":user_list,
					# 		"project_shifts":[{"shift_name":str(each_status_result["shift_name"]),"shift_id":str(each_status_result["shift_id"]),"shift_timings":str(each_status_result["shift_timings"])}]
					# 	}
					# 	data_set['projects'].append(data_set_dict)
					# 	proj_list.append(str(each_status_result['project_id']))
					# else:
					# 	for data_project in data_set["projects"]:
					# 		if data_project['project_name'] == str(each_status_result['project_name']):
					# 			print("\n",data_project['project_name'])
					# 			data_project['users'].append(user_dict)
					# 			for proj_shift in data_project['project_shifts']:
					# 				if str(proj_shift['shift_id']) != str(each_status_result["shift_id"]):
					# 					print(data_project['project_name'], proj_shift, str(each_status_result))
					# 					print("matched")
					# 					data_project['project_shifts'].append({"shift_name":str(each_status_result["shift_name"]),"shift_id":str(each_status_result["shift_id"]),"shift_timings":str(each_status_result["shift_timings"])})

					# break
			data_set = {"projects":list(new_set_dict.values())}
			all_shift_query = """
			SELECT 
				shift_name as shift_name,
				shift_id as shift_id,
				CONCAT(
					DATE_FORMAT(shift_time_in, '%h:%i %p'),
					' - ',
					DATE_FORMAT(shift_time_off, '%h:%i %p')
				) as shift_timings 
			FROM 
				`shift_timings_info`;
			"""
			dict_cursor = database_reconnection(cur="dict")
			dict_cursor.execute(all_shift_query)
			shift_result = dict_cursor.fetchall()
			if shift_result != []:
				data_set['all_shifts']=shift_result
			if emp_type not in ['ADMIN','TA']:
				new_user_query = """
				SELECT DISTINCT ei.employee_name, ei.employee_id, ei.wiss_employee_id, di.designation_id as newuser_desig_id, di.designation as newuser_desig
				FROM employee_process_info as epi
				LEFT JOIN shift_assign_records as sar ON epi.employee_id = sar.employee_id
				INNER JOIN employees_info as ei on ei.employee_id = epi.employee_id
                INNER JOIN designation_info as di on ei.designation_id = di.designation_id
				WHERE sar.employee_id IS NULL and epi.project_id in ({}) and epi.status = "Active" and ei.wiss_employee_id not in ("Vellai","Raj")
				ORDER BY ei.employee_name;
				""".format(",".join(proj_list))
			else:
				new_user_query = """
				SELECT DISTINCT ei.employee_name, ei.employee_id, ei.wiss_employee_id, di.designation_id as newuser_desig_id, di.designation as newuser_desig
				FROM employee_process_info as epi
				LEFT JOIN shift_assign_records as sar ON epi.employee_id = sar.employee_id
				INNER JOIN employees_info as ei on ei.employee_id = epi.employee_id
                INNER JOIN designation_info as di on ei.designation_id = di.designation_id
				WHERE sar.employee_id IS NULL and epi.status = "Active" and ei.wiss_employee_id not in ("Vellai","Raj")
				ORDER BY ei.employee_name;
				"""
			dict_cursor = database_reconnection(cur="dict")
			dict_cursor.execute(new_user_query)
			shift_result = dict_cursor.fetchall()
			if shift_result != []:
				data_set['project_new_users'] = shift_result
		except:
			print(traceback.format_exc())
		return data_set
	
	def shift_project_user_insert(session_data, form_data):
		shift_result = []
		try:
			db_date = session_data['db_date']
			project_id = ""
			manager_id = ""
			head_id = ""
			shift_id = ""
			shift_update = ""
			shift_check = 0
			update_check = 0
			selected_shift_data = []
			all_shift_data = []
			emp_list = []
			for data_k, data_v in form_data.items():
				if project_id == "":
					project_id = form_data['assign_project_id']
				elif manager_id == "":
					manager_id = form_data['manager_id']
				elif head_id == "":
					head_id = form_data['head_id']
				elif shift_id == "":
					shift_id = form_data['shift_timing_id'].split("|")[-1]
					# shift_update = form_data['shift_timing_id'].split("|")[0]
				if project_id != "":
					if "shift_timing_for_users" in data_k  and data_v != "":
						shift_update = data_v.split("|")[0]
						user_data = data_k.split("_")
						user_id = user_data[-2]
						desig_id = user_data[-1]
						if shift_update == "U":
							emp_list.append(user_id)
							if shift_id == "":
								shift_id = data_v.split("|")[1]
							update_check = 1
							selected_shift_data.append("('{}',{},{},{},{},{},{},{})".format(db_date,user_id,desig_id,project_id,manager_id,head_id,shift_id,session_data['employee_id']))
						all_shift_data.append("('{}',{},{},{},{},{},{},{})".format(db_date,user_id,desig_id,project_id,manager_id,head_id,shift_id,session_data['employee_id']))
			if update_check == 0:
				query_input = ", ".join(all_shift_data)
				select_query = ""
			else:
				select_query = " employee_id in ({}) AND ".format(", ".join(emp_list))
				query_input = ", ".join(selected_shift_data)
			get_shift_query = """
			SELECT * FROM `shift_assign_records`
			WHERE
				{}	project_id = {} and is_updated = "N";
			""".format(select_query,project_id)
			dict_cursor = database_reconnection(cur="dict")
			dict_cursor.execute(get_shift_query)
			shift_results = dict_cursor.fetchall()
			# if shift_results != []:
				# for shift_result in shift_results:
				# 	if str(shift_result['shift_id']) == str(shift_id) and shift_result['is_updated'] == "N":
				# 		shift_check = 1
			if shift_check == 0:
				update_exist_status_query = """
				UPDATE `shift_assign_records`
				SET
					is_updated = "Y"
				WHERE
					{} project_id = {};
				""".format(select_query,project_id)
				dict_cursor = database_reconnection(cur="dict")
				dict_cursor.execute(update_exist_status_query)
				db_test.commit()
				insert_shift_query = """
				INSERT INTO
					`shift_assign_records`
					(`updated_date`, `employee_id`, `designation_id`, `project_id`, `manager_id`, `bh_head_id`, `shift_id`, `id_modified`)
				VALUES
					{};
				""".format(query_input)
				dict_cursor = database_reconnection(cur="dict")
				dict_cursor.execute(insert_shift_query)
				shift_result = dict_cursor.fetchall()
				db_test.commit()
		except:
			print(traceback.format_exc())
		return shift_result
	
	def shift_new_user_insert(session_data, form_data):
		shift_result = []
		try:
			db_date = session_data['db_date']
			emp_id  = session_data['employee_id']
			user_list_desi = []
			desi_list = []
			project_id = 0
			shift_id = 0
			if form_data.get("multiselect_username_all_all",0) != 0:
				if form_data.get("newuser_project_id",0) != 0:
					pro_split = str(form_data["newuser_project_id"]).strip().split("|")
					if pro_split != []:
						project_id = pro_split[0]
						manager_id = pro_split[1]
						buss_head_id = pro_split[2]
				if form_data.get("newuser_selection_shift_id",0) != 0:
					shift_id = form_data["newuser_selection_shift_id"]
				for each_key,each_val in form_data.items():
					if str(each_key).lower().strip().startswith("multiselect_username"):
						if str(each_val).strip() != 'all':
							desi_split = str(each_key).strip().split("_")
							if desi_split != []:
								user_list_desi.append("('{}', '{}', '{}', {}, {}, {}, {}, 'N', '{}')".format(db_date,desi_split[-2],desi_split[-1],project_id,manager_id,buss_head_id,shift_id,emp_id))
			else:
				if form_data.get("newuser_project_id",0) != 0:
					pro_split = str(form_data["newuser_project_id"]).strip().split("|")
					if pro_split != []:
						project_id = pro_split[0]
						manager_id = pro_split[1]
						buss_head_id = pro_split[2]
				if form_data.get("newuser_selection_shift_id",0) != 0:
					shift_id = form_data["newuser_selection_shift_id"]
				for each_key,each_val in form_data.items():
					if str(each_key).lower().strip().startswith("multiselect_username"):
						if str(each_val).strip() != 'all':
							desi_split = str(each_key).strip().split("_")
							if desi_split != []:
								user_list_desi.append("('{}', '{}', '{}', {}, {}, {}, {}, 'N', '{}')".format(db_date,desi_split[-2],desi_split[-1],project_id,manager_id,buss_head_id,shift_id,emp_id))
								# user_list_desi.append([db_date,desi_split[-2],desi_split[-1],project_id,manager_id,buss_head_id,shift_id,'N',shift_id])
			query_data = ",".join(user_list_desi)
			shift_assign_insert_query = """INSERT INTO `shift_assign_records`(`updated_date`, `employee_id`, `designation_id`, `project_id`, `manager_id`, `bh_head_id`, `shift_id`, `is_updated`, `id_modified`) VALUES {};""".format(query_data)
			dict_cursor = database_reconnection(cur="dict")
			dict_cursor.execute(shift_assign_insert_query)
			shift_result = dict_cursor.fetchall()
			db_test.commit()
		except:
			print(traceback.format_exc())
		return shift_result