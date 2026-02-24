class SucksException(Exception):
    def __init__(self, rtc: int):
        self.rtc = rtc
