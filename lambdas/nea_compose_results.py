from string import Template


mail = Template("""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
 <head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <title>Weekly digest</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
 </head>
 <body>
  <h1>Happy Monday</h1>
  <p>Here are all blogs that were published during the last week</p>
  $posts
 </body>
</html>""")

blog_template = Template('<h2>$blog_title</h2><ul>$posts</ul>')
post_template = Template('<li><a href="$link">$title</a></li>')


def render(blogs):
    blogs = filter(lambda b: len(b['items']) > 0, blogs)

    rendered_blogs = []
    for blog in blogs:
        rendered_posts = [
            post_template.substitute(link=item['link'], title=item['title'])
            for item in blog['items']
        ]

        rendered_blogs.append(
            blog_template.substitute(
                blog_title=blog['title'],
                posts=''.join(rendered_posts)
            )
        )

    if not rendered_blogs:
        return None

    return mail.substitute(posts=''.join(rendered_blogs))


def lambda_handler(event, context):
    return {
        'message': render(event['blogs']),
        'email_from': event['email_from'],
        'email_to': event['email_to'],
    }
