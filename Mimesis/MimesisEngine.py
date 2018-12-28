import AlteryxPythonSDK as Sdk
import xml.etree.ElementTree as Et
from mimesis import Address
from mimesis import Code
from mimesis import Games
from mimesis import Food
from mimesis import Address
from mimesis import Person
from mimesis import Science
from mimesis import Transport

import pdb

class AyxPlugin:
    """
    Implements the plugin interface methods, to be utilized by the Alteryx engine to communicate with a plugin.
    Prefixed with "pi", the Alteryx engine will expect the below five interface methods to be defined.
    """

    def __init__(self, n_tool_id: int, alteryx_engine: object, output_anchor_mgr: object):
        """
        Constructor is called whenever the Alteryx engine wants to instantiate an instance of this plugin.
        :param n_tool_id: The assigned unique identification for a tool instance.
        :param alteryx_engine: Provides an interface into the Alteryx engine.
        :param output_anchor_mgr: A helper that wraps the outgoing connections for a plugin.
        """

        # Default properties
        self.n_tool_id = n_tool_id
        self.alteryx_engine = alteryx_engine
        self.output_anchor_mgr = output_anchor_mgr

        # Custom properties
        self.is_initialized = True
        self.single_input = None
        self.output_anchor = None
        self.output_field = None
        #make it a list
        self.column_name = []
        self.total_record_count = None
        #output all as v_wstrings
        self.output_type = Sdk.FieldType.v_wstring

        #soph added
        self.field_size = 500
        self.selected_fields = None
        self.record_limit = 0
        self.Locale = None


    def pi_init(self, str_xml: str):
        """
        Handles configuration based on the GUI.
        Called when the Alteryx engine is ready to provide the tool configuration from the GUI.
        :param str_xml: The raw XML from the GUI.
        """

        # Get the fields that the user selected, and make a list
        try:
            self.selected_fields = Et.fromstring(str_xml).find('ListBoxStringSelector').text
            self.column_name = self.selected_fields.split(',')
        except:
            self.display_error_msg('Please select at least one field.')

        #set Locale
        self.Locale = Et.fromstring(str_xml).find('Locale').text

        #if incoming connection is not detected, set number of records to output
        self.record_limit = int(Et.fromstring(str_xml).find('Number').text)

        # Check a selection if made for locale, error if not
        if self.Locale is None:
            self.display_error_msg('Please select a locale.')

        # Getting the output anchor from Config.xml by the output connection name
        self.output_anchor = self.output_anchor_mgr.get_output_anchor('Output')


    def pi_add_incoming_connection(self, str_type: str, str_name: str) -> object:
        """
        The IncomingInterface objects are instantiated here, one object per incoming connection.
        Called when the Alteryx engine is attempting to add an incoming data connection.
        :param str_type: The name of the input connection anchor, defined in the Config.xml file.
        :param str_name: The name of the wire, defined by the workflow author.
        :return: The IncomingInterface object(s).
        """

        self.single_input = IncomingInterface(self)
        return self.single_input


    def pi_add_outgoing_connection(self, str_name: str) -> bool:
        """
        Called when the Alteryx engine is attempting to add an outgoing data connection.
        :param str_name: The name of the output connection anchor, defined in the Config.xml file.
        :return: True signifies that the connection is accepted.
        """

        return True


    def pi_push_all_records(self, n_record_limit: int) -> bool:
        """
        Called when a tool has no incoming data connection.
        :param n_record_limit: Set it to <0 for no limit, 0 for no records, and >0 to specify the number of records.
        :return: True for success, False for failure.
        """

        if not self.is_initialized:
            return False

        # Save a reference to the RecordInfo passed into this function in the global namespace, so we can access it later.
        record_info_out = Sdk.RecordInfo(self.alteryx_engine)

        # Adds the new field to the record.
        for field in self.column_name:
            self.output_field = record_info_out.add_field(field, self.output_type, size=self.field_size)

        # Lets the downstream tools know what the outgoing record metadata will look like, based on record_info_out.
        self.output_anchor.init(record_info_out)
        # Creating a new, empty record creator based on record_info_out's record layout.
        record_creator = record_info_out.construct_record_creator()

        #import pdb; pdb.set_trace()

        #sophs code:
        for record in range(self.record_limit):
            for field in enumerate(record_info_out):
                if field[1].name == 'address_full_address':
                    mimesis_object = Address(self.Locale)
                    record_value = mimesis_object.address()
                if field[1].name == 'address_coordinates':
                    mimesis_object = Address(self.Locale)
                    record_value = str(mimesis_object.coordinates())
                if field[1].name == 'address_country':
                    mimesis_object = Address(self.Locale)
                    record_value = mimesis_object.country()
                if field[1].name == 'address_postal_code':
                    mimesis_object = Address(self.Locale)
                    record_value = mimesis_object.postal_code()
                if field[1].name == 'code_imei':
                    mimesis_object = Code(self.Locale)
                    record_value = mimesis_object.imei()
                if field[1].name == 'code_isbn':
                    mimesis_object = Code(self.Locale)
                    record_value = mimesis_object.isbn()
                if field[1].name == 'code_pin':
                    mimesis_object = Code(self.Locale)
                    record_value = mimesis_object.pin()
                if field[1].name == 'food_dish':
                    mimesis_object = Food(self.Locale)
                    record_value = mimesis_object.dish()
                if field[1].name == 'food_fruit':
                    mimesis_object = Food(self.Locale)
                    record_value = mimesis_object.fruit()
                if field[1].name == 'food_vegetables':
                    mimesis_object = Food(self.Locale)
                    record_value = mimesis_object.vegetable()
                if field[1].name == 'game_gaming_platform':
                    mimesis_object = Games(self.Locale)
                    record_value = mimesis_object.gaming_platform()
                if field[1].name == 'game_titles':
                    mimesis_object = Games(self.Locale)
                    record_value = mimesis_object.game()
                if field[1].name == 'person_blood_type':
                    mimesis_object = Person(self.Locale)
                    record_value = mimesis_object.blood_type()
                if field[1].name == 'person_email':
                    mimesis_object = Person(self.Locale)
                    record_value = mimesis_object.email()
                if field[1].name == 'person_full_name':
                    mimesis_object = Person(self.Locale)
                    record_value = mimesis_object.full_name()
                if field[1].name == 'person_nationality':
                    mimesis_object = Person(self.Locale)
                    record_value = mimesis_object.nationality()
                if field[1].name == 'person_occupation':
                    mimesis_object = Person(self.Locale)
                    record_value = mimesis_object.occupation()
                if field[1].name == 'person_telephone':
                    mimesis_object = Person(self.Locale)
                    record_value = mimesis_object.telephone()
                if field[1].name == 'science_atomic_number':
                    mimesis_object = Science(self.Locale)
                    record_value = str(mimesis_object.atomic_number())
                if field[1].name == 'science_chemical_element':
                    mimesis_object = Science(self.Locale)
                    record_value = mimesis_object.chemical_element()
                if field[1].name == 'transport_airplane':
                    mimesis_object = Transport(self.Locale)
                    record_value = mimesis_object.airplane()
                if field[1].name == 'transport_car':
                    mimesis_object = Transport(self.Locale)
                    record_value = mimesis_object.car()
                if field[1].name == 'transport_truck':
                    mimesis_object = Transport(self.Locale)
                    record_value = mimesis_object.truck()
                if field[1].name == 'transport_vehicle_reg_code':
                    mimesis_object = Transport(self.Locale)
                    record_value = mimesis_object.vehicle_registration_code()
                record_info_out[field[0]].set_from_string(record_creator, record_value)
            out_record = record_creator.finalize_record()
            self.output_anchor.push_record(out_record, False)
            record_creator.reset()


        # Make sure that the output anchor is closed.
        self.output_anchor.close()
        return True



    def pi_close(self, b_has_errors: bool):
        """
        Called after all records have been processed.
        :param b_has_errors: Set to true to not do the final processing.
        """

        # Checks whether connections were properly closed.
        self.output_anchor.assert_close()


    def display_error_msg(self, msg_string: str):
        """
        A non-interface method, that is responsible for displaying the relevant error message in Designer.
        :param msg_string: The custom error message.
        """

        self.is_initialized = False
        self.alteryx_engine.output_message(self.n_tool_id, Sdk.EngineMessageType.error, self.xmsg(msg_string))


    def xmsg(self, msg_string: str):
        """
        A non-interface, non-operational placeholder for the eventual localization of predefined user-facing strings.
        :param msg_string: The user-facing string.
        :return: msg_string
        """

        return msg_string


class IncomingInterface:
    """
    This class is returned by pi_add_incoming_connection, and it implements the incoming interface methods, to be\
    utilized by the Alteryx engine to communicate with a plugin when processing an incoming connection.
    Prefixed with "ii", the Alteryx engine will expect the below four interface methods to be defined.
    """

    def __init__(self, parent: object):
        """
        Constructor for IncomingInterface.
        :param parent: AyxPlugin
        """

        # Default properties
        self.parent = parent

        # Custom properties
        self.record_copier = None
        self.record_creator = None


    def ii_init(self, record_info_in: object) -> bool:
        """
        Handles appending the new field to the incoming data.
        Called to report changes of the incoming connection's record metadata to the Alteryx engine.
        :param record_info_in: A RecordInfo object for the incoming connection's fields.
        :return: False if there's an error with the field name, otherwise True.
        """

        if not self.parent.is_initialized:
            return False

        # Returns a new, empty RecordCreator object that is identical to record_info_in.
        self.record_info_out = record_info_in.clone()

        # Adds field to record with specified name and output type.

        for field in self.parent.column_name:
            self.parent.output_field = self.record_info_out.add_field(field, self.parent.output_type, size=self.parent.field_size)


        # Lets the downstream tools know what the outgoing record metadata will look like, based on record_info_out.
        self.parent.output_anchor.init(self.record_info_out)

        # Creating a new, empty record creator based on record_info_out's record layout.
        self.record_creator = self.record_info_out.construct_record_creator()

        # Instantiate a new instance of the RecordCopier class.
        self.record_copier = Sdk.RecordCopier(self.record_info_out, record_info_in)

        # Map each column of the input to where we want in the output.
        for index in range(record_info_in.num_fields):
            # Adding a field index mapping.
            self.record_copier.add(index, index)

        # Let record copier know that all field mappings have been added.
        self.record_copier.done_adding()

        # Grab the index of our new field in the record, so we don't have to do a string lookup on every push_record.

        #self.output_field = self.record_info_out.add_field(self.parent.column_name[index], self.parent.output_type, size=self.parent.field_size)

        return True

    def ii_push_record(self, in_record: object) -> bool:
        """
        Responsible for pushing records out.
        Called when an input record is being sent to the plugin.
        :param in_record: The data for the incoming record.
        :return: False if there's a downstream error, or if there's an error with the field name, otherwise True.
        """

        if not self.parent.is_initialized:
            return False

        #create the new fields
        record_value = None
        for field in enumerate(self.record_info_out):
            if field[1].name == 'address_full_address':
                mimesis_object = Address(self.parent.Locale)
                record_value = mimesis_object.address()
            if field[1].name == 'address_coordinates':
                mimesis_object = Address(self.parent.Locale)
                record_value = str(mimesis_object.coordinates())
            if field[1].name == 'address_country':
                mimesis_object = Address(self.parent.Locale)
                record_value = mimesis_object.country()
            if field[1].name == 'address_postal_code':
                mimesis_object = Address(self.parent.Locale)
                record_value = mimesis_object.postal_code()
            if field[1].name == 'code_imei':
                mimesis_object = Code(self.parent.Locale)
                record_value = mimesis_object.imei()
            if field[1].name == 'code_isbn':
                mimesis_object = Code(self.parent.Locale)
                record_value = mimesis_object.isbn()
            if field[1].name == 'code_pin':
                mimesis_object = Code(self.parent.Locale)
                record_value = mimesis_object.pin()
            if field[1].name == 'food_dish':
                mimesis_object = Food(self.parent.Locale)
                record_value = mimesis_object.dish()
            if field[1].name == 'food_fruit':
                mimesis_object = Food(self.parent.Locale)
                record_value = mimesis_object.fruit()
            if field[1].name == 'food_vegetables':
                mimesis_object = Food(self.parent.Locale)
                record_value = mimesis_object.vegetable()
            if field[1].name == 'game_gaming_platform':
                mimesis_object = Games(self.parent.Locale)
                record_value = mimesis_object.gaming_platform()
            if field[1].name == 'game_titles':
                mimesis_object = Games(self.parent.Locale)
                record_value = mimesis_object.game()
            if field[1].name == 'person_blood_type':
                mimesis_object = Person(self.parent.Locale)
                record_value = mimesis_object.blood_type()
            if field[1].name == 'person_email':
                mimesis_object = Person(self.parent.Locale)
                record_value = mimesis_object.email()
            if field[1].name == 'person_full_name':
                mimesis_object = Person(self.parent.Locale)
                record_value = mimesis_object.full_name()
            if field[1].name == 'person_nationality':
                mimesis_object = Person(self.parent.Locale)
                record_value = mimesis_object.nationality()
            if field[1].name == 'person_occupation':
                mimesis_object = Person(self.parent.Locale)
                record_value = mimesis_object.occupation()
            if field[1].name == 'person_telephone':
                mimesis_object = Person(self.parent.Locale)
                record_value = mimesis_object.telephone()
            if field[1].name == 'science_atomic_number':
                mimesis_object = Science(self.parent.Locale)
                record_value = str(mimesis_object.atomic_number())
            if field[1].name == 'science_chemical_element':
                mimesis_object = Science(self.parent.Locale)
                record_value = mimesis_object.chemical_element()
            if field[1].name == 'transport_airplane':
                mimesis_object = Transport(self.parent.Locale)
                record_value = mimesis_object.airplane()
            if field[1].name == 'transport_car':
                mimesis_object = Transport(self.parent.Locale)
                record_value = mimesis_object.car()
            if field[1].name == 'transport_truck':
                mimesis_object = Transport(self.parent.Locale)
                record_value = mimesis_object.truck()
            if field[1].name == 'transport_vehicle_reg_code':
                mimesis_object = Transport(self.parent.Locale)
                record_value = mimesis_object.vehicle_registration_code()
                #pdb.set_trace()
            self.record_info_out[field[0]].set_from_string(self.record_creator, record_value)
        out_record = self.record_creator.finalize_record()
        #self.parent.output_anchor.push_record(out_record, False)
        self.record_creator.reset()


        # Copy the data from the incoming record into the outgoing record.
        self.record_creator.reset()
        self.record_copier.done_adding()
        self.record_copier.copy(self.record_creator, in_record)

        # Push the record downstream and quit if there's a downstream error.
        if not self.parent.output_anchor.push_record(out_record):
            return False

        return True

    def ii_update_progress(self, d_percent: float):
        """
        Called by the upstream tool to report what percentage of records have been pushed.
        :param d_percent: Value between 0.0 and 1.0.
        """

        # Inform the Alteryx engine of the tool's progress.
        self.parent.alteryx_engine.output_tool_progress(self.parent.n_tool_id, d_percent)

        # Inform the outgoing connections of the tool's progress.
        self.parent.output_anchor.update_progress(d_percent)

    def ii_close(self):
        """
        Called when the incoming connection has finished passing all of its records.
        """

        # Close outgoing connections.
        self.parent.output_anchor.close()
