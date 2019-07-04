import praw
from keys import keys
import json
import os
import io
# REST API connection
reddit = praw.Reddit(client_id=keys['client_id'],
                     client_secret=keys['client_secret'],
                     user_agent=keys['user_agent'],
                     username=keys['username'],
                     password=keys['password'])

subreddit = reddit.subreddit(keys['subreddit'])
if os.path.isfile('Submissions.json') and os.access('Submissions.json', os.R_OK):
        # checks if file exists
        print ("File exists and is readable")
else:
    print ("Either file is missing or is not readable, creating file...")
    with io.open('Submissions.json', 'w') as db_file:
        db_file.write(json.dumps({}))

with open('Submissions.json') as f:
  submissionData = json.load(f)

if os.path.isfile('Comments.json') and os.access('Submissions.json', os.R_OK):
        # checks if file exists
        print ("File exists and is readable")
else:
    print ("Either file is missing or is not readable, creating file...")
    with io.open('Comments.json', 'w') as db_file:
        db_file.write(json.dumps({}))

with open('Comments.json') as f_c:
  commentData = json.load(f_c)

# Bot Credits, please don't remove them, if you do its fine too, im a comment not a cop
botCredits = "\n_________________\nThis is a bot providing a service. If you have any questions, please [contact the moderators](https://reddit.com/message/compose?to=/r/"+keys['subreddit']+")\n Bot Credit: [/u/MrEdinLaw](http://www.reddit.com/user/MrEdinLaw) | [GitHub](http://www.github.com/mredinlaw)."

for comment in subreddit.stream.comments():
    if comment.author_flair_template_id == keys['css_class']:
        submission = reddit.submission(id=comment.link_id[3:])
        if submission.id not in submissionData:
            reply = submission.reply("This is a list of links to comments made by [/r/" + keys['subreddit'] + "/](https://www.reddit.com/r/" + keys['subreddit'] + "/) staff in this thread: " +
                                     "\n\n- [Comment by /u/" + comment.author.name + "](" + comment.permalink + ")\n\n>" + comment.body + botCredits)
            reply.mod.distinguish(sticky=True)
            print("Comment Stickied\n\t" + "https://www.reddit.com" + reply.permalink)

            submissionData[submission.id] = reply.id
            with open('Submissions.json', 'w') as json_file:
                json.dump(submissionData, json_file)
                
            commentData[comment.id] = comment.id
            with open('Comments.json', 'w') as json_file:
                json.dump(commentData, json_file)
        else:
            if comment.id not in commentData:
                commentEdit = reddit.comment(id=submissionData[submission.id])
                oldText = commentEdit.body.replace(botCredits, "")
                commentEdit.edit(
                    oldText + "\n\n- [Comment by /u/" + comment.author.name + "](" + comment.permalink + ")\n\n>" + comment.body + botCredits)
                reply = commentEdit

                commentData[comment.id] = comment.id
                with open('Comments.json', 'w') as json_file:
                    json.dump(commentData, json_file)

                print("Comment Stickied\n\t" + "https://www.reddit.com" + reply.permalink)
