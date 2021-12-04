import os
import toml
import subprocess
import pygit2

class Agent(object):
    def __init__(self, config_file):    
        config = self._load_config(config_file)["bombcrypto"]
        self.browser_agent = BrowserAgent(config)
        self.update_agent = UpdateAgent(config)
        self.bomb_agent = BombAgent(config)
    
    def _load_config(self, config_file):
        config = toml.loads(open(config_file).read())
        return config

    def do_update(self):
        # print("update start")
        self.update_agent.update()

    def check_update(self):
        # print("update check")
        return self.update_agent.check()

    def check_script(self):
        # print("script check")
        return not self.bomb_agent.is_alive()

    def start(self):
        self.browser_agent.kill_browser()
        self.browser_agent.open_browser()
        self.bomb_agent.start()

    def stop(self):
        self.browser_agent.kill_browser()
        self.bomb_agent.stop()

class BombAgent(object):
    def __init__(self, config):
        self.proc = None
        self.server = config["server"]
        self.script_path = config["script_path"]
        self.script_file = config["script_file"]

        si = subprocess.STARTUPINFO()
        si.dwFlags = subprocess.STARTF_USESTDHANDLES | subprocess.STARTF_USESHOWWINDOW
        return
    
    def connect(self):
        return

    def stop(self):
        if self.proc is not None:
            self.proc.terminate()
            self.proc.kill()
            outs, errs = self.proc.communicate()
            self.proc = None
        return

    def start(self):
        self.proc = subprocess.Popen(["python", self.script_file], cwd=self.script_path)
        return

    def is_alive(self):
        if self.proc is None:
            return False
        
        if self.proc.poll() is None:
            return True
            
        return False

class UpdateAgent(object):
    def __init__(self, config) -> None:
        self.username = config["git_username"] 
        self.password = config["git_password"]
        self.git_url = config["git_url"]
        self.local_path = config["script_path"]
        
        try: 
            self.repo = pygit2.Repository(self.local_path)
        except:
            self.repo = None 

    """
    def check(self):
        if self.repo == None:
            return True
        self.repo.remotes["origin"].fetch(callbacks=self.GitCallbacks(self.pubkey, self.prikey))
        remote_master_id = self.repo.lookup_reference('refs/remotes/origin/main').target
        merge_result, _ = self.repo.merge_analysis(remote_master_id)
        if merge_result & pygit2.GIT_MERGE_ANALYSIS_UP_TO_DATE:
            return False
        elif merge_result & pygit2.GIT_MERGE_ANALYSIS_FASTFORWARD:
            return True

        return True

    def update(self):
        if self.repo == None:
            url = self.git_url.replace('https://', f'https://{self.username}:{self.password}@')
            subprocess.check_output(["git", "clone", url, self.local_path])
            # self.repo = pygit2.clone_repository(self.git_url, self.local_path,  callbacks=self.GitCallbacks(self.pubkey, self.prikey))
            return
        remote_master_id = self.repo.lookup_reference('refs/remotes/origin/main').target
        self.repo.checkout_tree(self.repo.get(remote_master_id))
        try:
            master_ref = self.repo.lookup_reference('refs/heads/main')
            master_ref.set_target(remote_master_id)
        except KeyError:
            self.repo.create_branch("main", self.repo.get(remote_master_id))

        self.repo.head.set_target(remote_master_id)
        if os.path.exists(self.local_path + os.sep + "requirements.txt"):
            subprocess.check_output(["python", "-m", "pip", "install", "-r", "requirements.txt"], cwd=self.local_path)
        if os.path.exists(self.local_path + os.sep + "setup.py"):
            subprocess.check_output(["python", "setup.py", "install"], cwd=self.local_path)

    class GitCallbacks(pygit2.RemoteCallbacks):
        def __init__(self, username, password):
            self.username = username
            self.password = password

        def credentials(self, url, username_from_url, allowed_types):
            if allowed_types & pygit2.credentials.GIT_CREDENTIAL_USERNAME:
                return pygit2.Username("git")
            #elif allowed_types & pygit2.credentials.GIT_CREDENTIAL_SSH_KEY:
            #    return pygit2.Keypair("git", self.pubkey , self.prikey, "")
            elif allowed_types & pygit2.credentials.GIT_CREDENTIAL_USERPASS_PLAINTEXT:
                return pygit2.UserPass(self.username, self.password)
            else:
                return None    
    """
    def check(self):
        if not os.path.exists(self.local_path):
            return True

        subprocess.check_output(["git", "fetch"], cwd=self.local_path)
        ret = subprocess.check_output(["git", "diff", "main", "origin/main"], cwd=self.local_path)
        if ret == b"":
            return False
        else:
            return True

    def update(self):
        if not os.path.exists(self.local_path):
            url = self.git_url.replace('https://', f'https://{self.username}:{self.password}@')
            subprocess.check_output(["git", "clone", url, self.local_path])
            return 

        subprocess.check_output(["git", "pull"], cwd=self.local_path)


class BrowserAgent(object):
    def __init__(self, config) -> None:
        self.browser_path = config["browser_path"] 
        self.app_url = config["app_url"]
        self.proc = None

    def kill_browser(self):
        if self.proc is not None:
            self.proc.terminate()
        self.proc = None

        try:
            subprocess.check_output(["taskkill","/f", "/im",os.path.basename(self.browser_path)])
        except:
            pass

    def open_browser(self):
        self.proc = subprocess.Popen([self.browser_path, self.app_url])
        # proc.communicate()
        pass
