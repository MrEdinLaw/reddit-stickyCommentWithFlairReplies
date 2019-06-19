import praw
from keys import keys

# REST API connection
reddit = praw.Reddit(client_id=keys['client_id'],
                     client_secret=keys['client_secret'],
                     user_agent=keys['user_agent'],
                     username=keys['username'],
                     password=keys['password'])

subreddit = reddit.subreddit(keys['subreddit'])
commentData = {}

# Bot Credits, please don't remove them, if you do its fine too, im a comment not a cop
botCredits = "\n\n^(| [Creator](http://www.reddit.com/user/MrEdinLaw) | [GitHub](http://www.github.com/mredinlaw) |)"

for comment in subreddit.stream.comments():
    if comment.author_flair_template_id == "8e18f8a6-5bd2-11e9-a942-0e5dd855cb30":
        submission = reddit.submission(id=comment.link_id[3:])
        if submission.id not in commentData:
            reply = submission.reply("Comments made by moderators: " +
                                     "\n\n[Comment by " + comment.author.name + "](" + comment.permalink + ")\n\n" + comment.body + botCredits)
            reply.mod.distinguish(sticky=True)
            commentData[submission.id] = reply.id
        else:
            commentEdit = reddit.comment(id=commentData[submission.id])
            oldText = commentEdit.body.replace(botCredits, "")
            commentEdit.edit(
                oldText + "\n\n[Comment by /u" + comment.author.name + "](" + comment.permalink + ")\n\n" + comment.body + botCredits)
            reply = commentEdit

        print("Comment Stickied\n\t" + "https://www.reddit.com" + reply.permalink)
