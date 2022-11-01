import dsi_util
import unix
import os
import pandas as pd
import datetime
import dsi_release
import sys
import traceback

class dsi_release_scheduler(object):
    """
    This class provides a release scheuler implementation.
    Scheduler provide too high level functionalities
      1) It uses PM_RELEASE_ACTIVITIES to schedule release activities
      2) Executes release activities as per schedule.

    Name : Vishal Sharma (01/08/2019) - Initial Version
    """
    def __init__(self,log_level=0, DRY_RUN=0):
        self.SCHEDULE_TIME='12'  ## Time of day when release activities will be scheduled.
        self.ACTIVITY_CREATION_BUFFER=15  ## Time of day when release activities will be scheduled.
        self.BUFFER_DAYS=0      ## Buffer Days before first activity for release starts
        self.LOG_LEVEL = log_level
        self.DRY_RUN = DRY_RUN
        self.unix = unix.unix(log_level=self.LOG_LEVEL)
        self.util = dsi_util.dsi_util(log_level=log_level)

        RELEASE_CONFIG_FILE='/abinitio/dev/data/config/release_configurations.cfg'
        self.release_config = self.util.get_config(RELEASE_CONFIG_FILE)
        self.RELEASE_ACTIVITY_TEMPLATE='/home/ai/Release/python/Release_Activity_Template.htm'
        self.RELEASE_HEADER_TEMPLATE='/home/ai/Release/python/Release_Header_Template.htm'

    def __repr__(self):
        return ('Class {} : Performs basic release scheduling functionalities.').format(self.__class__.__name__)

    def f_error(self, err_msg,email_to=''):
        self.log('An Error has occured.',0)

        msg = {}

        if email_to == '' :
            if 'RELEASE_TEAM_TO' in self.release_config :
                email_to = self.release_config['RELEASE_TEAM_TO']
            else :
                email_to = 'Ranjeeth.Kyatham@npd.com;Jingming.Ma@npd.com;Vishal.Sharma@npd.com'

        msg['Subject'] = "ERROR : dsi_release_scheduler (Release Activity Process)"
        msg['From'] = 'Release_Team'

        msg['To'] = email_to

        msg['Body'] = "An error occured in dsi_release_scheduler.py. Please investigate. \n {} ".format(err_msg)

        self.util.f_send_email(msg)
        self.util.f_error(err_msg,log=0)


    def log(self, data, level):
        """
        Writes details to log based on log level

        Attribute
        :param str[] data : data to be written to log
        :return: None
        :raises: None
        """
        data = "{} : {}".format(datetime.datetime.now(),data)
        self.util.log(data,level)

    def f_check_release_schedule(self):
        """
        This function checkes release schedule for any planned release. If any it will schedule release activities.

        Attribute
        :param : None
        :return: None
        :raises: None
        """
        self.log ("Checking PM_RELEASE_SCHEDULES for any planned release.",0)

        sql = """
        WITH RELEASES AS
        (
        SELECT RELEASE,RELEASE_PHASE, RELEASE_DATE,HOT_FIX_FLAG FROM ETL_RPT.PM_RELEASE_SCHEDULES
           WHERE RELEASE_DATE BETWEEN SYSDATE AND SYSDATE + {}
        UNION
        SELECT RELEASE,'MNA' RELEASE_PHASE, RELEASE_DATE,HOT_FIX_FLAG FROM ETL_RPT.PM_RELEASE_SCHEDULES
        WHERE RELEASE_DATE BETWEEN SYSDATE AND SYSDATE + {} AND RELEASE_PHASE = 'QA'
        ),
        RELEASE_TIME AS
        (
        SELECT ENVIRONMENT,TRUNC(MIN(START_TIME)/24  - {}) START_TIME FROM ETL_RPT.PM_RELEASE_ACTIVITIES GROUP BY ENVIRONMENT
        )
        SELECT
          RELEASE, RELEASE_PHASE,to_char(RELEASE_DATE,'YYYYMMDD') RELEASE_DATE,HOT_FIX_FLAG,TO_CHAR(RELEASE_DATE + START_TIME,'YYYY-MM-DD HH24:MI') ACTIVITY_SCHEDULE
        FROM  RELEASES A, RELEASE_TIME B
        WHERE
        B.ENVIRONMENT = A.RELEASE_PHASE
        and to_char(SYSDATE,'YYYY-MM-DD') <=  TO_CHAR(RELEASE_DATE + START_TIME,'YYYY-MM-DD') and  to_char(SYSDATE,'HH24') = '{}'
         """.format(self.ACTIVITY_CREATION_BUFFER,self.ACTIVITY_CREATION_BUFFER,self.BUFFER_DAYS,self.SCHEDULE_TIME)

        df = self.util.run_sql(sql)

        if df.empty :
            self.log("No new release activitity scheduling is required",0)
        else :
            for idx,row in df.iterrows():
                self.log("Release {} to {} is due for Activitity scheduling.".format(row['RELEASE'],row['RELEASE_PHASE'],row['RELEASE_DATE']),0)

                self.f_create_tag_entry_for_release(row['RELEASE'],row['RELEASE_PHASE'])

                if  self.f_get_activities_details(row['RELEASE'],row['RELEASE_PHASE']) is None:
                         sql_h = """
                         select HOT_FIX_FLAG from ETL_RPT.PM_RELEASE_SCHEDULES WHERE RELEASE = '{}'
                          """.format(row['RELEASE'])
                         df_h = self.util.run_sql(sql_h)
                         hot_fix_f = df_h['HOT_FIX_FLAG'][0]

                         if hot_fix_f == 0 :  activities=self.f_create_release_activities(row['RELEASE'],row['RELEASE_PHASE'],row['RELEASE_DATE'])
                         elif hot_fix_f == 1 :  activities=self.f_create_release_activities_hotfix(row['RELEASE'],row['RELEASE_PHASE'],row['RELEASE_DATE'])
                         else : self.log (" Checking HOT_FIX_FLAG in ETL_RPT.PM_RELEASE_SCHEDULES table, it is either 0 for regular schedule, or 1 for HOT_FIX.",0)
                else :
                      self.log("Activities have been already created for for release.",0)

    def f_create_tag_entry_for_release(self,release,env):
        """
        This function checkes if tag is defined. If not it will create tag entry.

        Attribute
        :param : None
        :return: None
        :raises: None
        """
        self.log (" Checking release tag entry. If not defined, creates it.",0)

        if not self.f_chcek_release_tag_entry(release,env) :
            self.log (" Tag entry does not exits for release. Creating it.",0)

            if env == 'MNA' :
                 new_env = 'QA'

                 sql = """
                  INSERT INTO ETL_RPT.PM_RELEASE_TAGS
                    (RELEASE_TAG,RELEASE,TAG_VALID_FROM,TAG_VALID_TO,STATUS,TAG_TYPE,DESCRIPTION,ADDED_DATE,ADDED_USER)
                    SELECT Y.NEW_TAG || '.'||'{0}',RELEASE,RELEASE_DATE - 10,RELEASE_DATE,'Active','{0}',Y.NEW_TAG,SYSDATE,'Release Scheduler'
                    FROM
                       ETL_RPT.PM_RELEASE_SCHEDULES X,
                   (SELECT
                       SUBSTR(RELEASE_TAG,0,INSTR(RELEASE_TAG,'_',-1)) ||
                        TO_CHAR(REPLACE(SUBSTR(RELEASE_TAG,INSTR(RELEASE_TAG,'_',-1)+1),'.'||'{0}','') + 1)  NEW_TAG,
                        RELEASE_TAG
                    FROM
                        ETL_RPT.PM_RELEASE_TAGS
                    WHERE
                        RELEASE =
                            (SELECT MAX(RELEASE) FROM
                                ETL_RPT.PM_RELEASE_SCHEDULES WHERE RELEASE < '{1}' AND
                                RELEASE_PHASE = '{0}' and HOT_FIX_FLAG=0
                   )) Y
                   WHERE
                   RELEASE = '{1}'
                   """.format(new_env,release)
            else :
                new_env = env

                sql = """
                   INSERT INTO ETL_RPT.PM_RELEASE_TAGS
                  (RELEASE_TAG,RELEASE,TAG_VALID_FROM,TAG_VALID_TO,STATUS,TAG_TYPE,DESCRIPTION,ADDED_DATE,ADDED_USER)            
                  SELECT Y.NEW_TAG || '.'||'{0}' TAG,RELEASE,RELEASE_DATE - 10,RELEASE_DATE, 'Active', '{0}',
                          Y.NEW_TAG,SYSDATE, 'Release Scheduler'
                  FROM
                        ETL_RPT.PM_RELEASE_SCHEDULES X,
                   (SELECT
                         SUBSTR(RELEASE_TAG,0,INSTR(RELEASE_TAG,'.')-1 )  NEW_TAG
                     FROM
                         ETL_RPT.PM_RELEASE_TAGS
                     WHERE
                         RELEASE = (SELECT MAX(RELEASE) FROM ETL_RPT.PM_RELEASE_SCHEDULES WHERE NEXT_PHASE_RELEASE = '{1}')
                   ) Y
               WHERE
                   RELEASE = '{1}'
                """.format(new_env,release)

            self.util.run_insert_sql(sql)
            return 0
        else :
            self.log (" Tag entry exits for release.",0)
            return 0

    def f_chcek_release_tag_entry(self,release,env):
        """
        This function checkes if tag is created or not.

        Attribute
        :param : None
        :return: None
        :raises: None
        """
        self.log (" Checking release tag entry in ETL_RPT.PM_RELEASE_TAGS.",0)
        sql = "select count(*) TAGS from ETL_RPT.PM_RELEASE_TAGS where release = '{}'".format(release)

        df = self.util.run_sql(sql)
        total_tags = df['TAGS'][0]

        if total_tags == 0 :
            return False
        elif total_tags == 1 :
            return True
        else :
            self.f_error('Multiple tags have been defined for release {}. We should have only one entry in ETL_RPT.PM_RELEASE_TAGS table.')

    def f_create_release_activities(self,release,env,rel_date):
        """
        This function creates activities for planned release.

        Attribute
        :param : None
        :return: None
        :raises: None
        """
        self.log (" Creating release activities for {} in PM_RELEASE_ACTIVITY_STATUS for any planned release.",0)

        sql="""
        INSERT INTO ETL_RPT.PM_RELEASE_ACTIVITY_STATUS (RELEASE,RELEASE_ACTIVITY_ID,STATUS_NOTE,STATUS_DATE, PLANNED_START_TIME,STATUS)
        SELECT '{}',RELEASE_ACTIVITY_ID,RELEASE_ACTIVITY_NAME,SYSDATE,TO_DATE('{}','YYYYMMDD')  + START_TIME/24, 0
        FROM
            ETL_RPT.PM_RELEASE_ACTIVITIES
        WHERE ENVIRONMENT = '{}'
        """.format(release,rel_date,env)

        self.util.run_insert_sql(sql)
        self.log (" Pulling tag details for the release.",0)

        sql="""
        SELECT RELEASE_TAG FROM ETL_RPT.PM_RELEASE_TAGS WHERE RELEASE = '{}'
        """.format(release)

        df = self.util.run_sql(sql)
        RELEASE_TAG = df['RELEASE_TAG'][0]

        self.f_send_summary_email(release,env,rel_date,RELEASE_TAG)
    def f_create_release_activities_hotfix(self,release,env,rel_date):
        """
        This function creates activities for planned release.

        Attribute
        :param : None
        :return: None
        :raises: None
        """
        self.log (" Creating release activities for {} in PM_RELEASE_ACTIVITY_STATUS for any planned release.",0)

        sql="""
        INSERT INTO ETL_RPT.PM_RELEASE_ACTIVITY_STATUS (RELEASE,RELEASE_ACTIVITY_ID,STATUS_NOTE,STATUS_DATE,PLANNED_START_TIME,STATUS)
        SELECT '{}',RELEASE_ACTIVITY_ID,RELEASE_ACTIVITY_NAME,SYSDATE,TO_DATE('{}','YYYYMMDD')  + START_TIME/24, 2
        FROM
            ETL_RPT.PM_RELEASE_ACTIVITIES
        WHERE ENVIRONMENT = '{}' AND RELEASE_ACTIVITY_NAME in ('Release_Plan_DSI','Release_Plan','Release_Deploy')
        """.format(release,rel_date,env)

        self.util.run_insert_sql(sql)
        self.log (" Pulling tag details for the release.",0)

        sql="""
        SELECT RELEASE_TAG FROM ETL_RPT.PM_RELEASE_TAGS WHERE RELEASE = '{}'
        """.format(release)

        df = self.util.run_sql(sql)
        RELEASE_TAG = df['RELEASE_TAG'][0]

        self.f_send_summary_email(release,env,rel_date,RELEASE_TAG)

    def f_send_summary_email(self,release,env,rel_date,release_tag,email_to='',email_cc=''):
        """
        This function creates activities for planned release.

        Attribute
        :param : None
        :return: None
        :raises: None
        """
        self.log (" Finally trying to send email with Activity details.",0)

        act_details =  self.f_get_activities_details(release,env)

        if act_details is None :
            self.f_error(' There is problem creating activities for release {} to {}.Please review logs at {}'.format( release,env,self.release_config['RELEASE_LOG_DIR']))
        else :
            msg = {}
            msg1 = open(self.RELEASE_ACTIVITY_TEMPLATE).read()
            msg1 = msg1.decode('utf-8')
            table1 = act_details.to_html(index = False).replace('<th>',"""<th style="font-family:'Calibri';font-size:12.0pt;background-color:'DodgerBlue">""").encode('utf-8')
            table1 = table1.replace('<td>',"""<td style="font-family:'Calibri';font-size:12.0pt">""")

            msg1 = msg1.replace('xxx_release_xxx',release.replace('QA',env))
            msg1 = msg1.replace('xxx_release_tag_xxx',release_tag)
            msg1 = msg1.replace('xxx_env_xxx',env)
            msg1 = msg1.replace('xxx_release_status_xxx','Activity Scheduling')

            act_message="DSI Release automation process has scheduled release activities for planned {} release {}. Please review the activities and their planned start time. If these need any change, please update ETL_RPT.PM_RELEASE_ACTIVITY_STATUS table. Release process will initiate these activities as per plan outlined.".format(env,release)
            msg1 = msg1.replace('xxx_message_xxx',act_message)
            msg1 = msg1.replace('xxx_release_activity_xxx',table1)

            msg['Subject'] = "{} Release Activities Scheduled (Please Review)".format(env, release)
            msg['From'] = 'Release_Team'

            if email_to == '' :
                if 'RELEASE_TEAM_TO' in self.release_config :
                    email_to = self.release_config['RELEASE_TEAM_TO']
                else :
                    email_to = 'Ranjeeth.Kyatham@npd.com;Jingming.Ma@npd.com;Vishal.Sharma@npd.com'

            if email_cc == '':
                if 'RELEASE_TEAM_CC' in self.release_config :
                    msg['Cc'] = self.release_config['RELEASE_TEAM_CC']
            else :
                msg['Cc'] = email_cc

            msg['To'] =  email_to
            msg['Body'] = msg1

            self.log (" Finally trying to send email with Activity details to - {}.".format(msg['To']),0)

            self.util.f_send_email(msg)


    def f_get_activities_details(self,release,env):
        """
        This function creates activities for planned release.

        Attribute
        :param : None
        :return: None
        :raises: None
        """
        sql="""
        SELECT RELEASE_ACTIVITY_NAME, DESCRIPTION, TO_CHAR(PLANNED_START_TIME,'Dy Mon DD, YYYY HH12:MI AM') START_TIME, STATUS
        FROM
          ETL_RPT.PM_RELEASE_ACTIVITIES A,ETL_RPT.PM_RELEASE_ACTIVITY_STATUS B
        WHERE
           ENVIRONMENT = '{}' AND  RELEASE = '{}' AND  A.RELEASE_ACTIVITY_ID = B.RELEASE_ACTIVITY_ID
        ORDER BY RUN_ORDER
        """.format(env,release)

        df = self.util.run_sql(sql)

        if df.empty :
            return None
        else :
            return df

    def f_perform_release_activity(self) :
        """
        This function performs a release activity.
        """
        self.log ("Finding out details of release activities scheduled for executions.",0)

        activities=self.f_get_release_activity_for_this_hr()

        if activities is not None :
            for idx,row in activities.iterrows() :
                self.log("Processing Activitity : {}-{} for {} release to {}. eMail IDs : {} and CC_eMail_IDs : {}".format(row['ACTIVITY_ID'],row['ACTIVITY_NAME'], row['RELEASE'],row['ENVIRONMENT'],row['EMAIL_IDS'] ,row['CC_EMAIL_IDS']),0)
                if self.f_check_if_activity_can_be_run(row['ACTIVITY_ID'],row['ACTIVITY_NAME'],row['RELEASE'],row['ENVIRONMENT']):
                    self.f_execute_activity(row['ACTIVITY_ID'],row['ACTIVITY_NAME'],row['RELEASE'],
                                            row['ENVIRONMENT'],row['EMAIL_IDS'] ,row['CC_EMAIL_IDS'])
        else :
            self.log("There are no activities due for this hr.",0)


    def f_get_release_activity_for_this_hr(self) :
        """
        This function finds out activities which are due for this hr.
        """
        sql="""
            SELECT
                 A.RELEASE_ACTIVITY_ID ACTIVITY_ID,RELEASE,ENVIRONMENT, RELEASE_ACTIVITY_NAME ACTIVITY_NAME,B.RUN_ORDER,
                 B.EMAIL_IDS,B.CC_EMAIL_IDS
            FROM
                 ETL_RPT.PM_RELEASE_ACTIVITY_STATUS A, ETL_RPT.PM_RELEASE_ACTIVITIES B
            WHERE
                 TO_CHAR(PLANNED_START_TIME,'YYYYMMDD HH24') <= TO_CHAR(SYSDATE,'YYYYMMDD HH24') AND
                 A.RELEASE_ACTIVITY_ID = B.RELEASE_ACTIVITY_ID and STATUS = 0
            ORDER BY RUN_ORDER
        """
        df = self.util.run_sql(sql)

        if df.empty :
            return None
        else :
            return df

    def f_check_if_activity_can_be_run(self,act_id,activity,release,env) :
        """
        This function checks if all the previous activties for the group has completed. If Yes, then returns true else False
        """
        sql="""
            SELECT
                 A.RELEASE_ACTIVITY_ID ACTIVITY_ID,RELEASE,ENVIRONMENT, RELEASE_ACTIVITY_NAME ACTIVITY_NAME,B.RUN_ORDER,STATUS
            FROM
                 ETL_RPT.PM_RELEASE_ACTIVITY_STATUS A  ,ETL_RPT.PM_RELEASE_ACTIVITIES B
            WHERE
                 A.RELEASE_ACTIVITY_ID = B.RELEASE_ACTIVITY_ID and
                 RELEASE = '{}' and A.RELEASE_ACTIVITY_ID < {} and STATUS != 2 and ENVIRONMENT = '{}'
        """.format(release,act_id,env)

        df = self.util.run_sql(sql)

        if df.empty :
            return True
        else :
            msg = "Below activities for the release have not completed. Release can not complete without their completion.\n\n"
            self.log(msg,0)
            print df
            table1 = df.to_html(index = False).replace('<th>','<th style = "background-color: DodgerBlue">').encode('utf-8')
            msg = msg + """<style="font-size:10.0pt;font-family:'Calibr">""" + table1 + "</style>"

            self.f_send_pending_activity_email(release,env,msg)
            return False

    def f_send_pending_activity_email(self,release,env,in_msg) :
        """
        Send email with issue details to release_team.
        """
        msg1 = open(self.RELEASE_HEADER_TEMPLATE).read()
        msg1 = msg1.decode('utf-8')

        msg1 = msg1.replace('xxx_release_xxx',release.replace('QA',env))
        msg1 = msg1.replace('xxx_env_xxx',env)
        msg1 = msg1.replace('xxx_message_xxx',in_msg)

        self.f_error(msg1)

    def f_execute_activity(self,act_id,activity,release,env,email_to='',email_cc=''):
        """
        This function performs a release activity.
        """
        self.log ("="*80,0)
        self.log ("             Executing activities : {}.".format(activity),0)
        self.log ("="*80,0)

        if '-' in activity :
            act_name      = activity.split('-')[0].strip().upper().strip()
            act_iteration = activity.split('-')[1]
        else :
            act_name      = activity.upper().strip()
            act_iteration = 0

        if act_name == 'REMINDER' :
            self.f_process_reminder(act_id,activity,release,env,iteration=act_iteration,email_to=email_to,email_cc=email_cc)
        elif act_name == 'RELEASE_PLAN_DSI' :
            self.f_process_release_plan_dsi(act_id,activity,release,env,email_to=email_to,email_cc=email_cc,iteration=act_iteration)
        elif act_name == 'RELEASE_ODS_CHANGES' :
            self.f_process_send_ods_changes_summary(act_id,activity,release,env,iteration=act_iteration, email_to=email_to,email_cc=email_cc)
        elif act_name == 'RELEASE_DEPLOY' :
            self.f_process_release_deploy(act_id,activity,release,env,iteration=act_iteration,email_to=email_to,email_cc=email_cc)
        elif act_name == 'RELEASE_COMMIT' :
            self.f_process_release_commit(act_id,activity,release,env,iteration=act_iteration)
        elif act_name == 'SANITY' :
            self.f_process_release_sanity(act_id,activity,release,env,iteration=act_iteration,email_to=email_to,email_cc=email_cc)
        elif act_name == 'SANITY_STATUS' :
            self.f_process_release_sanity_status(act_id,activity,release,env,iteration=act_iteration,email_to=email_to,email_cc=email_cc)
        elif act_name == 'RELEASE_PLAN' :
            self.f_process_release_plan(act_id,activity,release,env,iteration=act_iteration,email_to=email_to,email_cc=email_cc)
        elif act_name == 'STOP_SCHEDULER' :
            self.f_process_stop_scheduler(act_id,activity,release,env,iteration=act_iteration,email_to=email_to,email_cc=email_cc,sent_email = 'Y')
        elif act_name == 'KILL_JOBS' :
            self.f_process_kill_jobs(act_id,activity,release,env,iteration=act_iteration,email_to=email_to,email_cc=email_cc)
        elif act_name == 'START_SCHEDULER' :
            self.f_process_start_schedulers(act_id,activity,release,env,iteration=act_iteration,email_to=email_to,email_cc=email_cc,sent_email = 'Y')
        elif act_name == 'STOP_CRON' :
            self.f_process_stop_crons(act_id,activity,release,env,iteration=act_iteration,email_to=email_to,email_cc=email_cc)
        elif act_name == 'START_CRON' :
            self.f_process_start_crons(act_id,activity,release,env,iteration=act_iteration,email_to=email_to,email_cc=email_cc)
        else :
            self.f_error("Invalid activity {} - ID({})defined for {} to {} in ETL_RPT.PM_RELEASE_ACTIVITY_STATUS. This is not supported. Please check.".format(activity,act_id,release,env))

        self.log ("Executing of activity completed.",0)

    def f_register_activity(self,act_id,release,status,env='') :
        """ Thsi function updates release activity with status."""
        if status == 'START' :
            sid=1
            date_update = ',ACTUAL_START_TIME = sysdate'
        elif status == 'END' :
            sid=2
            date_update = ',ACTUAL_END_TIME = sysdate'
        elif status == 'FAIL' :
            sid=-1
            date_update = ',ACTUAL_END_TIME = sysdate'
        else :
            self.error("Invalid Status value of "" passed. This is not supported.".format(status),0)

        self.log ("Updating status to {} for activty {} for release.".format(status,env,release),0)

        sql = """
            UPDATE ETL_RPT.PM_RELEASE_ACTIVITY_STATUS SET STATUS = {} {} WHERE RELEASE = '{}' AND RELEASE_ACTIVITY_ID = {}
        """.format(sid,date_update,release,act_id)

        self.util.run_insert_sql(sql)

    def f_process_reminder(self,act_id,activity,release,env,iteration=0,email_to='',email_cc=''):
        """
        This function performs a release activity.
        """
        self.log ("Release reminder for {} release {}.".format(env,release),0)
        self.log ("Param : act_id - {} activity - {} release - {} env - {} email_to - {} email_cc - {} iteration - {} ".format(act_id,activity,release,env,email_to,email_cc,iteration),0)

        rel_obj = dsi_release.dsi_release(release,env=env,log_level=self.LOG_LEVEL)

        self.f_register_activity(act_id,release,status='START',env=env)
        ret_code = rel_obj.f_release_initiation(email_to=email_to,email_cc=email_cc,iteration=iteration)

        if ret_code == 0 :
            self.f_register_activity(act_id,release,status='END',env=env)
        else :
            self.f_register_activity(act_id,release,status='FAIL',env=env)

    def f_process_release_plan(self,act_id,activity,release,env,email_to='',email_cc='',iteration=0):
        """
        This function performs a release activity.
        """
        self.log ("Performing Release Plan activity for {} release to {}.".format(release,env),0)
        self.log ("Param : act_id - {} activity - {} release - {} env - {} email_to - {} email_cc - {} iteration - {} ".format(act_id,activity,release,env,email_to,email_cc,iteration),0)

        rel_obj = dsi_release.dsi_release(release,env=env,log_level=self.LOG_LEVEL)

        self.f_register_activity(act_id,release,status='START',env=env)
        ret_code = rel_obj.f_release_ticket_summary(include_bug=0,email_to=email_to,email_cc=email_cc)

        if ret_code == 0 :
            self.f_register_activity(act_id,release,status='END',env=env)
        else :
            self.f_register_activity(act_id,release,status='FAIL',env=env)


    def f_process_release_plan_dsi(self,act_id,activity,release,env,email_to='',email_cc='',iteration=0):
        """
        This function performs a release activity.
        """
        self.log ("Performing Release Plan to DSI activity for {} release to {}.".format(release,env),0)
        self.log ("Param : act_id - {} activity - {} release - {} env - {} email_to - {} email_cc - {} iteration - {} ".format(act_id,activity,release,env,email_to,email_cc,iteration),0)

        rel_obj = dsi_release.dsi_release(release,env=env,log_level=self.LOG_LEVEL)

        self.f_register_activity(act_id,release,status='START',env=env)
        ret_code = rel_obj.f_release_ticket_summary(include_bug=1,email_to=email_to,email_cc=email_cc)

        if ret_code == 0 :
            self.f_register_activity(act_id,release,status='END',env=env)
        else :
            self.f_register_activity(act_id,release,status='FAIL',env=env)

    def f_process_release_deploy(self,act_id,activity,release,env,iteration=0,email_to='',email_cc=''):
        """
        This function performs a release activity.
        """
        self.log ("Performing Release deploy to {} for the release {} ".format(env,release),0)

        self.f_register_activity(act_id,release,status='START',env=env)

        rel_obj = dsi_release.dsi_release(release,env=env,log_level=self.LOG_LEVEL)

        if env == 'MNA' :
            self.log ("Performing DB deploy to {} for the release {} ".format(env,release),0)
            ret_code = rel_obj.f_perform_sql_release()
            if ret_code != 0 :
                self.f_register_activity(act_id,release,status='FAIL',env=env)
                self.f_error("DB Deploy for {} to {} has Failed. Please check logs for details.".format(release,env))

        if rel_obj.HOT_FIX_IND :
            self.log ("Executing FAST-TRACK Abinitio Release to {} for the release {} ".format(env,release),0)
            ret_code = rel_obj.f_build_HF_abinitio_release()
            self.f_perform_return_code_check(act_id,ret_code,release,env,activity='Abinitio Release')

            self.log ("Executing FAST-TRACK SVN Release to {} for the release {} ".format(env,release),0)
            ret_code = rel_obj.f_build_HF_svn_release()
            self.f_perform_return_code_check(act_id,ret_code,release,env,activity='SVN Release')
        else :
            self.log ("Executing Abinitio Release to {} for the release {} ".format(env,release),0)
            ret_code = rel_obj.f_build_abinitio_release()
            self.f_perform_return_code_check(act_id,ret_code,release,env,activity='Abinitio Release')

            self.log ("Executing SVN Release to {} for the release {} ".format(env,release),0)
            ret_code = rel_obj.f_build_svn_release()
            self.f_perform_return_code_check(act_id,ret_code,release,env,activity='SVN Release')

        rel_obj.f_generate_release_summary_report(email_to=email_to,email_cc=email_cc)

        self.f_register_activity(act_id,release,status='END',env=env)

    def f_perform_return_code_check(self,act_id,ret_code,release,env,activity=''):
        """
        This function checkes return code to ensure process completed sucessfully.
        """
        self.log ("act_id - {} ({} ) completed with ret_code - {}".format(act_id,activity,ret_code),0)
        if ret_code == 0 :
            return 0
        else :
            self.f_register_activity(act_id,release,status='FAIL',env=env)
            self.f_error("Release activity {} execution has failed. Please check log file for details.".format(activity))

    def f_process_send_ods_changes_summary(self,act_id,activity,release,env,iteration=0,email_to='',email_cc=''):
        """
        This function Send tickets with ODS changes to release team.
        """
        self.log ("Performing ODS dependecy check for tickets for {} to {} ".format(release,env),0)
        rel_obj = dsi_release.dsi_release(release,env=env,log_level=self.LOG_LEVEL)

        self.f_register_activity(act_id,release,status='START',env=env)

        ret_code = rel_obj.f_process_send_ods_changes_summary(email_to=email_to,email_cc=email_cc)

        if ret_code == 0 :
            self.f_register_activity(act_id,release,status='END',env=env)
        else :
            self.f_register_activity(act_id,release,status='FAIL',env=env)


    def f_process_release_ods_changes(self,act_id,activity,release,env,iteration=0):
        """
        This function performs ODS changes for the release.
        """
        self.log ("Performing DB deploy to {} for the release {} ".format(env,release),0)

        self.f_register_activity(act_id,release,status='START',env=env)

        rel_obj = dsi_release.dsi_release(release,env=env,log_level=self.LOG_LEVEL)
        ret_code = rel_obj.f_perform_sql_release()

        if ret_code == 0 :
            self.f_register_activity(act_id,release,status='END',env=env)
        else :
            self.f_register_activity(act_id,release,status='FAIL',env=env)

    def f_process_release_commit(self,act_id,activity,release,env,iteration=0):
        """
        This function performs a release activity.
        """
        self.log ("Commiting release and restarting Scheduler in {} for the release {} ".format(env,release),0)

        self.f_register_activity(act_id,release,status='START',env=env)
        rel_obj = dsi_release.dsi_release(release,env=env,log_level=self.LOG_LEVEL)

##        self.log ("Stopping Scheduler in {} for the release {} ".format(env,release),0)
##        ret_code = rel_obj.f_stop_schedulers_for_env()
##        self.f_perform_return_code_check(act_id,ret_code,release,env,activity='Scheduler Killing')

        self.log ("Changing links in {} for the release {} ".format(env,release),0)
        ret_code = rel_obj.f_change_release_links()
        self.f_perform_return_code_check(act_id,ret_code,release,env,activity='Link Change')

        ### self.log ("------Correcting permissions for .ksh and .py files in {} for the release {} ".format(env,release),0)
        ### ret_code1 = rel_obj.f_change_permissions_after_release()
        ### self.f_perform_return_code_check(act_id,ret_code1,release,env,activity='Set Permissions')

        self.log ("------Changing password in {} for the release {} ".format(env,release),0)
        ret_code2 = rel_obj.f_change_passwd_after_release()
        self.f_perform_return_code_check(act_id,ret_code2,release,env,activity='Password Change')

        ##self.log ("Starting Scheduler in {} for the release {} ".format(env,release),0)
        ##ret_code = rel_obj.f_start_schedulers_for_env()
        ##self.f_perform_return_code_check(act_id,ret_code,release,env,activity='Scheduler Start')

        self.f_register_activity(act_id,release,status='END',env=env)


    def f_process_stop_scheduler(self,act_id,activity,release,env,iteration=0,email_to='',email_cc='',sent_email='N'):
        """
        This function performs a release activity.
        """
        self.log ("Stopping scheduler instance in {} for the release {} ".format(env,release),0)

        self.f_register_activity(act_id,release,status='START',env=env)

        rel_obj = dsi_release.dsi_release(release,env=env,log_level=self.LOG_LEVEL)
        ret_code = rel_obj.f_stop_schedulers_for_env()

        if ret_code == 0 :
            self.f_register_activity(act_id,release,status='END',env=env)
            if sent_email == 'Y' :
                self.f_send_activty_status_email('SUCCESS',act_id,activity,release,env,iteration=0,email_to='',email_cc='')
        else :
            self.f_register_activity(act_id,release,status='FAIL',env=env)
            self.f_send_activty_status_email('FAILED',act_id,activity,release,env,iteration=0,email_to='',email_cc='')


    def f_process_change_links(self,act_id,activity,release,env,iteration=0):
        """
        This function performs a release activity.
        """
        self.log ("Changing link to release version in {} for the release {} ".format(env,release),0)

        self.f_register_activity(act_id,release,status='START',env=env)

        rel_obj = dsi_release.dsi_release(release,env=env,log_level=self.LOG_LEVEL)
        ret_code = rel_obj.f_change_release_links()

        if ret_code == 0 :
            self.f_register_activity(act_id,release,status='END',env=env)
        else :
            self.f_register_activity(act_id,release,status='FAIL',env=env)

    def f_process_start_schedulers(self,act_id,activity,release,env,iteration=0,email_to='',email_cc='',sent_email = 'Y'):
        self.log ("Starting Scheduler Instances in {} for the release {} ".format(env,release),0)

        self.f_register_activity(act_id,release,status='START',env=env)

        rel_obj = dsi_release.dsi_release(release,env=env,log_level=self.LOG_LEVEL)
        ret_code = rel_obj.f_start_schedulers_for_env()

        if ret_code == 0 :
            self.f_register_activity(act_id,release,status='END',env=env)
            if sent_email == 'Y' :
                self.f_send_activty_status_email('SUCCESS',act_id,activity,release,env,iteration=0,email_to='',email_cc='')
        else :
            self.f_register_activity(act_id,release,status='FAIL',env=env)
            if sent_email == 'Y' :
                self.f_send_activty_status_email('FAIL',act_id,activity,release,env,iteration=0,email_to='',email_cc='')

    def f_process_kill_jobs(self,act_id,activity,release,env,iteration=0,email_to='',email_cc=''):
        self.log ("Killing jobs in {} for the release {} ".format(env,release),0)

        self.f_register_activity(act_id,release,status='START',env=env)

        rel_obj = dsi_release.dsi_release(release,env=env,log_level=self.LOG_LEVEL)
        ret_code = rel_obj.f_kill_running_jobs()

        if ret_code == 0 :
            self.f_register_activity(act_id,release,status='END',env=env)
        else :
            self.f_register_activity(act_id,release,status='FAIL',env=env)

    def f_send_activty_status_email(self,status,act_id,activity,release,env,iteration=0,email_to='',email_cc=''):
        """
        This function send status email on activity
        """
        self.log ("Trying to send {} status email for activity ".format(status,activity),0)
        msg = {}
        msg1 = open(self.RELEASE_ACTIVITY_TEMPLATE).read()
        msg1 = msg1.decode('utf-8')
        msg1 = msg1.replace('xxx_release_xxx',release.replace('QA',env))
        msg1 = msg1.replace('xxx_release_tag_xxx',' ')
        msg1 = msg1.replace('xxx_env_xxx',env)
        msg1 = msg1.replace('xxx_release_status_xxx',activity + " : " + status)

        act_message="Release find below status for release activity.\n\n         {} :  {} ".format(activity,status)
        msg1 = msg1.replace('xxx_message_xxx',act_message)
        msg1 = msg1.replace('xxx_release_activity_xxx',' ')

        msg['Subject'] = "{} Release Activity {} : {} ".format(release,activity, status)
        msg['From'] = 'Release_Team'

        if email_to == '' :
            if 'RELEASE_TEAM_TO' in self.release_config :
                email_to = self.release_config['RELEASE_TEAM_TO']
            else :
                email_to = 'Ranjeeth.Kyatham@npd.com;Jingming.Ma@npd.com;Vishal.Sharma@npd.com'

        if email_cc == '':
            if 'RELEASE_TEAM_CC' in self.release_config :
                msg['Cc'] = self.release_config['RELEASE_TEAM_CC']
        else :
            msg['Cc'] = email_cc

        msg['To'] =  email_to
        msg['Body'] = msg1

        self.log (" Finally trying to send email with Activity details to - {}.".format(msg['To']),0)

        self.util.f_send_email(msg)


    def f_get_db_deploy_script(self,act_id,activity,release,env,iteration=0,email_to='',email_cc=''):
        """
        This function pulls DB scripts details so that they can be added to release deploy package.
        """
        self.log ("trying to DB Release deploy package to {}  for release {} to ".format(env,release),0)


    def f_process_release_sanity(self,act_id,activity,release,env,iteration=0,email_to='',email_cc=''):
        """
        This function tries to schedule sanity jobs for the release.
        """
        self.log ("Trying to schedule sanity jobs for the release {} to {}".format(release,env),0)

        self.f_register_activity(act_id,release,status='START',env=env)

        rel_obj = dsi_release.dsi_release(release,env=env,log_level=self.LOG_LEVEL)
        ret_code = rel_obj.f_schedulers_sanity_jobs_for_env()

        if ret_code == 0 :
            self.f_register_activity(act_id,release,status='END',env=env)
        else :
            self.f_register_activity(act_id,release,status='FAIL',env=env)

    def f_process_release_sanity_status(self,act_id,activity,release,env,iteration=0,email_to='',email_cc=''):
        """
        This function tries to schedule sanity jobs for the release.
        """
        self.log ("Trying to schedule sanity jobs for the release {} to {}".format(release,env),0)

        self.f_register_activity(act_id,release,status='START',env=env)

        rel_obj = dsi_release.dsi_release(release,env=env,log_level=self.LOG_LEVEL)
        ret_code = rel_obj.f_process_release_sanity_status(email_to='',email_cc='')

        sql = "select count(*) rec_count from ETL_MGR.ETL_JOB_LOG where RUN_USER = '{}' and status not in (2,10) and JOB_ID in (select JOB_ID from ETL_MGR.ETL_SANITY_FREQ)".format(rel_obj.RELEASE_TAG)
        rec_count = self.util.run_sql(sql,env)

        ## Update table to reschedule activity if there are any job that did not complete.
        self.log ("Total records with status other than completed : {} ".format(rec_count['REC_COUNT'][0]),0)

        if rec_count['REC_COUNT'][0] > 0 :
            sql = """
                    UPDATE ETL_RPT.PM_RELEASE_ACTIVITY_STATUS SET STATUS = {},PLANNED_START_TIME = sysdate + 2/24  WHERE RELEASE = '{}' AND RELEASE_ACTIVITY_ID = {}
                  """.format(0,release,act_id)
        else:
            sql = """
                    UPDATE ETL_RPT.PM_RELEASE_ACTIVITY_STATUS SET STATUS = {},ACTUAL_END_TIME = sysdate  WHERE RELEASE = '{}' AND RELEASE_ACTIVITY_ID = {}
                  """.format(2,release,act_id)

        self.util.run_insert_sql(sql)

    def update_activity_status_as_failed(self) :
        self.log ("Updating status to Failed for activty running.",0)

        sql = """
            UPDATE ETL_RPT.PM_RELEASE_ACTIVITY_STATUS SET STATUS = -1 WHERE STATUS = 1
        """

        self.util.run_insert_sql(sql)

    def f_process_stop_crons(self,act_id,activity,release,env,iteration=0,email_to='',email_cc='',sent_email = 'Y'):
        self.log ("Stoping cron Instances in {} for the release {} ".format(env,release),0)

        self.f_register_activity(act_id,release,status='START',env=env)

        rel_obj = dsi_release.dsi_release(release,env=env,log_level=self.LOG_LEVEL)
        ret_code = rel_obj.f_stop_all_crons_for_env()

        if ret_code == 0 :
            self.f_register_activity(act_id,release,status='END',env=env)
            if sent_email == 'Y' :
                self.f_send_activty_status_email('SUCCESS',act_id,activity,release,env,iteration=0,email_to='',email_cc='')
        else :
            self.f_register_activity(act_id,release,status='FAIL',env=env)
            if sent_email == 'Y' :
                self.f_send_activty_status_email('FAIL',act_id,activity,release,env,iteration=0,email_to='',email_cc='')

    def f_process_start_crons(self,act_id,activity,release,env,iteration=0,email_to='',email_cc='',sent_email = 'Y'):
        self.log ("Starting Scheduler Instances in {} for the release {} ".format(env,release),0)

        self.f_register_activity(act_id,release,status='START',env=env)

        rel_obj = dsi_release.dsi_release(release,env=env,log_level=self.LOG_LEVEL)
        ret_code = rel_obj.f_start_schedulers_for_env()

        if ret_code == 0 :
            self.f_register_activity(act_id,release,status='END',env=env)
            if sent_email == 'Y' :
                self.f_send_activty_status_email('SUCCESS',act_id,activity,release,env,iteration=0,email_to='',email_cc='')
        else :
            self.f_register_activity(act_id,release,status='FAIL',env=env)
            if sent_email == 'Y' :
                self.f_send_activty_status_email('FAIL',act_id,activity,release,env,iteration=0,email_to='',email_cc='')

def draw_line(sym='*') :
    print(sym * 80)

if __name__ == '__main__' :
    util = dsi_util.dsi_util()
    RELEASE_CONFIG_FILE='/abinitio/dev/data/config/release_configurations.cfg'
    release_config = util.get_config(RELEASE_CONFIG_FILE)

    try :
       LOG_LEVEL=0
       rel_sch = dsi_release_scheduler(log_level=LOG_LEVEL)
       rel_sch.log(" ",0)
       rel_sch.log(" ",0)
       draw_line()
       draw_line()
       rel_sch.log("                                   Scheduler Invoked              ",0)
       draw_line()
       draw_line()
       rel_sch.log("Checking Release scheduler for any releases in next few days.",0)
       draw_line()
       rel_sch.f_check_release_schedule()
       draw_line()
       rel_sch.log("Trying to see if there are any activities due for execution.",0)
       draw_line()
       rel_sch.f_perform_release_activity()
       draw_line()
       rel_sch.log("Scheduler completed operations Successfully.",0)
       draw_line()
    except :
        rel_sch.update_activity_status_as_failed()
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        body = ''.join('<br> ' + line for line in lines)

        msg = {}
        msg['Body'] = """<b>Scheduler Failed while exceuting Activities. Please take a look into log file for details.</b>
                      {}
                      """.format(body)
        print body
        msg['From'] = 'Release_Team@lpwaidqu14.npd.com'

        if 'RELEASE_TEAM_TO' in release_config :
            msg['To'] = release_config['RELEASE_TEAM_TO']
        else :
            msg['To'] =  'Ranjeeth.Kyatham@npd.com;Jingming.Ma@npd.com'

        if 'RELEASE_TEAM_CC' in release_config :
            msg['Cc'] = release_config['RELEASE_TEAM_CC']
        else :
            msg['Cc'] =  'Vishal.Sharma@npd.com'

        msg['Subject'] =  'ERROR : dsi_release_scheduler (Release Activity Process)'

        util.f_send_email(msg)
        print("program failed. Please fix.")
        raise
