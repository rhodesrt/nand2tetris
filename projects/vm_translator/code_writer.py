class ASMCodeWriter:
  def __init__(self, path):
    self.output_file = open(f"{path[:-3]}.asm", "w")
    self.function_name = None
    self.return_label_counter = 0

  def set_filename(self, filename):
    self.filename = filename

  def write_arithmetic(self, command):
    self.write_line(f"// {command}")

    if command == "add":
      instructions = [
        "@SP",
        "M=M-1",
        "A=M",
        "D=M",
        "@SP",
        "M=M-1",
        "A=M",
        "D=D+M",
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1",
      ]
    elif command == "sub":
      instructions = [
        "@SP",
        "M=M-1",
        "A=M",
        "D=M",
        "@SP",
        "M=M-1",
        "A=M",
        "D=M-D",
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1",
      ]
    elif command == "neg":
      instructions = ["@SP", "M=M-1", "A=M", "M=-M", "@SP", "M=M+1"]
    elif command == "eq":
      instructions = [
        "@SP",
        "M=M-1",
        "A=M",
        "D=M",
        "@SP",
        "M=M-1",
        "A=M",
        "D=D-M",
        "@TRUE",
        "D;JEQ",
        "M=0",
        "@CONTINUE",
        "0;JMP",
        "(TRUE)",
        "M=-1",
        "(CONTINUE)",
        "@SP",
        "M=M+1",
      ]
    elif command == "gt":
      instructions = [
        "@SP",
        "M=M-1",
        "A=M",
        "D=M",
        "@SP",
        "M=M-1",
        "D=M-D",  # x - y
        "@TRUE",
        "D;JGT",
        "M=0",
        "@CONTINUE",
        "0;JMP",
        "(TRUE)",
        "M=-1",
        "(CONTINUE)",
        "@SP",
        "M=M+1",
      ]
    elif command == "lt":
      instructions = [
        "@SP",
        "M=M-1",
        "A=M",
        "D=M",
        "@SP",
        "M=M-1",
        "D=M-D",  # x - y
        "@TRUE",
        "D;JLT",
        "M=0",
        "@CONTINUE",
        "0;JMP",
        "(TRUE)",
        "M=-1",
        "(CONTINUE)",
        "@SP",
        "M=M+1",
      ]
    elif command == "and":
      instructions = [
        "@SP",
        "M=M-1",
        "A=M",
        "D=M",
        "@SP",
        "M=M-1",
        "A=M",
        "M=M&D",  # x & y
        "@SP",
        "M=M+1",
      ]
    elif command == "or":
      instructions = [
        "@SP",
        "M=M-1",
        "A=M",
        "D=M",
        "@SP",
        "M=M-1",
        "A=M",
        "M=M|D",  # x | y
        "@SP",
        "M=M+1",
      ]
    elif command == "not":
      instructions = ["@SP", "M=M-1", "A=M", "M=!M", "@SP", "M=M+1"]

    for ins in instructions:
      self.write_line(ins)

  def write_push_pop(self, command, segment, index):
    self.write_line(f"// {command} {segment} {index}")

    if command == "push":
      if segment == "local":
        instructions = [
          f"@{index}",
          "D=A",
          "@LCL",
          "A=M+D",
          "D=M",
          "@SP",
          "A=M",
          "M=D",
          "@SP",
          "M=M+1",
        ]
      elif segment == "constant":
        instructions = [f"@{index}", "D=A", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
      elif segment == "pointer":
        instructions = [
          "@THIS" if index == "0" else "@THAT",
          "D=M",
          "@SP",
          "A=M",
          "M=D",
          "@SP",
          "M=M+1",
        ]
      elif segment == "temp":
        instructions = [
          f"@{index}",
          "D=A",
          "@5",
          "A=A+D",
          "D=M",
          "@SP",
          "A=M",
          "M=D",
          "@SP",
          "M=M+1",
        ]
      elif segment == "argument":
        instructions = [
          f"@{index}",
          "D=A",
          "@ARG",
          "A=M+D",
          "D=M",
          "@SP",
          "A=M",
          "M=D",
          "@SP",
          "M=M+1",
        ]
      elif segment == "this":
        instructions = [
          f"@{index}",
          "D=A",
          "@THIS",
          "A=M+D",
          "D=M",
          "@SP",
          "A=M",
          "M=D",
          "@SP",
          "M=M+1",
        ]
      elif segment == "that":
        instructions = [
          f"@{index}",
          "D=A",
          "@THAT",
          "A=M+D",
          "D=M",
          "@SP",
          "A=M",
          "M=D",
          "@SP",
          "M=M+1",
        ]
      elif segment == "static":
        instructions = [
          f"@{self.filename}.{index}",
          "D=M",
          "@SP",
          "A=M",
          "M=D",
          "@SP",
          "M=M+1",
        ]
    elif command == "pop":
      if segment == "local":
        instructions = [
          f"@{index}",
          "D=A",
          "@LCL",
          "D=M+D",
          "@R13",
          "M=D",
          "@SP",
          "M=M-1",
          "A=M",
          "D=M",
          "@R13",
          "A=M",
          "M=D",
        ]
      elif segment == "constant":
        raise ValueError("Cannot 'pop' into the 'constant' segment.")
      elif segment == "pointer":
        symbol = "THIS" if index == "0" else "THAT"
        instructions = ["@SP", "M=M-1", "A=M", "D=M", f"@{symbol}", "M=D"]
      elif segment == "temp":
        instructions = [
          f"@{index}",
          "D=A",
          "@5",
          "D=A+D",
          "@R13",
          "M=D",
          "@SP",
          "M=M-1",
          "A=M",
          "D=M",
          "@R13",
          "A=M",
          "M=D",
        ]
      elif segment == "argument":
        instructions = [
          f"@{index}",
          "D=A",
          "@ARG",
          "D=M+D",
          "@R13",
          "M=D",
          "@SP",
          "M=M-1",
          "A=M",
          "D=M",
          "@R13",
          "A=M",
          "M=D",
        ]
      elif segment == "this":
        instructions = [
          f"@{index}",
          "D=A",
          "@THIS",
          "D=M+D",
          "@R13",
          "M=D",
          "@SP",
          "M=M-1",
          "A=M",
          "D=M",
          "@R13",
          "A=M",
          "M=D",
        ]
      elif segment == "that":
        instructions = [
          f"@{index}",
          "D=A",
          "@THAT",
          "D=M+D",
          "@R13",
          "M=D",
          "@SP",
          "M=M-1",
          "A=M",
          "D=M",
          "@R13",
          "A=M",
          "M=D",
        ]
      elif segment == "static":
        instructions = [
          "@SP",
          "M=M-1",
          "A=M",
          "D=M",
          f"@{self.filename}.{index}",
          "M=D",
        ]

    for ins in instructions:
      self.write_line(ins)

  def write_label(self, label):
    self.write_line(f"// label {label}")
    if self.function_name:
      self.write_line(f"({self.function_name}${label})")
    else:
      self.write_line(f"({label})")

  def write_goto(self, label):
    self.write_line(f"// goto {label}")
    if self.function_name:
      instructions = [f"@{self.function_name}${label}", "0;JMP"]
    else:
      instructions = [f"@{label}", "0;JMP"]

    for ins in instructions:
      self.write_line(ins)

  def write_if(self, label):
    self.write_line(f"// if-goto {label}")
    instructions = [
      "@SP",
      "M=M-1",
      "A=M",
      "D=M",
      f"@{self.function_name}${label}" if self.function_name else f"@{label}",
      "D;JNE",
    ]
    for ins in instructions:
      self.write_line(ins)

  def write_function(self, function_name, n_vars):
    self.write_line(f"// function {function_name} {n_vars}")
    self.function_name = function_name
    self.write_line(f"({function_name})")
    n_vars = int(n_vars)
    for _ in range(n_vars):
      instructions = ["@0", "D=A", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
      for ins in instructions:
        self.write_line(ins)

  def write_call(self, function_name, n_args):
    self.write_line(f"// call {function_name} {n_args}")

    return_label = f"{function_name}$ret.{self.return_label_counter}"
    self.return_label_counter += 1
    n_args = int(n_args)

    instructions = [
      f"@{return_label}",
      "D=A",
      "@SP",
      "A=M",
      "M=D",
      "@SP",
      "M=M+1",
    ]
    for segment_pointer in ["LCL", "ARG", "THIS", "THAT"]:
      instructions.extend(
        [
          f"@{segment_pointer}",
          "D=M",
          "@SP",
          "A=M",
          "M=D",
          "@SP",
          "M=M+1",
        ]
      )
    instructions.extend(
      [
        "@SP",
        "D=M",
        f"@{n_args}",
        "D=D-A",  # D = SP - n_args
        "@5",
        "D=D-A",  # D = SP - n_args - 5
        "@ARG",
        "M=D",
      ]
    )
    instructions.extend(
      [
        "@SP",
        "D=M",
        "@LCL",
        "M=D",
      ]
    )
    instructions.extend(
      [
        f"@{function_name}",
        "0;JMP",
      ]
    )
    instructions.append(f"({return_label})")

    for ins in instructions:
      self.write_line(ins)

  def write_return(self):
    self.write_line("// return")
    instructions = [
      # FRAME = LCL
      "@LCL",
      "D=M",
      "@R13",
      "M=D",
      # RET = *(FRAME - 5)
      "@5",
      "A=D-A",
      "D=M",
      "@R14",
      "M=D",
      # *ARG = pop()
      "@SP",
      "M=M-1",
      "A=M",
      "D=M",
      "@ARG",
      "A=M",
      "M=D",
      # SP = ARG + 1
      "@ARG",
      "D=M+1",
      "@SP",
      "M=D",
      # THAT = *(FRAME - 1)
      "@R13",
      "A=M-1",
      "D=M",
      "@THAT",
      "M=D",
      # THIS = *(FRAME - 2)
      "@R13",
      "D=M",
      "@2",
      "A=D-A",
      "D=M",
      "@THIS",
      "M=D",
      # ARG = *(FRAME - 3)
      "@R13",
      "D=M",
      "@3",
      "A=D-A",
      "D=M",
      "@ARG",
      "M=D",
      # LCL = *(FRAME - 4)
      "@R13",
      "D=M",
      "@4",
      "A=D-A",
      "D=M",
      "@LCL",
      "M=D",
      # goto RET
      "@R14",
      "A=M",
      "0;JMP",
    ]

    for ins in instructions:
      self.write_line(ins)

  def loop(self):
    self.write_line("// Infinite loop")
    self.write_line("(END)")
    self.write_line("@END")
    self.write_line("0;JMP")

  def write_line(self, line):
    self.output_file.write(line + "\n")

  def close(self):
    self.output_file.close()
