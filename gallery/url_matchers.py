class board_url_matcher:
    regex = '^[a-z]{1,20}$'
    def to_python(self, value):
        return value

    def to_url(self, value):
        return str(value)
