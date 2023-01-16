class Algorithm:
    def __init__(self):
        self.run_times = [] # 记录每次测试算法完成的时间便于后续统计
        self.preprocessing_times = [] # 如果算法有预处理时间的话

    def get_time(self,start_time,end_time): #import time 每次算法运行开始和结束时记录time = time.time()，最后传入这个函数
        return abs(end_time - start_time)

    def record_run_time(self,start_time,end_time):
        time = self.get_time(start_time,end_time)
        self.run_times.append(time)

    def record_preprocessing_time(self,start_time,end_time):
        time = self.get_time(start_time,end_time)
        self.preprocessing_times.append(time)

    def get_ready(self): # maybe the preprocessing
        pass

    def run(self):
        pass

    def show_result(self):
        pass

