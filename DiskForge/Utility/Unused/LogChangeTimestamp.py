def get_indexes_by_timestamp(data, target_timestamp, target_message):
    if target_message is None and target_timestamp is None:
        return [index for index, item in enumerate(data)]
    if target_message is None:
        return [index for index, item in enumerate(data) if
                item.timestamp == target_timestamp]
    if target_timestamp is None:
        return [index for index, item in enumerate(data) if target_message.replace(
            " ", "") in item.get('message').replace(",", " ").replace(" ", "")]

    return [index for index, item in enumerate(data) if
            item.get('timestamp') == target_timestamp and target_message.replace(
                " ", "") in item.get('message').replace(",", " ").replace(" ", "")]


months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def changeTimestamp(parsedLogs, timestamp_old, message, timestamp_new):
    neededIndexes = get_indexes_by_timestamp(parsedLogs, timestamp_old, message)
    '''
    So also wir haben die Zeitstempel welche wir verändern wollen
    Also müssen wir jetzt den Zeitstemple ändern
    Und die Events dann an der richtigen Stelle einfügen
        Dafür wieder Unixtimestamp berechnen
    '''
    for i in range(len(neededIndexes)):
        parsedLogs[neededIndexes[i]]["timestamp"] = timestamp_new[5:]
