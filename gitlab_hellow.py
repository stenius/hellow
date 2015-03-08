import datetime
import subprocess

now = datetime.datetime.now()
message = 'hello'

characters = {
    'h': [
        [True,False,False,True],
        [True,False,False,True],
        [True,True,True,True],
        [True,False,False,True],
        [True,False,False,True]
        ],
    'e': [
        [True,True,True,True],
        [True,False,False,False],
        [True,True,True,False],
        [True,False,False,False],
        [True,True,True,True]
        ],
    'l': [
        [True,False,False,False],
        [True,False,False,False],
        [True,False,False,False],
        [True,False,False,False],
        [True,True,True,True]
        ],
    'o': [
        [False,True,True,False],
        [True,False,False,True],
        [True,False,False,True],
        [True,False,False,True],
        [False,True,True,False]
        ]
}


def make_commit(day):
    index = day - start_day
    index_str = str(index.days)
    subprocess.call(['touch', index_str])
    subprocess.call(['git',  'add', index_str])
    subprocess.call(['git',  'commit', '-m', '"printing %s"' % message])
    days = (now-day).days
    asdf = subprocess.check_output(['date', '--date', '%s day ago' % days]).rstrip()
    env = {'GIT_COMMITTER_DATE': asdf}
    subprocess.call(['git',  'commit', '--amend', '--date', '"%s"' % asdf, '-m', '"printing %s"' % message], env=env)


msg_weeks = 0
#figure out how many weeks to go back plus space between each character
for i in message:
    msg_weeks += len(characters[i][0]) + 1

# if not saturday, begin a new week
if now.weekday() == 5:
    msg_weeks -= 1
    last_monday = now - datetime.timedelta(days = now.weekday())
elif now.weekday() == 0:
    last_monday = now - datetime.timedelta(days=6)
else:
    last_monday = now - datetime.timedelta(days = now.weekday() + 1)


#last monday should actually be a week later
last_monday += datetime.timedelta(weeks=1)

start_day = last_monday - datetime.timedelta(weeks=msg_weeks - 1)
day = start_day
for c in message:
    for j in range(4):
        for i in range(7):
            if i > 0 and i < 6:
                value = characters[c][i - 1][j]
            else:
                value = False
            if value:
                make_commit(day)

            day += datetime.timedelta(days=1)
    if day != last_monday:
        for i in range(7):
            value = False
            day += datetime.timedelta(days=1)
            if value:
                make_commit(day)
