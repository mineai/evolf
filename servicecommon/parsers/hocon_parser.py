from pyhocon import ConfigFactory
from pyhocon import HOCONConverter
import json

from framework.interfaces.parser.parser import Parser


class ParseHocon(Parser):
    """
    This class parses a hocon file to
    a dictionary.
    """

    @staticmethod
    def parse(hocon_file):
        """
        This function takes a hocon file
        and returns a dictionary.
        :param hocon_file: Path to hocon file.
        :returns conf: Dictionary version of passed hocon file
        """
        conf = ConfigFactory.parse_file(hocon_file)
        conf = json.loads(HOCONConverter.convert(conf, 'json'))
        return conf