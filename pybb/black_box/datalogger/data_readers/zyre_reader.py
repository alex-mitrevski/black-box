import time
from ropod.pyre_communicator.base_class import PyreBaseCommunicator

class ZyreReader(PyreBaseCommunicator):
    '''An interface for managing ROS topic listeners.

    Constructor arguments:
    @param config_params -- an instance of black_box.config.config_params.RosParams
    @param data_logger -- a black_box.loggers.LoggerBase instance
    @param interface_name -- name of the data source; prepended to the topic name for defining
                             the full name of the logged data collection (default "zyre")

    @author Alex Mitrevski, Santosh Thoduka
    @contact aleksandar.mitrevski@h-brs.de, santosh.thoduka@h-brs.de

    '''
    def __init__(self, config_params, data_logger, interface_name='zyre'):
        super(ZyreReader, self).__init__(node_name=config_params.node_name,
                                         groups=config_params.groups,
                                         message_types=config_params.message_types)
        self.config_params = config_params
        self.data_logger = data_logger

        self.variable_names = {}
        for message_type in self.config_params.message_types:
            self.variable_names[message_type] = '{0}_{1}'.format(interface_name, message_type)

    def receive_msg_cb(self, msg_content):
        dict_msg = self.convert_zyre_msg_to_dict(msg_content)
        if dict_msg is None:
            return

        message_type = dict_msg['header']['type']
        if message_type in self.config_params.message_types:
            timestamp = time.time()
            variable_name = self.variable_names[message_type]
            self.data_logger.log_data(variable_name, timestamp, dict_msg)
