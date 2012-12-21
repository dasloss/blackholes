from models import get_db, clear_candidates, insert_candidates
import json
import sys

def load_data():
    data = json.load(open("data.json"))
    count = len(data)
    print "Found {count} fresh things to load".format(count=count)
    db = get_db()
    count = db.candidate.count()
    print "Clearing {count} stale things from collection".format(count=count)
    clear_candidates()
    for candidate in data:
        db.candidate.insert(candidate, safe=True)
    count = db.candidate.count()
    print "{count} fresh things now in collection!".format(count=count)

def prompt():
    print "This will clear the existing thing DB and load it from data.json!"
    print "Are you sure you want to continue? [y/N]",
    resp = raw_input()
    if resp.strip() == "y":
        load_data()
    else:
        print "Aborting."
        sys.exit(1)

if __name__ == "__main__":
    prompt()
