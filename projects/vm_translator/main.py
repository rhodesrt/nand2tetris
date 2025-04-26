import sys
import os
from parser import VMParser
from code_writer import ASMCodeWriter
from parser import C


def main():
  args = sys.argv[1:]
  validation_result = validate_args(args)
  if validation_result is None:
    return

  vm_files, output_asm_path = validation_result

  code_writer = ASMCodeWriter(output_asm_path)

  if os.path.isdir(args[0]):
    code_writer.write_init()

  for vm_file_path in vm_files:
    print(f"Processing file: {vm_file_path}")
    parser = VMParser(vm_file_path)
    base_filename = os.path.basename(vm_file_path)[:-3]
    code_writer.set_filename(base_filename)

    while parser.has_more_lines():
      parser.advance()
      ct = parser.command_type()

      if ct == C.ARITHMETIC:
        code_writer.write_arithmetic(parser.arg_1())
      elif ct == C.POP or ct == C.PUSH:
        command_str = "pop" if ct == C.POP else "push"
        code_writer.write_push_pop(command_str, parser.arg_1(), parser.arg_2())
      elif ct == C.LABEL:
        code_writer.write_label(parser.arg_1())
      elif ct == C.GOTO:
        code_writer.write_goto(parser.arg_1())
      elif ct == C.IF:
        code_writer.write_if(parser.arg_1())
      elif ct == C.FUNCTION:
        code_writer.write_function(parser.arg_1(), parser.arg_2())
      elif ct == C.CALL:
        code_writer.write_call(parser.arg_1(), parser.arg_2())
      elif ct == C.RETURN:
        code_writer.write_return()

    parser.close()

  code_writer.close()


def validate_args(args):
  if len(args) != 1:
    print(
      "Usage: Input one argument corresponding to a .vm file or a directory containing .vm files"
    )
    return

  input_path = args[0]
  vm_files = []
  output_asm_path = ""

  if os.path.isdir(input_path):
    print(f"Input is a directory: {input_path}")
    dir_path = os.path.abspath(input_path)
    dir_name = os.path.basename(dir_path)
    output_asm_path = os.path.join(dir_path, f"{dir_name}.asm")
    try:
      files_in_dir = os.listdir(dir_path)
      for f in files_in_dir:
        if f.endswith(".vm"):
          vm_files.append(os.path.join(dir_path, f))
      if not vm_files:
        print(f"Error: No .vm files found in directory '{input_path}'")
        return None
      vm_files.sort()
    except OSError as e:
      print(f"Error accessing directory '{input_path}': {e}")
      return None

  elif os.path.isfile(input_path):
    print(f"Input is a file: {input_path}")
    if not input_path.endswith(".vm"):
      print(f"Error: Input file '{input_path}' must be a .vm file.")
      return None

    vm_files.append(os.path.abspath(input_path))
    # Output file is FileName.asm in the same location
    output_asm_path = os.path.abspath(input_path)[:-3] + ".asm"

  else:
    print(f"Error: Input path '{input_path}' is not a valid file or directory.")
    return None

  return vm_files, output_asm_path


if __name__ == "__main__":
  main()
