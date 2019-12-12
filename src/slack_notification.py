# -*- coding:utf-8 -*-

import requests
import json

class SlackNotification(object):
    def __init__(self, hook_url, channel, icon_emoji=":arrows_counterclockwise:", username="MySQL-DDL-WATCHER"):
        self._hook_url = hook_url
        self._channel = channel
        self._icon_emoji = icon_emoji
        self._username = username

    def _notification(self, text, attachments=None):
        payload = dict({
            "channel": self._channel,
            "text": text,
            "icon_emoji": self._icon_emoji,
            "username": self._username,
            "mrkdwn": True,
        })
        if attachments:
            payload["attachments"] = attachments

        post_body = dict({
            'payload': json.dumps(payload, ensure_ascii=False)
        })

        requests.post(self._hook_url, data=post_body)

    def notification(self, diffs):
        text = u"``` {text} ```".format(text=json.dumps(diffs, indent=2, ensure_ascii=False))
        self._notification(text)
