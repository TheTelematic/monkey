import types

import config
from consumers.types.translations import translate

consumers = types.SimpleNamespace()
CONSUMER_TRANSLATIONS = "translations"
consumers.TRANSLATIONS = CONSUMER_TRANSLATIONS

ROUTES = {
    consumers.TRANSLATIONS: {"queue": config.RABBITMQ_QUEUE_TRANSLATIONS, "callback": translate},
}
