# -*- coding: utf-8 -*-
default_app_config = 'src.comments.apps.CommentsConfig'


def get_form():
    from src.comments.forms import CommentRecaptchaForm
    return CommentRecaptchaForm