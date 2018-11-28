# Youtube History Snarfer

## What?
Grab the list of youtube video IDs that a user has watched. Requires authentication as that user.

## Why?
I have reasons. Sure, you could use the great [youtube-dl](https://github.com/rg3/youtube-dl) to do it, but that's >118K lines of code that you'd be allowing to authenticate to youtube's servers. Here I've pulled out just the relevant code, which makes for only ~100 lines to audit if you worry about such things. Of course, there's no reason to suspect `youtube-dl` of doing anything shady, but some people (me) sleep better at night this way.

## How?
`ythistory.py -j cookiefile >videolist.txt`

`ythistory` uses the Netscape cookies.txt format to store cookies. If you don't already have your youtube auth cookies, here's how to get them in Chrome:

1. Log in to youtube, and open a new tab.
2. Hit `F12` and switch to the Network panel.
3. visit https://youtube.com/feed/history
4. Right-click on the first resource that shows up (`history`) and select "Copy -> Copy as cURL"
5. In the command you've just copied, you'll have a section that is `-H 'cookie: ` and then a bunch of `key=value; ` pairs. Copy just the key/value pairs.
6. Run `ythistory.py -j cookiefile -c "COOKIES" --max 1`, pasting the copied key/value pairs instead of `COOKIES` (but keep the double quotes).
7. `cookiefile` now has your cookies saved as well, no need to pass them on the command line anymore.

If you only want to incrementally list video ids after a certain point, use `--since` and a list of videos that delimit the oldest watching history you want to include (the history doesn't track _when_ a video was watched, so I do simple pattern-matching). Eg. to only get the video ids since you finished watching [Clickspring's clock build](https://www.youtube.com/playlist?list=PLZioPDnFPNsETq9h35dgQq80Ryx-beOli) in one sitting, you could pass the last four videos in reverse order:

`ythistory.py -j cookiefile --since "J3ZGlpDa-0g,NsnLVYwqESM,T28sGA597IE,R9m4X_R9HPs"`

Giving `ythistory` a list of videos makes increases confidence that it has found the point you intended, in case you watch the same video, or even a handful of videos, again more recently.

## Who?
I mean, I'm [patrickyeon](https://github.com/patrickyeon), but this is mostly just re-packaging work done by some subset of the [youtube-dl contributors](https://github.com/rg3/youtube-dl/blob/master/AUTHORS).

In the spirit of `youtube-dl`, this code is released into public domain. Do what you want with it.

## Help?
I guess if you want. Bug reports and bugfix PRs accepted, new features highly unlikely to be accepted (the point is to expose auth capabilities to a minimum amount of code). 
