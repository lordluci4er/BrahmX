import re
import math
from typing import Optional


# -------- SAFE EVAL --------
ALLOWED_NAMES = {
    "sqrt": math.sqrt,
    "sin": lambda x: math.sin(math.radians(x)),
    "cos": lambda x: math.cos(math.radians(x)),
    "tan": lambda x: math.tan(math.radians(x)),
    "log": math.log10,
    "ln": math.log,
    "pi": math.pi,
    "e": math.e,
}


def safe_eval(expr: str) -> float:
    """
    Evaluate math expression safely (no eval abuse)
    """
    try:
        code = compile(expr, "<string>", "eval")

        for name in code.co_names:
            if name not in ALLOWED_NAMES:
                raise ValueError(f"Use of '{name}' not allowed")

        return eval(code, {"__builtins__": {}}, ALLOWED_NAMES)

    except Exception:
        raise ValueError("Invalid expression")


# -------- MAIN SOLVER --------
def solve_math(user_input: str) -> Optional[str]:
    try:
        if not user_input:
            return None

        text = user_input.lower()

        # -------- SQRT --------
        if "sqrt" in text or "square root" in text:
            nums = re.findall(r'\d+\.?\d*', text)
            if nums:
                result = math.sqrt(float(nums[0]))
                return f"√{nums[0]} = {round(result, 4)}"

        # -------- POWER --------
        if "power" in text or "^" in text:
            nums = re.findall(r'\d+\.?\d*', text)
            if len(nums) >= 2:
                result = math.pow(float(nums[0]), float(nums[1]))
                return f"{nums[0]}^{nums[1]} = {round(result, 4)}"

        # -------- TRIG --------
        if "sin" in text:
            num = float(re.findall(r'\d+\.?\d*', text)[0])
            result = math.sin(math.radians(num))
            return f"sin({num}) = {round(result, 4)}"

        if "cos" in text:
            num = float(re.findall(r'\d+\.?\d*', text)[0])
            result = math.cos(math.radians(num))
            return f"cos({num}) = {round(result, 4)}"

        if "tan" in text:
            num = float(re.findall(r'\d+\.?\d*', text)[0])
            result = math.tan(math.radians(num))
            return f"tan({num}) = {round(result, 4)}"

        # -------- LOG --------
        if "log" in text:
            num = float(re.findall(r'\d+\.?\d*', text)[0])
            result = math.log10(num)
            return f"log({num}) = {round(result, 4)}"

        if "ln" in text:
            num = float(re.findall(r'\d+\.?\d*', text)[0])
            result = math.log(num)
            return f"ln({num}) = {round(result, 4)}"

        # -------- BASIC EXPRESSION --------
        # allow only safe chars
        if any(op in text for op in ["+", "-", "*", "/", "(", ")"]):
            expr = re.findall(r'[\d\.\+\-\*\/\(\)]+', text)

            if expr:
                result = safe_eval(expr[0])
                return f"Result = {round(result, 4)}"

    except Exception:
        return "⚠️ Invalid math expression"

    return None