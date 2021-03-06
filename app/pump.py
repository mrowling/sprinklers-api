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
        self._register_event_detect(self.clear_running)

    @property
    def running(self):
        # If it's on, it's defintely on
        return self.state

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

    def clear_running(self, channel=None):
        if channel:
            print("Detected change on channel {}".format(channel))
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
            "estimated_end_time": estimated_end_time,
            "increment_count": self.pump.increments
        }
        resp.body = json.dumps(doc, ensure_ascii=False)
        resp.status = falcon.HTTP_200
