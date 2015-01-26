'''
    starting point for bottle framwork
    this will start as service
    with run method
'''
# bottle framework
from bottle import Bottle
from bottle import static_file
from bottle import Request
from bottle import request
from bottle import redirect
from bottle import SimpleTemplate

# built in function
import importlib
import os
import copy

# main class of framework
class Main(Bottle):

    def __init__(self):
        Bottle.__init__(self)
        
        # set configuration
        self._set_configuration()
        
        # call route
        # register route
        self._set_route()
        
    # configuration
    def _set_configuration(self):
        # add config
        # configuration for running service
        self.config['ip_address'] = '127.0.0.1'
        self.config['port'] = 8888
        self.config['reloader'] = True
        self.config['interval'] = 1
        self.config['apps'] = {'sikilku':'app_1'}
        self.config['active_app'] = self.config['apps']['sikilku']
        self.config['page_url'] = '/p/home/page'
        
        # global template path
        # path global view under apps
        tpl_views_folder = r'' + self.config['active_app'] + os.path.sep + 'views' + os.path.sep
        self.config['views_path'] = tpl_views_folder
        
    # this is will get request from client
    def _request(self):
        return Request(request.environ)
        
    # redirect url
    def goto_url(self, url):
        redirect(url)
        
    # goto default url
    def _default_page(self):
        self.goto_url(self.config['page_url'])
        
    # register route
    # create custrom route is okay!
    def _set_route(self):
        # default page url
        self.route(path='/', method='GET', callback=self._default_page, name='default_page')
    
        # basic framwork route
        self.route(path='/p/<module>/<action>', method='GET', callback=self._parse_request, name='parse_get')
        self.route(path='/p/<module>/<action>', method='POST', callback=self._parse_request, name='parse_post')
        self.route(path='/p/<module>/<action>/<method>', method='GET', callback=self._parse_request, name='parse_action_method_get')
        self.route(path='/p/<module>/<action>/<method>', method='POST', callback=self._parse_request, name='parse_action_method_post')
        
        self.route(path='/statics/<filepath:path>', method='GET', callback=self._serve_static, name='static_get')
    
    # parse callback
    # module is module name
    # action is action name
    # index is default value
    # if method not defined then call default module action method index
    def _parse_request(self, module, action, method='index'):
        module_action = importlib.import_module(self.config['active_app'] + '.modules.' + module + '.actions.' + action)
        module_action = importlib.reload(module_action)
        
        # set active modules call path
        # this path is used when call template file
        tpl_views_folder = r'' + self.config['active_app'] + os.path.sep + 'modules' + os.path.sep + module + os.path.sep + 'views' + os.path.sep
        self.config['module_views_path'] = tpl_views_folder
        
        module_action = module_action.Action(bottle_obj=self, DOPOST=self._request().POST, DOGET=self._request().GET)
        
        call_method = getattr(module_action, method)
        return call_method()
        
    # render template
    # template name
    # template name should be end with .tpl
    # call template must be using
    # appviews.template_name => this is for view under apps/views
    # views.template_name => this is for view under modules_name/views
    def render(self, template_name, param=None):
        # read template file
        # validate if template path exist
        tpl_path = ''
        if template_name.find('appviews.') == 0:
            tpl_path = self.config['views_path'] + template_name.split('.')[1] + '.tpl'
            
        elif template_name.find('views.') == 0:
            tpl_path = self.config['module_views_path'] + template_name.split('.')[1] + '.tpl'
        
        # setup param data    
        param_data = {}
        
        if param:
            param_data = copy.deepcopy(param)
            
        # make available to include other view from appview and module view
        param_data['appviews'] = self.config['views_path']
        param_data['views'] = self.config['module_views_path']
        
        # read template file
        if os.path.isfile(tpl_path):
            tpl_file = open(tpl_path)
            tpl_content = ''.join(tpl_file.readlines())
            tpl_file.close()
            
            # return parsed template
            return SimpleTemplate(tpl_content).render(data=param_data)
        
        # if tpl file not found
        else:
            return 'Template file not found ' + template_name
        
    # server static file under apps/static folder
    def _serve_static(self, filepath):
        return static_file(filepath, root=self.config['active_app'] + '/statics')
        
    def serve(self):
        self.run(host=self.config['ip_address'], port=self.config['port'], reloader=self.config['reloader'], interval=self.config['interval'])
        
if __name__ == '__main__':
    Main().serve()
