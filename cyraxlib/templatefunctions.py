from jinja2 import contextfunction
from cyraxlib import utils

@contextfunction
def url_for(context, path):
    basepath = utils.get_base_path(context['site'].url)
    return utils.safe_url_join(basepath, path)


@contextfunction
def absolute_url_for(context, path):
    return utils.safe_url_join(context['site'].url, path)


functions = [url_for, absolute_url_for]

