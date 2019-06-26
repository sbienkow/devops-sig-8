#!/usr/bin/env python
import falcon
import threading
import time
import yaml

config = { 'magic_word': 'abc' }


class VarResource:
    def on_get(self, req, resp):
        obj = {'todays_magic_word': config['magic_word']}
        resp.media = obj


class ConstResource:
    def on_get(self, req, resp):
        resp.media = { 'devops_sig_no': 8 }


class TimeResource:
    def on_get(self, req, resp):
        resp.media = int(time.time())

with open('/etc/app/config.yaml', 'r') as f:
    config = yaml.safe_load(f)

api = falcon.API()
api.add_route('/var', VarResource())
api.add_route('/const', ConstResource())
api.add_route('/time', TimeResource())
