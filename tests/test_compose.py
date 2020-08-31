from lambdas import nea_compose_results
from unittest.mock import patch


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

    posts = (
        '<h2 style="font-size: 1rem; margin: 1rem 0 0 0;">Blog 1</h2>'
        '<ul style="margin: 0; padding-left: 1rem;"><li><a href="http://example.com/post1.1">Post 1.1</a></li>'
        '<li><a href="http://example.com/post1.2">Post 1.2</a></li></ul>'
        '<h2 style="font-size: 1rem; margin: 1rem 0 0 0;">Blog 2</h2>'
        '<ul style="margin: 0; padding-left: 1rem;"><li><a href="http://example.com/post2.1">Post 2.1</a></li></ul>'
    )

    expected = nea_compose_results.mail.substitute(posts=posts)

    actual = nea_compose_results.render(blogs)
    assert actual == expected


@patch('lambdas.nea_compose_results.render')
def test_lambda_handler(render):
    render.return_value = 'Message'

    event = {
        'email_to': 'john@example.com',
        'email_from': 'jane@example.com',
        'blogs': [{'title': 'Some Blog'}]
    }

    result = nea_compose_results.lambda_handler(event, {})

    assert result['message'] == 'Message'
    assert result['email_to'] == event['email_to']
    assert result['email_from'] == event['email_from']
    render.assert_called_with(event['blogs'])
