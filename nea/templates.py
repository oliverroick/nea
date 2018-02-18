from string import Template


mail = Template("""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
 <head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <title>Weekly digest</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
 </head>
 <body>
  <ul>$posts</ul>
 </body>
</html>""")

post = Template('<li>$blog_title: <a href="$link">$title</a></li>')


def render(blogs):
    posts = []
    blogs = filter(lambda b: b.items > 0, blogs)

    for blog in blogs:
        for item in blog.items:
            posts.append(post.substitute(blog_title=blog.title,
                                         link=item.link,
                                         title=item.title))

    return mail.substitute(posts=''.join(posts))
