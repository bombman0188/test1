import time
import threading
from bomb_agent import Agent

config_file = "config.toml"

class RepeatTimer(threading.Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

def start():
    """if agent.check_update() or agent.check_script():
        agent.stop()
        agent.do_update()
        agent.start()
    """
    if agent.check_script():
        agent.stop()
        agent.start()

if __name__ == "__main__":
    agent = Agent(config_file)
    start()
    # 업데이트 체크 쓰레드 
    timer = RepeatTimer(30, start)
    timer.start()
    timer.join()
