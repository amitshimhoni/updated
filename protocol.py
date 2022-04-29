# Exercise 2.7
# Amit Shimoni
# 27.7.21
# protocol.py



def create_msg(data):
    """Create a protocol message, with length field"""
    if type(data) is not bytes:  # אם מדובר בקובץ טקסט (string)
        data = data.encode()  # קודד לבינארי

    len_data = str(len(data)).encode()
    zfill_length = len_data.zfill(4)
    message = zfill_length + data  # אורך הודעה+הודעה

    return message  # החזרת ההודעה המקודדת



def get_msg(my_socket):
    """Extract message from protocol, without the length field
       If length field does not include a number, returns False, "Error" """

    len_message = int(my_socket.recv(4))
    message = my_socket.recv(len_message)
    try:
        return message

    except:
        return message

