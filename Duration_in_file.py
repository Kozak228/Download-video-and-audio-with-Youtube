def duration_in_file(all_time):
    s = all_time % 60
    m = (all_time // 60) % 60
    h = all_time // 3600

    if h > 0:
        return f"{h} г. {add_zero(m)} хв. {add_zero(s)} с."
    elif m > 0 and h <= 0:
        return f"{m} хв. {add_zero(s)} с."
    else:
        return f"{s} с."

def add_zero(num):
    return "0" + str(num) if num < 10 else str(num)