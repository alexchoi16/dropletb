from manage import *
from db.models import *
from google.appengine.api import users
from __init__ import *
import webapp2, jinja2
from google.appengine.ext import ndb


class MainHandler(AdminBaseHandler):
    def get(self):
        user = users.get_current_user()
        template_values = {}
        if user:
            self.redirect('/admin/overview')
            # greeting = 'Welcome, {}! (<a href="{}">sign out</a>)'.format(
            #     nickname, logout_url)
        else:
            template_values = {
                'login_url': users.create_login_url('/admin')
            }
            self.redirect(template_values['login_url'])
        #     greeting = '<a href="{}">Sign in</a>'.format(login_url)
        #
        # self.response.write(
        #     '<html><body>{}</body></html>'.format(greeting))

class LogoutHandler(AdminBaseHandler):

    def get(self):
        template_values = {}
        if users.get_current_user():
            self.redirect(users.create_logout_url('/admin'))
        else:
            self.redirect('/admin')    


class AdminHandler(AdminBaseHandler):
    def get(self):
        user = users.get_current_user()
        template_values = {}
        if user:
            if users.is_current_user_admin():
                self._serve_page()
            else:
                self.response.write('You are not an administrator.')
        else:
            self.response.write('You are not logged in.')

    def post(self):
        event = Event(event_title = self.request.get('event-title'),
            event_description = self.request.get('event-description'),
            address = self.request.get('event-address'),
            city = self.request.get('event-city'),
            zip_code = self.request.get('event-zip_code'),
            event_date = self.request.get('event-date'),
            event_time = self.request.get('event-time'))
        event.put()
        self._serve_page()
    #
    def delete_event(self):
        event_id = self.request.get('id')
        Event.get(event_id).delete()
    def _serve_page(self):
        query_event = Event.query()
        results = query_event.fetch()
        template_values = {
            'results': results

        }
        self.render_template('admin-overview.html',template_values)


app = webapp2.WSGIApplication([
    webapp2.Route('/admin', MainHandler),
    webapp2.Route('/admin/overview', AdminHandler),
    webapp2.Route('/admin/logout', LogoutHandler)
], debug=True)
