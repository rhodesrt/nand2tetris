import os
from enum import Enum


class C(Enum):
  ARITHMETIC = "C_ARITHMETIC"
  PUSH = "PUSH"
  POP = "POP"


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
    return line != ""

  def advance(self):
    self.command = self.file.readline()

  def command_type(self):
    command = self.command.strip().split()[0]
    if command in self.ARITHMETIC_COMMANDS:
      return C.ARITHMETIC
    elif command == "push":
      return C.PUSH
    elif command == "pop":
      return C.POP

  def arg_1(self):
    if self.command_type() == C.ARITHMETIC:
      return self.command
    elif self.command_type() == C.POP or self.command_type() == C.PUSH:
      return self.command.strip().split()[1]

  def arg_2(self):
    if self.command_type() == C.PUSH or self.command_type() == C.POP:
      return self.command.strip().split()[2]
