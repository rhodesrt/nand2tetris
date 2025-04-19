import os
from enum import Enum


class C(Enum):
  ARITHMETIC = "C_ARITHMETIC"
  PUSH = "PUSH"
  POP = "POP"
  LABEL = "LABEL"
  GOTO = "GOTO"
  IF = "IF"
  FUNCTION = "FUNCTION"
  RETURN = "RETURN"
  CALL = "CALL"


class VMParser:
  ARITHMETIC_COMMANDS = {"add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"}

  def __init__(self, path):
    self.path = path
    if not os.path.exists(path):
      raise FileNotFoundError(f"File not found: {path}")

    self.file = open(path, "r")

  def has_more_lines(self):
    pos = self.file.tell()
    line = self.file.readline()
    self.file.seek(pos)
    return line

  def advance(self):
    while True:
      line = self.file.readline()
      if not line or line.strip() == "" or line.strip().startswith("//"):
        continue
      self.command = line
      break

  def command_type(self):
    command = self.command.strip().split()[0]
    if command in self.ARITHMETIC_COMMANDS:
      return C.ARITHMETIC
    elif command == "push":
      return C.PUSH
    elif command == "pop":
      return C.POP
    elif command == "label":
      return C.LABEL
    elif command == "goto":
      return C.GOTO
    elif command == "if-goto":
      return C.IF
    elif command == "function":
      return C.FUNCTION
    elif command == "call":
      return C.CALL
    elif command == "return":
      return C.RETURN
    else:
      raise ValueError("command type does not exist")

  def arg_1(self):
    ct = self.command_type()
    if ct == C.ARITHMETIC:
      return self.command.strip()
    elif (
      ct == C.POP
      or ct == C.PUSH
      or ct == C.LABEL
      or ct == C.GOTO
      or ct == C.IF
      or ct == C.FUNCTION
      or ct == C.CALL
    ):
      return self.command.strip().split()[1]
    else:
      raise ValueError("arg_1 not applicable for this command type")

  def arg_2(self):
    if (
      self.command_type() == C.PUSH
      or self.command_type() == C.POP
      or self.command_type() == C.FUNCTION
      or self.command_type() == C.CALL
    ):
      return self.command.strip().split()[2]
    else:
      raise ValueError("arg_2 not applicable for this command type")
