import traceback
import os
import re
import shutil

from handler_base import HandlerBase
from gdrivesync import GDriveSync


class SyncHandler(HandlerBase):
    LOC = '~/'

    def get(self):
        self.logger.info('synchandler ' + str(self.request.uri))
        try:
            self.set_gtok()
            gdrive_repos = SyncHandler.get_gdrive_repos()
            gapi_keys = self.settings['google_oauth']
            self.rendertpl("sync.tpl",
                           gdrive_repos=gdrive_repos,
                           browser_api_key=gapi_keys['browser_api_key'],
                           appid=gapi_keys['key'],
                           authtok=GDriveSync.AUTH_TOK,
                           user_id=GDriveSync.USER_ID)
        except:
            traceback.print_exc()
            self.logger.info('Not authenticated yet. Redirecting for Google auth.')
            self.redirect('/auth/')

    def set_gtok(self):
        tokfile = self.settings['token_file']

        self.logger.debug('Checking for auth token at ' + tokfile)
        if not os.path.exists(tokfile):
            self.logger.debug('Auth token does not exist at ' + tokfile)
            raise Exception('No authentication token found')

        self.logger.debug('Reading auth token from ' + tokfile)
        with open(tokfile, 'r') as gtok_file:
            credsb64 = gtok_file.read()
            self.logger.debug('Initializing drive creds')
            GDriveSync.init_creds(credsb64)

    def post(self):
        self.logger.info('synchandler ' + str(self.request.uri))
        action = self.get_argument('action', None)
        retcode = 0
        if None != action:
            try:
                if action == 'addgdrive':
                    retcode = self.action_addgdrive()
                elif action == 'delgdrive':
                    retcode = self.action_delgdrive()
                elif action == 'syncgdrive':
                    retcode = self.action_syncgdrive()
            except:
                # TODO: handle auth tok expiry and send out separate error code
                traceback.print_exc()
                retcode = -1
        response = {'code': retcode, 'data': ''}
        self.write(response)

    def action_addgdrive(self):
        self.set_gdrive_auth_tok()
        retcode = 0
        gfolder = self.get_argument('repo', '').strip()
        loc = SyncHandler.sanitize_loc(self.get_argument('loc', '').strip())
        loc = os.path.join(os.path.expanduser(SyncHandler.LOC), loc)
        GDriveSync.clone(gfolder, loc, True)
        return retcode

    def action_delgdrive(self):
        self.set_gdrive_auth_tok()
        repo_id = self.get_argument('repo', None)
        repo = SyncHandler.get_gdrive_repo(repo_id)
        if (None != repo) and os.path.exists(repo.loc):
            shutil.rmtree(repo.loc)
        return 0

    def action_syncgdrive(self):
        self.set_gdrive_auth_tok()
        retcode = 0
        repo_id = self.get_argument('repo', None)
        repo = SyncHandler.get_gdrive_repo(repo_id)
        if None != repo:
            repo.sync()
        return retcode

    @staticmethod
    def get_gdrive_repos():
        gdriverepo_paths = GDriveSync.scan_repo_paths([os.path.expanduser(SyncHandler.LOC)])
        gdriverepos = {}
        for repopath in gdriverepo_paths:
            gs = GDriveSync(repopath)
            gdriverepos[gs.repo_hash()] = gs
        return gdriverepos

    @staticmethod
    def get_gdrive_repo(repokey, gdriverepos=None):
        if None == gdriverepos:
            gdriverepos = SyncHandler.get_gdrive_repos()
        if repokey in gdriverepos:
            return gdriverepos[repokey]
        return None

    def set_gdrive_auth_tok(self):
        gauth = self.get_argument('gauth', '')
        if len(gauth) > 0:
            GDriveSync.init_creds(gauth)

    @staticmethod
    def sanitize_loc(loc):
        return re.sub(r'^[\.\\/]*', '', loc)