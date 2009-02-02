import StringIO, os
import ConfigParser

ConfigLocations = ['/etc/pybrightcove.cfg', os.path.expanduser('~/.pybrightcove')]
ConfigPath = ConfigLocations[0]
UserConfigPath = ConfigLocations[1]

class Config(ConfigParser.SafeConfigParser):

    def __init__(self, path=None, fp=None):
        ConfigParser.SafeConfigParser.__init__(self, {'working_dir' : '/tmp',
                                                      'debug' : '0'})
        if path:
            self.read(path)
        elif fp:
            self.readfp(fp)
        else:
            self.read(ConfigLocations)

    def save_option(self, path, section, option, value):
        """
        Write the specified Section.Option to the config file specified by path.
        Replace any previous value.  If the path doesn't exist, create it.
        Also add the option the the in-memory config.
        """
        config = ConfigParser.SafeConfigParser()
        config.read(path)
        if not config.has_section(section):
            config.add_section(section)
        config.set(section, option, value)
        fp = open(path, 'w')
        config.write(fp)
        fp.close()
        if not self.has_section(section):
            self.add_section(section)
        self.set(section, option, value)

    def save_user_option(self, section, option, value):
        self.save_option(os.path.expanduser(UserConfigPath), section, option, value)

    def save_system_option(self, section, option, value):
        self.save_option(ConfigPath, section, option, value)

    def get_value(self, section, name, default=None):
        return self.get(section, name, default)

    def get(self, section, name, default=None):
        try:
            val = ConfigParser.SafeConfigParser.get(self, section, name)
        except:
            val = default
        return val.strip("'")
    
    def getint(self, section, name, default=0):
        try:
            val = ConfigParser.SafeConfigParser.getint(self, section, name)
        except:
            val = int(default)
        return val
    
    def getfloat(self, section, name, default=0.0):
        try:
            val = ConfigParser.SafeConfigParser.getfloat(self, section, name)
        except:
            val = float(default)
        return val

    def getbool(self, section, name, default=False):
        if self.has_option(section, name):
            val = self.get(section, name)
            if val.lower() == 'true':
                val = True
            else:
                val = False
        else:
            val = default
        return val
    
    def setbool(self, section, name, value):
        if value:
            self.set(section, name, 'true')
        else:
            self.set(section, name, 'false')
    

