from LFSR import LFSR

generalExpectedOutput = [
  0b0110, 
  0b0011, 0b1001, 0b0100, 0b0010, 
  0b0001, 0b1000, 0b1100, 0b1110, 
  0b1111, 0b0111, 0b1011, 0b0101, 
  0b1010, 0b1101, 0b0110, 0b0011, 
  0b1001, 0b0100, 0b0010, 0b0001
]

def evaluate(
    expectedOutput,
    lfsr = LFSR(
      [0, 1, 1, 0], 
      taps = [0, 3]
    ),
    n = 20
) :
  
  print("t \t Expected \t Output \t Match")
  print("-" * 50)
  
  # Generate the next n bits of the LFSR
  output = []
  match = 0
  for i in range(n + 1):
    output.append(lfsr.getCurrentState())
    print(i, "\t", lfsr.bin(expectedOutput[i]), "\t", lfsr.bin(output[i]), "\t", expectedOutput[i] == output[i])
    if expectedOutput[i] == output[i]:
      match += 1
    lfsr.shift()
  
  print("-" * 50)
  print("Match:", match - 1, "/", n)

  lfsr.reset()
  return output
  

if __name__ == "__main__":
  # Test the General LFSR
  print("General LFSR Test")
  generalLfsr = LFSR([0, 1, 1, 0])
  generalOutput = evaluate(generalExpectedOutput, generalLfsr)
  
  # Test the Custom LFSR
  print("\nCustom LFSR Test")
  customLfsr = LFSR([0, 1, 1, 0])

  # Set the initial state
  print("> Setting initial state to 0b110010")
  customLfsr.setInitialState(0b110010)
  if customLfsr.getInitialState() == 0b110010:
    print("  Initial state set to 0b110010")
  else:
    print("  Initial state not set to 0b110010")

  # Set the tap sequence
  print("> Setting tap sequence to [0, 1, 4]")
  customLfsr.setTapSequence([0, 1, 4])
  if customLfsr.getTapSequence() == [0, 1, 4]:
    print("  Tap sequence set to [0, 1, 4]")
  else:
    print("  Tap sequence not set to [0, 1, 4]")

  # Generate the next 5 bits of the LFSR
  print("> Generating the next 5 bits of the LFSR\n")
  customLfsr.generate(5)

  # Set the register size
  print("\n> Setting register size to 4")
  customLfsr.setRegSize(4)
  if customLfsr.getRegSize() == 4:
    print("  Register size set to 4")
  else:
    print("  Register size not set to 4")

  # Get the current state
  print("> Getting the current state")
  print("  Current state:", customLfsr.bin(customLfsr.getCurrentState()))

  # Reset the LFSR
  print("> Resetting the LFSR")
  customLfsr.reset()
  print("  LFSR reset, current state:", customLfsr.bin(customLfsr.getCurrentState()))

  # Set all configuration to math the general LFSR
  print("> Setting all configuration to match the general LFSR")
  customLfsr.setInitialState([0, 1, 1, 0])
  customLfsr.setTapSequence([0, 3])
  customLfsr.setRegSize(4)
  print("  Configuration set\n")
  print(customLfsr)

  # Compare the output of the general LFSR and the custom LFSR
  print("\n> Comparing the output of the general LFSR and the custom LFSR")
  customOutput = evaluate(generalExpectedOutput, customLfsr)