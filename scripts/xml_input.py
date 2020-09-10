from scripts.licence import Licence
from scripts.device import Device
from scripts.html import clean_html



class XmlInput:
    def __init__(self, doc):

        self.__validation_report = []
        self.general_id = doc.getElementsByTagName("general")
        self.car_data = doc.getElementsByTagName("car_data")
        self.common_data = doc.getElementsByTagName("common_data")
        self.device_data = doc.getElementsByTagName("device_data")
        try:
            result_temp = doc.getElementsByTagName("result")[0]
            result_value = result_temp.firstChild.data
            clean_result = clean_html(result_value)
            self.result = clean_result
        except IndexError as err:
            pass
        self.__id = 0
        self.licence_number = None  # redundant
        self.__device_number = None  # redundant
        self.__bln_general_id = False
        self.__bln_validate_year = False
        self.__bln_validate_vin_car = False
        self.__bln_validate_date = True
        self.__bln_validate_device = False
        self.__country_code = None
        self.__bln_validate_licence = False
        self.__bln_calibration_pass = False

    def get_country_code(self):
        return self.__country_code

    def __set_country_code(self, val):
        self.__country_code = val


    def get_validation_report(self):
        list_items = ''
        for item in self.__validation_report:
            if str(item).find('failed') > 0:
                list_items += '<li>{}</li>'.format(str(
                    item).replace('failed', '<b><font color="red">FAILED</font></b>'))
            elif str(item).find('passed') > 0:
                list_items += '<li>{}</li>'.format(str(
                    item).replace('passed', '<b><font color="green">PASSED</font></b>'))
            else:
                list_items += '<li>{}</li>'.format(str(item))

        my_list = '<ul>{}</ul>'.format(list_items)
        return my_list

    def set_validation_report(self, description):
        self.__validation_report.append(description)

    def get_bln_general_id(self):
        return self.__bln_general_id

    def set_bln_general_id(self, val):
        self.__bln_general_id = val

    def get_bln_validate_year(self):
        return self.__bln_validate_year

    def set_bln_validate_year(self, val):
        self.__bln_validate_year = val

    def get_bln_validate_vin_car(self):
        return self.__bln_validate_vin_car

    def set_bln_validate_vin_car(self, val):
        self.__bln_validate_vin_car = val

    def get_bln_validate_date(self):
        return self.__bln_validate_date

    def set_bln_validate_date(self, val):
        self.__bln_validate_date = val

    def get_bln_validate_device(self):
        return self.__bln_validate_device

    def set_bln_validate_device(self, val):
        self.__bln_validate_device = val

    def set_bln_validation_licence(self, val):
        self.__bln_validate_licence = val

    def get_bln_validation_licence(self):
        return self.__bln_validate_licence

    def get_calibration_pass(self):
        return self.__bln_calibration_pass

    def __set_calibration_pass(self, val):
        self.__calibration_pass = val

    def get_device_no(self):
        if self.__device_number:
            return self.__device_number
        else:
            return 'Unknown device number'

    def __set_device_no(self, val):
        self.__device_number = val

    def get_id(self):
        return self.__id

    def __set_id(self, val):
        self.__id = val

    def get_validation_pass(self):
        if self.get_bln_general_id() and \
                self.get_bln_validate_year() and \
                self.get_bln_validate_vin_car() and \
                self.get_bln_validate_date() and \
                self.get_bln_validate_device() and \
                self.get_bln_validation_licence():
            return True
        else:
            return False

    def validation_passed_for_non_domiciled_bucket(self):
        if self.get_bln_general_id() and \
                self.get_bln_validate_year() and \
                self.get_bln_validate_vin_car() and \
                self.get_bln_validate_date() and \
                not(self.get_bln_validate_device()) and \
                self.get_bln_validation_licence():
            return True
        else:
            return False

    def validate_fields(self):
        self.__validate_general_id()
        self.__validate_year()
        self.__validate_device()
        self.__validate_vin_car()
        self.__validate_date()
        return self.get_validation_report()

    def validation_failure_massage(self, method_name, suggested_fix):
        """
        :param method_name: The validation method that was being assessed
        :param suggested_fix: Contextual information suggesting a potential fix
        :return: Response that will form the body of an exception email
        """
        return "The validation for {0} failed. Suggested fix: {1}".format(method_name, suggested_fix)

    def validation_pass_massage(self, method_name):
        """
        :param method_name: The validation method that was being assessed
        :return: Response that can form the body of an email to group admins
        """
        return "The validation for {0} passed".format(method_name)

    def __validate_general_id(self):
        try:
            if len(self.general_id) == 0:
                self.set_validation_report(self.validation_failure_massage("GENERAL ID",
                                                                           "general id is missing from file"))
            else:
                for item in self.general_id:
                    general_id = item.getElementsByTagName("id")[0]
                    general_id_value = general_id.firstChild.data
                    if general_id_value is None:
                        self.set_validation_report(self.validation_failure_massage("GENERAL ID",
                                                                                   "general id tag is not in file"))
                    else:
                        self.set_bln_general_id(True)
                        self.__set_id(general_id_value)
                        self.set_validation_report(self.validation_pass_massage("GENERAL ID"))
        except IndexError as error:
            self.set_validation_report(self.validation_failure_massage("GENERAL_ID",
                                                                       "general id is missing "
                                                                       "from file {0}".format(error)))
        except AttributeError as error:
            self.set_validation_report(self.validation_failure_massage("GENERAL >> ID",
                                                                       "<general><id> is missing "
                                                                       "from file {0}".format(error)))

    def __validate_year(self):
        try:
            if len(self.car_data) == 0:
                self.set_validation_report(self.validation_failure_massage("YEAR", "year is missing from the file"))
            else:
                for item in self.car_data:
                    manufacturer = item.getElementsByTagName("year")[0]
                    if manufacturer is None:
                        self.set_validation_report(self.validation_failure_massage("YEAR", "year is missing "
                                                                                   "from file"))
                    else:
                        self.set_bln_validate_year(True)
                        self.set_validation_report(self.validation_pass_massage("YEAR"))
        except IndexError as error:
            self.set_validation_report(self.validation_failure_massage("YEAR", "year is missing "
                                                                               "from file {0}".format(error)))
        except AttributeError as error:
            self.set_validation_report(self.validation_failure_massage("YEAR", "year value "
                                                                               "is missing from "
                                                                               "file {0}".format(error)))

    def __validate_vin_car(self):
        valid_vin_char_lengths = [17, 12]
        try:
            if len(self.car_data) == 0:
                self.set_validation_report(self.validation_failure_massage("VIN_CAR", "vin_car value "
                                                                                      "is missing from file"))
            else:
                for item in self.car_data:
                    vin_car = item.getElementsByTagName("vin_car")[0]
                    vin_car_value = vin_car.firstChild.data
                    if vin_car is None:
                        self.set_validation_report(self.validation_failure_massage("VIN_CAR", "vin_car "
                                                                                              "is missing from file"))
                    elif len(str(vin_car_value)) not in valid_vin_char_lengths:
                        self.set_validation_report(self.validation_failure_massage("VIN_CAR", "vin number is "
                                                                                              "not in the correct "
                                                                                              "format. Vin numbers "
                                                                                              "must be between 12 "
                                                                                              "and 17 characters in "
                                                                                              "length"))
                    else:
                        self.set_bln_validate_vin_car(True)
                        self.set_validation_report(self.validation_pass_massage("VIN_CAR"))
        except IndexError as error:
            self.set_validation_report(self.validation_failure_massage("VIN_CAR", "vin_car value "
                                                                                  "is missing from "
                                                                                  "file {0}".format(error)))
        except AttributeError as error:
            self.set_validation_report(self.validation_failure_massage("VIN_CAR", "vin_car value "
                                                                                  "is missing from "
                                                                                  "file {0}".format(error)))

    def __validate_date(self):
        try:
            if len(self.common_data) == 0:
                self.set_validation_report(self.validation_failure_massage("COMMON DATA", "Cannot detect common_data "
                                                                                          "during validation"))
            else:
                for item in self.common_data:
                    common_data_date = item.getElementsByTagName("date")[0]
                    common_data_date_value = item.getElementsByTagName('date')[0].firstChild.data
                    if common_data_date is None:
                        self.set_validation_report(self.validation_failure_massage("DATE", "Cannot find date"))
                        self.set_bln_validate_date(False)
                    if common_data_date_value is None:
                        self.set_validation_report(self.validation_failure_massage("DATE", "Cannot find date value"))
                        self.set_bln_validate_date(False)
                if self.get_bln_validate_date():
                    self.set_validation_report(self.validation_pass_massage("DATE"))
        except IndexError as error:
            self.set_validation_report(self.validation_failure_massage("DATE", "date "
                                                                               "is missing from "
                                                                               "file {0}".format(error)))
        except AttributeError as error:
            self.set_validation_report(self.validation_failure_massage("DATE", "Cannot find date "
                                                                               "value: {0}. The data "
                                                                               "item within the tag is "
                                                                               "missing".format(error)))

    def __validate_device(self):
        try:
            if len(self.device_data) == 0:
                self.set_validation_report(self.validation_failure_massage("DEVICE", "device_no is missing from the file"))
            else:
                for item in self.device_data:
                    device_no = item.getElementsByTagName("device_no")[0]
                    device_no_value = device_no.firstChild.data
                    if device_no is None:
                        self.set_validation_report(self.validation_failure_massage("DEVICE", "device_no value "
                                                                                             "not in file"))
                    else:
                        # validate licence after device validation since there is a dependency here
                        device = Device(device_no_value)
                        if device.load_by_device_number(device_no_value):
                            self.__set_device_no(device_no_value)
                            self.set_bln_validate_device(True)
                            self.set_validation_report(self.validation_pass_massage("DEVICE"))
                            self.__set_country_code(device.get_country_code())
                            self.__validate_licence(device.get_country_code())
                        else:
                            self.set_validation_report(self.validation_failure_massage("DEVICE", "device_no "
                                                                                                 "not in file. "
                                                                                                 "Add to list"))
                            self.__validate_licence()
        except IndexError as error:
            self.set_validation_report(self.validation_failure_massage("DEVICE", "device_no tag "
                                                                                 "not in file {0}.".format(error)))
        except AttributeError as error:
            self.set_validation_report(self.validation_failure_massage("DEVICE", "device_no value "
                                                                                 "is missing from "
                                                                                 "file {0}".format(error)))

    def __validate_licence(self, country_code=""):
        """
        :param country_code: optional. Emission of the country_code variable will mean the
        validation runs a generic validation
        """
        try:
            for item in self.car_data:
                licence = item.getElementsByTagName("licence")[0]
                if licence is not None:
                    license_value = str(item.getElementsByTagName('licence')[0].firstChild.data)
                    if license_value is None:
                        self.set_validation_report(self.validation_failure_massage("LICENCE", "license value "
                                                                                              "is missing"))
                    else:
                        vehicle_license = Licence(country_code)
                        self.licence_number = license_value
                        if vehicle_license.get_valid_country_code():
                            method = "validate_" + vehicle_license.get_country()
                        else:
                            method = "validate_generic"
                        licence_validation = vehicle_license.run_anonymous_validation(method, license_value)
                        if not licence_validation:
                            self.set_validation_report(self.validation_failure_massage("LICENCE", "the licence format "
                                                                                       "validation failed "))
                        else:
                            self.set_bln_validation_licence(True)
                            self.set_validation_report(self.validation_pass_massage("LICENCE"))
                else:
                    self.set_validation_report(self.validation_failure_massage("LICENCE", "Cannot find tag licence"))
        except IndexError as error:
            self.set_validation_report(self.validation_failure_massage("LICENCE", "Cannot find tag "
                                                                                  "licence in file {0}".format(error)))
        except AttributeError as error:
            self.set_validation_report(self.validation_failure_massage("LICENCE", "licence value "
                                                                                  "is missing from "
                                                                                  "file {0}".format(error)))





