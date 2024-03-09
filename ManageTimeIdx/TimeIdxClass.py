from datetime import datetime


class TimeAndIdxManage:
    def __init__(self):
        self.define_variables()

    def define_variables(self):
        self.difference_time = None
        self.difference_idx = None

    def setupIdxAndTimeManage(self, idx, last_date):
        self.idx = idx
        self.last_date = last_date

        self.set_variables()

    def set_variables(self):
        if self.last_date is None:
            self.last_date = datetime.strptime("2020-01-01", "%Y-%m-%d")
            print(self.last_date)
        time_last = int(datetime.timestamp(self.last_date))
        time_now = int(datetime.timestamp(datetime.now()))
        self.difference_time = time_now - time_last
        print("difference_time:", self.difference_time)

        time_idx_now = time_now - (time_now % 60)
        self.difference_idx = int((time_last - time_idx_now) / 60) + 1
        print("difference_idx :", self.difference_idx)

    def set_idx_data_difference(self):
        if -1 > self.difference_idx > -20:
            self.idx = self.difference_idx
            print("difference_idx>-20 :", self.idx)
        elif self.difference_idx <= -20:
            self.idx = -21
            print("difference_idx<=-20 :", self.idx)
        else:
            print("difference_idx=-1 :", self.idx)

    def set_correct_idx(self):
        if self.idx == 0:
            self.idx = -20
        elif self.idx < -1:
            self.idx += 1
        else:
            self.idx = -1
        return self.idx

    # def set_is_coordinated(self):
    #     different_time_minute = self.difference_time / 60
    #     print("different_time_minute:", different_time_minute)
    #     if different_time_minute < 2:
    #         self.is_coordinated = True
    #     else:
    #         self.is_coordinated = False
    #     return self.is_coordinated

    def get_sleep_time(self):
        self.sleep_time_sec = 60 - (self.difference_time % 60)
        return self.sleep_time_sec

    def get_idx(self, idx, last_date):
        self.setupIdxAndTimeManage(idx=idx, last_date=last_date)
        if self.idx == -1:
            self.set_idx_data_difference()
        else:
            self.set_correct_idx()
        return self.idx
