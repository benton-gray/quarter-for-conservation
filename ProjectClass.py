# definition of Project Class
# from array import array


# noinspection PyMissingOrEmptyDocstring
class Project:
    segment_data: int = 0
    segment_clock: int = 0
    segment_latch: int = 0
    first_interrupt: int = 0
    second_interrupt: int = 0
    stored_number_file_name: str = ""
    current_number: int = 0

    def init(self, segment_latch: int, segment_clock: int, segment_data: int, stored_number_file_name: str,
             first_interrupt: int,
             second_interrupt: int,
             current_number: int) -> int:
        """
        Holds all values of each project including GPIO pins and count
        :return:
        :param segment_latch:
        :param segment_clock:
        :param segment_data:
        :param stored_number_file_name:
        :param first_interrupt:
        :param second_interrupt:
        :param current_number:
        """
        self.segment_data = segment_data
        self.segment_clock = segment_clock
        self.segment_latch = segment_latch
        self.stored_number_file_name = stored_number_file_name
        self.first_interrupt = first_interrupt
        self.second_interrupt = second_interrupt
        self.current_number = current_number
        return 0
