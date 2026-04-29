import re
import math

def solve_math(user_input):
    try:
        user_input = user_input.lower()

        if "sqrt" in user_input or "square root" in user_input:
            num = int(re.findall(r'\d+', user_input)[0])
            return f"Square root is {math.sqrt(num)}"

        if "power" in user_input or "^" in user_input:
            nums = re.findall(r'\d+', user_input)
            if len(nums) >= 2:
                return f"Result is {math.pow(int(nums[0]), int(nums[1]))}"

        if "sin" in user_input:
            num = int(re.findall(r'\d+', user_input)[0])
            return f"sin({num}) = {math.sin(math.radians(num))}"

        if "cos" in user_input:
            num = int(re.findall(r'\d+', user_input)[0])
            return f"cos({num}) = {math.cos(math.radians(num))}"

        if "tan" in user_input:
            num = int(re.findall(r'\d+', user_input)[0])
            return f"tan({num}) = {math.tan(math.radians(num))}"

        if any(op in user_input for op in ["+", "-", "*", "/"]):
            expression = re.findall(r'[\d\.\+\-\*\/]+', user_input)
            if expression:
                return f"Result is {eval(expression[0])}"

    except:
        return "Math error"

    return None