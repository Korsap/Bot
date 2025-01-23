import datetime
def logger(*name_parts):
    now = datetime.datetime.now().strftime("[%d.%m.%Y, %H:%M:%S]")
    message = now
    for part in name_parts:
        message += " " + part
    print(message)
    with open('log.txt', 'a') as log:
        log.write(message + '\n')
    return