import os
import sys
from code_writer import CodeWriter
from parser import Parser


def main():
  args = sys.argv[1:]
  if len(args) != 1:
    print("Usage: Input one argument corresponding to .vm file path")
    return

  path = args[0]
  if path[-3:] != ".vm":
    print("Usage: Must be .vm file input")
    return

  asm_file_name = f"{path[:-3]}.asm"
  if os.path.exists(asm_file_name):
    os.remove(asm_file_name)

  parser = Parser()
  code_writer = CodeWriter()

  with open(path, "r") as file:
    lines = file.readlines()
    line_number = 0

    for line in lines:
      line = line.rstrip("\n")
      line = line.lstrip()
      if line[:2] == "//" or len(line) == 0:
        continue

      command_type = parser.command_type(line)
      arg1 = parser.arg1(line, command_type)
      arg2 = parser.arg2(line, command_type)

      with open(asm_file_name, "a") as asm_file:
        if command_type == "C_ARITHMETIC":
          arithmetic_arr = code_writer.gen_arithmetic_asm(arg1)
          for asm_snippet in arithmetic_arr:
            asm_file.write(f"{asm_snippet}\n")
        if command_type == "C_PUSH" or command_type == "C_POP":
          push_pop_arr = code_writer.gen_push_pop_asm(command_type, arg1, arg2)
          for asm_snippet in push_pop_arr:
            asm_file.write(f"{asm_snippet}\n")


if __name__ == "__main__":
  main()
