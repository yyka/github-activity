# github-activity
A simple CLI program to fetch the recent activity of a GitHub user, built in Python

For more info: https://roadmap.sh/projects/github-user-activity

Usage: 'github-activity.py [-h | --help] [-e | --events] [<username> [-f <filter>] [-l <limit>]]'

'''
# show a list of commands
github-activity.py --help

# fetch github activity for a user
github-activity.py <username>

# filter results by type
github-activity.py <username> -f <filter>

# list all event types
github-activity.py -e

# limit output size
github-activity.py <username> -l <limit>

# show yyka's last 3 commits
github-activity.py yyka -l 3 -f PushEvent
'''

<details>
<summary>Misc</summary>
Total time taken: 10h
</details>