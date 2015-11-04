import schedule

def init(config):
    global context
    context = config
    print config.host
    
    schedule.every().second.do(job)
    
    
def job():
    print context.host