class Kernel_Registry:

    """
    Class to control all kernels: user-defined + pre-defined
    """
    def __init__(self):
        self.kernel_list = []

    def initialize_kernel_registry(self):
        '''
        Makes all the predefined kernels available to the programmer
        '''
        raise NotImplementedError()

    def register_new_kernel(self, kernel_name, kernel_args, kernel_impl):
        '''
        Adds new kernel to the registry
        :param kernel_name: name of the kernel to register (names are unique)
        :param kernel_args: args to provide to the kernel # provides flexibility of sending 1 frame or multiple frames
        :param kernel_impl: function providing the implementation of the kernel
        :return true if registered successfully, else false
        '''
        pass

    def lookup_registry(self, kernel_name):
        '''
        Looks for a specific kernel in the registry
        Returns true if found, else false
        '''
        pass
