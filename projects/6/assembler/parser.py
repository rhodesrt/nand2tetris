class Parser:
  A_INSTRUCTION = "A_INSTRUCTION"
  C_INSTRUCTION = "C_INSTRUCTION"
  L_INSTRUCTION = "L_INSTRUCTION"

  def instructionType(self, line):
    if line[0] == "@":
      return self.A_INSTRUCTION
    elif line[0] == "(":
      return self.L_INSTRUCTION
    else:
      return self.C_INSTRUCTION

  def symbol(self, line):
    if self.instructionType(line) == self.C_INSTRUCTION:
      return None
    elif self.instructionType(line) == self.A_INSTRUCTION:
      return str(line[1:])
    else:
      return str(line[1:-1])

  def dest(self, line):
    if self.instructionType(line) == self.A_INSTRUCTION:
      return None
    else:
      equals_idx = line.find("=")
      if equals_idx == -1:
        return None
      else:
        return str(line[:equals_idx])

  def comp(self, line):
    if self.instructionType(line) == self.A_INSTRUCTION:
      return None
    else:
      semicolon_idx = line.find(";")
      equals_idx = line.find("=")

      if semicolon_idx == -1:
        return str(line[(equals_idx + 1) :])
      elif equals_idx == -1:
        return str(line[:semicolon_idx])
      else:
        return str(line[(equals_idx + 1) : semicolon_idx])

  def jump(self, line):
    if self.instructionType(line) == self.A_INSTRUCTION:
      return None
    else:
      semicolon_idx = line.find(";")
      if semicolon_idx == -1:
        return None
      else:
        return str(line[(semicolon_idx + 1) :])
