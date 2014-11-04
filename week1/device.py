class Device(object):
    # Initializer
    def __init__(self, ip, user, passw):
        # An instance variable to hold the device's name
        self._ip = ip
        self._user = user
        self._passw = passw
 
    # IP Getter method
    @property
    def ip(self):
        """Get the current ip address."""
        return self._ip
 
    # IP Setter method
    @ip.setter
    def ip(self, new_ip):
        """Change the ip address for this device. """
        self._ip = new_ip
        
    # User Getter method
    @property
    def user(self):
        """Get the current user name for logging on to this device."""
        return self._user
 
    # User Setter method
    @user.setter
    def user(self, new_user):
        self._user = new_user
        
    # Password Getter method
    @property
    def passw(self):
        """Get the current password for logging on to this device."""
        return self._passw
 
    # Password Setter method
    @passw.setter
    def passw(self, new_passw):
        self._passw = new_passw
        
    def __str__(self):
        return "{\"device\": { \"ip\": "+str(self._ip)+", \"user\": "+str(self._user)+", \"passw\": "+str(self._passw)+"}}"
    def __unicode__(self):
        return u"{\"device\": { \"ip\": "+str(self._ip)+", \"user\": "+str(self._user)+", \"passw\": "+str(self._passw)+"}}"
        
