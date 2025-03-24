class LFSR:
  """
  A class representing a Linear Feedback Shift Register (LFSR).

  Attributes:
    initialState (list): The initial state of the LFSR.
    currentState (list): The current state of the LFSR.
    tapSequence (list): The tap sequence used for generating the next state.

  Methods:
    create(taps): Updates the tap sequence of the LFSR.
  """

  def __init__(self, initialState, regSize = None, taps = None):
    """
    Initializes the LFSR with the given initial state.

    Args:
      initialState (list): The initial state of the LFSR.
    """

    self.__regSize = regSize if regSize is not None else initialState.bit_length() if isinstance(initialState, int) else len(initialState)

    # Check if the initial state is a list, string, bytes, or int
    if isinstance(initialState, list):
      for i in range(len(initialState)):
        if (initialState[i] != 0 and initialState[i] != "0") and (initialState[i] != 1 and initialState[i] != "1"):
          raise ValueError("The initial state should be a list of 0s and 1s.")

      # Convert the list to a bin integer
      initialState = int("".join(str(bit) for bit in initialState), 2)


    # If the initial state is a string, check if it contains only 0s and 1s
    elif isinstance(initialState, str):
      for bit in initialState:
        if bit != '0' and bit != '1':
          raise ValueError("The initial state should be a string of 0s and 1s.")
      initialState = int(initialState, 2)

    # If the initial state is a bytes object, check if it contains only b'0's and b'1's
    elif isinstance(initialState, bytes):
      for bit in initialState:
        if bit != b'0' and bit != b'1':
          raise ValueError("The initial state should be a bytes object of b'0's and b'1's.")
        
      initialState = int(initialState.decode(), 2)

    elif isinstance(initialState, int):
      pass

    # If the initial state is not a list, string, or bytes object, raise an error
    else:
      raise ValueError("The initial state should be a list, string, or bytes object.")

    self.__initialState = initialState

    if regSize is not None and regSize < initialState.bit_length():
      initialState = initialState >> (initialState.bit_length() - regSize)

    self.__currentState = initialState

    if taps is not None:
      self.setTapSequence(taps)
    else:
      self.__tapSequence = [0, self.__regSize - 1]

  # Methods
  def shift(self):
    """
    Shifts the LFSR by one step.
    """

    # Calculate the next state
    nextState = 0
    for tap in self.__tapSequence:
      nextState ^= (self.__currentState >> tap) & 1

    # Shift the current state
    self.__currentState = (nextState << (self.__regSize - 1)) | (self.__currentState >> 1)

  def stream(self):
    """
    Shifts the LFSR by one step and returns the next bit.
    """

    # Shift the LFSR
    self.shift()

    # Return the next bit
    return self.__currentState >> (self.__regSize - 1)

  def reset(self):
    """
    Resets the LFSR to the initial state.
    """

    self.__currentState = self.__initialState
    self.__regSize = self.__initialState.bit_length()

  def generate(self, n):
    """
    Generates the next n bits of the LFSR and prints the state of the LFSR at each step.

    Args:
      n (int): The number of bits to generate.
    """

    # Generate the next n bits
    for i in range(n):
      print(i, "\t", self.bin(self.__currentState))
      self.shift()
    
    print(n, "\t", self.bin(self.__currentState))


  # Setters
  def setInitialState(self, initialState):
    """
    Sets the initial state of the LFSR.

    Args:
      initialState (list): The initial state of the LFSR.
    """

    self.__init__(initialState)

  def setRegSize(self, regSize):
    """
    Sets the register size of the LFSR.

    Args:
      regSize (int): The register size of the LFSR.
    """

    if regSize < self.__initialState.bit_length():
      # Slice the current state to the new register size
      self.__currentState = self.__currentState >> (self.__initialState.bit_length() - regSize)
    
    self.__regSize = regSize

  def setTapSequence(self, tapSequence):
    """
    Sets the tap sequence of the LFSR.

    Args:
      tapSequence (list): The tap sequence used for generating the next state.
    """

    # Check if the tap sequence is a list
    if not isinstance(tapSequence, list):
      raise ValueError("The tap sequence should be a list of integers.")

    # Check if the tap sequence is at least of length 2
    if len(tapSequence) < 2:
      raise ValueError("The tap sequence should contain at least 2 indices.")

    # Check if the tap sequence is a valid index
    if not all(isinstance(tap, int) for tap in tapSequence):
      raise ValueError("The tap sequence should be a list of integers.")

    # Check if the tap sequence is a list of unique indices
    if len(tapSequence) != len(set(tapSequence)):
      raise ValueError("The tap sequence should contain unique indices.")

    # Check if the tap sequence contains valid indices
    if not all(0 <= tap < self.__regSize for tap in tapSequence):
      raise ValueError("The tap sequence should contain valid indices.")

    self.__tapSequence = tapSequence

  # Getters
  def getInitialState(self):
    """
    Returns the initial state of the LFSR.
    """

    return self.__initialState
  
  def getCurrentState(self):
    """
    Returns the current state of the LFSR.
    """

    return self.__currentState
  
  def getRegSize(self):
    """
    Returns the register size of the LFSR.
    """

    return self.__regSize
  
  def getTapSequence(self):
    """
    Returns the tap sequence of the LFSR.
    """
      
    return self.__tapSequence 
  
  def __str__(self):
    """
    Returns a string representation of the LFSR.
    """

    return f"Initial State: {self.bin(self.__initialState)}\nCurrent State: {self.bin(self.__currentState)}\nRegister Size: {self.__regSize}\nTap Sequence: {self.__tapSequence}"
  
  def bin(self, byte):
    """
    Returns a prettified string representation of a byte.
    """

    return f"0b{byte:0{self.__regSize}b}"
  
# Run if main
if __name__ == "__main__":
  # Create an LFSR with an initial state of [1, 0, 1, 0] and a tap sequence of [0, 3]
  lfsr = LFSR([0, 1, 1, 0], taps = [0, 3])

  # Generate the next 5 bits of the LFSR
  lfsr.generate(5)

  lfsr.setRegSize(6)
  lfsr.generate(5)

  lfsr.setRegSize(3)
  lfsr.generate(5)

  lfsr.setInitialState([1, 0, 1, 1, 1, 0, 1])
  lfsr.setTapSequence([0, 1, 2])
  lfsr.generate(5)