import re

variableName = ["22hgal", "_hgal", "hgal22_", "ggh ahg al", "ghal!"]

for v in variableName:
    result = re.match(r"[A-z_]+[A-z_]*", v)
    if v == result:
        print(result, "是合法变量名！")
    else:
        print(v, "不是合法变量名！")
