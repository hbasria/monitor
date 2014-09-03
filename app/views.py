import urllib2
from flask import render_template
from flask import request
from app import app, db, models

__author__ = 'hbasria'

@app.route('/')
@app.route('/index/<group_name>', methods=['POST', 'GET'])
def index(group_name=None):

    group = models.Group.query.filter_by(name=group_name).first()
    nodes = []

    message = None
    if request.method == 'POST':

        if 'groupName' in request.form:
            groupName = request.form['groupName']

            new_group = models.Group()
            new_group.name = groupName
            db.session.add(new_group)
            db.session.commit()

            message = 'New group name added %s'%groupName

        if 'node_name' in request.form:
            new_node = models.Node()
            new_node.name = request.form['node_name']
            new_node.ip = request.form['node_ip']
            new_node.port = request.form['node_port']
            new_node.group_id = group.id

            db.session.add(new_node)
            db.session.commit()

            message = 'New node added %s'%new_node




    if group:
        nodes = models.Node.query.filter_by(group_id=group.id)
        message = '%s nodes found' % len(list(nodes))

    groups = models.Group.query.all()

    return render_template('index.html',
        title='Home',
        groups=groups,
        nodes=nodes,
        message=message)

@app.route('/proxy/<ip>')
def proxy(ip=None, port=2812):

    try:
        response = urllib2.urlopen('http://%s:%s/'%(ip, port), timeout=1).read()
        #response = urllib.request.urlopen('http://%s:%s/'%(ip, port), timeout=1).read()
    except:
        response = 'TIMEOUT_ERROR'
        pass

    return response
