import types

import config
from consumers.types.summaries import make_summary
from consumers.types.translations import translate

consumers = types.SimpleNamespace()
CONSUMER_TRANSLATIONS = "translations"
CONSUMER_SUMMARIES = "summaries"
consumers.TRANSLATIONS = CONSUMER_TRANSLATIONS
consumers.SUMMARIES = CONSUMER_SUMMARIES

ROUTES = {
    consumers.TRANSLATIONS: {"queue": config.RABBITMQ_QUEUE_TRANSLATIONS, "callback": translate},
    consumers.SUMMARIES: {"queue": config.RABBITMQ_QUEUE_SUMMARIES, "callback": make_summary},
}
