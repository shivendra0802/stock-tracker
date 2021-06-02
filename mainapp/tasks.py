from celery import shared_task
from yahoo_fin.stock_info import *
import queue
from threading import Thread

@shared_task(bind=True)
def update_stock(self, stockpicker):
    data = {}
    avilable_stocks = tickers_nifty50()
    for i in stockpicker:
        if i in avilable_stocks:
            pass
        else:
            stockpicker.remove(i)
    
    n_threads = len(stockpicker)
    thread_list = []
    que = queue.Queue()
  
    for i in range(n_threads):
        thread = Thread(target = lambda q, arg1: q.put({stockpicker[i]: get_quote_table(arg1)}), args = (que, stockpicker[i]))
        thread_list.append(thread)
        thread_list[i].start()

    for thread in thread_list:
        thread.join()
    
    while not que.empty():
        result = que.get()
        data.update(result)

    return 'Done'