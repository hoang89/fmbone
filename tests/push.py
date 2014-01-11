from gcm import GCM
def push(data=None):
    """
    This is simple push notification to push notification to client
    """
    if data is None:
        return
    #project id: 992540290187
    reg_id = "APA91bHagz8HB7stTexv5ssoQn3YZAEGpOmrgMGEFgwys9eE2iURu90bJIrAGkAWoEnMq95O-S2Nbk6n1ppw_iWR0LrAn8qLL9XGsBO_FDOSxhqUOmghutTKcsejQ2OzfDlK52OVIE538mX8wgQTBByAAhFw5SU7DQ"
    API_KEY = "AIzaSyAU2YCOwq1Q5D2S9rvbM2vDIH9uO1oYxro"
    gcm = GCM(API_KEY)

    # Plaintext request
    res = gcm.plaintext_request(registration_id=reg_id, data=data)
    print res