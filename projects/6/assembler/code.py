class Code:
  COMP_TABLE = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
  }

  def getCode(self, instructionType, symbol, dest, comp, jump):
    if instructionType == "A_INSTRUCTION":
      return "0" + str(bin(int(symbol))[2:])
    elif instructionType == "C_INSTRUCTION":
      comp_code = str(int(not self.ZERO_COMPS.contains(comp)))
