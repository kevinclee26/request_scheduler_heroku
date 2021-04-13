from apscheduler.schedulers.blocking import BlockingScheduler
import fetch

sched=BlockingScheduler()
fetch_freq_mins=1
process_freq_mins=15

@sched.scheduled_job('interval', minutes=fetch_freq_mins)
def data(): 
	fetch.get_bike_data()
# 	fetch.all_scooter_data()
# 	# fetch.weather_data()
	print(f'This job is run every {fetch_freq_mins} minutes.')
	return None

# @sched.scheduled_job('internal', minutes=process_freq_mins)
# def process_logs():
# 	fetch.process_log()
# 	print(f'This job is run every {process_freq_mins} minutes.')
# 	return None

# # @sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
# # def scheduled_job():
# #     print('This job is run every weekday at 5pm.')

sched.start()