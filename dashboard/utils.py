import datetime

def serialize_data(all_logging):

    json_data = []
    for logging in all_logging:
        date = str(logging.created)
        split_datetime = date.split()
        split_time = split_datetime[1].split(':')

        json_data.append({
        	"user": logging.user.full_name,
            "action": logging.action,
            "date": split_datetime[0],
            "time": '{}:{}'.format(split_time[0], split_time[1])
            })

    return json_data