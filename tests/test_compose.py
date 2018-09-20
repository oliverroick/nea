from lambdas import nea_compose_results


def test_render():
    assert nea_compose_results.render([]) is None

    blogs = [{
        'title': 'Blog 1',
        'items': [{
            'title': 'Post 1.1',
            'link': 'http://example.com/post1.1'
        }, {
            'title': 'Post 1.2',
            'link': 'http://example.com/post1.2'
        }]
    }, {
        'title': 'Blog 2',
        'items': [{
            'title': 'Post 2.1',
            'link': 'http://example.com/post2.1'
        }]
    }, {
        'title': 'Blog 3',
        'items': []
    }]

    posts = ('<li>Blog 1: <a href="http://example.com/post1.1">Post 1.1</a>'
             '</li><li>Blog 1: <a href="http://example.com/post1.2">'
             'Post 1.2</a>'
             '</li><li>Blog 2: <a href="http://example.com/post2.1">'
             'Post 2.1</a></li>')

    expected = nea_compose_results.mail.substitute(posts=posts)

    actual = nea_compose_results.render(blogs)
    assert actual == expected
