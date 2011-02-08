import logging

from docutils import nodes
from docutils.parsers.rst import directives, Directive

logger = logging.getLogger(__name__)

RST_SETTINGS = {
    'initial_header_level': 2,
    'footnote_references': 'superscript'
    }


class Pygments(Directive):
    """ Source code syntax hightlighting.

    Example:

        .. sourcecode:: python

            My code goes here.

    If you want line numbers, use it like this:

        .. sourcecode:: python
            :linenos:

            My code goes here.

    If you want to use it, don't forget to generate style css.
    """
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = True

    def __init__(self, *args, **kwargs):
        self.VARIANTS = {
            'default': HtmlFormatter(noclasses=False),
            'linenos': HtmlFormatter(noclasses=False, linenos=True),
            }
        self.option_spec = dict((key, directives.flag) for key in self.VARIANTS)
        super(Pygments, self).__init__(*args, **kwargs)

    def run(self):
        self.assert_has_content()
        try:
            lexer = get_lexer_by_name(self.arguments[0])
        except ValueError:
            # no lexer found - use the text one instead of an exception
            lexer = TextLexer()
        # take an arbitrary option if more than one is given
        variant = self.options and self.options.keys()[0] or 'default'
        formatter = self.VARIANTS[variant]
        parsed = highlight(u'\n'.join(self.content), lexer, formatter)
        return [nodes.raw('', parsed, format='html')]

try:
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name, TextLexer
    from pygments.formatters import HtmlFormatter
    directives.register_directive('sourcecode', Pygments)
except ImportError:
    logger.debug('Pygments are not installed')
