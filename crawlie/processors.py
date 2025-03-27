import re
from itemloaders import arg_to_iter


class RemoveRegex(object):
    """
    This processor removes regex patterns from a string/list of strings
    """
    def __init__(self, patterns):
        if not patterns:
            raise ValueError('Please type a pattern that you want to match')

        self.patterns = patterns
        self.processor = StripAndRemoveConsecutiveSpaces()

    def __call__(self, value):
        values = arg_to_iter(value)
        patterns = arg_to_iter(self.patterns)
        try:
            compiled_patterns = [re.compile(p) for p in patterns]

            new_values = []
            for v in values:
                if not isinstance(v, str):
                    # ignore everything that's not a string
                    continue

                for pattern in compiled_patterns:
                    v = pattern.sub('', v)

                v = self.processor(v)

                if '' != v:
                    new_values.append(v)

            if len(new_values) < 1:
                return None if not isinstance(value, list) else []

            return new_values[0] if not isinstance(value, list) else new_values

        except TypeError:
            raise ValueError('Invalid patten data type provided. The regex pattern has to be "str".')
        except re.error:
            raise ValueError("Invalid patterns were found. Please ensure that you didn't miss anything")


class StripAndRemoveConsecutiveSpaces(object):
    def __call__(self, value):
        return re.sub(r'\s+', ' ', value).strip(' \r\n\t') if isinstance(value, str) else None
