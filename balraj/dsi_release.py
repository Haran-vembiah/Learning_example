# import dsi_util
import eme
import svn
import unix
import os, re
import pandas as pd
import datetime


# import util_sanity_performance


class dsi_release(object):
    """
    This class provides some of the basic features of the release tasks.

    Name : Vishal Sharma (09/25/2018) - Initial Version

    :param str RELEASE : A string indicating release.
    :param str ENV : environment to which release is to be done
    :raises : DSIError Exception
    """

    def __init__(self, release, env="XXX", pre_release="", log_level=0, DRY_RUN=0):
        self.VALID_SCHEMAS = {'ODS': 10, 'ETL_MGR': 20, 'ETL_USER': 30, 'IPF_MGR': 40, 'FOOCNS': 99, 'ONSCNS': 100,
                              'ETL_RPT': 35, 'MATCH_APP': 50, 'ETL_APP': 31, 'HDP_MGR': 100, 'JOB_MGR': 110,
                              'REST_API_MGR': 120, 'ETL_RUN': 140, 'ETL_MTA': 150}
        self.RELEASE = release
        self.LOG_LEVEL = log_level
        self.DRY_RUN = DRY_RUN
        self.util = dsi_util.dsi_util(log_level=log_level)
        self.STANDARD_VARIABLES = ['HOME', 'STAGE']
        self.env_var = self.util.get_env_var(self.STANDARD_VARIABLES)
        self.PRE_RELEASE = ""
        self.PRE_BASE_RELEASE_TAG = ""
        self.BASE_RELEASE_TAG = ""
        self.HOT_FIX_IND = 0
        self.ENV = env.strip().upper()
        self.svn_add_obj_list = []
        self.ab_tickets = None
        self.svn_tickets = None
        self.release_tickets = None
        self.sql_df = None
        self.valid_sql = None
        self.invalid_sql = None

        if self.ENV not in ['XXX', 'QA', 'UAT', 'MNA', 'UAT', 'PROD']:
            self.f_error(
                "Target environment value of {} is not valid. Expected values are QA,MNA,UAT or PROD.".format(self.ENV))

        self.f_validate_release()

        if self.ENV == 'MNA':
            self.TAG_ENV = 'QA'
        else:
            self.TAG_ENV = self.ENV

        self.RELEASE_TAG = self.BASE_RELEASE_TAG
        self.PRE_RELEASE_TAG = self.PRE_BASE_RELEASE_TAG

        self.RELEASE_STAGING_TAG = self.RELEASE_TAG + '.STAGING'
        self.PRE_RELEASE_STAGING_TAG = self.PRE_RELEASE_TAG + '.STAGING'

        self.HF_RELEASE_TAG = self.RELEASE_TAG + '.HOT_FIX'
        self.NEW_HF_RELEASE_TAG = self.RELEASE_TAG + '.HOT_FIX.' + self.RELEASE
        self.PRE_HF_RELEASE_TAG = self.PRE_RELEASE_TAG + '.HOT_FIX'

        self.emeobj = eme.eme(log_level=self.LOG_LEVEL)
        self.svnobj = svn.svn(log_level=self.LOG_LEVEL)
        self.unix = unix.unix(log_level=self.LOG_LEVEL)
        self.util = dsi_util.dsi_util()
        self.sanity_performance = util_sanity_performance.util_sanity_performance()

        RELEASE_CONFIG_FILE = '/abinitio/dev/data/config/release_configurations.cfg'
        self.release_config = self.util.get_config(RELEASE_CONFIG_FILE)

        self.f_summarize_release()
        self.RELEASE_SUMMARY_TEMPLATE = '/home/ai/Release/python/Release_Summary_template.htm'
        self.RELEASE_INIT_TEMPLATE = '/home/ai/Release/python/Release_Initiation_template.htm'
        self.RELEASE_TKT_SUM_TEMPLATE = '/home/ai/Release/python/Release_Ticket_Summary_template.htm'
        self.RELEASE_TKT_ONLY_SUM_TEMPLATE = '/home/ai/Release/python/Release_Ticket_Only_Summary_template.htm'
        self.RELEASE_HEADER_TEMPLATE = '/home/ai/Release/python/Release_Header_Template.htm'
        self.f_validate_release_for_objects()
        ##self.f_register_release(event='START')
        pd.set_option('display.max_colwidth', -1)

    def __repr__(self):
        return ('Class {} : Performs basic release tasks.').format(self.__class__.__name__)

    def f_error(self, msg):
        self.log('Raising Error.', 2)
        self.util.f_error(msg)

    def f_validate_release_for_objects(self, email_to='', email_cc=''):
        """
        This function will validate release to ensure there are no object going with an earlier version.
        """
        self.log("Trying to ensure that no ticket is causing an objects old version to be released.", 0)

        if self.ENV == 'MNA':
            test_env = 'QA'
        else:
            test_env = self.ENV

        sql = """
        with pre_release as
(
select b.object_id,b.object_name, max(a.object_version) object_version,max(a.TICKET_NUMBER) 
from etl_rpt.pm_object_tagging a, etl_rpt.pm_objects b 
where
a.object_id = b.object_id and {0}_release <= '{1}' group by b.object_id,b.object_name
),
curr_release as
(
select b.object_id,b.object_name, max(a.object_version) object_version,max(c.TICKET_NUMBER) TICKET_NUMBER,  max(pres.first_name) first_name
from etl_rpt.pm_object_tagging a, etl_rpt.pm_objects b,etl_rpt.pm_releasing c,etl_rpt.pm_resources pres
 where
 c.assignee = pres.resource_id  and c.ACTIVE_FLAG = 1 and 
a.object_id = b.object_id and c.{0}_release = '{2}' and c.TICKET_NUMBER = a.TICKET_NUMBER group by b.object_id,b.object_name
)
select 
   first_name,
   c.TICKET_NUMBER,
   p.object_id,
   p.object_name object_name,
   p.object_version prev_version,
   c.object_version curr_version
from 
  pre_release p,
  curr_release c
where
  p.object_id = c.object_id   and
  p.object_version > c.object_version
        """.format(test_env, self.PRE_RELEASE, self.RELEASE)

        data = self.util.run_sql(sql)

        if data.empty:
            self.log("Release validation passed.We are good to start the release.", 0)
        else:
            msg = {}
            release = self.RELEASE
            msg1 = open(self.RELEASE_HEADER_TEMPLATE).read()
            msg1 = msg1.decode('utf-8')

            msg1 = msg1.replace('xxx_release_xxx', release.replace('QA', self.ENV))
            msg1 = msg1.replace('xxx_env_xxx', self.ENV)
            table1 = data.to_html(index=False).replace('<th>',
                                                       """<th style="font-family:'Calibri';font-size:12.0pt;background-color:'DodgerBlue">""").encode(
                'utf-8')
            table1 = table1.replace('<td>', """<td style="font-family:'Calibri';font-size:12.0pt">""")
            msg2 = """<style="font-size:10.0pt;font-family:'Calibr'"> <b> Some of the objects in the release are reverting to old version. Release could not be validate. Please fix This.</b><br> """ + table1 + "</style>"

            msg1 = msg1.replace('xxx_message_xxx', msg2)

            msg['Subject'] = "{}: Release validation Failed".format(self.RELEASE)
            msg['From'] = 'Release_Team'
            msg['Body'] = msg1

            if email_to is None or email_to == '':
                msg['To'] = 'Ranjeeth.Kyatham@npd.com;Jingming.Ma@npd.com;Vishal.sharma@npd.com'
            else:
                msg['To'] = email_to.replace(' ', '')

            if email_cc is None or email_cc == '':
                msg['CC'] = 'Ranjeeth.Kyatham@npd.com;Jingming.Ma@npd.com;Vishal.sharma@npd.com;'
            else:
                msg['CC'] = email_cc.replace(' ', '')

            self.log("Sending email to {} : with CC as {} ".format(msg['To'], msg['CC']), 0)

            self.util.f_send_email(msg)
            self.util.f_error("Could not continue release as there are objects which are reverting to old versions.")

    def f_register_release(self, event=''):
        """
        This function update PM_RELEASE_TAGS with start time
        """
        self.log('                Updating PM_RELEASE_TAGS table with start time ', 0)

        if event == 'START':
            sql = "update ETL_RPT.PM_RELEASE_TAGS set RELEASE_START_TIME = sysdate  where RELEASE = '{}'".format(
                self.RELEASE)
        elif event == 'END':
            sql = "update ETL_RPT.PM_RELEASE_TAGS set RELEASE_END_TIME = sysdate  where RELEASE = '{}'".format(
                self.RELEASE)
        else:
            self.f_error("Invalid event type({}) passed. Please check.".format(event))

        df = self.util.run_insert_sql(sql)

    def f_summarize_release(self):
        self.log('Summarizing Release.', 2)
        LINE = '=' * 80
        self.log(LINE, 0)
        self.log('                Release                      : {}'.format(self.RELEASE), 0)
        self.log('                Release Tag                  : {}'.format(self.RELEASE_TAG), 0)
        self.log('                Release Staging Tag          : {}'.format(self.RELEASE_STAGING_TAG), 0)
        self.log('                Release Hot-Fix Tag          : {}'.format(self.HF_RELEASE_TAG), 0)

        if self.HOT_FIX_IND == 0:
            self.log('                Previous Release             : {}'.format(self.PRE_RELEASE), 0)
            self.log('                Previous Release Tag         : {}'.format(self.PRE_RELEASE_TAG), 0)
            self.log('                Previous Release Staging Tag : {}'.format(self.PRE_RELEASE_STAGING_TAG), 0)
            self.log('                Previous Hot-Fix Release Tag : {}'.format(self.PRE_HF_RELEASE_TAG), 0)
            self.log('                Target Environment   : {}'.format(self.ENV), 0)
            self.log('                -------------------------------------------------', 0)
            self.log('                This release is MAIN Release ', 0)
        else:
            self.log('                This release is a HOT - FIX Release ', 0)
            self.log('                -------------------------------------------------', 0)
            self.log('        Hot-Fix Tag for this deploy          : {}'.format(self.NEW_HF_RELEASE_TAG), 0)
        self.log(LINE, 0)

    def log(self, data, level):
        """
        Writes details to log based on log level

        Attribute
        :param str[] data : data to be written to log
        :return: None
        :raises: None
        """
        data = "{} : {}".format(datetime.datetime.now(), data)
        self.util.log(data, level)

    def f_validate_release(self):
        """
        Gets necessary release details from  ETL_RPT tables like tag, previous release and environment.

        Attribute
        :param None :
        :return: None
        :raises: None
        """
        self.log('Initiating Release Validation Process.', 0)

        self.f_get_tag_details()
        self.f_get_env_details()

        if not self.HOT_FIX_IND:
            self.f_get_previous_tag_details()

    def f_get_tag_details(self):
        """
        Gets release tag details from  ETL_RPT.PM_RELEASE_TAGS

        Attribute
        :param None :
        :return: None
        :raises: None
        """
        self.log('Trying to get tag details from DB.', 0)

        sql = "select HOT_FIX_FLAG from ETL_RPT.PM_RELEASE_SCHEDULES where RELEASE = '{}'".format(self.RELEASE)
        df = self.util.run_sql(sql)

        if df.empty:
            self.f_error(
                "Release {} is not defined in ETL_RPT.PM_RELEASE_SCHEDULES. Please define release with                  details.".format(
                    self.RELEASE))
        else:
            self.HOT_FIX_IND = df['HOT_FIX_FLAG'][0]

        sql = "select RELEASE_TAG from ETL_RPT.PM_RELEASE_TAGS where RELEASE = '{}'".format(self.RELEASE)
        df = self.util.run_sql(sql)

        if df.empty:
            self.f_error(
                "Release {} is not defined in ETL_RPT.PM_RELEASE_TAGS. Please define release with tag                 details.".format(
                    self.RELEASE))
        else:
            if self.HOT_FIX_IND:
                self.NEW_HF_RELEASE_TAG = df['RELEASE_TAG'][0]
                self.BASE_RELEASE_TAG = self.NEW_HF_RELEASE_TAG.split('.')[0] + '.' + \
                                        self.NEW_HF_RELEASE_TAG.split('.')[1]
            else:
                self.BASE_RELEASE_TAG = df['RELEASE_TAG'][0]

    def f_get_previous_tag_details(self):
        """
        Gets previous release details from  ETL_RPT.PM_RELEASE_TAGS

        Attribute
        :param str RELEASE : data to be written to log
        :return: None
        :raises: None
        """
        self.log('Trying to get previous tag details from DB.', 2)

        if self.ENV == 'MNA':
            test_env = 'QA'
        else:
            test_env = self.ENV

        sql = """
         select RELEASE_TAG,RELEASE from ETL_RPT.PM_RELEASE_TAGS where RELEASE = (select max(RELEASE) from
         ETL_RPT.PM_RELEASE_SCHEDULES where release < '{}' and RELEASE_PHASE = '{}' and HOT_FIX_FLAG = 0)
         """.format(self.RELEASE, test_env)

        df = self.util.run_sql(sql)
        if df.empty:
            self.f_error(
                "Could not find Previous release tag details from ETL_RPT.PM_RELEASE_SCHEDULES. Please define release with tag details.\n========> SQL used :\n     {} ".format(
                    sql))
        else:
            self.PRE_BASE_RELEASE_TAG = df['RELEASE_TAG'][0]
            self.PRE_RELEASE = df['RELEASE'][0]

    def f_get_env_details(self):
        """
        Gets release environment details from  ETL_RPT.PM_RELEASE_TAGS

        Attribute
        :param str RELEASE : data to be written to log
        :return: None
        :raises: None
        """
        self.log('Trying to get release env details.', 2)

        if self.ENV == "XXX":
            env2 = self.RELEASE[0:2]
            env3 = self.RELEASE[0:3]

            if self.RELEASE[0:4] == 'PROD':
                self.ENV = 'PROD'
            elif env3 in ['UAT', 'MNA']:
                self.ENV = env3
            elif env2 in ['QA']:
                self.f_validate_env_with_user()
            else:
                self.f_error(
                    "Release value : {} appears invalid. It need to be <<env>><<date>> [env as QA,UAT,PROD,MNA]. Please fix this in ETL_RPT.PM_RELEASE_TAGS.".format(
                        self.RELEASE))
        else:
            self.log('Env is passed as argument as {}. Using it.'.format(self.ENV), 2)

    def f_validate_env_with_user(self):
        """
        tries to validate environmentif it turns out to be QA as QA and MNA share same release.

        Attribute
        :param sNone :
        :return: None
        :raises: None
        """
        self.log('Trying to validate env as QA and MNA release share the Release.', 2)

        msg = "MNA and QA share the same release. Could you please verify if release is to MNA or QA.\n ========> Enter 1 for MNA and 2 for QA : "
        res = raw_input('{}'.format(msg))

        while res not in ['1', '2']:
            msg = "Invalid value passed. \n ========> Enter 1 for MNA and 2 for QA :"
            res = raw_input('{}'.format(msg))

        if res == '1':
            self.ENV = 'MNA'
        elif res == '2':
            self.ENV = 'QA'
        else:
            self.f_error(" Environment value passed is incorrect. Please fix it.")

    def f_describe_release(self):
        """
        Displays release details.

        Attribute
        :param : None
        :return: None
        :raises: None
        """
        self.log('Describe Release functionality invoked.', 2)
        space20 = ' ' * 20
        self.log('*' * 80, 0)
        self.log("{} Release             : {}".format(space20, self.RELEASE), 0)
        self.log("{} Target Environment  : {}".format(space20, self.ENV), 0)
        self.log("{} Release Tag         : {}".format(space20, self.RELEASE_TAG), 0)
        self.log('*' * 80, 0)

    def f_pull_release_tickets(self):
        """
        This function pulls tickets associated with the release.

        Attribute
        :param str RELEASE : The RELEASE, whose tickets needs to be pulled from ETL_RPT.PM_RELEASING
        :return: List of tickets associated with the release
        :raises: None
        """
        self.log('Pulling details of tickets that make up the release.', 2)

        if self.ENV in ['MNA', 'QA']:
            sql = "select TICKET_NUMBER from ETL_RPT.PM_RELEASING where ACTIVE_FLAG = 1 AND QA_RELEASE = '{}'".format(
                self.RELEASE)
        elif self.ENV in ['UAT']:
            sql = "select TICKET_NUMBER from ETL_RPT.PM_RELEASING where ACTIVE_FLAG = 1 AND UAT_RELEASE = '{}'".format(
                self.RELEASE)
        elif self.ENV in ['PROD']:
            sql = "select TICKET_NUMBER from ETL_RPT.PM_RELEASING where ACTIVE_FLAG = 1 AND PROD_RELEASE = '{}'".format(
                self.RELEASE)
        else:
            self.f_error(
                "Target environment value of {} is not valid. Expected values are QA,MNA,UAT or PROD.".format(self.ENV))

        df = self.util.run_sql(sql)
        return df['TICKET_NUMBER']

    def f_get_tickets_with_type(self, rep_type):
        """
        This function pulls tickets associated with the release of a particular repository type.

        Attribute
        :param str type : Type of repository ex abinitio or svn
        :return: List of tickets associated with the release having particular type
        :raises: None
        """
        self.log('    Pulling details of tickets that make up the release and have {} objects.'.format(rep_type), 0)

        if self.ENV in ['MNA', 'QA']:
            sql1 = "select TICKET_NUMBER from ETL_RPT.PM_RELEASING where ACTIVE_FLAG = 1 AND QA_RELEASE = '{}'".format(
                self.RELEASE)
        elif self.ENV in ['UAT']:
            sql1 = "select TICKET_NUMBER from ETL_RPT.PM_RELEASING where ACTIVE_FLAG = 1 AND UAT_RELEASE = '{}'".format(
                self.RELEASE)
        elif self.ENV in ['PROD']:
            sql1 = "select TICKET_NUMBER from ETL_RPT.PM_RELEASING where ACTIVE_FLAG = 1 AND PROD_RELEASE = '{}'".format(
                self.RELEASE)
        else:
            self.f_error(
                "Target environment value of {} is not valid. Expected values are QA,MNA,UAT or PROD.".format(self.ENV))

        if rep_type in ['abinitio']:
            sql = """SELECT 
                        distinct ticket_number,object_path,object_version
                     FROM
                        ETL_RPT.PM_OBJECTS O,
                        ETL_RPT.PM_OBJECT_TAGGING OT
                     WHERE
                        O.object_id = OT.object_id and 
                        ticket_number in ({}) 
                        and OBJECT_PATH like ('/Projects/%')
               """.format(sql1)
        elif rep_type in ['svn']:
            sql = """SELECT max(ticket_number) ticket_number,object_path,object_version FROM (
                 SELECT ticket_number,object_path,object_version,
                      rank() over (partition by object_path order by object_version  desc) max_ticket
                 FROM
                    ETL_RPT.PM_OBJECT_TAGGING A, ETL_RPT.PM_OBJECTS B
                 WHERE    
                       a.object_id = b.object_id and
                       object_path like ('/npd/%') and   
                       ticket_number in ( {} )
                 ) WHERE max_ticket = 1  group by object_path,object_version    
               """.format(sql1)
        else:
            self.f_error(
                "Invalid repository ({}) type passed to function.Supported are abinitio or SVN.".format(rep_type))

        df = self.util.run_sql(sql)

        ##print df

        if rep_type in ['abinitio']:
            self.ab_tickets = df
            return df['TICKET_NUMBER'].unique().tolist()
        else:
            self.svn_tickets = df
            return df

    def f_build_release(self):
        """
        This function builds release.

        Attribute
        :param : None
        :return: None
        :raises: None
        """
        if self.HOT_FIX_IND:
            self.log('Trying to build FAST-TRACK release by applying release tag to objects.', 2)
            self.f_build_HF_abinitio_release()
            self.f_build_HF_svn_release()
        else:
            self.log('Trying to build release by applying release tag to objects.', 2)
            self.f_build_abinitio_release()
            self.f_build_svn_release()

        self.f_register_release(event='END')

    def f_update_tickets_with_status(self, ob_type=''):
        """
        This function builds SVN FAST TRACK release by adding creating HF branch.

        Attribute
        :param : ob_type : SVN or Abinitio
        :return: None
        :raises: None
        """

        if ob_type == 'SVN':
            tickets_list = self.svn_tickets['TICKET_NUMBER'].unique().tolist()
        elif ob_type == 'ABINITIO':
            tickets_list = self.ab_tickets['TICKET_NUMBER'].unique().tolist()
        else:
            self.f_error("Invalid object type. We support SVN and ABINITIO only right now.")

        tickets = ",".join(["'{}'".format(x) for x in tickets_list])

        if tickets.strip() == '':
            self.log(
                "There are no tickets that have object type of {}. Skipping update of ETL_RPT.PM_OBJECT_TAGGING.".format(
                    ob_type), 0)
            return 0

        if self.ENV in ['MNA', 'QA']:
            sql = "update ETL_RPT.PM_OBJECT_TAGGING set QA_RELEASE = '{}', QA_RELEASE_TAG = '{}' where TICKET_NUMBER in ({})".format(
                self.RELEASE, self.RELEASE_TAG, tickets)
        elif self.ENV in ['UAT']:
            sql = "update ETL_RPT.PM_OBJECT_TAGGING set UAT_RELEASE = '{}', UAT_RELEASE_TAG = '{}' where TICKET_NUMBER in ({})".format(
                self.RELEASE, self.RELEASE_TAG, tickets)
        elif self.ENV in ['PROD']:
            sql = "update ETL_RPT.PM_OBJECT_TAGGING set PROD_RELEASE = '{}', PROD_RELEASE_TAG = '{}' where TICKET_NUMBER in ({})".format(
                self.RELEASE, self.RELEASE_TAG, tickets)
        else:
            self.f_error(
                "Target environment value of {} is not valid. Expected values are QA,MNA,UAT or PROD.".format(self.ENV))

        df = self.util.run_insert_sql(sql)

    def f_build_HF_svn_release(self):
        """
        This function builds SVN FAST TRACK release by adding creating HF branch.

        Attribute
        :param : None
        :return: None
        :raises: None
        """
        self.log('Initiaing SVN Build for Fast Track Deploy.', 0)
        self.set_svn_release_var()
        svn_df = self.f_get_tickets_with_type('svn')

        if svn_df.empty:
            self.log('There are no tickets with SVN changes for this release. Skipping SVN deploy.', 0)
            return 0

        self.log('Ticktes with SVN objects are :\n {} .'.format(svn_df), 3)

        self.svnobj.del_tag(self.NEW_HF_RELEASE_TAG, quite=1, dont_fail=1)
        self.build_staging_tag(self.NEW_HF_RELEASE_TAG, svn_df)

        self.svnobj.f_checkout_proj(self.C_SVN_HF_LOC, loc=self.C_WRK_HF_LOC, no_loc_check=1)
        self.f_deploy_HF_objects_to_target_env()
        self.f_update_tickets_with_status(ob_type='SVN')

        self.log("\n\nSVN HF release completed successfully.", 0)
        return 0

    def f_deploy_HF_objects_to_target_env(self):
        """
        This function deploys HF SVN objects to target servers and builds jars.

        Attribute
        :param : None
        :return: None
        :raises: None
        """
        self.log(
            'Deploying SVN objects from {} to target servers of {} envirionment.'.format(self.C_WRK_HF_LOC, self.ENV),
            0)

        if (self.ENV == 'MNA'):
            env = 'staging'
        else:
            env = self.ENV.lower()

        env_owner = 'ai' + env

        actual_base = "/home/{}/{}".format(env_owner, env)
        actual_workspace = "{}/hadoop_{}/workspace/npd/dsi".format(actual_base, self.RELEASE_TAG)
        actual_npd_batch = "{}/npd_batch_{}".format(actual_base, self.RELEASE_TAG)

        cmd = 'find {}/npd_hadoop/ -type f '.format(self.C_WRK_HF_LOC)
        self.unix.run(cmd, quite=1, dont_fail=1)
        workspace_objects = [x for x in self.unix.out.split('\n') if x.strip() != '']

        cmd = 'find {}/npd_batch/ -type f '.format(self.C_WRK_HF_LOC)
        self.unix.run(cmd, quite=1, dont_fail=1)
        npd_batch_objects = [x for x in self.unix.out.split('\n') if x.strip() != '']

        sql = """
        select virtual_name from etl_mgr.etl_env_servers a, etl_mgr.etl_servers b
where a.server_id = b.server_id and env_id in (select env_id from etl_mgr.etl_environments where lower(env_name) = '{}')
""".format(env)
        df = self.util.run_sql(sql, env=env)

        if df.empty:
            self.f_error(
                "Could not find target server details for {} using sql.\n========> SQL used :\n     {} ".format(
                    target_env, sql))

        for server in df['VIRTUAL_NAME']:
            if workspace_objects:
                self.log("  ======> Copying workspcae objects to server : {}".format(server), 0)
                for obj in workspace_objects:
                    tar_loc = obj.replace(self.C_WRK_HF_LOC, actual_workspace)
                    self.log("  ========> Copying {} \n              to {}".format(obj, tar_loc), 0)
                    cmd = "scp {} {}@{}:{}".format(obj, env_owner, server, tar_loc)
                    # self.unix.run(cmd)
                    os.system(cmd)

                self.log("  ===> Finally Building the jars for hadoop workspace on server : {}".format(server), 0)
                self.svnobj.build(actual_workspace, server=server, owner=env_owner)

            if npd_batch_objects:
                self.log("  ======> Copying npd_batch project objects to server : {}".format(server), 0)
                for obj in npd_batch_objects:
                    tar_loc = obj.replace(self.C_WRK_HF_LOC, actual_npd_batch)
                    self.log("  ========> Copying {} \n              to {}".format(obj, tar_loc), 0)
                    cmd = "scp {} {}@{}:{}".format(obj, env_owner, server, tar_loc)
                    self.unix.run(cmd)

                self.log("  ===> Finally Building the jars for npd_batch on server : {}".format(server), 0)
                self.svnobj.build(actual_npd_batch, server=server, owner=env_owner)

    def f_build_HF_abinitio_release(self):
        """
        This function builds abinitio FAST TRACK release by adding release tag to abinitio objects.

        Attribute
        :param : None
        :return: None
        :raises: None
        """
        self.log('Initiaing FAST TRACK Abinitio Build.', 0)

        ab_tkts = self.f_get_tickets_with_type('abinitio')
        self.log('Ticktes with abinio objects are :\n {} .'.format(ab_tkts), 3)

        if not ab_tkts:
            self.log('There are no tickets with Abinitio changes for this release. Skipping Abinitio deploy.', 0)
            return 0

        self.f_build_hf_abinitio_tag(ab_tkts)
        self.create_and_deploy_eme_save_file()
        self.finally_create_abinitio_sandboxes()
        self.f_update_tickets_with_status(ob_type='ABINITIO')
        self.log("\n\nAbinitio HF release completed successfully.", 0)
        return 0

    def f_build_hf_abinitio_tag(self, ab_tkts):
        """
        This function builds HF release by taging objects with Hot-Fix.

        Attribute
        :param : None
        :return: None
        :raises: None
        """
        if self.emeobj.f_tag_exists(self.NEW_HF_RELEASE_TAG, dont_fail=1, quite=1):
            self.log('    ===> Tag {} exits.'.format(self.NEW_HF_RELEASE_TAG), 0)
            self.log('    ===> deleting old tag so that it can be recreated.'.format(self.NEW_HF_RELEASE_TAG), 0)
            self.emeobj.del_tag(self.NEW_HF_RELEASE_TAG, dont_fail=1, quite=1)

        self.log(
            '    Generating HF tag {} by combining ticket tags {} .'.format(self.NEW_HF_RELEASE_TAG, ' '.join(ab_tkts)),
            0)
        self.emeobj.f_combine_tags(self.NEW_HF_RELEASE_TAG, ab_tkts)

        self.log(
            '    Combining HF tag {} into master HF tag : {} .'.format(self.NEW_HF_RELEASE_TAG, self.HF_RELEASE_TAG), 0)

        if self.emeobj.f_tag_exists(self.HF_RELEASE_TAG, dont_fail=1, quite=1):
            self.emeobj.rename_tag(self.HF_RELEASE_TAG, self.HF_RELEASE_TAG + 'BKUP')
            self.emeobj.f_combine_tags(self.HF_RELEASE_TAG, [self.HF_RELEASE_TAG + 'BKUP', self.NEW_HF_RELEASE_TAG])
            self.emeobj.del_tag(self.HF_RELEASE_TAG + 'BKUP')
        else:
            self.emeobj.f_combine_tags(self.HF_RELEASE_TAG, [self.NEW_HF_RELEASE_TAG])

    def f_build_and_deploy_only_abinitio_release(self):
        """
        This function builds abinitio release by adding release tag to abinitio objects.

        Attribute
        :param : None
        :return: None
        :raises: None
        """
        self.log('Initiaing Abinitio Build.', 0)

        ab_tkts = self.f_get_tickets_with_type('abinitio')
        self.log('Ticktes with abinio objects are :\n {} .'.format(ab_tkts), 3)

        if not self.emeobj.f_tag_exists(self.RELEASE_TAG, dont_fail=1, quite=1):
            self.log('    It appears base tag {} does not exit. Building it.'.format(self.RELEASE_TAG), 0)
            self.f_build_ab_base_tag()
        else:
            self.log('    It appears base tag {} was created already. Skipping this step.'.format(self.RELEASE_TAG), 0)

        self.log('    Trying to bundle release tickets into release tag {}.'.format(self.RELEASE_STAGING_TAG), 0)

        if self.emeobj.f_tag_exists(self.RELEASE_STAGING_TAG, dont_fail=1, quite=1):
            self.log('    ===> Deleting old release bundle tag {}.'.format(self.RELEASE_STAGING_TAG), 0)
            self.emeobj.del_tag(self.RELEASE_STAGING_TAG, dont_fail=1, quite=1)
        else:
            self.log('    ===> This appears first deployment. Building tag {}.'.format(self.RELEASE_STAGING_TAG), 0)

        if not ab_tkts:
            self.log('    There are no tickets with ABinitio changes checked in. So skipping Abinitio deploy', 0)
            self.log('    ==================================================================================', 0)
        elif self.emeobj.f_tag_exists(self.HF_RELEASE_TAG, dont_fail=1, quite=1):
            self.emeobj.f_combine_tags(self.RELEASE_STAGING_TAG, ab_tkts + [self.HF_RELEASE_TAG])
        else:
            self.emeobj.f_combine_tags(self.RELEASE_STAGING_TAG, ab_tkts)

        self.create_and_deploy_eme_save_file()

        self.log("\n\nAbinitio build and deploy release completed successfully.", 0)
        return 0

    def f_build_abinitio_release(self):

        """
        This function builds abinitio release by adding release tag to abinitio objects.

        Attribute
        :param : None
        :return: None
        :raises: None
        """
        print("hello")
        self.log('Initiaing Abinitio Build.', 0)

        ab_tkts = self.f_get_tickets_with_type('abinitio')
        self.log('Ticktes with abinio objects are :\n {} .'.format(ab_tkts), 3)

        if not self.emeobj.f_tag_exists(self.RELEASE_TAG, dont_fail=1, quite=1):
            self.log('    It appears base tag {} does not exit. Building it.'.format(self.RELEASE_TAG), 0)
            self.f_build_ab_base_tag()
        else:
            self.log('    It appears base tag {} was created already. Skipping this step.'.format(self.RELEASE_TAG), 0)

        self.log('    Trying to bundle release tickets into release tag {}.'.format(self.RELEASE_STAGING_TAG), 0)

        if self.emeobj.f_tag_exists(self.RELEASE_STAGING_TAG, dont_fail=1, quite=1):
            self.log('    ===> Deleting old release bundle tag {}.'.format(self.RELEASE_STAGING_TAG), 0)
            self.emeobj.del_tag(self.RELEASE_STAGING_TAG, dont_fail=1, quite=1)
        else:
            self.log('    ===> This appears first deployment. Building tag {}.'.format(self.RELEASE_STAGING_TAG), 0)

        if not ab_tkts:
            self.log('    There are no tickets with ABinitio changes checked in. So skipping Abinitio deploy', 0)
            self.log('    ==================================================================================', 0)
        elif self.emeobj.f_tag_exists(self.HF_RELEASE_TAG, dont_fail=1, quite=1):
            self.emeobj.f_combine_tags(self.RELEASE_STAGING_TAG, ab_tkts + [self.HF_RELEASE_TAG])
        else:
            self.emeobj.f_combine_tags(self.RELEASE_STAGING_TAG, ab_tkts)

        self.create_and_deploy_eme_save_file()
        self.finally_create_abinitio_sandboxes()
        self.f_update_tickets_with_status(ob_type='ABINITIO')
        self.f_create_non_standard_sandboxes(sand_type='ABINITIO')

        self.log("\n\nAbinitio release completed successfully.", 0)
        return 0

    def create_and_deploy_eme_save_file(self):
        """
        This function create and deploys save files onto target EME.

        Attribute
        :param : None
        :return: None
        :raises: None
        """
        self.log('Trying to create save file and loading in into target EME.', 0)

        ##      Base location for temporary checkout from svn
        loc_deploy_base_loc = self.env_var['HOME'] + '/migration/eme_release'
        target_env = self.ENV
        if (target_env == 'MNA'):
            env = 'staging'
        else:
            env = target_env.lower()

        env_owner = 'ai' + env

        target_AB_AIR_ROOT = '//' + self.release_config['{}_EME_SERVER'.format(target_env)] + self.release_config[
            '{}_AB_AIR_ROOT'.format(target_env)]

        tar_eme = eme.eme(target_AB_AIR_ROOT, ab_server=self.release_config['{}_EME_SERVER'.format(target_env)],
                          owner=self.release_config['{}_EME_OWNER'.format(target_env)])

        if self.HOT_FIX_IND:
            if tar_eme.f_tag_exists(self.NEW_HF_RELEASE_TAG, dont_fail=1, quite=1):
                self.log('   HF package {} has already been deployed to target EME {}. Deleting it.'.format(
                    self.NEW_HF_RELEASE_TAG, target_AB_AIR_ROOT), 0)
                tar_eme.del_tag(self.NEW_HF_RELEASE_TAG, quite=1)
            self.log('    ====> Trying to create save file for HF release and loading in into target EME.', 0)
            self.emeobj.create_save_file(self.NEW_HF_RELEASE_TAG, base_loc=loc_deploy_base_loc)
            self.deploy_release_save_file(self.NEW_HF_RELEASE_TAG)
            return 0

        if tar_eme.f_tag_exists(self.RELEASE_TAG, dont_fail=1, quite=1):
            self.log('   Base package {} has already been deployed to target EME {}.'.format(self.RELEASE_TAG,
                                                                                             target_AB_AIR_ROOT), 0)
        else:
            self.log('    Base package {} has not been deployed to target EME {}. Initiating its deployment.'.format(
                self.RELEASE_TAG, target_AB_AIR_ROOT), 0)
            self.log('    ====> Trying to create save file for base release and loading in into target EME.', 0)
            self.emeobj.create_save_file(self.RELEASE_TAG, self.PRE_RELEASE_TAG, loc_deploy_base_loc)
            self.deploy_release_save_file(self.RELEASE_TAG)

        if tar_eme.f_tag_exists(self.RELEASE_STAGING_TAG, dont_fail=1, quite=1):
            tar_eme.del_tag(self.RELEASE_STAGING_TAG, quite=1)

        self.log('    Applying newely released objects using tag {}.'.format(self.RELEASE_STAGING_TAG), 0)
        self.log('    ====> Trying to create save file for new release and loading in into target EME.', 0)
        self.emeobj.create_save_file(self.RELEASE_STAGING_TAG, base_loc=loc_deploy_base_loc)
        self.deploy_release_save_file(self.RELEASE_STAGING_TAG)

    def finally_create_abinitio_sandboxes(self):
        """
        This function creates abinitio sandboxes on env servers.

        Attribute
        :param : None
        :return: None
        :raises: None
        """
        self.log('Deploying code to  Abinitio servers.', 0)

        target_env = self.util.f_env_deploy_loc(self.ENV)
        env_owner = self.util.f_primary_owner(self.ENV)
        deploy_loc = '/home/{}/{}/sand_{}'.format(env_owner, target_env, self.RELEASE_TAG)

        sql = """
        select virtual_name from etl_mgr.etl_env_servers a, etl_mgr.etl_servers b
where a.server_id = b.server_id and env_id in (select env_id from etl_mgr.etl_environments where lower(env_name) = '{}')
""".format(target_env)
        df = self.util.run_sql(sql, env=self.ENV)

        if df.empty:
            self.f_error(
                "Could not find target server details for {} using sql.\n========> SQL used :\n     {} ".format(
                    target_env, sql))

        for server in df['VIRTUAL_NAME']:
            if server in ['lpschdenp01.npd.com', 'lpschdenp02.npd.com', 'lpwhdpld01.npd.com', 'lpwhdpld02.npd.com',
                          'lpschdplp02.npd.com', 'lpschdplp01.npd.com', 'lpschdenp04.npd.com', 'lpschdenp03.npd.com',
                          'lpschdenp04.npd.com', 'lpschdenp05.npd.com', 'lpschdenp06.npd.com', 'lpwhbend01.npd.com',
                          'lpschbenp01.npd.com', 'lpschbenp02.npd.com', 'lpwhbenu01.npd.com']:
                continue
            elif self.HOT_FIX_IND:
                self.log('Deploying HF release', 0)
                self.util.f_update_abinitio_sandboxes(server, env_owner, deploy_loc, self.NEW_HF_RELEASE_TAG)
            else:
                self.log('Deploying base release', 0)

                if self.f_check_if_base_released_deployed(server, env_owner, deploy_loc, self.RELEASE_TAG):
                    self.log('Base deploy for release is done. Skipping base release.', 0)
                else:
                    self.log('Base deploy for release is not done yet. Deploying base release.', 0)
                    self.util.f_update_abinitio_sandboxes(server, env_owner, deploy_loc, self.RELEASE_TAG, main_tag=1)

                self.log('Deploying Current release', 0)
                self.util.f_update_abinitio_sandboxes(server, env_owner, deploy_loc, self.RELEASE_STAGING_TAG)

    def f_check_if_base_released_deployed(self, server, owner, deploy_loc, release_tag):
        """
        This function checkes if base release is deployed.

        Attribute
        :param : None
        :return: None
        :raises: None
        """
        done_file_loc = "{}/.{}_done".format(deploy_loc, release_tag)
        LOC_CHECK = self.f_target_loc_type(owner, server, done_file_loc)

        if LOC_CHECK == 'NA':
            self.log("Basline release has not happened yet. Need to deploy.", 2)
            return False
        else:
            self.log("Basline release is complete.", 2)
            return True

    def deploy_release_save_file(self, TAG_NAME):
        """
        This function deployes save files to target environment.

        Attribute
        :param : None
        :return: None
        :raises: None
        """
        target_env = self.ENV
        target_eme_server = self.release_config['{}_EME_SERVER'.format(target_env)]
        target_AB_AIR_ROOT = self.release_config['{}_AB_AIR_ROOT'.format(target_env)]
        target_eme_owner = self.release_config['{}_EME_OWNER'.format(target_env)]

        if (target_env == 'MNA'):
            env = 'staging'
        else:
            env = target_env.lower()

        loc_deploy_base_loc = self.env_var['HOME'] + '/migration/eme_release'
        target_deploy_base_loc = '/home/{}/migration/eme_release'.format(target_eme_owner)

        self.log('Copying save file to {} and loading to {}.'.format(target_eme_server, target_AB_AIR_ROOT), 0)
        r_unix = unix.unix(server=target_eme_server, owner=target_eme_owner, log_level=self.LOG_LEVEL)

        self.log('Removing old dataset and Recreating folder', 0)
        cmd = "rm -f {}/{}.save".format(target_deploy_base_loc, TAG_NAME)
        r_unix.run(cmd)

        self.log('Creating top level release folder, if not present.', 0)
        cmd = "mkdir -p {}".format(target_deploy_base_loc)
        r_unix.run(cmd)

        self.log('Copying save file to target environment.', 0)
        cmd = 'scp {0}/{1}.save {2}@{3}:{4}/'.format(loc_deploy_base_loc, TAG_NAME, target_eme_owner, target_eme_server,
                                                     target_deploy_base_loc)
        self.unix.run(cmd)

        self.log('Loading save file {}/{}.save onto {} and loading to {}.'.format(target_deploy_base_loc, TAG_NAME,
                                                                                  target_eme_server,
                                                                                  target_AB_AIR_ROOT), 0)
        cmd = ". ~/.profile && air object load {}/{}.save".format(target_deploy_base_loc, TAG_NAME)
        r_unix.run(cmd)

    def f_build_ab_base_tag(self):
        """
        This function builds base release by copying files from previous release and its Hot-Fix.

        Attribute
        :param : None
        :return: None
        :raises: None
        """
        self.log('    ===> Trying to create baseline tag {} from tag  {} ,{} and {} .'.format(self.RELEASE_TAG,
                                                                                              self.PRE_RELEASE_TAG,
                                                                                              self.PRE_RELEASE_STAGING_TAG,
                                                                                              self.PRE_HF_RELEASE_TAG),
                 0)
        TAGS_TO_COMBINE = []

        if self.emeobj.f_tag_exists(self.PRE_RELEASE_TAG, dont_fail=1, quite=1):
            self.log('    ===> Tag {} exits.'.format(self.PRE_RELEASE_TAG), 0)
            TAGS_TO_COMBINE.append(self.PRE_RELEASE_TAG)
        else:
            self.log('    ===> Tag {} does not exit.'.format(self.PRE_RELEASE_TAG), 0)

        if self.emeobj.f_tag_exists(self.PRE_RELEASE_STAGING_TAG, dont_fail=1, quite=1):
            self.log('    ===> Tag {} exits.'.format(self.PRE_RELEASE_STAGING_TAG), 0)
            TAGS_TO_COMBINE.append(self.PRE_RELEASE_STAGING_TAG)
        else:
            self.log('    ===> Tag {} does not exit.'.format(self.PRE_RELEASE_STAGING_TAG), 0)

        if self.emeobj.f_tag_exists(self.PRE_HF_RELEASE_TAG, dont_fail=1, quite=1):
            self.log('    ===> Tag {} exits.'.format(self.PRE_HF_RELEASE_TAG), 0)
            TAGS_TO_COMBINE.append(self.PRE_HF_RELEASE_TAG)
        else:
            self.log('    ===> Tag {} does not exit.'.format(self.PRE_HF_RELEASE_TAG), 0)

        if TAGS_TO_COMBINE:
            self.log('    Combining tags to new release base tag.' + ' '.join(TAGS_TO_COMBINE), 0)
            self.emeobj.f_combine_tags(self.RELEASE_TAG, TAGS_TO_COMBINE)
        else:
            self.f_error('    ===> It appears no tags exists for previous release. there appears some issue')

    def f_get_env_servers(self, env):
        """
        This function pulls list of servers that are configured for environment.
        """
        if (env.upper() == 'MNA'):
            env = 'staging'
        else:
            env = env.lower()

        sql = """
        select virtual_name from etl_mgr.etl_env_servers a, etl_mgr.etl_servers b
where a.server_id = b.server_id and env_id in (select env_id from etl_mgr.etl_environments where lower(env_name) = '{}')
""".format(env)
        df = self.util.run_sql(sql, env=env)

        if df.empty:
            self.f_error(
                "Could not find target server details for {} using sql.\n========> SQL used :\n     {} ".format(
                    target_env, sql))

        return df['VIRTUAL_NAME']

    def deploy_code_to_servers(self, target_env, tar_loc, env_owner=''):
        """
        Deployes SVN build to environment specific folders.

        param str tar_loc : Location where tar file is saved
        param str target_env : Environment to shich code has to be deployed
        :return: None
        """
        self.log('Deploying SVN code package {} to {} environment servers .'.format(tar_loc, target_env), 0)

        if (target_env == 'MNA'):
            env = 'staging'
        else:
            env = target_env.lower()

        if env_owner == '':
            env_owner = 'ai' + env

        deploy_loc_base = "/home/{}/migration/svn_release".format(env_owner)
        deploy_loc = "{}/{}".format(deploy_loc_base, self.RELEASE_TAG)
        deploy_loc_workspace = "{}/workspace".format(deploy_loc)

        actual_base = "/home/{}/{}".format(env_owner, env)
        actual_workspace = "{}/hadoop_{}".format(actual_base, self.RELEASE_TAG)
        actual_npd_batch = "{}/npd_batch_{}".format(actual_base, self.RELEASE_TAG)

        for server in self.f_get_env_servers(env=env):
            r_unix = unix.unix(server=server, owner=env_owner, log_level=self.LOG_LEVEL)
            self.unix = unix.unix(log_level=self.LOG_LEVEL)

            self.log('Deploying code to  {} on {}.'.format(deploy_loc, server), 0)

            self.log('Removing old dataset and Recreating folder', 0)
            cmd = "rm -rf {0}.tar.gz".format(deploy_loc)
            r_unix.run(cmd)

            self.log('Creating top level folder', 0)
            cmd = "mkdir -p {0}".format(deploy_loc_base)
            r_unix.run(cmd)

            cmd = 'scp {0} {1}@{2}:{3}.tar.gz'.format(tar_loc, env_owner, server, deploy_loc)
            self.unix.run(cmd)

            self.log('Untarring package {}.tar.gz'.format(deploy_loc), 0)
            cmd = "tar -xvf {0}/{1} --directory {0} ".format(deploy_loc_base, self.RELEASE_TAG + '.tar.gz')
            r_unix.run(cmd)

            self.log('Changing permissions of ksh files at {}'.format(deploy_loc), 0)
            cmd = "find {} -type f -name '*.ksh' | xargs chmod +x ".format(deploy_loc)
            r_unix.run(cmd)

            self.log('Creating sandbox locations {} and {}.'.format(actual_workspace, actual_npd_batch), 0)
            cmd = " rm -rf {0}".format(actual_workspace)
            r_unix.run(cmd, dont_fail=1)
            cmd = " mkdir -p {0}".format(actual_workspace)
            r_unix.run(cmd, dont_fail=1)

            cmd = " rm -rf {0}".format(actual_npd_batch)
            r_unix.run(cmd, dont_fail=1)

            cmd = " mkdir -p {0}".format(actual_npd_batch)
            r_unix.run(cmd, dont_fail=1)

            self.log('Moving deployed code from {} to {}.'.format(deploy_loc_workspace, actual_workspace), 0)
            cmd = " mv {} {} ".format(deploy_loc_workspace, actual_workspace)
            r_unix.run(cmd)

            hydrograph_link_loc = '{}/workspace/npd/dsi/'.format(actual_workspace)
            hydrograph_link = '{}/npd_hydrograph/workspace/npd/dsi/npd_hydrograph'.format(actual_base)

            self.log('Adding Link for CNS hydrograph {} at location {}.'.format(hydrograph_link, hydrograph_link_loc),
                     0)
            cmd = "cd {}; ln -sf {} npd_hydrograph".format(hydrograph_link_loc, hydrograph_link)
            r_unix.run(cmd)

            self.log('Moving deployed code from {} to {}.'.format(deploy_loc, actual_npd_batch), 0)
            cmd = " mv {}/* {}".format(deploy_loc, actual_npd_batch)
            r_unix.run(cmd)

            self.log('Performing cleanup of temporary release area - {0}.'.format(deploy_loc_base), 0)
            cmd = " rm -rf {0}".format(deploy_loc_base)
            r_unix.run(cmd)

    def f_perform_sql_release(self):
        """
        This function builds SQL release.

        Attribute
        :param : None
        :return: None
        :raises: None
        """
        self.log("Initiating the DB release process.", 0)

        self.f_register_release_in_etl_versions()

        SVN_VERSION = self.RELEASE_TAG.split('.')[0] + '.dev'

        db_svnobj = svn.svn(REPO=self.release_config['DB_SVN_REPO'], log_level=self.LOG_LEVEL,
                            SVN_USER=self.release_config['DB_SVN_REPO_ID'],
                            SVN_PASS=self.release_config['DB_SVN_REPO_PWD'])
        SVN_SQL_LOC = "{}/tags/releases/dev/{}".format(self.release_config['DB_SVN_REPO'], SVN_VERSION)
        LOC_SQL_LOC = self.env_var['HOME'] + '/migration/db_release/' + self.RELEASE_TAG

        if db_svnobj.exists(SVN_SQL_LOC, quite=1):
            self.log("Checking out SQLs that are associated with current release.", 0)
            db_svnobj.f_checkout_proj(SVN_SQL_LOC, loc=LOC_SQL_LOC, no_loc_check=1)
            self.f_validate_sql_naming_convention(LOC_SQL_LOC)
            print
            "SQLs failed naming convention validations."
            print
            self.invalid_sql
            ##        self.valid_sql.sort_values(by=['Schema Run Order','Run Order'])
            self.valid_sql.set_index(['Schema Run Order', 'Run Order'], inplace=True)
            self.valid_sql.sort_index(inplace=True)
            self.f_create_db_release_folder()
            self.f_execute_n_register_sql()
            sql_rel = self.f_get_db_release_summary()
            print
            sql_rel
            print
            "SQL Release completed."
        else:
            self.log("There are no objects checked into SVN for this release. Skipping SQL deploy step.", 0)

        return 0

    def f_create_db_release_folder(self):
        """
        This function builds SQL release.

        Attribute
        :param : None
        :return: None
        :raises: None
        """
        self.log("Creating log location to store log files.", 0)
        MNA_DB_RELASE_BASE = self.release_config['MNA_DB_LOG_LOC']
        self.MNA_DB_RELEASE_MYSQL_LOG = MNA_DB_RELASE_BASE + '/' + self.RELEASE + '/' + 'MySQL'
        self.MNA_DB_RELEASE_LOG = MNA_DB_RELASE_BASE + '/' + self.RELEASE
        cmd = "mkdir -p {}".format(self.MNA_DB_RELEASE_MYSQL_LOG)
        self.unix.run(cmd)

    def f_validate_sql_naming_convention(self, base_loc):
        """
        This function builds SQL release.

        Attribute
        :param : None
        :return: None
        :raises: None
        """
        print
        "base_loc - {}".format(base_loc)
        cmd = 'find {} -type f -maxdepth 2 -name *.sql '.format(base_loc)
        self.unix.run(cmd)
        print
        "**************************************"
        print
        self.unix.out
        print
        "**************************************"
        sql_files = [s for s in self.unix.out.split('\n') if s != '']

        valid_sql = []
        invalid_sql = []

        for sql in sql_files:
            self.log('Validating naming conventions for SQL file : {}'.format(sql), 0)
            try:
                error = ''
                file_name = file_schema = file_type = ticket_details = project_name = file_exec_order = file_extension = sch_run_order = ''
                file_name = sql.split('/')[-1]
                file_name_splits = file_name.split('_')
                match_list = ['_dev_', '_DEV_', '_STAGE_']
                if len(file_name_splits) > 5:
                    if '/mysql/' in sql.lower():
                        file_sub = re.sub('|'.join(match_list), '~', file_name)
                        file_schema = file_sub.split('~')[0].upper()
                        file_name_sub_splits = file_sub.split('~')[1].split('_')
                        file_type = file_name_sub_splits[0].upper()
                        ticket_details = file_name_sub_splits[1].upper()
                        project_name = file_name_sub_splits[2].upper()
                    else:
                        file_schema = ('_').join(file_name_splits[:2]).upper()
                        file_type = file_name_splits[2].upper()
                        ticket_details = file_name_splits[3].upper()
                        project_name = file_name_splits[4].upper()
                    file_exec_order = file_name_splits[-1].split('.')[0]
                    file_extension = file_name.split('.')[-1].upper()
                    try:
                        sch_run_order = self.VALID_SCHEMAS[file_schema]
                    except KeyError:
                        error = 'Invalid Schema NAme'
                else:
                    error = 'Invalid File naming Convention.'
            except ValueError:
                error = 'filename(as per convention).'

            ticket_details = self.format_pke_number(ticket_details)

            error = error + self.is_invalid_schema(file_schema)
            error = error + self.is_invalid_file_type(file_type)
            error = error + self.is_invalid_pke(ticket_details)
            error = error + self.is_invalid_project(project_name)
            error = error + self.is_invalid_extension(file_extension)

            if error.strip() == '':
                self.log('  ----> Validating Passed', 0)
                valid_sql.append(
                    [file_name, file_schema, file_type, ticket_details, project_name, file_exec_order, file_extension,
                     sch_run_order, sql])
            else:
                self.log('  ----> Validating Failed', 0)
                invalid_sql.append(
                    [file_name, file_schema, file_type, ticket_details, project_name, file_exec_order, file_extension,
                     sch_run_order, 'Invalid: ' + error, sql])

        valid_df_col = ['File Name', 'Schema', 'Type', 'Ticket', 'Project', 'Run Order', 'Extension',
                        'Schema Run Order', 'Full Path']
        invalid_df_col = ['File Name', 'Schema', 'Type', 'Ticket', 'Project', 'Run Order', 'Extension',
                          'Schema Run Order', 'Error Details', 'Full Path']

        self.valid_sql = pd.DataFrame(valid_sql, columns=valid_df_col)
        self.invalid_sql = pd.DataFrame(invalid_sql, columns=invalid_df_col)

    def f_execute_n_register_sql(self):
        """
        This function runs SQLs part of a release.
        """
        self.sql_status = []
        self.sql_comments = []
        ## This pulls the DB Version for current release.
        db_base, db_patch, db_version = self.f_get_db_version_for_release(self.RELEASE_TAG)

        for index, row in self.valid_sql.iterrows():
            S_LINE = '*' * 80
            self.log("{}\nTrying to execute SQL in file {} in {} with schema as {}\n{}".format(S_LINE, row['Full Path'],
                                                                                               self.ENV, row['Schema'],
                                                                                               S_LINE), 0)
            ## Register SQL in PM_OBJECTS if not registered
            sql_deploy_path = row['Schema'].lower() + '/' + db_version + '/' + row['File Name']
            sql_id = self.util.f_register_sql(sql_deploy_path, row['Full Path'], row['File Name'], row['Schema'],
                                              row['Type'])
            ## Register SQL in PM_OBJECT_TAGGIS if not registered. -1 implies not executed
            self.util.f_register_obj_n_tag(row['Full Path'], row['Ticket'], 1, ob_id=sql_id)

            if self.util.f_sql_execution_status(sql_id, row['Ticket'], row['Full Path'], env=self.ENV):
                self.log("    --->SQL has been already executed", 0)
                self.sql_status.append('Success')
                self.sql_comments.append('Executed in previous Run')
            else:
                self.log("    --->SQL has not been already executed. Trying to execute it.", 0)

                rc = self.f_execute_sqls(row['Full Path'], env=self.ENV, schema=row['Schema'],
                                         sql_name=row['File Name'])
                if rc == 0:
                    self.log("Execution of SQL was successful. Updating execution status.", 0)
                    self.util.f_update_sql_execution_status(row['Full Path'], sql_id, row['Ticket'], self.RELEASE,
                                                            self.RELEASE_TAG, env=self.ENV)
                    ## Notes are used to pull DB deploy package
                    self.f_update_sql_notes(sql_id, db_version, row['Ticket'])
                else:
                    self.log("Execution of SQL failed. Skipping update of execution status.", 0)

        print
        self.sql_status
        print
        self.sql_comments

        self.valid_sql['Status'] = pd.Series(self.sql_status, index=self.valid_sql.index)
        self.valid_sql['Comments'] = pd.Series(self.sql_comments, index=self.valid_sql.index)

    def f_update_sql_notes(self, obj_id, db_rel, ticket):
        """
        This function updates SQL notes. These notes are used for generating deploy package.
        """
        sql = """
         update  ETL_RPT.PM_OBJECT_TAGGING set notes = 
         (select max(lower(substr(object_name,0,instr(object_name,'_',5)-1)) ||'/{0}/'||  object_name)
          from ETL_RPT.PM_OBJECTS where OBJECT_ID = {1}
          ) where OBJECT_ID = {1} and ticket_number = '{2}'        
        """.format(db_rel, obj_id, ticket)

        df1 = self.util.run_insert_sql(sql, owner='ETL_RPT')

    def f_execute_sqls(self, sqlfile, env='dev', schema='ETL_USER', sql_name=''):
        """
        This function Executes SQL and MYSQL against DB.

        Attribute
        :param :
           sql : Filename having actual SQL in it
           DB  : Environment against which SQL/MYSQL has to be executed.
           schema : Schema owner.
        :return: None
        :raises: None
        """
        if '/mysql/' in sqlfile.lower():
            mysql_log_file = self.MNA_DB_RELEASE_MYSQL_LOG + '/' + sql_name
            mysql_err_file = self.MNA_DB_RELEASE_MYSQL_LOG + '/' + sql_name + '.error'
            mysql_succ_file = self.MNA_DB_RELEASE_MYSQL_LOG + '/' + sql_name + '.success'
            self.util.f_run_mysql_in_file(sqlfile, mysql_log_file, env=env, schema=schema)
            if "ERROR " in open(mysql_log_file).read():
                cmd = 'mv {} {}'.format(mysql_log_file, mysql_err_file)
                self.unix.run(cmd)
                self.log("Execution Status : Failed.", 0)
                self.sql_status.append('Failed')
                link_details = "\\pwnas\aipvwarehouse\dev\DSI\DB_RELEASE\MySQL\{}".format(sql_name + ".error")
                self.sql_comments.append("<a href = {}> Error Details </a>".format(link_details))
                self.log("Copying SQL to log location {}".format(self.MNA_DB_RELEASE_MYSQL_LOG), 0)
                cmd = 'cp {} {}'.format(sqlfile, self.MNA_DB_RELEASE_MYSQL_LOG)
                self.unix.run(cmd)
                return 1
            else:
                cmd = 'mv {} {}'.format(mysql_log_file, mysql_succ_file)
                self.unix.run(cmd)
                self.log("Execution Status : Success.", 0)
                self.sql_status.append('Success')
                link_details = "\\pwnas\aipvwarehouse\dev\DSI\DB_RELEASE\MySQL\{}".format(sql_name + ".success")
                self.sql_comments.append("<a href = {}> Error Details </a>".format(link_details))
                self.log("Copying SQL to log location {}".format(self.MNA_DB_RELEASE_MYSQL_LOG), 0)
                cmd = 'cp {} {}'.format(sqlfile, self.MNA_DB_RELEASE_MYSQL_LOG)
                self.unix.run(cmd)
                return 0
        else:
            output, error = self.util.f_run_sql_in_file(sqlfile, env=env, schema=schema)
            self.log("Copying SQL to log location {}".format(self.MNA_DB_RELEASE_LOG), 0)
            cmd = 'cp {} {}'.format(sqlfile, self.MNA_DB_RELEASE_LOG)
            self.unix.run(cmd)
            if 'ERROR' in output:
                self.log("Execution Status : Failed.", 0)
                self.log("Failed running SQL in File. Error Details \n: {}".format(output), 3)
                self.sql_status.append('Failed')
                log_file = self.MNA_DB_RELEASE_LOG + '/' + sql_name + ".error"
                lfh = open(log_file, 'w')
                lfh.write(output)
                lfh.close()
                link_details = "\\pwnas\aipvwarehouse\dev\DSI\DB_RELEASE\{}".format(sql_name + ".error")
                self.sql_comments.append("<a href = {}> Error Details </a>".format(link_details))
                return 1
            else:
                self.log("Execution Status : Success.", 0)
                self.log("Successfully ran SQL in File. Message Details \n: {}".format(output), 3)
                self.sql_status.append('Success')
                ##self.sql_comments.append(output)
                log_file = self.MNA_DB_RELEASE_LOG + '/' + sql_name + ".success"
                lfh = open(log_file, 'w')
                lfh.write(output)
                lfh.close()
                link_details = "\\pwnas\aipvwarehouse\dev\DSI\DB_RELEASE\{}".format(sql_name + ".success")
                self.sql_comments.append("<a href = {}> Error Details </a>".format(link_details))
                return 0

    def format_pke_number(self, inval):
        """
        This function formats PKE to have leading zeros if required.

        Attribute
        :param : None
        :return: None
        :raises: None
        """

        inval_3 = inval[:3]

        if inval_3 == 'PKE':
            pke_number = 'PKE' + inval[3:].zfill(12)
        elif inval_3 == 'BUG':
            pke_number = 'BUG' + inval[3:]
        else:
            pke_number = inval

        return pke_number

    def is_invalid_schema(self, inval):
        """
        This function builds SQL release.

        Attribute
        :param : None
        :return: None
        :raises: None
        """
        if inval in self.VALID_SCHEMAS.keys():
            return ''
        else:
            return 'Schema:'

    def is_invalid_file_type(self, inval):
        """
        This function builds SQL release.

        Attribute
        :param : None
        :return: None
        :raises: None
        """
        VALID_TYPES = ['DDL', 'DML', 'PLSQL']

        if inval in VALID_TYPES:
            return ''
        else:
            return 'Type(ddl/dml/plsql):'

    def is_invalid_pke(self, pke_number):
        """
        This function builds SQL release.

        Attribute
        :param : None
        :return: None
        :raises: None
        """
        inval_3 = pke_number[:3]

        if inval_3 == 'PKE':
            pke_number = 'PKE' + pke_number[3:].zfill(12)
        elif inval_3 == 'BUG':
            pke_number = 'BUG' + pke_number[3:]
        else:
            return 'PKE/Bug:'

        if self.release_tickets is None:
            self.release_tickets = self.f_pull_release_tickets().tolist()
            print
            self.release_tickets

        if pke_number in self.release_tickets:
            return ''
        else:
            return 'PKE/Bug:'

    def is_invalid_project(self, inval):
        """
        This function builds SQL release.

        Attribute
        :param : None
        :return: None
        :raises: None
        """
        if len(self.emeobj.f_match_proj_with_master_list(inval)) == 0:
            if len(self.svnobj.f_match_proj_with_master_list(inval)) == 0:
                return 'Project:'

        return ''

    def is_invalid_extension(self, inval):
        """
        This function builds SQL release.

        Attribute
        :param : None
        :return: None
        :raises: None
        """
        VALID_EXTNS = ['SQL']

        if inval in VALID_EXTNS:
            return ''
        else:
            return 'Extension(sql):'

    def f_generate_release_summary_report(self, email_to='', email_cc=''):
        """
        This function generate release summary.
        """
        msg = {}
        msg1 = open(self.RELEASE_SUMMARY_TEMPLATE).read()
        msg1 = msg1.decode('utf-8')

        rel_summary = self.f_get_release_summary()
        if self.ENV == 'MNA':
            user_id = 'aistaging'
            env = 'staging'
        else:
            user_id = 'ai' + self.ENV.lower()
            env = self.ENV.lower()

        rel_sand_validation = self.f_get_sandbox_summary(env, user_id)
        table1 = rel_sand_validation.to_html(index=False).replace('<th>',
                                                                  """<th style="font-family:'Calibri';font-size:12.0pt;background-color:'DodgerBlue">""").encode(
            'utf-8')
        table1 = table1.replace('<td>', """<td style="font-family:'Calibri';font-size:12.0pt">""")

        rel_tkt_summary = self.f_get_release_ticket_summary()
        table2 = rel_tkt_summary.to_html(index=False).replace('<th>',
                                                              """<th style="font-family:'Calibri';font-size:12.0pt;background-color:'DodgerBlue">""").encode(
            'utf-8')
        table2 = table2.replace('<td>', """<td style="font-family:'Calibri';font-size:12.0pt">""")

        db_release_summary = self.f_get_db_release_summary()
        table3 = db_release_summary.to_html(index=False).replace('<th>',
                                                                 """<th style="font-family:'Calibri';font-size:12.0pt;background-color:'DodgerBlue">""").encode(
            'utf-8')
        table3 = table3.replace('<td>', """<td style="font-family:'Calibri';font-size:12.0pt">""")

        msg1 = msg1.replace('xxx_release_xxx', self.RELEASE)
        msg1 = msg1.replace('xxx_release_tag_xxx', self.RELEASE_TAG)
        msg1 = msg1.replace('xxx_env_xxx', self.ENV)
        msg1 = msg1.replace('xxx_release_status_xxx', 'Deployed')

        rel_message = "Code has been deployed and SQL pacakges have been exceuted for the release. Please validate your changes. Also review SQLs that have failed and fix them. We will change links once developer confirms validation of the objects."
        msg1 = msg1.replace('xxx_message_xxx', rel_message)

        msg1 = msg1.replace('xxx_release_summary_xxx', rel_summary)
        msg1 = msg1.replace('xxx_sand_summary_xxx', table1)
        msg1 = msg1.replace('xxx_ticket_summary_xxx', table2)
        msg1 = msg1.replace('xxx_db_release_xxx', table3)

        msg['Subject'] = "{} : {} Release Summary".format(self.ENV, self.RELEASE_TAG)
        msg['From'] = 'Release_Team'

        if email_to == '':
            msg['To'] = 'Ranjeeth.Kyatham@npd.com;Jingming.Ma@npd.com;Vishal.Sharma@npd.com;Ashis.Das@npd.com'
        else:
            msg['To'] = email_to

        if email_cc == '':
            msg['Cc'] = 'Ranjeeth.Kyatham@npd.com;Jingming.Ma@npd.com'
        else:
            msg['Cc'] = email_cc

        msg['Body'] = msg1

        self.util.f_send_email(msg)

    def f_get_db_release_summary(self):
        """
        Gets DB release summary for the release.
        """
        if self.ENV == "MNA":
            sql = """select
    object_name,Object_type, ticket_number, case when QA_RELEASE = '{0}' then 'Success' else 'Failed' end STATUS, ' ' LINK
from
     ETL_RPT.PM_OBJECT_TAGGING OT, ETL_RPT.PM_OBJECTS OB
where
 OT.object_id = OB.object_id and ticket_number in
 (select ticket_number from ETL_RPT.pm_releasing where ACTIVE_FLAG = 1 and QA_RELEASE = '{0}') and ( object_type like 'SQL%' or object_type like 'MYSQL%' )
order by ticket_number,object_type,object_name
""".format(self.RELEASE)
        else:
            rel_chk = self.f_get_table_check_sql()
            sql = """
select
    object_name,Object_type, ticket_number, case when {0}_RELEASE = '{1}' then 'Success' else 'Failed' end STATUS
from
     ETL_RPT.PM_OBJECT_TAGGING OT, ETL_RPT.PM_OBJECTS OB
where
 OT.object_id = OB.object_id and ticket_number in
 (select ticket_number from ETL_RPT.pm_releasing where ACTIVE_FLAG = 1 and {2}) and (object_type like 'SQL%' or object_type like 'MYSQL%' )
order by ticket_number,object_type,object_name
""".format(self.ENV, self.RELEASE, rel_chk)
        print
        sql
        df1 = self.util.run_sql(sql)

        if self.ENV == "MNA":
            for ix in df1.index:
                if 'MYSQL' in df1.loc[ix, 'OBJECT_TYPE']:
                    link = """\\\\pwnas\\aipvwarehouse\\dev\\DSI\\DB_RELEASE\\{}\\{}\\{}""".format(self.RELEASE,
                                                                                                   'MySQL', df1.loc[
                                                                                                       ix, 'OBJECT_NAME'])
                else:
                    link = """\\\\pwnas\\aipvwarehouse\\dev\\DSI\\DB_RELEASE\\{}\\{}""".format(self.RELEASE, df1.loc[
                        ix, 'OBJECT_NAME'])

                if df1.loc[ix, 'STATUS'] == "Success":
                    link1 = "{}.success".format(link)
                else:
                    link1 = "{}.error".format(link)

                df1.loc[ix, 'LINK'] = link1

        return df1

    def f_get_table_check_sql(self, tab_alias=''):
        """
        form SQL part for checking release column.
        """
        if self.ENV == 'MNA' or self.ENV == 'QA':
            rel_check = " {}QA_RELEASE = '{}' ".format(tab_alias, self.RELEASE)
        elif self.ENV == 'UAT':
            rel_check = " {}UAT_RELEASE = '{}' ".format(tab_alias, self.RELEASE)
        elif self.ENV == 'PROD':
            rel_check = " {}PROD_RELEASE = '{}' ".format(tab_alias, self.RELEASE)
        else:
            f_error("Invalid value for environment variable. Value is : {}".self.ENV)

        return rel_check

    def f_get_release_summary(self):
        """
        This function generate release summary.
        """

        rel_check = self.f_get_table_check_sql()

        sql = """
        select count(distinct case when ticket_number like 'PKE%' then ticket_number end ) tickets, 
          count(distinct case when ticket_number like 'BUG%' then ticket_number end ) bugs,
          count(distinct ticket_number) total  
         from ETL_RPT.PM_OBJECT_TAGGING where {}
         """.format(rel_check)

        df1 = self.util.run_sql(sql)

        sql = """
        select count(distinct case when object_path like '/Projects/%' then object_name end ) abinitio, 
             count(distinct case when object_path like '/npd/%'  then object_name end ) svn,
             count(distinct case when object_type like '%SQL%' or object_type like 'ODS_%' then object_name end ) sqls,
             count(distinct object_name) total
         from ETL_RPT.PM_OBJECT_TAGGING OT, ETL_RPT.PM_OBJECTS OB where OT.object_id = OB.object_id and {}
         """.format(rel_check)

        df2 = self.util.run_sql(sql)

        top_summary = """
        <table style="width:30%", border="3">
        <tr>
           <th colspan="2" , style = "font-family:'Calibri';font-size:12.0pt;background-color: DodgerBlue">Ticket Summary</th>
           <th colspan="2" , style = "font-family:'Calibri';font-size:12.0pt;background-color: DodgerBlue">Object Summary</th>
        </tr>
        <tr>
           <td>Total Tickets in Release </td>
           <td>{} </td>
           <td>Total Objects in Release </td>
           <td> {} </td>
        </tr>
        <tr>
            <td>     Remedy Tickets </td>
            <td> {} </td>
            <td>     Abinitio Objects </td>
            <td> {} </td>
        </tr>
        <tr>
            <td>     Bugzilla Tickets</td>
            <td> {} </td>
            <td>    SVN Objects</td>
            <td> {} </td>

        </tr>
        <tr>
            <td>  </d>
            <td>  </td>
            <td>    DB Objects</td>
            <td> {} </td>
        </tr>
        </table>
        """.format(df1['TOTAL'][0], df2['TOTAL'][0], df1['TICKETS'][0], df2['ABINITIO'][0], df1['BUGS'][0],
                   df2['SVN'][0], df2['SQLS'][0])

        top_summary = top_summary.replace('<td>', """<td style="font-family:'Calibri';font-size:12.0pt">""")
        return top_summary

    def f_get_sandbox_summary(self, env, owner, servers=""):
        """
        This function pulls objects in sandboxes on deployment server.
        """
        if servers == "":
            servers = self.f_get_env_servers(self.ENV)

        wrk_stats = []

        for server in servers:
            r_unix = unix.unix(server=server, owner=owner, log_level=self.LOG_LEVEL)

            self.log('Pulling object counts for deployed sandboxes on {}'.format(server), 3)
            srv_stats = [server]

            for wrk in ['sand', 'hadoop', 'npd_batch']:
                base_loc = '/home/{}/{}/{}/'.format(owner, env, wrk + '_' + self.RELEASE_TAG)
                cmd = "find {} -type f | wc -l ".format(base_loc)
                r_unix.run(cmd, quite=1)
                self.log('    Total objects in {} = {} '.format(base_loc, r_unix.out), 3)
                srv_stats.append(r_unix.out.replace("\n", ""))

            wrk_stats.append(srv_stats)

        df = pd.DataFrame(wrk_stats,
                          columns=['Server Name', 'Abinitio Sand', 'Hadoop Workspace', 'NPD Batch Workspace'])

        return df

    def f_get_release_ticket_summary(self, include_bug=1, email=''):
        """
        This function gets details of the tickets in release.
        """
        rel_check = self.f_get_table_check_sql(tab_alias='PR.')

        sql = """
            select PR.TICKET_NUMBER ||'-  '|| SUMMARY TICKET_NUMBER ,replace(replace(OBJECT_PATH,'/Projects/NPD/OPS','$SBASE'),'/npd/dsi/npd_hadoop/publish','$BASE') OBJECT_PATH, max(OBJECT_VERSION) OBJECT_VERSION,max(OT.ADDED_USER) ADDED_USER from 
   ETL_RPT.PM_RELEASING PR, ETL_RPT.PM_OBJECT_TAGGING OT, ETL_RPT.PM_OBJECTS PO, ETL_RPT.PM_TICKETS PT
where 
   {} and
   OT.TICKET_NUMBER = PR.TICKET_NUMBER and
   PO.OBJECT_ID = OT.OBJECT_ID and
   PT.TICKET_NUMBER = PR.TICKET_NUMBER and
   PR.ACTIVE_FLAG = 1
group by  PR.TICKET_NUMBER ,SUMMARY,OBJECT_PATH  
order by 1,2
             """.format(rel_check)

        tkts = self.util.run_sql(sql)
        ## Blank out repeatation of ticket number for objects in same ticket
        pre = ' '
        for ix in tkts.index:
            if pre == tkts.loc[ix, 'TICKET_NUMBER']:
                tkts.loc[ix, 'TICKET_NUMBER'] = ''
            else:
                pre = tkts.loc[ix, 'TICKET_NUMBER']

        return tkts

    def f_release_initiation(self, include_bug=1, email_cc='', email_to='', iteration=0):
        """
        This function send release initiation email.
        """
        msg = {}

        if os.path.isfile(self.RELEASE_INIT_TEMPLATE + '.' + self.RELEASE.strip()):
            msg1 = open(self.RELEASE_INIT_TEMPLATE + '.' + self.RELEASE.strip()).read()
        elif os.path.isfile(self.RELEASE_INIT_TEMPLATE):
            msg1 = open(self.RELEASE_INIT_TEMPLATE).read()
        else:
            self.error("Template file {} is missing. Please fix this.".format(self.RELEASE_INIT_TEMPLATE))

        ##msg1 = msg1.decode('utf-8')

        msg1 = msg1.replace('xxx_release_xxx', self.RELEASE)
        msg1 = msg1.replace('xxx_release_tag_xxx', self.RELEASE_TAG)
        msg1 = msg1.replace('xxx_env_xxx', self.ENV)
        msg1 = msg1.replace('xxx_release_status_xxx', 'Initiated')

        if iteration > 0:
            ADD_ITERATION = "- {}".format(iteration)
        else:
            ADD_ITERATION = ""

        msg['Subject'] = "{} : {}-{} Release Reminder {}".format(self.ENV, self.RELEASE_TAG.split('.')[0], self.RELEASE,
                                                                 ADD_ITERATION)
        msg['From'] = 'Release_Team'

        if email_to is None or email_to == '':
            msg['To'] = 'Ranjeeth.Kyatham@npd.com;Jingming.Ma@npd.com;vishal.sharma@npd.com@npd.com'
        else:
            msg['To'] = email_to

        if email_cc is None or email_cc == '':
            msg['Cc'] = 'Ranjeeth.Kyatham@npd.com;Jingming.Ma@npd.com'
        else:
            msg['Cc'] = email_cc

        msg['Body'] = msg1

        self.log("Sending email to {}".format(msg['To']), 0)
        self.util.f_send_email(msg)
        return 0

    def f_release_ticket_summary(self, include_bug=1, email_to='', email_cc=''):
        """
        This function send release ticket details to group.
        """
        msg = {}

        if include_bug:
            TEMPLATE = self.RELEASE_TKT_SUM_TEMPLATE
        else:
            TEMPLATE = self.RELEASE_TKT_ONLY_SUM_TEMPLATE

        if os.path.isfile(TEMPLATE):
            msg1 = open(TEMPLATE).read()
        else:
            self.error("Template file {} is missing. Please fix this.".format(self.RELEASE_INIT_TEMPLATE))

        ##msg1 = msg1.decode('utf-8')

        # table1 = self.f_get_release_tickets(TICKET_TYPE='PKE').to_html(index = False).replace('<th>',"""<th style="font-family:'Calibri';font-size:12.0pt;background-color:'DodgerBlue">""").encode('utf-8')
        table1 = self.f_get_release_tickets_comb(TICKET_TYPE='AZU').to_html(index=False).replace('<th>',
                                                                                                 """<th style="font-family:'Calibri';font-size:12.0pt;background-color:'DodgerBlue">""").encode(
            'utf-8')
        table1 = table1.replace('<td>', """<td style="font-family:'Calibri';font-size:12.0pt">""")

        if include_bug:
            table2 = self.f_get_release_tickets(TICKET_TYPE='BUG').to_html(index=False).replace('<th>',
                                                                                                """<th style="font-family:'Calibri';font-size:12.0pt;background-color:'DodgerBlue">""").encode(
                'utf-8')
            table2 = table2.replace('<td>', """<td style="font-family:'Calibri';font-size:12.0pt">""")

        plan_msg = """
        Please find list of the tickets that are staged for this release to xxx_env_xxx. Please review this list carefully and let release team know if anything needs to be added or removed.
        """
        msg1 = msg1.replace('xxx_msg_xxx', plan_msg)
        msg1 = msg1.replace('xxx_release_xxx', self.RELEASE)
        msg1 = msg1.replace('xxx_release_tag_xxx', self.RELEASE_TAG)
        msg1 = msg1.replace('xxx_env_xxx', self.ENV)
        msg1 = msg1.replace('xxx_release_status_xxx', 'Planning')

        msg1 = msg1.replace('xxx_release_status_xxx', 'Planning')

        msg1 = msg1.replace('xxx_ticket_summary_xxx', table1)

        if include_bug:
            msg1 = msg1.replace('xxx_bug_summary_xxx', table2)

        msg['Subject'] = "{} : {} Release Planned. Please Review.".format(self.ENV, self.RELEASE_TAG)
        msg['From'] = 'Release_Team'
        msg['Body'] = msg1

        if email_to is None or email_to == '':
            ##          msg['To'] = 'ETL_DEV@npd.com;DSI_Offshore@npd.com'
            msg['To'] = 'Ranjeeth.Kyatham@npd.com;Jingming.Ma@npd.com;Vishal.sharma@npd.com'
        else:
            msg['To'] = email_to.replace(' ', '')

        if email_cc is None or email_cc == '':
            msg['CC'] = 'Ranjeeth.Kyatham@npd.com;Jingming.Ma@npd.com;Vishal.sharma@npd.com;'
        else:
            msg['CC'] = email_cc.replace(' ', '')

        self.log("Sending email to {}".format(msg['To']), 0)
        self.util.f_send_email(msg)
        return 0

    def f_get_release_tickets_comb(self, TICKET_TYPE=''):
        """
        This function send release ticket details to group.
        """
        rel_check = self.f_get_table_check_sql(tab_alias='PR.')

        sql = """
        select case when LEAD = 'Stephanie Shen' then ASSIGNEE else LEAD end as lead,
       ASSIGNEE,TICKET_NUMBER,SUMMARY,QA_DISCUSSION,DB_CHANGE,ODS_CHANGE,IMPACT,QA_BASELINE,TEST_PLAN,PRIORITY,RELATED_PROJECT,APPLICATION
from
(SELECT (select FIRST_NAME ||' ' || LAST_NAME from ETL_RPT.PM_RESOURCES where RESOURCE_ID = LEAD) LEAD,
      (select FIRST_NAME ||' ' || LAST_NAME from ETL_RPT.PM_RESOURCES where RESOURCE_ID = PR.ASSIGNEE) ASSIGNEE,
      PR.TICKET_NUMBER, substr(SUMMARY,1,150) SUMMARY,
      regexp_replace(QA_DISCUSSION,'None|Undefined|No',' ') QA_DISCUSSION,
      regexp_replace(DB_CHANGE,'None|Undefined|No',' ') DB_CHANGE,
      regexp_replace(ODS_CHANGE,'Undefined|None|No',' ') ODS_CHANGE,
      regexp_replace(IMPACT,'\n|Undefined|None|NONE|No',' ') IMPACT,
      regexp_replace(QA_BASELINE,'Undefined|None|No|NA|ne',' ') QA_BASELINE,
      TEST_PLAN,
      PT.PRIORITY,
      PT.RELATED_PROJECT,
      PT.APPLICATION
FROM ETL_RPT.pm_releasing PR, ETL_RPT.PM_TICKETS PT
where {} and PT.TICKET_NUMBER = PR.TICKET_NUMBER and (PR.TICKET_NUMBER like '{}%' or PR.TICKET_NUMBER like 'PKE%')
and PR.ACTIVE_FLAG = 1
) Y
order by 1 ,2
       """.format(rel_check, TICKET_TYPE)

        tkts = self.util.run_sql(sql)

        ##        tkts.set_index(['LEAD'],inplace=True)
        ##        tkts.sort_index(inplace=True)
        ## Blank out repeatation of ticket number for objects in same ticket
        ##        pre = ' '
        ##        for ix in tkts.index :
        ##            if pre == tkts.loc[ix,'LEAD'] :
        ##                tkts.loc[ix,'LEAD'] = ''
        ##            else :
        ##                pre = tkts.loc[ix ,'LEAD']

        return tkts

    def f_get_release_tickets(self, TICKET_TYPE=''):
        """
        This function send release ticket details to group.
        """
        rel_check = self.f_get_table_check_sql(tab_alias='PR.')

        sql = """
        select case when LEAD = 'Stephanie Shen' then ASSIGNEE else LEAD end as lead,
       ASSIGNEE,TICKET_NUMBER,SUMMARY,QA_DISCUSSION,DB_CHANGE,ODS_CHANGE,IMPACT,QA_BASELINE,TEST_PLAN,PRIORITY,RELATED_PROJECT,APPLICATION
from       
(SELECT (select FIRST_NAME ||' ' || LAST_NAME from ETL_RPT.PM_RESOURCES where RESOURCE_ID = LEAD) LEAD,
      (select FIRST_NAME ||' ' || LAST_NAME from ETL_RPT.PM_RESOURCES where RESOURCE_ID = PR.ASSIGNEE) ASSIGNEE, 
      PR.TICKET_NUMBER, substr(SUMMARY,1,150) SUMMARY,
      regexp_replace(QA_DISCUSSION,'None|Undefined|No',' ') QA_DISCUSSION, 
      regexp_replace(DB_CHANGE,'None|Undefined|No',' ') DB_CHANGE,
      regexp_replace(ODS_CHANGE,'Undefined|None|No',' ') ODS_CHANGE,
      regexp_replace(IMPACT,'\n|Undefined|None|NONE|No',' ') IMPACT, 
      regexp_replace(QA_BASELINE,'Undefined|None|No|NA|ne',' ') QA_BASELINE,
      TEST_PLAN,
      PT.PRIORITY, 
      PT.RELATED_PROJECT,
      PT.APPLICATION
FROM ETL_RPT.pm_releasing PR, ETL_RPT.PM_TICKETS PT 
where {} and PT.TICKET_NUMBER = PR.TICKET_NUMBER and PR.TICKET_NUMBER like '{}%' 
and PR.ACTIVE_FLAG = 1
) Y
order by 1 ,2
       """.format(rel_check, TICKET_TYPE)

        tkts = self.util.run_sql(sql)

        ##        tkts.set_index(['LEAD'],inplace=True)
        ##        tkts.sort_index(inplace=True)
        ## Blank out repeatation of ticket number for objects in same ticket
        ##        pre = ' '
        ##        for ix in tkts.index :
        ##            if pre == tkts.loc[ix,'LEAD'] :
        ##                tkts.loc[ix,'LEAD'] = ''
        ##            else :
        ##                pre = tkts.loc[ix ,'LEAD']

        return tkts

    def f_target_loc_type(self, owner, server, loc, log_level=0):
        """ This function checks what a link points to """
        r_unix = unix.unix(server=server, owner=owner, log_level=self.LOG_LEVEL)
        cmd = "file {}".format(loc)
        r_unix.run(cmd, quite=1)

        if 'No such file or directory' in r_unix.out:
            out_value = 'NA'
        elif ': symbolic link to' in r_unix.out:
            link_dest = r_unix.out.split('`')[-1].replace("'", "").replace("\n", "")
            out_value = 'LINK:{}'.format(link_dest)
        elif ': directory' in r_unix.out:
            out_value = 'DIRECTORY'
        else:
            out_value = 'FILE'

        return out_value

    def f_check_sanity_performance_after_release(self, env=''):
        """ This function creates sanity performance report, by comparing a sanity job with previous sessions from same JOB_ID
            Attributes:
            env str : Target environment where sanity jobs are running, and defined in ETL_MGR.ETL_SANITY_FREQ
        """
        self.log(
            " ******************** Start f_check_sanity_performance_after_release, to create Sanity Performance Report *****************",
            0)
        if env == "":
            env = self.ENV

        PERCENTAGE_THRESHOLD = 0.0
        PREVIOUS_DAYS = 0
        EPORT_EMAIL_ADDRESS = ''
        PERCENTAGE_THRESHOLD = self.sanity_performance.f_get_percentage_threshold(env)
        PREVIOUS_DAYS = self.sanity_performance.f_get_previous_days_for_comparing(env)
        REPORT_EMAIL_ADDRESS = self.sanity_performance.f_get_email_address_for_report(env)
        self.sanity_performance.f_check_sanity_performance(env, PERCENTAGE_THRESHOLD, PREVIOUS_DAYS,
                                                           REPORT_EMAIL_ADDRESS)
        self.log(" ******************** End f_check_sanity_performance_after_release *****************", 0)

    def f_change_permissions_after_release(self, env='', owner='', servers=None):
        """ This function corrects permissions for .ksh, .sh, and .py files on the servers for account aiprod/aiuat/aiqa.
            Attributes:
            env str : Target environment where permissions need to be changed. Used for finding server details."
        """
        if env == "":
            env = self.ENV

        if (env == 'MNA'):
            target_env = 'staging'
        else:
            target_env = env.lower()

        if servers == None:
            servers = self.f_get_env_servers(env)

        if owner == '':
            owner = 'ai' + target_env

        ba_path = "/home/ai{0}/{0}".format(target_env)

        self.log(
            " ******************** Processing on correction of permissions for .ksh, .sh, and .py files, for all severs *****************",
            0)
        self.f_change_all_permissions(env, ba_path, owner, servers)
        self.log(" ******************** Completed on changing permissions. *****************", 0)
        return 0

    def f_change_all_permissions(self, env, ba_path, owner, servers):
        """ This function changes  permissions of .ksh, .sh and .py on all servers """
        for server in servers:
            self.log("=" * 80, 0)
            self.log("=" * 80, 0)
            for proj in ['sand', 'hadoop', 'npd_batch']:
                self.log("Changing permissions for {}, on Server {}".format(proj, server), 0)
                self.f_change_permission(server, owner, ba_path, proj)

        self.log("=== Permissions changed.", 0)

        return 0

    def f_change_permission(self, server, owner, ba_path, proj):
        """ This function changes  permission of .ksh, .sh, and .py  """
        pr_path = "{}/{}/".format(ba_path, proj)
        r_unix = unix.unix(server=server, owner=owner, log_level=self.LOG_LEVEL)
        cmd = "find {} -type f -name '*.ksh' -o -name '*.py' -o -name '*.sh'| xargs chmod +x".format(pr_path)
        r_unix.run(cmd, quite=1, dont_fail=1)
        return 0

    def f_change_passwd_after_release(self, env='', owner='', servers=None):
        """ This function changes password on the servers for account aiprod/aiuat.
            Both curr_password and new_password in format of (key:value) are saved in /home/ai/Release/python/.release_password_change_{}.txt
            Attributes:
            env str : Target environment where password needs to be changed. Used for finding server details."
        """
        if env == "":
            env = self.ENV

        if (env == 'MNA'):
            target_env = 'staging'
        else:
            target_env = env.lower()

        if servers == None:
            servers = self.f_get_env_servers(env)

        if owner == '':
            owner = 'ai' + target_env

        RELEASE_PASSWORD_CHANGE_FILE = "/home/ai/Release/python/.release_password_change_{}.txt".format(self.ENV)
        RELEASE_PASSWORD_CHANGE_FILE_BAK = "/home/ai/Release/python/.release_password_change_{}_BAK-{}.txt".format(
            self.ENV, self.RELEASE)
        self.log("***looking for Password Change file - {} ...".format(RELEASE_PASSWORD_CHANGE_FILE), 0)

        if os.path.isfile("{}".format(RELEASE_PASSWORD_CHANGE_FILE)):
            self.release_password_change = self.util.get_config(RELEASE_PASSWORD_CHANGE_FILE)
            key_curr = 'curr_password'
            key_new = 'new_password'
            if key_curr in self.release_password_change and key_new in self.release_password_change:
                curr_pass = self.release_password_change['curr_password'].strip()
                new_pass = self.release_password_change['new_password'].strip()
                if curr_pass == '' or new_pass == '':
                    self.log(
                        "******Could not find curr_password or new_password in Password Change file - {}. Make sure you have the right format of key:value inside file. Skip changing password process.".format(
                            RELEASE_PASSWORD_CHANGE_FILE), 0)
                else:
                    self.log(
                        " ------------------- Changing password from current {} to new {} ------------------------ ".format(
                            curr_pass, new_pass), 0)
                    self.f_change_all_password(env, curr_pass, new_pass, owner, servers)
                    self.log("   ------rename the password file to {}".format(RELEASE_PASSWORD_CHANGE_FILE_BAK), 0)
                    rn_cmd = "mv -f {} {}".format(RELEASE_PASSWORD_CHANGE_FILE, RELEASE_PASSWORD_CHANGE_FILE_BAK)
                    os.system(rn_cmd)
                    self.log(" ------------------- Changing password completed ------------------------ ", 0)
            else:
                self.log(
                    "******Could not find curr_password or new_password in Password Change file - {} . Skip changing password process.".format(
                        RELEASE_PASSWORD_CHANGE_FILE), 0)
        else:
            self.log("******The Password Change file - {} does not exist. Skip changing password process.".format(
                RELEASE_PASSWORD_CHANGE_FILE), 0)

        return 0

    def f_change_all_password(self, env, curr_pass, new_pass, owner, servers):
        """ This function changes password on the servers
        """
        for server in servers:
            self.log("=" * 80, 0)
            self.log("=" * 80, 0)
            if server not in ['lpscaimlp1.npd.com', 'lpscaimlp02.npd.com', 'lpscaimlp01.npd.com']:
                self.log("Changing password for Server : {}".format(server), 0)
                self.f_change_password(server, owner, curr_pass, new_pass)

            self.log("=== ", 0)

        return 0

    def f_change_password(self, server, owner, curr_pass, new_pass):
        """ This function changes password on the server"""
        r_unix = unix.unix(server=server, owner=owner, log_level=self.LOG_LEVEL)
        cmd = """echo -e "{0}\n{1}\n{1}" | passwd""".format(curr_pass, new_pass)
        r_unix.run(cmd, quite=1)
        return 0

    def f_change_release_links(self, env='', target_version='', owner='', servers=None):
        """ This functions changes links on the servers to newer release version
            Attributes:
            env str : Target environment where link needs to be changed. Used for finding server details and path details."
            target_version str : version to which link needs to be changed. It will be same as self.RELEASE_TAG in most cases.
        """
        if env == "":
            env = self.ENV

        if (env == 'MNA'):
            target_env = 'staging'
        else:
            target_env = env.lower()

        if target_version == "":
            target_version = self.RELEASE_TAG

        if servers == None:
            servers = self.f_get_env_servers(env)

        if owner == '':
            owner = 'ai' + target_env

        self.log(" ******************** Processing Standard sandboxes Links *****************", 0)
        self.f_change_all_links(env, target_version, owner, servers)
        self.log(" ******************** Standard sandboxes Link processing completed*****************", 0)
        self.f_change_non_std_release_links()
        return 0

    def f_change_all_links(self, env, target_version, owner, servers):
        """ This functions changes links on the servers to newer release version
            Attributes:
            env str : Target environment where link needs to be changed. Used for finding server details and path details."
            target_version str : version to which link needs to be changed. It will be same as self.RELEASE_TAG in most cases.
        """

        if (env == 'MNA'):
            target_env = 'staging'
        else:
            target_env = env.lower()

        BASE = "/home/" + owner + "/{}/".format(target_env)
        ABINITION_LOC = BASE + "sand"
        HADOOP_LOC = BASE + "hadoop"
        NPD_BATCH_LOC = BASE + "npd_batch"

        LINKS = [ABINITION_LOC, HADOOP_LOC, NPD_BATCH_LOC]

        for server in servers:
            self.log("=" * 80, 0)
            self.log("Link Processing for Server : {}".format(server), 0)
            self.log("=" * 80, 0)
            for LINK in LINKS:
                if LINK in [ABINITION_LOC] and server in ['lpschdenp01.npd.com', 'lpschdenp02.npd.com',
                                                          'lpwhdpld01.npd.com', 'lpwhdpld02.npd.com',
                                                          'lpschdenp04.npd.com', 'lpwhbend01.npd.com',
                                                          'lpschdenp03.npd.com', 'lpschdenp04.npd.com',
                                                          'lpschdenp05.npd.com', 'lpschdenp06.npd.com',
                                                          'lpschbenp01.npd.com', 'lpschbenp02.npd.com',
                                                          'lpwhbenu01.npd.com']:
                    continue

                self.log("====> LINK  : {} ".format(LINK), 0)
                CHK_VALUE = self.f_target_loc_type(owner, server, LINK)

                LINK_BASE = LINK.split('/')[-1]
                target_folder = LINK_BASE + "_" + target_version
                target_loc = BASE + target_folder

                if 'DIRECTORY' not in self.f_target_loc_type(owner, server, target_loc):
                    self.f_error(
                        "Target {} does not exist on server {}. Link can not be created.".format(target_loc, server))

                if 'LINK' in CHK_VALUE:
                    CURR_LINK_TO = CHK_VALUE.split(':')[-1]
                    self.log("  current link {} on {} points to {}".format(LINK, server, CURR_LINK_TO), 3)

                    if CURR_LINK_TO != target_folder:
                        self.log(
                            "========> {} is being changed to {} from {}.".format(LINK, target_folder, CURR_LINK_TO), 0)
                        self.f_change_link(server, owner, LINK, target_folder)
                    else:
                        self.log(" ========> {} is pointing to {}. No change is required.".format(LINK, target_folder,
                                                                                                  server), 0)

                elif 'DIRECTORY' in CHK_VALUE:
                    self.log(" ========> {} is not a link on server {} so NO change in required.".format(LINK, server),
                             0)
                else:
                    self.log(" ========> {} does not exists. Creating it.".format(LINK, server), 0)
                    self.f_change_link(server, owner, LINK, target_folder)

                self.log(" ", 0)

        return 0

    def f_change_link(self, server, owner, link_nm, target):
        """ This functions changes links on the servers to newer release version"""
        r_unix = unix.unix(server=server, owner=owner, log_level=self.LOG_LEVEL)
        cmd = "rm -f {0} ".format(link_nm)
        r_unix.run(cmd, quite=1)

        cmd = "ln -sf {} {}".format(target, link_nm)
        r_unix.run(cmd)
        return 0

    def f_change_non_std_release_links(self, env='', target_version=''):
        """ This functions changes links for any non-standard sandboxes for the release."""
        self.log('=' * 80, 0)
        self.log("************************ Non Standard sandbox processing *************************", 0)
        self.log('=' * 80, 0)

        sandboxes = self.f_get_non_standard_sandboxes()

        for key in sandboxes:
            if key in self.release_config:
                users_n_servers = self.release_config[key].strip()
                if key == 'QA_NON_STD_SANDBOXES':
                    user_env = 'DEV'
                else:
                    user_env = self.ENV

                if users_n_servers != 'None' and users_n_servers != '':
                    for data in users_n_servers.split('#'):
                        user = data.split('@')[0].strip()
                        servers = data.split('@')[1].split(',')
                        self.log("-" * 80, 0)
                        self.log(" Non Standard sandbox Links for {} on servers : {}".format(user, ','.join(servers)),
                                 0)
                        self.f_change_all_links(env=user_env, target_version=self.RELEASE_TAG, owner=user,
                                                servers=servers)
            else:
                self.log("There are no non-standard sandboxes configured for update in {}.".format(RELEASE_CONFIG_FILE),
                         0)
                self.log(" ", 0)

        self.log("************************Non Standard sandbox update completed sucessfully************************", 0)
        return 0

    def f_stop_schedulers_for_env(self):
        self.util.f_stop_schedulers_for_env(self.ENV)
        return 0

    def f_start_schedulers_for_env(self):
        self.util.f_start_schedulers_for_env(self.ENV)
        return 0

    def f_get_non_standard_sandboxes(self):
        if self.ENV == 'MNA':
            sandboxes = ['DEV_NON_STD_SANDBOXES', 'MNA_NON_STD_SANDBOXES']
        elif self.ENV == 'QA':
            sandboxes = ['QA_NON_STD_SANDBOXES']
        elif self.ENV == 'UAT':
            sandboxes = ['UAT_NON_STD_SANDBOXES']
        elif self.ENV == 'PROD':
            sandboxes = ['PROD_NON_STD_SANDBOXES']
        else:
            sandboxes = []

        self.log("Processing Non-Standard sandboxes keys : {}".format(','.join(sandboxes)), 0)

        return sandboxes;

    def f_create_non_standard_sandboxes(self, sand_type=''):
        """ This functions updates any non-standard sandboxes for the release."""
        self.log('=' * 80, 0)
        self.log("************************ Non Standard sandbox processing *************************", 0)
        self.log('=' * 80, 0)

        sandboxes = self.f_get_non_standard_sandboxes()

        for key in sandboxes:
            self.log(" Processing {}".format(key), 0)
            if key in self.release_config:
                self.log(" Processing {}".format(self.release_config[key].strip()), 0)
                user_n_server = self.release_config[key].strip()

                if key == 'QA_NON_STD_SANDBOXES':
                    user_env = 'DEV'
                else:
                    user_env = self.ENV

                if user_n_server != 'None' and user_n_server != '':
                    sand_type = sand_type.strip().upper()
                    print
                    "sand_type - {}".format(sand_type)
                    if sand_type == 'ABINITIO':
                        self.f_process_sandboxes_for_users(user_n_server, user_env)
                    elif sand_type == 'SVN':
                        self.f_process_svn_code_deploy_for_users(user_n_server, user_env)
                    else:
                        self.f_error(
                            'Invalid sand_type value of {} passed. valid values are ABINITIO | SVN.'.format(sand_type))
            else:
                self.log("There are no non-standard sandboxes configured for update in {}.".format(RELEASE_CONFIG_FILE),
                         0)
                self.log(" ", 0)

        self.log("************************Non Standard sandbox update completed sucessfully************************", 0)
        return 0

    def f_process_sandboxes_for_users(self, users_n_servers, user_env):
        """ This functions parses user and servers string and calls update sandboxes on them.
            Attributes
            users_n_servers : string with user@server1,server2#user2@server
        """
        for data in users_n_servers.split('#'):
            user = data.split('@')[0].strip()
            servers = data.split('@')[1].split(',')

            target_env = self.util.f_env_deploy_loc(user_env)
            self.log("Environment Details for deployment is - {}".format(target_env), 0)
            deploy_loc = '/home/{}/{}/sand_{}'.format(user, target_env, self.RELEASE_TAG)

            if user == '':
                self.f_error(
                    'Invalid non standard sandbox update configuration[{}] in {}.'.format(data, RELEASE_CONFIG_FILE))

            for server in servers:
                if server.strip() == '' or server in ['lpschdenp01.npd.com', 'lpschdenp02.npd.com',
                                                      'lpwhdpld01.npd.com', 'lpwhdpld02.npd.com', 'lpschdenp04.npd.com',
                                                      'lpschdenp03.npd.com', 'lpschdenp04.npd.com',
                                                      'lpschdenp05.npd.com', 'lpschdenp06.npd.com',
                                                      'lpschbenp01.npd.com', 'lpschbenp02.npd.com',
                                                      'lpwhbenu01.npd.com']:
                    continue

                if self.HOT_FIX_IND:
                    self.log('Deploying HF release', 0)
                    self.util.f_update_abinitio_sandboxes(server, user, deploy_loc, self.NEW_HF_RELEASE_TAG)
                else:
                    self.log('Deploying base release', 0)
                    if self.f_check_if_base_released_deployed(server, user, deploy_loc, self.RELEASE_TAG):
                        self.log('Base deploy for release is done. Skipping base release.', 0)
                    else:
                        self.log('Base deploy for release is not done yet. Deploying base release.', 0)
                        self.util.f_update_abinitio_sandboxes(server, user, deploy_loc, self.RELEASE_TAG)

                    self.log('Deploying Current release', 0)
                    self.util.f_update_abinitio_sandboxes(server, user, deploy_loc, self.RELEASE_STAGING_TAG)

    def f_process_svn_code_deploy_for_users(self, users_n_servers, user_env):
        """ This functions parses user and servers string and calls update sandboxes on them.
            Attributes
            users_n_servers : string with user@server1,server2#user2@server
        """
        env = user_env
        self.set_svn_release_var()
        tar_loc = self.C_WRK_LOC + '.tar.gz'

        for data in users_n_servers.split('#'):
            env_owner = data.split('@')[0].strip()
            servers = data.split('@')[1].split(',')

            target_env = self.util.f_env_deploy_loc(user_env)

            deploy_loc_base = "/home/{}/migration/svn_release".format(env_owner)
            deploy_loc = "{}/{}".format(deploy_loc_base, self.RELEASE_TAG)
            deploy_loc_workspace = "{}/workspace".format(deploy_loc)

            actual_base = "/home/{}/{}".format(env_owner, target_env)
            actual_workspace = "{}/hadoop_{}".format(actual_base, self.RELEASE_TAG)
            actual_npd_batch = "{}/npd_batch_{}".format(actual_base, self.RELEASE_TAG)

            if env_owner == '':
                self.f_error(
                    'Invalid non standard sandbox update configuration[{}] in {}.'.format(data, RELEASE_CONFIG_FILE))

            for server in servers:
                r_unix = unix.unix(server=server, owner=env_owner, log_level=self.LOG_LEVEL)
                self.unix = unix.unix(log_level=self.LOG_LEVEL)
                self.log('Deploying code to  {} on {}.'.format(deploy_loc, server), 0)

                if server.strip() == '':
                    continue

                self.log('Removing old dataset and Recreating folder', 0)
                cmd = "rm -rf {0}.tar.gz".format(deploy_loc)
                r_unix.run(cmd)

                self.log('Creating top level folder', 0)
                cmd = "mkdir -p {0}".format(deploy_loc_base)
                r_unix.run(cmd)

                cmd = 'scp {0} {1}@{2}:{3}.tar.gz'.format(tar_loc, env_owner, server, deploy_loc)
                self.unix.run(cmd)

                self.log('Untarring package {}.tar.gz'.format(deploy_loc), 0)
                cmd = "tar -xvf {0}/{1} --directory {0} ".format(deploy_loc_base, self.RELEASE_TAG + '.tar.gz')
                r_unix.run(cmd)

                if self.HOT_FIX_IND:
                    self.log('Deploying SVN HF release', 0)
                ##                    self.util.f_update_abinitio_sandboxes(server,user,deploy_loc,self.NEW_HF_RELEASE_TAG)
                else:
                    self.log('Creating sandbox locations {} and {}.'.format(actual_workspace, actual_npd_batch), 0)
                    cmd = " rm -rf {0}".format(actual_workspace)
                    r_unix.run(cmd, dont_fail=1)
                    cmd = " mkdir -p {0}".format(actual_workspace)
                    r_unix.run(cmd, dont_fail=1)

                    cmd = " rm -rf {0}".format(actual_npd_batch)
                    r_unix.run(cmd, dont_fail=1)

                    cmd = " mkdir -p {0}".format(actual_npd_batch)
                    r_unix.run(cmd, dont_fail=1)

                    self.log('Moving deployed code from {} to {}.'.format(deploy_loc_workspace, actual_workspace), 0)
                    cmd = " mv {} {} ".format(deploy_loc_workspace, actual_workspace)
                    r_unix.run(cmd)

                    hydrograph_link_loc = '{}/workspace/npd/dsi/'.format(actual_workspace)
                    hydrograph_link = '{}/npd_hydrograph/workspace/npd/dsi/npd_hydrograph'.format(actual_base)

                    self.log('Adding Link for CNS hydrograph {} at location {}.'.format(hydrograph_link,
                                                                                        hydrograph_link_loc), 0)
                    cmd = "cd {}; ln -sf {} npd_hydrograph".format(hydrograph_link_loc, hydrograph_link)
                    r_unix.run(cmd)

                    self.log('Moving deployed code from {} to {}.'.format(deploy_loc, actual_npd_batch), 0)
                    cmd = " mv {}/* {}".format(deploy_loc, actual_npd_batch)
                    r_unix.run(cmd)

    def f_process_send_ods_changes_summary(self, include_bug=1, email_to='', email_cc=''):
        """
        This function Send tickets with ODS changes to DB team.
        """
        self.log("Generating email with ODS changes for {} release to {}".format(self.RELEASE_TAG, self.ENV), 0)

        msg = {}

        if os.path.isfile(self.RELEASE_HEADER_TEMPLATE):
            msg1 = open(self.RELEASE_HEADER_TEMPLATE).read()
        else:
            self.f_error("Template file {} is missing. Please fix this.".format(self.RELEASE_HEADER_TEMPLATE))

        ods_pkes = self.f_get_tickets_with_ods_changes()

        if ods_pkes is None:
            msg2 = " There are no tickets with ODS changes for this release."
        else:
            table1 = ods_pkes.to_html(index=False).replace('<th>',
                                                           """<th style="font-family:'Calibri';font-size:12.0pt;background-color:'DodgerBlue">""").encode(
                'utf-8')
            table1 = table1.replace('<td>', """<td style="font-family:'Calibri';font-size:12.0pt">""")

            msg2 = " Please find details of the tickets with ODS changes.\n {}\n Please let DSI release team know if any questions.".format(
                table1, )

        msg1 = msg1.replace('xxx_release_xxx', self.RELEASE)
        msg1 = msg1.replace('xxx_env_xxx', self.ENV)
        msg1 = msg1.replace('xxx_message_xxx', msg2)

        msg['Subject'] = 'ODS Changes for {} Release'.format(self.RELEASE)
        msg['From'] = 'Release_Team'
        msg['Body'] = msg1

        if email_to is None or email_to == '':
            ##          msg['To'] = 'ETL_DEV@npd.com;DSI_Offshore@npd.com'
            msg['To'] = 'Ranjeeth.Kyatham@npd.com;Jingming.Ma@npd.com;Vishal.sharma@npd.com'
        else:
            msg['To'] = email_to.replace(' ', '')

        if email_cc is None or email_cc == '':
            msg['CC'] = 'Ranjeeth.Kyatham@npd.com;Jingming.Ma@npd.com;Vishal.sharma@npd.com;'
        else:
            msg['CC'] = email_cc.replace(' ', '')

        self.log("Sending email to {} : with CC as {} ".format(msg['To'], msg['CC']), 0)
        self.util.f_send_email(msg)
        return 0

    def f_get_tickets_with_ods_changes(self, include_bug=1):
        """
        This function gets tickets with ODS changes.
        """
        self.log("Pulling tickets for {} to {} with ODS changes".format(self.RELEASE_TAG, self.ENV), 0)

        if include_bug:
            bug_chk = ""
        else:
            bug_chk = " AND A.TICKET_NUMBER like 'PKE%'"

        rel_chk = self.f_get_table_check_sql()

        sql = """
        SELECT A.TICKET_NUMBER,B.SUMMARY,B.ASSIGNEE
        from ETL_RPT.PM_RELEASING A, ETL_RPT.PM_TICKETS B 
        WHERE UPPER(ODS_CHANGE) = 'YES' AND {} AND A.ACTIVE_FLAG = 1 AND
        A.TICKET_NUMBER = B.TICKET_NUMBER {}
        """.format(rel_chk, bug_chk)

        df = self.util.run_sql(sql)

        if df.empty:
            return None

        return df

    def f_register_release_in_etl_versions(self):
        """
        This function registers release in ETL_MGR.ETL_RELEASE_VERSIONS.
        V3_0_44 : implies app_ver - 3 min_ver - 44 and rel_ver - 0
        """
        self.log("Registering release {} in ETL_VERSIONS table.".format(self.RELEASE_TAG), 0)

        (new_base, new_patch, new_db_ver) = self.f_get_db_version_for_release(self.RELEASE_TAG)

        if new_base is None:
            (base, patch, db_ver) = self.f_get_db_version_for_release(self.PRE_RELEASE_TAG)

            if base is None:
                self.error("===>Previous release entry({}) does not exist in ETL_MGR.ETL_VERSIONS. Please fix this.")
            else:
                if patch == 9:
                    new_patch = 0
                    new_base += 1
                    new_db_version = 'b{}'.format(new_base)
                else:
                    new_patch = int(patch) + 1
                    new_base = base
                    new_db_version = 'b{}p{}'.format(new_base, new_patch)

            self.log("===>Registering release {} and DB version {} in ETL_MGR.ETL_VERSIONS.".format(self.RELEASE,
                                                                                                    new_db_version), 0)

            (app_ver, min_ver, rel_ver) = self.f_split_release_versions(self.RELEASE_TAG)

            sql = """
            INSERT INTO ETL_MGR.ETL_VERSIONS(RELEASE_VERSION,MINOR_VERSION,APP_VERSION,
            RELEASE_NOTES,RELEASE_DATE,RELEASE_USER,DB_RELEASE_VERSION)
            values
            ({},{},{},'QA release {}',sysdate,'Rel_System','{}')
            """.format(rel_ver, min_ver, app_ver, self.RELEASE, new_db_version)

            df = self.util.run_insert_sql(sql, owner='etl_mgr')
        else:
            self.log("===>Release {} is already registered in ETL_MGR.ETL_VERSIONS with DB version as {}.".format(
                self.RELEASE, new_db_ver), 0)

        return 0

    def f_split_release_versions(self, tag):
        """
        This function splits release tag into seperate versions tuple (App version,minor version and release version).
        V3_0_44 : implies app_ver - 3 min_ver - 44 and rel_ver - 0
        """
        rep_list = ['.QA', '.UAT', '.PROD']

        app_ver = tag.split('_')[0].replace('V', '')
        min_ver_sub = tag.split('_')[2]
        min_ver = re.sub('|'.join(rep_list), '', min_ver_sub)
        rel_ver = tag.split('_')[1]

        self.log("APP_VERSION : {}         MINOR_VERSION : {}            RELEASE_VERSION : {}".format(app_ver, min_ver,
                                                                                                      rel_ver), 3)

        return (app_ver, min_ver, rel_ver)

    def f_get_db_version_for_release(self, tag):
        """
        This function get DB version details for the tag.
        V3_0_44 : implies app_ver - 3 min_ver - 44 and rel_ver - 0
        """
        self.log("===>Trying to get DB release version associated with release {}.".format(tag), 0)

        (app_ver, min_ver, rel_ver) = self.f_split_release_versions(tag)

        sql = """
            SELECT DB_RELEASE_VERSION FROM ETL_MGR.ETL_VERSIONS
            WHERE APP_VERSION = {} AND MINOR_VERSION = {} AND  RELEASE_VERSION = {}
        """.format(app_ver, min_ver, rel_ver)

        df = self.util.run_sql(sql)

        if df.empty:
            return (None, None, None)
        else:
            db_version = df['DB_RELEASE_VERSION'][0]
            if 'p' in db_version and 'b' in db_version:
                base = db_version.split('p')[0].replace('b', '')
                patch = db_version.split('p')[1].strip()
            elif 'b' in db_version:
                base = db_version.replace('b', '').strip()
                patch = 0
            else:
                self.f_error(
                    "===>DB Release version {} is not in valid format for release {}.valid format is b<<nnn>>p<<nn>> or b<<nn>> where <<nn>> is version number".format(
                        db_version, tag))

        return base, patch, db_version

    def f_get_db_deploy_package(self):
        """
        This function get DB scripts that will be deployed along with path summary for release.
        """
        sql = " "

    def f_kill_running_jobs(self):
        """
        This kills any running jobs.
        """
        self.f_send_jobs_being_killed_email()
        self.util.f_kill_env_job(self.ENV)
        return 0

    def f_send_jobs_being_killed_email(self, email_to='', email_cc=''):
        """
        Send email with jobs details to release_team that will be killed.
        """
        msg = {}
        running_jobs = self.util.f_get_runing_session_on_env(self.ENV)
        release = self.RELEASE
        msg1 = open(self.RELEASE_HEADER_TEMPLATE).read()
        msg1 = msg1.decode('utf-8')

        msg1 = msg1.replace('xxx_release_xxx', release.replace('QA', self.ENV))
        msg1 = msg1.replace('xxx_env_xxx', self.ENV)
        table1 = running_jobs.to_html(index=False).replace('<th>',
                                                           '<th style = "background-color: DodgerBlue">').encode(
            'utf-8')
        msg2 = "<h2> Following jobs are being killed to fascilitate release.</h2><br> " + """<style="font-size:10.0pt;font-family:'Calibr">""" + table1 + "</style>"

        msg1 = msg1.replace('xxx_message_xxx', msg2)

        msg['Subject'] = "Killed Jobs for {} Release".format(self.RELEASE)
        msg['From'] = 'Release_Team'
        msg['Body'] = msg1

        if email_to is None or email_to == '':
            ##          msg['To'] = 'ETL_DEV@npd.com;DSI_Offshore@npd.com'
            msg['To'] = 'Ranjeeth.Kyatham@npd.com;Jingming.Ma@npd.com;Vishal.sharma@npd.com'
        else:
            msg['To'] = email_to.replace(' ', '')

        if email_cc is None or email_cc == '':
            msg['CC'] = 'Ranjeeth.Kyatham@npd.com;Jingming.Ma@npd.com;Vishal.sharma@npd.com;'
        else:
            msg['CC'] = email_cc.replace(' ', '')

        self.log("Sending email to {} : with CC as {} ".format(msg['To'], msg['CC']), 0)

        self.util.f_send_email(msg)

    def f_schedulers_sanity_jobs_for_env(self, email_to='', email_cc=''):
        """
        This function schedules sanity jobs for release.
        """
        server = self.util.f_get_env_servers(self.ENV, primary_ind='y')
        primary_server = server[0]
        target_env = self.util.f_env_deploy_loc(self.ENV)
        env_owner = self.util.f_primary_owner(self.ENV)
        sanity_graph_loc = '/home/{}/{}/sand/NPD/OPS/SYSTEM/BATCH/mp/sanity_jobs_sheduler.mp'.format(env_owner,
                                                                                                     target_env)

        r_unix = unix.unix(server=primary_server, owner=env_owner, log_level=self.LOG_LEVEL)

        self.log(
            'Calling sanity job scheduler program on server {} for user {} at loc {}'.format(primary_server, env_owner,
                                                                                             sanity_graph_loc), 0)
        cmd = ". ~/.profile && export CURRENT_RELEASE_VERSION='{}'; export PREVIOUS_RELEASE_VERSION='{}' && air sandbox run {}".format(
            self.RELEASE_TAG, self.PRE_RELEASE_TAG, sanity_graph_loc)
        r_unix.run(cmd)

        return r_unix.rc

    def f_process_release_sanity_status(self, email_to='', email_cc=''):
        """
        This function checks sanity jobs status and send summary email.
        """
        data = self.f_get_sanity_job_status()
        msg = {}
        release = self.RELEASE
        msg1 = open(self.RELEASE_HEADER_TEMPLATE).read()
        msg1 = msg1.decode('utf-8')

        msg1 = msg1.replace('xxx_release_xxx', release.replace('QA', self.ENV))
        msg1 = msg1.replace('xxx_env_xxx', self.ENV)
        table1 = data.to_html(index=False).replace('<th>',
                                                   """<th style="font-family:'Calibri';font-size:12.0pt;background-color:'DodgerBlue">""").encode(
            'utf-8')
        table1 = table1.replace('<td>', """<td style="font-family:'Calibri';font-size:12.0pt">""")
        table1 = table1.replace("FAILED", '<span style="background-color: #f18973"><b>FAILED</b></span> ')
        table1 = table1.replace("COMPLETED", '<span style="background-color: #d5f4e6"><b>COMPLETED</b></span> ')

        msg2 = """<style="font-size:10.0pt;font-family:'Calibr'"> <b> Please find below statuses of the sanity jobs.</b><br> """ + table1 + "</style>"

        msg1 = msg1.replace('xxx_message_xxx', msg2)

        msg['Subject'] = "{}:Sanity Job(s) Status for {} Release".format(self.ENV, self.RELEASE)
        msg['From'] = 'Release_Team'
        msg['Body'] = msg1

        if email_to is None or email_to == '':
            msg['To'] = 'Ranjeeth.Kyatham@npd.com;Jingming.Ma@npd.com;Vishal.sharma@npd.com'
        else:
            msg['To'] = email_to.replace(' ', '')

        if email_cc is None or email_cc == '':
            msg['CC'] = 'Ranjeeth.Kyatham@npd.com;Jingming.Ma@npd.com;Vishal.sharma@npd.com;'
        else:
            msg['CC'] = email_cc.replace(' ', '')

        self.log("Sending email to {} : with CC as {} ".format(msg['To'], msg['CC']), 0)

        self.util.f_send_email(msg)
        return 0

    def f_get_sanity_job_status(self):
        """
        This function pulls sanity jobs status from DB.
        """
        self.log('Pulling sanity job status from DB.', 0)
        sql = """
SELECT 
   BUS_FREQ, JOB_NAME,JOB_ID,X.JOB_LOG_ID,PPMONTH,PPWEEK,STATUS_NAME,(SELECT MODULE_NAME FROM ETL_MGR.ETL_MODULES MM WHERE MM.MODULE_ID = Y.MODULE_ID ) LAST_MODULE
FROM
    (   
    SELECT A.BUSINESS||'/'||A.DATA_SOURCE||A.FREQUENCY BUS_FREQ, JOB_NAME, A.JOB_ID, A.JOB_LOG_ID, A.PPMONTH, A.PPWEEK, STATUS_NAME 
    FROM ETL_MGR.ETL_JOB_LOG A, ETL_MGR.ETL_JOBS B, ETL_MGR.ETL_STATUSES C
    WHERE 
    A.RUN_USER = '{0}' AND A.JOB_ID = B.JOB_ID AND A.STATUS = C.STATUS and
    A.JOB_ID in (select JOB_ID from ETL_MGR.ETL_SANITY_FREQ)
    ) X, 
    (
    SELECT JOB_LOG_ID, MODULE_ID, STATUS
    FROM
    (
     SELECT
      A.JOB_LOG_ID, A.MODULE_ID, A.STATUS,
      RANK() OVER (PARTITION BY A.JOB_LOG_ID ORDER BY J.MODULE_RUN_ORDER) MODULE_RANK 
    FROM ETL_MGR.ETL_MODULE_LOG A, ETL_MGR.ETL_JOB_LOG B , ETL_MGR.ETL_JOB_DETAILS J
    WHERE A.JOB_LOG_ID = B.JOB_LOG_ID AND A.STATUS = B.STATUS 
      AND J.JOB_ID = B.JOB_ID AND J.MODULE_ID = A.MODULE_ID AND B.RUN_USER = '{0}'
    )  
    WHERE MODULE_RANK = 1
    ) Y
WHERE   
    X.JOB_LOG_ID = Y.JOB_LOG_ID 
ORDER BY STATUS_NAME,X.JOB_LOG_ID    
       """.format(self.RELEASE_TAG)

        data = self.util.run_sql(sql, self.ENV)

        return data

    def f_stop_all_crons_for_env(self):
        """
        This process stops crons for the env
        """
        self.log('Initaiting backup of crons for the env {}.'.format(self.ENV), 0)
        self.util.f_backup_env_crons(self.ENV)
        self.log('Initaiting stop of crons for the env {}.'.format(self.ENV), 0)
        self.util.f_stop_env_crons(self.ENV)
        return 0

    def f_start_all_crons_for_env(self):
        """
        This process stops crons for the env
        """
        self.log('Initaiting start of crons for the env {}.'.format(self.ENV), 0)
        self.util.f_start_env_crons(self.ENV)
        return 0

    def f_release_folder_cleanup(self, versions_to_clean=-2):
        """
        This process stops crons for the env
        """
        self.log('Initaiting cleanup of teh release area in {}.'.format(self.ENV), 0)
        cleanup_version = self.f_get_older_release_version(versions_to_clean)

    def f_get_older_release_version(self, versions_to_clean=-2):
        """
        Gets previous release details from  ETL_RPT.PM_RELEASE_TAGS

        Attribute
        :return: None
        :raises: None
        """
        self.log('Trying to get old version details from DB.', 2)

        if self.ENV == 'MNA':
            test_env = 'QA'
        else:
            test_env = self.ENV

        sql = """
         select RELEASE_TAG,RELEASE from ETL_RPT.PM_RELEASE_TAGS where RELEASE = (select max(RELEASE) from
         ETL_RPT.PM_RELEASE_SCHEDULES where release < '{}' and RELEASE_PHASE = '{}' and HOT_FIX_FLAG = 0)
         """.format(self.RELEASE, test_env)

        df = self.util.run_sql(sql)
        if df.empty:
            self.f_error(
                "Could not find Previous release tag details from ETL_RPT.PM_RELEASE_SCHEDULES. Please define release with tag details.\n========> SQL used :\n     {} ".format(
                    sql))
        else:
            self.PRE_BASE_RELEASE_TAG = df['RELEASE_TAG'][0]
            self.PRE_RELEASE = df['RELEASE'][0]
