import sys
from parser import Parser
from code import Code


def main():
  args = sys.argv[1:]
  if len(args) != 1:
    print("Usage: Input one argument corresponding to .asm file path")
    return

  path = args[0]
  if path[-4:] != ".asm":
    print("Usage: Must be .asm file input")
    return

  hackFileName = f"{path[:-4]}.hack"
  parser = Parser()
  code = Code()
  symbol_table = {
    "R0": 0,
    "R1": 1,
    "R2": 2,
    "R3": 3,
    "R4": 4,
    "R5": 5,
    "R6": 6,
    "R7": 7,
    "R8": 8,
    "R9": 9,
    "R10": 10,
    "R11": 11,
    "R12": 12,
    "R13": 13,
    "R14": 14,
    "R15": 15,
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "SCREEN": 16384,
    "KBD": 24576,
  }

  with open(path, "r") as file:
    lines = file.readlines()
    line_number = 0
    # 1st pass
    for line in lines:
      line = line.rstrip("\n")
      line = line.lstrip()
      if line[:2] == "//" or len(line) == 0:
        continue

      instructionType = parser.instructionType(line)
      symbol = parser.symbol(line)

      if instructionType == "L_INSTRUCTION":
        if symbol not in symbol_table.keys():
          symbol_table[symbol] = line_number
          continue

      line_number += 1

    # 2nd pass
    line_number = 0
    a_symbol_count = 15
    for line in lines:
      line = line.rstrip("\n")
      line = line.lstrip()
      if line[:2] == "//" or len(line) == 0:
        continue

      instructionType = parser.instructionType(line)
      symbol = parser.symbol(line)

      if instructionType == "A_INSTRUCTION":
        if not symbol[0].isdigit():
          if symbol not in symbol_table.keys():
            a_symbol_count += 1
            symbol_table[symbol] = a_symbol_count
      line_number += 1

    line_number = 0
    for line in lines:
      line = line.rstrip("\n")
      line = line.lstrip()
      if line[:2] == "//" or len(line) == 0:
        continue

      instructionType = parser.instructionType(line)
      symbol = parser.symbol(line)
      dest = parser.dest(line)
      comp = parser.comp(line)
      jump = parser.jump(line)

      # write binary code as new line
      with open(hackFileName, "a") as hackFile:
        binaryCode = code.getCode(
          instructionType, symbol, dest, comp, jump, symbol_table
        )
        if binaryCode is not None:
          hackFile.write(f"{binaryCode}\n")

  print(symbol_table)


if __name__ == "__main__":
  main()
