import debugpy
from .app import application  # noqa # pylint: disable=unused-import

debugpy.listen(5678)
debugpy.wait_for_client()
