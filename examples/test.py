




import re

def extract_width_height_generic(input_str: str) -> tuple:
    input_str = input_str.replace("(", "").replace(")", "")  # Entferne Klammern aus dem Eingabestring
    input_str = input_str.replace(" ", "")
    res_match = re.search(r'(\d+),(\d+)', input_str)
    
    if res_match:
        width = int(res_match.group(1))
        height = int(res_match.group(2))
        return width, height
    else:
        return None, None

teststring = "( 1980 ,    2300   )"
width, height = extract_width_height_generic(input_str=teststring)

print(width)
print(height)
print('pause')



# import re

# def extract_width_height_generic(input_str: str) -> tuple:
#     input_str = input_str.replace("(", "").replace(")", "")  # Entferne Klammern aus dem Eingabestring
#     res_match = re.search(r'\s*$((\d+)\s*,\s*(\d+))$\s*', input_str)
    
#     if res_match:
#         width = int(res_match.group(1))
#         height = int(res_match.group(2))
#         return width, height
#     else:
#         return None, None

# teststring = "(1980,2300)"
# width, height = extract_width_height_generic(input_str=teststring)

# print(width)
# print(height)
# print('pause')
