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

  with open(path, "r") as file:
    for line in file:
      line = line.rstrip("\n")
      if line[:2] == "//" or len(line) == 0:
        continue

      instructionType = parser.instructionType(line)
      symbol = parser.symbol(line)
      dest = parser.dest(line)
      comp = parser.comp(line)
      jump = parser.jump(line)

      # write binary code as new line
      with open(hackFileName, "a") as hackFile:
        binaryCode = code.getCode(instructionType, symbol, dest, comp, jump)
        hackFile.write(f"{binaryCode}\n")


if __name__ == "__main__":
  main()
