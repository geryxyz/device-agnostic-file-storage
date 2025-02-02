def get_remarkable_ip_address():
    """
    Get the IP address of the Remarkable device.
    """
    with open("remarkable.ip", "r") as f:
        return f.read().strip()


def get_remarkable_password():
    """
    Get the password of the Remarkable device.
    """
    with open("remarkable.password", "r") as f:
        return f.read().strip()
