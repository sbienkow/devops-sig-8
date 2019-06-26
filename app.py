#!/usr/bin/env python
import falcon
import threading
import time
import yaml

global_config_lock = threading.Lock()
config = { 'magic_word': 'abc' }


def dummy_config_changer():
    try:
        open('/etc/app/config.yaml', 'r')
    except FileNotFoundError:
        pass
    i = 0
    while True:
        i += 1
        time.sleep(10)
        try:
            #open('/var/run/app.lock', 'r')
            print('GCL locking')
            with global_config_lock:
                config['magic_word'] = str(i)
                print('GCL unlocking')
        except Exception as e:
            print('exc')
    print("Thread %s: finishing")


def filewatcher_config_changer():
    path = '/etc/app/config.yaml'
    try:
        open(path, 'r')
    except FileNotFoundError:
        pass
    while True:
        time.sleep(1)
        try:
            cfg_file = open(path, 'r')
            new_cfg = yaml.load(cfg_file)
            if new_cfg != config:
                print('GCL locking')
                with global_config_lock:
                    config.clear()
                    config.update(new_cfg)
                print('GCL unlocking')
        except FileNotFoundError as e:
            print('exc')
    print("Thread %s: finishing")


config_changers = {
    'dummy_config_changer': dummy_config_changer,
    'filewatcher_config_changer': filewatcher_config_changer
}


class VarResource:
    def on_get(self, req, resp):
        with global_config_lock:
            obj = {'todays_magic_word': config['magic_word']}
            resp.media = obj


class ConstResource:
    def on_get(self, req, resp):
        resp.media = { 'devops_sig_no': 8 }


class TimeResource:
    def on_get(self, req, resp):
        resp.media = int(time.time())

config_changer = 'filewatcher_config_changer'
config_changer_thread = threading.Thread(target=config_changers[config_changer])
config_changer_thread.start()
api = falcon.API()
api.add_route('/var', VarResource())
api.add_route('/const', ConstResource())
api.add_route('/time', TimeResource())
