from .app import application  # noqa
import debugpy
debugpy.listen(5678)
debugpy.wait_for_client()
