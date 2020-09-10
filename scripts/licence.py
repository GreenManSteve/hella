class Licence:
    def __init__(self, country_code):
        self.__country_code = country_code
        self.__country = None
        self.__valid_country_code = True
        self.load_by_country_code(country_code)

    def __set_country_code(self, val):
        self.__country = val

    def get_country_code(self):
        return self.__country_code

    def __set_valid_country_code(self, val):
        self.__valid_country_code = val

    def get_valid_country_code(self):
        return self.__valid_country_code

    def get_country(self):
        return self.__country

    def load_by_country_code(self, country_code):
        countries = {
            "AT": "Austria",
            "AU": "Australia",
            "BE": "Belgium",
            "BR": "Brazil",
            "CH": "Switzerland",
            "DE": "Germany",
            "DK": "Denmark",
            "EE": "Estonia",
            "ES": "Spain",
            "FI": "Finland",
            "FR": "France",
            "GB": "United_Kingdom_of_Great_Britain_and_Northern_Ireland",
            "GR": "Greece",
            "HU": "Hungary",
            "IE": "Ireland",
            "IT": "Italy",
            "LT": "Lithuania",
            "MA": "Morocco",
            "NL": "Netherlands",
            "NO": "Norway",
            "NZ": "New_Zealand",
            "PT": "Portugal",
            "RU": "Russian_Federation",
            "SE": "Sweden",
            "SI": "Slovenia",
            "TR": "Turkey",
        }
        if country_code in countries:
            self.__set_country_code(countries.get(country_code))
            self.__set_valid_country_code(True)
        else:
            self.__set_valid_country_code(False)

    def validate_alpha_numberic_formats(self, license_number):
        val = str(license_number)
        if val.isdigit():
            return True
        else:
            return False

    def run_anonymous_validation(self, method, license_number):
        function_name = method.lower()
        function_string = "self.{0}(\'{1}\')".format(function_name, license_number)
        func = function_string
        result = eval(func)
        return result

    def validate_generic(self, licence_number):
        return self.validate_alpha_numberic_formats(licence_number)

    def validate_austria(self, licence_number):
        return self.validate_alpha_numberic_formats(licence_number)

    def validate_australia(self, licence_number):
        return self.validate_alpha_numberic_formats(licence_number)

    def validate_belgium(self, licence_number):
        result = licence_number.startswith('SOB')
        if result:
            return True
        else:
            return self.validate_alpha_numberic_formats(licence_number)

    def validate_brazil(self, licence_number):
        return self.validate_alpha_numberic_formats(licence_number)

    def validate_switzerland(self, licence_number):
        return self.validate_alpha_numberic_formats(licence_number)

    def validate_germany(self, licence_number):
        return self.validate_alpha_numberic_formats(licence_number)

    def validate_denmark(self, licence_number):
        return self.validate_alpha_numberic_formats(licence_number)

    def validate_estonia(self, licence_number):
        return self.validate_alpha_numberic_formats(licence_number)

    def validate_spain(self, licence_number):
        return self.validate_alpha_numberic_formats(licence_number)

    def validate_finland(self, licence_number):
        return self.validate_alpha_numberic_formats(licence_number)

    def validate_france(self, licence_number):
        return self.validate_alpha_numberic_formats(licence_number)

    def validate_united_kingdom_of_great_britain_and_northern_ireland(self, licence_number):
        return self.validate_alpha_numberic_formats(licence_number)

    def validate_greece(self, licence_number):
        return self.validate_alpha_numberic_formats(licence_number)

    def validate_hungary(self, licence_number):
        return self.validate_alpha_numberic_formats(licence_number)

    def validate_ireland(self, licence_number):
        return self.validate_alpha_numberic_formats(licence_number)

    def validate_italy(self, licence_number):
        return self.validate_alpha_numberic_formats(licence_number)

    def validate_lithuania(self, licence_number):
        return self.validate_alpha_numberic_formats(licence_number)

    def validate_morocco(self, licence_number):
        return self.validate_alpha_numberic_formats(licence_number)

    def validate_netherlands(self, licence_number):
        return self.validate_alpha_numberic_formats(licence_number)

    def validate_norway(self, licence_number):
        return self.validate_alpha_numberic_formats(licence_number)

    def validate_new_zealand(self, licence_number):
        return self.validate_alpha_numberic_formats(licence_number)

    def validate_portugal(self, licence_number):
        return self.validate_alpha_numberic_formats(licence_number)

    def validate_russian_federation(self, licence_number):
        return self.validate_alpha_numberic_formats(licence_number)

    def validate_sweden(self, licence_number):
        return self.validate_alpha_numberic_formats(licence_number)

    def validate_slovenia(self, licence_number):
        return self.validate_alpha_numberic_formats(licence_number)

    def validate_turkey(self, licence_number):
        return self.validate_alpha_numberic_formats(licence_number)




