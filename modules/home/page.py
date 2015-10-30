# load extensions example
from extensions.system.session import Session

class Page():
    
    # init action constructor
    def __init__(self, app):
        self.app = app
        self.session = Session(app)
        
    # default page if url call without controller method
    def index(self):
        return self.app.render('site.home', {})
        
    # test front page
    def front(self):
        return self.app.render('site.front', {})
        