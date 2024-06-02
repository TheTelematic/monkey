from api.ai.ask import router as ai_ask_router  # noqa: F401 # pylint: disable=unused-import
from api.ai.hello import router as ai_hello_router  # noqa: F401 # pylint: disable=unused-import
from api.ai.summary import router as ai_summary_router  # noqa: F401 # pylint: disable=unused-import
from api.apps.sandbox import router as ws_sandbox_router  # noqa: F401 # pylint: disable=unused-import
from api.apps.summary_and_translate import (  # noqa: F401 # pylint: disable=unused-import
    router as ws_summary_and_translate_router,
)
from api.probes import router as probes_router  # noqa: F401 # pylint: disable=unused-import
from api.ui import router as ui_router  # noqa: F401 # pylint: disable=unused-import
