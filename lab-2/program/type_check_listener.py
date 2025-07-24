from SimpleLangListener import SimpleLangListener
from SimpleLangParser import SimpleLangParser
from custom_types import IntType, FloatType, StringType, BoolType

class TypeCheckListener(SimpleLangListener):

  def __init__(self):
    self.errors = []
    self.types = {}

  def enterMulDivMod(self, ctx: SimpleLangParser.MulDivModContext):
    pass

  def exitMulDivMod(self, ctx: SimpleLangParser.MulDivModContext):
    left_type = self.types[ctx.expr(0)]
    right_type = self.types[ctx.expr(1)]
    op = ctx.op.text
    
    # Operaciones aritméticas (* y /)
    if op in ['*', '/']:
        if not self.is_valid_arithmetic_operation(left_type, right_type):
            self.errors.append(f"Unsupported operand types for {op}: {left_type} and {right_type}")
        self.types[ctx] = FloatType() if isinstance(left_type, FloatType) or isinstance(right_type, FloatType) else IntType()
    
    # Operación módulo (%)
    elif op == '%':
        if not (isinstance(left_type, IntType) and isinstance(right_type, IntType)):
            self.errors.append(f"Modulo operation (%) requires integer operands, got {left_type} and {right_type}")
        self.types[ctx] = IntType()

  def enterAddSub(self, ctx: SimpleLangParser.AddSubContext):
    pass

  def exitAddSub(self, ctx: SimpleLangParser.AddSubContext):
    left_type = self.types[ctx.expr(0)]
    right_type = self.types[ctx.expr(1)]
    if not self.is_valid_arithmetic_operation(left_type, right_type):
      self.errors.append(f"Unsupported operand types for + or -: {left_type} and {right_type}")
    self.types[ctx] = FloatType() if isinstance(left_type, FloatType) or isinstance(right_type, FloatType) else IntType()

  def enterComparison(self, ctx: SimpleLangParser.ComparisonContext):
    pass

  def exitComparison(self, ctx: SimpleLangParser.ComparisonContext):
    left_type = self.types[ctx.expr(0)]
    right_type = self.types[ctx.expr(1)]
    op = ctx.op.text
    
    # Igualdad y desigualdad pueden comparar tipos iguales
    if op in ['==', '!=']:
        if type(left_type) != type(right_type):
            self.errors.append(f"Cannot compare different types with {op}: {left_type} and {right_type}")
    
    # Comparaciones de orden solo para números
    elif op in ['<', '>', '<=', '>=']:
        if not self.is_valid_arithmetic_operation(left_type, right_type):
            self.errors.append(f"Comparison operator {op} requires numeric types, got {left_type} and {right_type}")
    
    self.types[ctx] = BoolType()

  def enterLogicalOp(self, ctx: SimpleLangParser.LogicalOpContext):
    pass

  def exitLogicalOp(self, ctx: SimpleLangParser.LogicalOpContext):
    left_type = self.types[ctx.expr(0)]
    right_type = self.types[ctx.expr(1)]
    op = ctx.op.text
    
    if not (isinstance(left_type, BoolType) and isinstance(right_type, BoolType)):
        self.errors.append(f"Logical operator {op} requires boolean operands, got {left_type} and {right_type}")
    
    self.types[ctx] = BoolType()

  def enterLogicalNot(self, ctx: SimpleLangParser.LogicalNotContext):
    pass

  def exitLogicalNot(self, ctx: SimpleLangParser.LogicalNotContext):
    expr_type = self.types[ctx.expr()]
    
    if not isinstance(expr_type, BoolType):
        self.errors.append(f"Logical NOT (!) requires boolean operand, got {expr_type}")
    
    self.types[ctx] = BoolType()

  def enterInt(self, ctx: SimpleLangParser.IntContext):
    self.types[ctx] = IntType()

  def enterFloat(self, ctx: SimpleLangParser.FloatContext):
    self.types[ctx] = FloatType()

  def enterString(self, ctx: SimpleLangParser.StringContext):
    self.types[ctx] = StringType()

  def enterBool(self, ctx: SimpleLangParser.BoolContext):
    self.types[ctx] = BoolType()

  def enterParens(self, ctx: SimpleLangParser.ParensContext):
    pass

  def exitParens(self, ctx: SimpleLangParser.ParensContext):
    self.types[ctx] = self.types[ctx.expr()]

  def is_valid_arithmetic_operation(self, left_type, right_type):
    if isinstance(left_type, (IntType, FloatType)) and isinstance(right_type, (IntType, FloatType)):
      return True
    return False