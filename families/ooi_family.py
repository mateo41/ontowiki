import family

class Family(family.Family):
    def __init__(self):
        family.Family.__init__(self)
         
        self.name = 'ooi'
        self.langs = {'en': 'vmlinux.sdsc.edu'}
        
        self.content_id = 'mainContent'

   # def version(self, code):
   #     return "1.13.2"
        
    def apipath(self, code):
        return '%s/api.php' % self.scriptpath(code)

    def scriptpath(self, code):
        return '/mediawiki'

