class Parser:
  C_ARITHMETIC = "C_ARITHMETIC"
  C_PUSH = "C_PUSH"
  C_POP = "C_POP"
  C_FUNCTION = "C_FUNCTION"
  C_CALL = "C_CALL"

  arithmetic_cmds = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]

  def command_type(self, line):
    if self.arithmetic_cmds.includes(line):
      return self.C_ARITHMETIC
    elif line.split()[0] == "push":
      return self.C_PUSH
    elif line.split()[1] == "pop":
      return self.C_POP

  def arg1(self, line, command_type):
    if command_type == self.C_ARITHMETIC:
      return line.split()[0]
    elif command_type == self.C_PUSH or command_type == self.C_POP:
      return line.split()[1]

  def arg2(self, line, command_type):
    if (
      command_type == self.C_PUSH
      or command_type == self.C_POP
      or command_type == self.C_FUNCTION
      or command_type == self.C_CALL
    ):
      return line.split()[3]
