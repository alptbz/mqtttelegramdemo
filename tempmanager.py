

class TemperatureManager:

    def __init__(self):
        self.last_temperature = -200
        self.temperature = -200
        self.last_temperature_with_significant_difference = -200
        self.temperature_changed_significantly_callback = None

    def update(self, temp):
        self.last_temperature = self.temperature
        self.temperature = temp
        return self.last_temperature

    def is_change_significant(self):
        return abs(self.temperature - self.last_temperature_with_significant_difference) >= 2

    def notify_once_if_change_significant(self):
        if self.is_change_significant():
            self.last_temperature_with_significant_difference = self.temperature
            if self.temperature_changed_significantly_callback is not None:
                self.temperature_changed_significantly_callback(self.temperature)

    def update_and_notify(self, temp):
        self.update(temp)
        self.notify_once_if_change_significant()


temperatureManager = TemperatureManager()