__all__ = ("router_list", "middleware_list")

# usually routers would be in sub dirs
from .example_router_file import example_router

router_list = [example_router]
middleware_list = []
