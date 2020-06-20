from datetime import datetime, timedelta
import json
import falcon


from .input import Input


class Pump(Input):
    def __init__(self, channel):
        self.estimated_end_time = None
        self.expected_running = False
        self.running_sprinkler_name = None
        self.increments = 0
        super().__init__(channel)

    @property
    def running(self):
        # If it's on, it's defintely on
        if self.state:
            return True
        if self.expected_running:
            now = datetime.now()
            if self.estimated_end_time > now:
                return True
            time_diff = now - self.estimated_end_time
            if time_diff.seconds > 10:
                self.clear_running()
                return self.running
        return False

    def safe_to_trigger(self, name):
        if not self.expected_running:
            return True
        if self.running_sprinkler_name == name and self.increments < 3:
            return True
        return False

    def set_running(self, name):
        self.expected_running = True
        self.running_sprinkler_name = name
        if not self.estimated_end_time:
            self.estimated_end_time = datetime.now()
        self.estimated_end_time = self.estimated_end_time + \
            timedelta(minutes=1)
        self.increments = self.increments + 1

    def clear_running(self):
        self.expected_running = False
        self.running_sprinkler_name = None
        self.estimated_end_time = None
        self.increments = 0


class PumpResource():  # pylint: disable=too-few-public-methods
    def __init__(self, pump: Pump):
        self.pump = pump

    def on_get(self, req, resp):  # pylint: disable=unused-argument
        estimated_end_time = self.pump.estimated_end_time
        if estimated_end_time:
            estimated_end_time = self.pump.estimated_end_time.isoformat()
        doc = {
            "running": self.pump.running,
            "running_sprinkler_name": self.pump.running_sprinkler_name,
            "estimated_end_time": estimated_end_time
        }
        resp.body = json.dumps(doc, ensure_ascii=False)
        resp.status = falcon.HTTP_200
