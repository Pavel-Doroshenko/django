class FourDigitYearConverter:
    regex = "[0-9]{4}"

    @staticmethod
    def to_python(_self, value):
        return int(value)

    @staticmethod
    def to_url(_self, value):
        return "%04d" % value
