# python3 main.py <source.vm>

import sys
import os
from parser import VMParser
from code_writer import ASMCodeWriter
from parser import C


def main():
  args = sys.argv[1:]
  path = validate_args(args)

  parser = VMParser(path)
  code_writer = ASMCodeWriter(path)
  code_writer.set_filename(path.split("/")[-1][:-3])

  while parser.has_more_lines():
    parser.advance()

    if parser.command_type() == C.ARITHMETIC:
      code_writer.write_arithmetic(parser.arg_1())
    elif parser.command_type() == C.POP:
      code_writer.write_push_pop("pop", parser.arg_1(), parser.arg_2())
    elif parser.command_type() == C.PUSH:
      code_writer.write_push_pop("push", parser.arg_1(), parser.arg_2())

  code_writer.loop()
  code_writer.close()


def validate_args(args):
  if len(args) != 1:
    print("Usage: Input one argument corresponding to .vm file path")
    return

  path = args[0]
  if path[-3:] != ".vm":
    print("Usage: Must be .vm file input")
    return
  filename = os.path.basename(path)
  if not filename[0].isupper():
    print("Usage: .vm file must have first character uppercase")
    return

  return os.path.relpath(path)


if __name__ == "__main__":
  main()
