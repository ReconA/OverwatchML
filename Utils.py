def calculate_accuracy():
    print 'a'

# API returns integers with commas, eg. 1,398
def remove_commas(integer):
    return integer.replace(",","")


# Some times in json are in form H:mm:ss.
# Convert them to seconds for better comparing.
def to_seconds(time_str):
    h,m,s = 0,0,0;
    count = time_str.count(':')
    if count == 0:
        s = time_str
    elif count == 1:
        m,s = time_str.split(':')
    else:
        h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)