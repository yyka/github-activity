# github-activity
A simple CLI program to fetch the recent activity of a GitHub user, built in Python

For more info: https://roadmap.sh/projects/github-user-activity

Usage: 'github_activity.py [-h | --help] [-e | --events] [<username> [-f <filter>] [-l <limit>]]'

'''
# show a list of commands
github_activity.py --help

# fetch github activity for a user
github_activity.py <username>

# filter results by type
github-activity.py <username> -f <filter>

# list all event types
github_activity.py -e

# limit output size
github_activity.py <username> -l <limit>

# show yyka's last 3 commits
github_activity.py yyka -l 3 -f PushEvent
'''

<details>
<summary>Misc</summary>
Total time taken: 10h
</details>