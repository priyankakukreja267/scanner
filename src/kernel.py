class Kernel:
    """
    Encapsulates an image manipulation kernel with internal state that can be reset.
    
    Note: I actually don't think we need kernels to be able to request some number of frames,
    since they can keep previous frames in internal storage. That way we can be closer to the
    way scanner does things. 
    Reply PK: Agreed!
    
    Also, in Scanner, kernels must actually be able to take ~100 frames at a time to reduce
    scheduling overhead. I don't know if we should do that as well.
    Reply PK: Let's start off small, and then incrementally add that feature
    """
    def get_input_dtypes(self):
        """
        :return: A list of dtypes 
        TODO: not used for now
        """
        raise NotImplementedError()

    def get_output_dtypes(self):
        """
        :return: A list of (video: bool, types: list(dtypes)).
        """
        raise NotImplementedError()

    def apply(self, inputs):
        """
        Apply the kernel to some input
        :return: A tuple representing values to insert into rows
        """
        raise NotImplementedError()

    def reset(self): # we can have stateful kernels now
        """
        Forces the kernel to forget any internal state
        """
        raise NotImplementedError()
