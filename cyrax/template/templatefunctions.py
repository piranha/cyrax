from jinja2 import contextfunction

from cyrax import utils


@contextfunction
def url_for(context, path):
    if not path:
        return ''
    basepath = utils.base_path(context['site'].url)
    return utils.relpath(
        utils.safe_url_join(basepath, context['entry'].get_relative_url()),
        utils.safe_url_join(basepath, path))


@contextfunction
def absolute_url_for(context, path):
    return utils.safe_url_join(context['site'].url, path)


functions = [url_for, absolute_url_for]

