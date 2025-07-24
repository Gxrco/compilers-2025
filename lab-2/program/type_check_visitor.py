from SimpleLangParser import SimpleLangParser
from SimpleLangVisitor import SimpleLangVisitor
from custom_types import IntType, FloatType, StringType, BoolType

class TypeCheckVisitor(SimpleLangVisitor):

  def visitMulDivMod(self, ctx: SimpleLangParser.MulDivModContext):
    left_type = self.visit(ctx.expr(0))
    right_type = self.visit(ctx.expr(1))
    op = ctx.op.text
    
    # Operaciones aritméticas (* y /)
    if op in ['*', '/']:
        if isinstance(left_type, (IntType, FloatType)) and isinstance(right_type, (IntType, FloatType)):
            return FloatType() if isinstance(left_type, FloatType) or isinstance(right_type, FloatType) else IntType()
        else:
            raise TypeError("Unsupported operand types for {} : {} and {}".format(op, left_type, right_type))
    
    # Operación módulo (%)
    elif op == '%':
        if isinstance(left_type, IntType) and isinstance(right_type, IntType):
            return IntType()
        else:
            raise TypeError("Modulo operation (%) requires integer operands, got {} and {}".format(left_type, right_type))

  def visitAddSub(self, ctx: SimpleLangParser.AddSubContext):
    left_type = self.visit(ctx.expr(0))
    right_type = self.visit(ctx.expr(1))
    
    if isinstance(left_type, (IntType, FloatType)) and isinstance(right_type, (IntType, FloatType)):
        return FloatType() if isinstance(left_type, FloatType) or isinstance(right_type, FloatType) else IntType()
    else:
        raise TypeError("Unsupported operand types for + or -: {} and {}".format(left_type, right_type))

  def visitComparison(self, ctx: SimpleLangParser.ComparisonContext):
    left_type = self.visit(ctx.expr(0))
    right_type = self.visit(ctx.expr(1))
    op = ctx.op.text
    
    # Igualdad y desigualdad pueden comparar tipos iguales
    if op in ['==', '!=']:
        if type(left_type) == type(right_type):
            return BoolType()
        else:
            raise TypeError("Cannot compare different types with {}: {} and {}".format(op, left_type, right_type))
    
    # Comparaciones de orden solo para números
    elif op in ['<', '>', '<=', '>=']:
        if isinstance(left_type, (IntType, FloatType)) and isinstance(right_type, (IntType, FloatType)):
            return BoolType()
        else:
            raise TypeError("Comparison operator {} requires numeric types, got {} and {}".format(op, left_type, right_type))

  def visitLogicalOp(self, ctx: SimpleLangParser.LogicalOpContext):
    left_type = self.visit(ctx.expr(0))
    right_type = self.visit(ctx.expr(1))
    op = ctx.op.text
    
    if isinstance(left_type, BoolType) and isinstance(right_type, BoolType):
        return BoolType()
    else:
        raise TypeError("Logical operator {} requires boolean operands, got {} and {}".format(op, left_type, right_type))

  def visitLogicalNot(self, ctx: SimpleLangParser.LogicalNotContext):
    expr_type = self.visit(ctx.expr())
    
    if isinstance(expr_type, BoolType):
        return BoolType()
    else:
        raise TypeError("Logical NOT (!) requires boolean operand, got {}".format(expr_type))
  
  def visitInt(self, ctx: SimpleLangParser.IntContext):
    return IntType()

  def visitFloat(self, ctx: SimpleLangParser.FloatContext):
    return FloatType()

  def visitString(self, ctx: SimpleLangParser.StringContext):
    return StringType()

  def visitBool(self, ctx: SimpleLangParser.BoolContext):
    return BoolType()

  def visitParens(self, ctx: SimpleLangParser.ParensContext):
    return self.visit(ctx.expr())