def serialize_data(all_logging):

    json_data = []

    for logging in all_logging:

        json_data.append({
        	"user": logging.user.full_name,
            "action": logging.action,
            "datetime": logging.created
            })

    return json_data