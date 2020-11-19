from scripts.base import Base
from boto3.dynamodb.conditions import Key
from scripts.hash import sha_3_hex_digest
from scripts.html import clean_html
import boto3
client = boto3.client('dynamodb')


class Xml_Hella_gutmann(Base):
    def __init__(self, doc, s3_link, country_code):
        Base.__init__(self)
        self.xml_file = doc
        self.s3_link = s3_link
        self.country_code = country_code
        self.__records_list = []
        self.ok_to_go = True
        self.__validation_report = []
        self.__prepare_record_write_list()


    def get_calibration_date(self):
        try:
            common_data = self.xml_file.getElementsByTagName("common_data")
            date_value = common_data[0].getElementsByTagName("date")[0].firstChild.data
            calibration_date = date_value[0:10]
            return calibration_date[0:10]
        except AttributeError as err:
            return '0000-00-00'

    def get_ttl(self):
        return 1

    def get_ok_to_go(self):
        return self.ok_to_go

    def get_vin_car(self):
        vin_car = self.xml_file.getElementsByTagName("vin_car")[0]
        vin_car_value = vin_car.firstChild.data
        return vin_car_value

    def get_device_id(self):
        device_no = self.xml_file.getElementsByTagName("device_no")[0]
        device_no_value = device_no.firstChild.data
        return device_no_value

    def get_id(self):
        id_no = self.xml_file.getElementsByTagName("id")[0]
        id_value = id_no.firstChild.data
        return id_value

    def get_records_list(self):
        return self.__records_list

    def __set_records_list(self, val):
        self.__records_list.append(val)

    def get_bucket(self):
        return self.s3_link['bucket_name']

    def get_file_id(self):
        return self.s3_link['file_id']

    def get_validation_report(self):
        return self.__validation_report

    def set_validation_report(self, msg):
        self.__validation_report.append(msg)

    def confirm_record_not_saved(self):
        table = "Hella-Gutmann"
        pk = 'device_no-{}'.format(self.get_device_id())
        sk = 'id-{}'.format(self.get_id())
        response = client.query(
            TableName='Hella-Gutmann',
            KeyConditionExpression="#S = :pk AND #T = :sk",
            ExpressionAttributeNames={
                "#S": "PK", "#T": "SK"
            },
            ExpressionAttributeValues={
                ":pk": {"S": pk},
                ":sk": {"S": sk}
            }
        )
        if response['Count'] != 0:
            self.ok_to_go = False
            self.set_validation_report("The records for this file already exist "
                                       "in the dynamoDb table <i>{0}</i>".format(table))
            return False
        else:
            return True

    def __prepare_record_write_list(self):
        if self.confirm_record_not_saved():
            self.__write_device_data()
            self.__write_car_data()
            self.__write_fele_common_data()
            self.__write_felg_parameter()
            self.__write_result()

    def __write_device_data(self):
        device_data = self.xml_file.getElementsByTagName("device_data")
        i_count = 0
        for item in device_data:
            product_name = item.getElementsByTagName("product_name")[0]
            product_name_value = product_name.firstChild.data
            device_no_value = self.get_device_id()
            general_id = self.get_id()
            i_count += 1
            item = {
                'PK': {'S': 'device_no-{0}'.format(device_no_value)},
                'SK': {'S': 'id-{0}'.format(general_id)},
                'product_name': {'S': product_name_value},
                'country_code': {'S': self.country_code},
                'calibration_date': {'S': '{0}'.format(self.get_calibration_date())},
                'date_stamp': {'S': '{0}'.format(self.get_time_stamp())},
                'ttl': {'S': '{0}'.format(self.get_ttl())},
                }
            self.__set_records_list(item)

    def __write_car_data(self):
        car_data = self.xml_file.getElementsByTagName("car_data")
        i_count = 0
        for item in car_data:
            try:
                manufacturer = item.getElementsByTagName("manufacturer")[0].firstChild.data
            except AttributeError as err:
                manufacturer = '--'

            try:
                calibration_type = item.getElementsByTagName("type")[0].firstChild.data
            except AttributeError as err:
                calibration_type = '--'

            try:
                motor_code = item.getElementsByTagName("motorcode")[0].firstChild.data
            except AttributeError as err:
                motor_code = '--'

            try:
                year = item.getElementsByTagName("year")[0].firstChild.data
            except AttributeError as err:
                year = '--'

            try:
                licence = item.getElementsByTagName("licence")[0].firstChild.data
            except AttributeError as err:
                licence = '--'

            device_no_value = self.get_device_id()
            general_id = self.get_id()
            i_count += 1
            item = {
               'PK': {'S': 'device_no-{0}'.format(device_no_value)},
               'SK': {'S': 'id-{0}-vin-{1}'.format(general_id, sha_3_hex_digest(self.get_vin_car()))},
               'id': {'S': 'id-{0}'.format(general_id)},
               'manufacturer': {'S': manufacturer},
               'type': {'S': calibration_type},
               'motorcode': {'S': motor_code},
               'year': {'S': year},
               'licence': {'S': sha_3_hex_digest(licence)},
               'vin_car': {'S': sha_3_hex_digest(self.get_vin_car())},
               'ttl': {'S': '{}'.format(self.get_ttl())},
               's3': {'S': self.get_bucket()},
               'file_id': {'S': self.get_file_id()},
               }
            self.__set_records_list(item)

    def __write_fele_common_data(self):
        device_no_value = self.get_device_id()
        general_id = self.get_id()
        common_data = self.xml_file.getElementsByTagName("fele")
        i_count = 0
        for item in common_data:
            try:
                date_value = item.getElementsByTagName("date")[0].firstChild.data
            except AttributeError as err:
                date_value = '0000-00-00 00:00:00'

            try:
                assembly_group_name_value = item.getElementsByTagName("assembly_group_name")[0].firstChild.data
            except AttributeError as err:
                assembly_group_name_value = '--'

            try:
                assembly_name_value = item.getElementsByTagName("assembly_name")[0].firstChild.data
            except AttributeError as err:
                assembly_name_value = '--'

            try:
                assembly_group_short_value = item.getElementsByTagName("assembly_group_short")[0].firstChild.data
            except AttributeError as err:
                assembly_group_short_value = '--'

            try:
                mileage_temp = ''
                mileage = '0'
                mileage_value = str(item.getElementsByTagName("milage")[0].firstChild.data)
                for i in range(0, len(mileage_value)):
                    if mileage_value[i] in '0123456789':
                        mileage_temp += mileage_value[i]
                        if mileage_temp:
                            mileage = mileage_temp
                        else:
                            mileage = '0'
            except AttributeError as err:
                mileage = '0'

            try:
                start_time_value = item.getElementsByTagName("starttime")[0].firstChild.data
            except AttributeError as err:
                start_time_value = '0000-00-00 00:00:00'

            try:
                data_version = item.getElementsByTagName("data_version")[0].firstChild.data
            except AttributeError as err:
                data_version = '--'

            fault_code_list = item.getElementsByTagName("faultcode_list")
            e_obd = '--'
            fault_code_string = '--'
            for fault in fault_code_list:
                try:
                    e_obd = fault.getElementsByTagName("e_obd")[0].firstChild.data
                except AttributeError as err:
                    e_obd = '--'
                try:
                    fault_code_string = fault.getElementsByTagName("faultcode_string")[0].firstChild.data
                except AttributeError as err:
                    fault_code_string = '--'




            i_count += 1
            item = {
               'PK': {'S': 'device_no-{}'.format(device_no_value)},
               'SK': {'S': 'id-{}_common_data-{}'.format(general_id, i_count)},
               'common_data': {'S': 'common_data-{}'.format(i_count)},
               'calibration_start_time': {'S': start_time_value},
               'calibration_end_time': {'S': date_value},
               'calibration_date': {'S': self.get_calibration_date()},
               'assembly_group_name': {'S': assembly_group_name_value},
               'assembly_name': {'S': assembly_name_value},
               'assembly_group_short': {'S': assembly_group_short_value},
               'milage': {'S': mileage},
               'date_stamp': {'S': '{}'.format(self.get_time_stamp())},
               'data_version': {'S': '{}'.format(data_version)},
               'e_obd': {'S': '{}'.format(e_obd)},
               'faultcode_string': {'S': '{}'.format(fault_code_string)},
               'ttl': {'S': '{}'.format(self.get_ttl())},
                }
            self.__set_records_list(item)

    def __write_felg_parameter(self):
        device_no_value = self.get_device_id()
        general_id = self.get_id()
        try:
            felg_parameter = self.xml_file.getElementsByTagName("felg_parameter")
            i_count = 0
            for item in felg_parameter:
                try:
                    fault_code_count = item.getElementsByTagName("faultcode_count")[0].firstChild.data
                except AttributeError as err:
                    fault_code_count = '--'

                try:
                    assembly_group_name = item.getElementsByTagName("assembly_group_name")[0].firstChild.data
                except AttributeError as err:
                    assembly_group_name = '--'

                try:
                    assembly_group_short = item.getElementsByTagName("assembly_group_short")[0].firstChild.data
                except AttributeError as err:
                    assembly_group_short = '--'

                try:
                    assembly_name = item.getElementsByTagName("assembly_name")[0].firstChild.data
                except AttributeError as err:
                    assembly_name = '--'
                i_count += 1

                item = {
                    'PK': {'S': 'device_no-{}'.format(device_no_value)},
                    'SK': {'S': 'id-{}_felg_parameter-{}'.format(general_id, i_count)},
                    'felg_parameter': {'S': 'felg_parameter-{}'.format(i_count)},
                    'calibration_date': {'S': self.get_calibration_date()},
                    'faultcode_count': {'S': fault_code_count},
                    'assembly_group_name': {'S': assembly_group_name},
                    'assembly_group_short': {'S': assembly_group_short},
                    'assembly_name': {'S': assembly_name},
                    'date_stamp': {'S': '{}'.format(self.get_time_stamp())},
                    'ttl': {'S': '{}'.format(self.get_ttl())},
                    }
                self.__set_records_list(item)
        except IndexError as err:
            self.ok_to_go = False
            self.set_validation_report("an index error occurred when attempted to process "
                                       "a felg_parameter - {0}".format(err))

    def __write_result(self):
        device_no_value = self.get_device_id()
        general_id = self.get_id()
        result_data = self.xml_file.getElementsByTagName("car_history")
        i_count = 0
        for item in result_data:
            try:
                calibration_result = clean_html(item.getElementsByTagName("result")[0].firstChild.data)

                i_count += 1

                item = {
                    'PK': {'S': 'device_no-{}'.format(device_no_value)},
                    'SK': {'S': 'id-{}-{}'.format(general_id, self.get_calibration_date())},
                    'calibration_date': {'S': '{}'.format(self.get_calibration_date())},
                    'result': {'S': calibration_result},
                    'ttl': {'S': '{}'.format(self.get_ttl())},
                    }
                self.__set_records_list(item)

            except AttributeError as err:
                self.ok_to_go = False
                self.set_validation_report("an attribute error occurred when attempted to process "
                                           "the result field - {0}".format(err))
            except IndexError as err:
                self.ok_to_go = False
                self.set_validation_report("an index error occurred when attempted to process "
                                           "the result field - {0}".format(err))
