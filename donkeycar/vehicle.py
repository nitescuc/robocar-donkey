#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 25 10:44:24 2017

@author: wroscoe
"""

import time
from threading import Thread
from .memory import Memory


class Vehicle():
    def __init__(self, mem=None):

        if not mem:
            mem = Memory()
        self.mem = mem
        self.parts = []
        self.on = True
        self.threads = []


    def add(self, part, inputs=[], outputs=[], 
            threaded=False, run_condition=None, can_apply_config=False):
        """
        Method to add a part to the vehicle drive loop.

        Parameters
        ----------
            inputs : list
                Channel names to get from memory.
            ouputs : list
                Channel names to save to memory.
            threaded : boolean
                If a part should be run in a separate thread.
        """

        p = part
        print('Adding part {}.'.format(p.__class__.__name__))
        entry={}
        entry['part'] = p
        entry['inputs'] = inputs
        entry['outputs'] = outputs
        entry['run_condition'] = run_condition
        entry['can_apply_config'] = can_apply_config

        if threaded:
            t = Thread(target=part.update, args=())
            t.daemon = True
            entry['thread'] = t

        self.parts.append(entry)


    def start(self, rate_hz=10, max_loop_count=None):
        """
        Start vehicle's main drive loop.

        This is the main thread of the vehicle. It starts all the new
        threads for the threaded parts then starts an infinit loop
        that runs each part and updates the memory.

        Parameters
        ----------

        rate_hz : int
            The max frequency that the drive loop should run. The actual
            frequency may be less than this if there are many blocking parts.
        max_loop_count : int
            Maxiumum number of loops the drive loop should execute. This is
            used for testing the all the parts of the vehicle work.
        """

        try:

            self.on = True

            for entry in self.parts:
                if entry.get('thread'):
                    #start the update thread
                    entry.get('thread').start()

            #wait until the parts warm up.
            print('Starting vehicle...')
            time.sleep(1)

            loop_count = 0
            last = 0
            while self.on:
                start_time = time.time()
                loop_count += 1

                self.update_parts()

                #stop drive loop if loop_count exceeds max_loopcount
                if max_loop_count and loop_count > max_loop_count:
                    self.on = False

                if rate_hz != 0:
                    sleep_time = 1.0 / rate_hz - (time.time() - start_time)
                    if last+5 < start_time:
                        print(sleep_time)
                        last = start_time
                    if sleep_time > 0.0:
                        time.sleep(sleep_time)

        except KeyboardInterrupt:
            pass
        finally:
            self.stop()


    def update_parts(self):
        '''
        loop over all parts
        '''
        for entry in self.parts:
            #don't run if there is a run condition that is False
            run = True
            if entry.get('run_condition'):
                run_condition = entry.get('run_condition')
                run = self.mem.get([run_condition])[0]
                #print('run_condition', entry['part'], entry.get('run_condition'), run)
            
            if run:
                p = entry['part']
                #get inputs from memory
                inputs = self.mem.get(entry['inputs'])

                #run the part
                if entry.get('thread'):
                    outputs = p.run_threaded(*inputs)
                else:
                    outputs = p.run(*inputs)

                #save the output to memory
                if outputs is not None:
                    self.mem.put(entry['outputs'], outputs)

    def apply_config(self, config):
        for entry in self.parts:
            if entry.get('can_apply_config'):
                entry['part'].apply_config(config)

    def stop(self):
        print('Shutting down vehicle and its parts...')
        for entry in self.parts:
            try:
                entry['part'].shutdown()
            except Exception as e:
                print(e)
        print(self.mem.d)
