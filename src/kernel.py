class Kernel:
    """
    Encapsulates an image manipulation kernel with internal state that can be reset.
    
    Note: I actually don't think we need kernels to be able to request some number of frames,
    since they can keep previous frames in internal storage. That way we can be closer to the
    way scanner does things.
    
    Also, in Scanner, kernels must actually be able to take ~100 frames at a time to reduce
    scheduling overhead. I don't know if we should do that as well.
    """
    def __init__(self):
        raise NotImplementedError()

    def apply(self, inputs):
        """
        Apply the kernel to some input
        :return: A tuple representing values to insert into rows
        """
        raise NotImplementedError()

    def reset(self):
        """
        Forces the kernel to forget any internal state
        """
        raise NotImplementedError()
