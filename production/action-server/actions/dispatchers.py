
fault_codes = {
    '__CODE0__': 'utter_not_found',
    '__CODE1__': 'utter_not_found',
    '__CODE2__': 'utter_cant_answer',
}

def dispatch(tracker, dispatcher, message):
    message_id = tracker.latest_message['message_id']
    if message in fault_codes:
        response = fault_codes[message]
        button = [{"payload": "/addition_request\
            {{\"message_id\":\"{id}\"}}".format(id=message_id), 
            "title": "request addition to database"},]
        dispatcher.utter_message(response=response,
                                 buttons=button,
                                 button_type='inline',
                                 )
    else:
        message_id = tracker.latest_message['message_id']
        buttons = [
            {"payload": "/good_response{{\"message_id\":\"{id}\"}}".format(id=message_id),
            "title": "👍🏻"},
            {"payload": "/bad_response{{\"message_id\":\"{id}\"}}".format(id=message_id), 
            "title": "👎🏻"},
            ]
        dispatcher.utter_message(text=message,
                                 buttons=buttons,
                                 button_type='inline',
                                 )
    