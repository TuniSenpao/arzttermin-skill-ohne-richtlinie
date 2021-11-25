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

from datetime import datetime, timedelta
from mycroft import MycroftSkill, intent_handler
from mycroft.util.parse import extract_number, extract_datetime


class ArztterminSkillOhneRichtlinie(MycroftSkill):
    def __init__(self):
        super(ArztterminSkillOhneRichtlinie, self).__init__()

    def initialize(self):
        pass
            

    @intent_handler('Reminder.intent')
    def add_unspecified_reminder(self, msg=None):
        self.speak_dialog('RequestAllInformations', expect_response=True)

    @intent_handler('RequestAllInformations.intent')
    def handleAllInformations(self, message):
        time = message.data.get('time')
        date = message.data.get('date')
        name = message.data.get('name')

        if (time is None):
            # TIME:
            time_response = self.get_response('ParticularTime', on_fail='wait.for.answer', num_retries=20)
            # Check if a time was in the response
            dt, rest = extract_datetime(time_response) or (None, None)
            if dt or self.response_is_affirmative(time_response):
                if not dt:
                    # No time specified
                    time = self.get_response('ParticularTime', on_fail='wait.for.answer', num_retries=20) or ''
                    dt, rest = extract_datetime(time) or None, None
                    if not dt:
                        self.speak_dialog('Fine')
                        return

            time = datetime.strftime(dt, "%H:%M")
        if (date is None):
            date = None
            date_response = self.get_response('ParticularDateAgain', on_fail='wait.for.answer', num_retries=20)
            months = ['januar', 'februar','märz', 'april', 'mai', 'juni', 'juli', 'august', 'september','oktober','november','dezember',
                'januar.', 'februar.','märz.', 'april.', 'mai.', 'juni.', 'juli.', 'august.', 'september.','oktober.','november.','dezember.', '. erster', '. ersten', '. zweiter','. zweiten' ,'. dritter', '. dritten','. 3','. 4','. 5','. 6','. 7','. 8','. 9','. 10','. 11','. 12','. 13','. 14','. 15',
                '. 16','. 17','. 18','. 19','. 20','. 21','. 22','. 23','. 24','. 25','. 26','. 27','. 28','. 29','. 30','. 31']
            days = ['erster', 'ersten', 'zweiter','zweiten' ,'dritter', 'dritten','3','4','5','6','7','8','9','10','11','12','13','14','15',
                '16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
            day = [d for d in days if(d in date_response.lower())]
            month = [m for m in months if(m in date_response.lower())]

            if (bool(day) and bool(month)):
                date = day[-1] + '. ' + month[-1]
        
        if (name is None):
            name = self.get_response('ParticularNameAgain', on_fail='wait.for.answer', num_retries=20)
            name = name.lower().replace('der', '').replace('termin', '').replace('ist', '').replace('bei', '').replace('er heißt', '').replace('ich', '').replace('glaube', '').replace('dieser', '').replace('mein', '').replace('arzttermin', '').replace('arzt', '').replace('ärztin', '')

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
        pass


    

def create_skill():
    return ArztterminSkillOhneRichtlinie()
