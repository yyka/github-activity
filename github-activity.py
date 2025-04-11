import argparse
import re
import requests
import sys
from constants import EVENTS


def parser_func():
    parser = argparse.ArgumentParser(
        description=(
            "A simple CLI program to fetch the "
            "recent activity of a GitHub user"
            ), usage = (
                "github-activity.py [-h | --help] [-e | --events]\n"
                "                          "
                "[<username> [-f <filter>] [-l <limit>]]"
            ))
    parser.add_argument("-e", "--events", action="store_true",
                        help="list event types filters")
    parser.add_argument("username", nargs="?", help="github username")
    parser.add_argument("-f", type=str, help="filter results by type",
                        metavar="filter", dest="filter")
    parser.add_argument("-l", type=int, help="limit output size",
                        metavar="limit", dest="limit")
    
    return parser


def main():
    parser = parser_func()
    args = parser.parse_args()
    
    try:
        if args.events is True:
            if (args.filter is None
                and args.limit is None
                and args.username is None):
                list_events(EVENTS)
                sys.exit(0)
            else:
                raise SyntaxError
        elif args.username is None:
            raise SyntaxError
        elif args.filter is not None:
            if args.filter not in EVENTS.keys():
                raise ValueError
    except ValueError:
        sys.exit(f"Filter does not exist. See: \"{sys.argv[0]} -e\"")
    except SyntaxError:
        print(parser.format_usage(), end="")
        sys.exit(1)
    
    username = args.username.strip()

    if not re.fullmatch(r"[a-zA-Z0-9\-]*", username):
        sys.exit("Invalid username")
    
    response = requests.get(
        f"https://api.github.com/users/{username}/events"
        )
    
    match response.status_code:
        case 200:
            data = response.json() # -> list
            if args.filter is not None:
                data = [r for r in data if r["type"] == args.filter]
            if args.limit is not None:
                data = [r for r in data][:args.limit]
            for e in data:
                print(f"- {match_event(e)}")
        case _:
            print(f"An error occured while fetching data "
                  f"from the API: {response.status_code}")
            
    # TODO
    ## Cache fetched data to improve performance
    ## Explore GitHub API to fetch other data
    
def list_events(e):
    for event, desc in e.items():
        print(f"\"{event}\" - {desc}")


def match_event(e: dict):
    '''
    Return formatted string corresponding to event
    '''
    p = e["payload"]
    repo = e["repo"]["name"]
    
    match e["type"]:
        case "CommitCommentEvent":
            s = (f"Commented a commit in {repo}: {p["comment"]})")
        case "CreateEvent":
            s = f"Created a new {p["ref_type"]} in {repo}"
        case "DeleteEvent":
            s = f"Deleted a {p["ref_type"]} in {repo}"
        case "ForkEvent":
            s = f"Forked {p["forkee"]["full_name"]} from {repo}"
        case "GollumEvent":
            s = (f"{p["pages"][0]["action"].title()} wiki page "
                 f"\"{p["pages"][0]["page_name"]}\" in {repo}")
        case "IssueCommentEvent":
            s = f"{p["action"].title()} an issue in {repo}: \"{p["issue"]["title"]}\""
        case "IssuesEvent":
            s = f"{p["action"].title()} an issue in {repo}: \"{p["issue"]["title"]}\""
        case "MemberEvent":
            s = f"{p["action"].title()} {p["member"]} in {repo}"
        case "PublicEvent":
            s = f"Set visibility for {repo} to public"
        case "PullRequestEvent":
            s = f"{p["action"].title()} a pull request in {repo}"
        case "PullRequestReviewEvent":
            s = (f"{p["action"].title()} a pull request "
                 f"review for \"{p["pull_request"]["title"]}\" in {repo}")
        case "PullRequestReviewCommentEvent":
            s = (f"{p["action"].title()} a pull request review "
                 f"comment for \"{p["pull_request"]["title"]}\" in {repo}")
        case "PullRequestReviewThreadEvent":
            s = f"Marked {p["pull_request"]} as {p["action"]} in {repo}"
        case "PushEvent":
            c = len(p["commits"])
            s = f"Pushed {c} commit{"s" if c > 1 else ""} to {repo}"
        case "ReleaseEvent":
            s = f"{p["action"].title()} {p["release"]} in {repo}"
        case "SponsorshipEvent":
            s = f"{p["action"].title()} a sponsorship listing"
        case "WatchEvent":
            s = f"Starred {repo}"
        case _:
            s = f"Unknown"
            
    return s

    
if __name__ == "__main__":
    main()