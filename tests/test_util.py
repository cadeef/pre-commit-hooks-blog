# from pathlib import Path

import pytest  # type: ignore[import]

from pre_commit_hooks_blog.util import Hook, Post


@pytest.fixture
def post(test_files):
    """
    Returns an instances of pre_commit_hooks_blog.util.Post
    """
    return Post.load(test_files["good.md"]["path"])


@pytest.fixture
def hook():
    """
    Returns an instances of pre_commit_hooks_blog.util.Post
    """
    return Hook(name=__name__, function=run_step, ansi=True, verbose=True)


def test_hook_init():
    hook = Hook(name=__name__, function=run_step, ansi=True, verbose=True)
    assert isinstance(hook, Hook)


def test_post_load(post):
    """Verify that attributes are properly parsed"""
    assert post.title == "About"
    assert post.tags == ["about", "faq", "cade"]
    assert isinstance(post.meta, dict)
    assert isinstance(post.body(), str)


def test_post_body_list(post):
    assert isinstance(post.body(return_type="list"), list)
    assert len(post.body(return_type="list")) == 63


def run_step():
    # TODO: Implement
    pass
