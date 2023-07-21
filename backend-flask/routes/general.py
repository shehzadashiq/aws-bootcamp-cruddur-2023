from flask import request, g
import rollbar
import rollbar.contrib.flask

def load(app):
  @app.route('/api/health-check')
  def health_check():
    return {'success': True, 'ver': 1}, 200

  @app.route('/rollbar/test')
  def rollbar_test():
    try:
      g.rollbar.report_message('Hello World!', 'warning')
    except AttributeError:
      print('No such attribute')
    return "Hello World!"