class MismatchedSignature(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return 'incorrect instruction signature byte'

class NONE:
    """real NOP"""

    def __init__(self):
        pass

    def __str__(self):
        return '(no instruction)'

    def setup(self, proc, rip):
        """Grab necessary data from processor's memory.
        Store them in `self`.
        pre-FETCH stage
        """
        pass

    def fetch(self, proc, F, D):
        """Real FETCH stage"""
        pass

    def decode(self, proc, D, E):
        """DECODE stage"""
        pass

    def execute(self, proc, E, M):
        """EXECUTE stage"""
        pass

    def memory(self, proc, M, W):
        """MEMORY stage"""
        pass

    def write(self, proc, W, _):
        """WRITE stage"""
        pass