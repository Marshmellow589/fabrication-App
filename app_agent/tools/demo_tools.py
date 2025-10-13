import random
import ast
import operator
from datetime import datetime
from langchain_core.tools import tool, ToolException

# 安全计算操作符映射
safe_operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

def safe_eval(expression: str):
    """安全评估数学表达式"""
    try:
        # 解析表达式为AST
        tree = ast.parse(expression, mode='eval')
        
        # 递归检查AST节点是否安全
        def check_node(node):
            if isinstance(node, (ast.Expression, ast.Num, ast.Constant)):
                return True
            elif isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
                return check_node(node.operand)
            elif isinstance(node, ast.BinOp) and type(node.op) in safe_operators:
                return check_node(node.left) and check_node(node.right)
            else:
                return False
        
        if not check_node(tree.body):
            raise ValueError("表达式包含不安全操作")
        
        # 编译并执行安全的AST
        code = compile(tree, '<string>', 'eval')
        return eval(code, {"__builtins__": {}}, safe_operators)
    except Exception as e:
        raise ValueError(f"表达式评估失败: {e}")

# --- 1. 定义工具函数 ---
@tool
def calculator(expression: str) -> str:
    """一个安全的计算器函数。当需要进行数学计算时使用。输入应该是一个有效的数学表达式，如 '2 + 3 * 4'。"""
    try:
        result = safe_eval(expression)
        return str(result)
    except Exception as e:
        raise ToolException(f"计算出错: {e}")

@tool
def get_current_time() -> str:
    """获取当前日期和时间字符串。当用户询问时间或日期时使用。"""
    current_time = datetime.now().isoformat()
    return f"当前时间是 {current_time}"

@tool
def dice_roller(sides: int = 6) -> str:
    """掷一个指定面数的骰子并返回结果。输入是骰子的面数，默认为6。"""
    try:
        if sides < 2 or sides > 100:
            return "错误: 骰子面数必须在2到100之间"
        result = random.randint(1, sides)
        return f"你掷出了 {result} (使用 {sides} 面骰子)"
    except Exception as e:
        return f"掷骰子出错: {e}"

# --- 2. 将工具函数聚合到一个列表中 ---
tools = [calculator, get_current_time, dice_roller]