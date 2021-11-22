# Copyright 2016 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re
import time
from os.path import dirname, join
from datetime import datetime, timedelta
from mycroft import MycroftSkill, intent_handler
from mycroft.util.parse import extract_datetime, normalize
from mycroft.util.time import now_local
from mycroft.util.format import nice_time, nice_date
from mycroft.util import play_wav
from mycroft.messagebus.client import MessageBusClient


class ArztterminSkillOhneRichtlinie(MycroftSkill):
    def __init__(self):
        super(ArztterminSkillOhneRichtlinie, self).__init__()
        self.notes = {}
        self.primed = False

    def initialize(self):
        # Handlers for notifications after speak
        # TODO Make this work better in test
        if isinstance(self.bus, MessageBusClient):
            self.bus.on('speak', self.prime)
            self.bus.on('mycroft.skill.handler.complete', self.notify)
            self.bus.on('mycroft.skill.handler.start', self.reset)

    @intent_handler('Reminder.intent')
    def add_unspecified_reminder(self, msg=None):
        self.speak_dialog('RequestAllInformations', expect_response=True)

    @intent_handler('RequestAllInformations.intent')
    def handleAllInformations(self, message):
        time = message.data.get('time')
        date = message.data.get('date')
        name = message.data.get('name')

        if (time is None):
            self.speak_dialog('debug', data={'debug':'time is None'})
        if (date is None):
            self.speak_dialog('debug', data={'debug':'date is None'})
        if (name is None):
            self.speak_dialog('debug', data={'debug':'name is None'})

        if (time is not None and date is not None and name is not None):
            self.speak_dialog('confirm_arzttermin', data={
                'time': time,
                'date':date,
                'name':name
            })
        else:
            self.speak_dialog('confirm.without.variables')

    def stop(self, message=None):
        if self.__cancel_active():
            self.speak_dialog('ReminderCancelled')
            return True
        else:
            return False

    def shutdown(self):
        if isinstance(self.bus, MessageBusClient):
            self.bus.remove('speak', self.prime)
            self.bus.remove('mycroft.skill.handler.complete', self.notify)
            self.bus.remove('mycroft.skill.handler.start', self.reset)


    

def create_skill():
    return ArztterminSkillOhneRichtlinie()
