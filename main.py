from eklasescraper import eklase
import dotenv
from os import getenv
from ics import Calendar, Event
import datetime

dotenv.load_dotenv()

eklase = eklase.Scraper()

eklase.login(getenv("USERNAME"), getenv("PASSWORD"), getenv("PROFILE_ID"), getenv("ORGANIZATION_ID"), getenv("PROFILE_INDEX"))

# Fetch 3 diaries
now = datetime.datetime.now()

diaries = []

for week in range(-2, 3):
    thisweek = now + datetime.timedelta(weeks=week)
    diaries.append(eklase.fetch_diary(thisweek.strftime("%d.%m.%Y.")))
    
# Fetch timetable
lesson_times_list = eklase.fetch_lesson_times()

lesson_times = {}

for time in lesson_times_list:
    index = time.index
    lesson_times[index] = time
    

# Create new calendar
c = Calendar()

for diary in diaries:
    for day in diary.days:
        for lesson in day.lessons:
            e = Event(            
                name = lesson.lesson,
                begin = day.timestamp + (lesson_times[lesson.index].start_timedelta * 60),
                end = day.timestamp + (lesson_times[lesson.index].end_timedelta * 60),
                location = lesson.room,
                description = "\n".join(["Subject:", lesson.subject.text, "\nHomework:", lesson.hometask.text, "\nScore:", lesson.score]),
                uid = "_".join([str(day.timestamp), lesson.index, "@eklasecalendar"]),
                last_modified = now
            )
            
            c.events.add(e)
                
        
with open('eklase.ics', 'w') as f:
    f.writelines(c.serialize_iter())