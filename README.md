# nea

Νέα – Greek for _news_.

## Why

*	Getting updates online in 2018 sucks. I don't want to use Twitter or Facebook or any other site that lets my attention span drop to the level of a two-year-old.
*	Good old RSS feeds are the solution; they come with more signal and less noise. But I don't want to use an RSS feed reader, because I don't need an app to follow the four to five people I want to read regularly.
*	I’m good at e-mail; over the years I developed techniques to stay on top of my inbox, so getting new reads delivered to my inbox would be perfect. 
*	Yet, I don’t want to get an e-mail every time someone I follow posts something new. I want to receive a digest once a week. 

## What

I want to build a thing that:

*	Takes in a list of RSS feeds. That list will be in a file for the time being. 
*	Pull the updates of all feeds.
*	Parse the feeds and extract all items that were published during the last seven days. 
*	Sends an email to me, containing titles and links to all the new articles grouped by blog. 

## Deploy

To deploy, run the deployment script:

```sh
./deploy.sh --email=joe@example.com --profile=joe --stage=prod

```

### Arguments

| argument             | default   | description                                                 |
|----------------------|-----------|-------------------------------------------------------------|
| `email`              |           | The address used as sender and receiver for the feed email. | 
| `profile` (optional) | `default` | AWS credentials profile to use when deploying.              |
| `stage` (optional)   | `dev`     | The name of the stage.                                      |
