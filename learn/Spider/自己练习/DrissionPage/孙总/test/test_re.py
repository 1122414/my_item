import re
def convert_wan_to_number(text):
  # 匹配含“万”的数值（如3.6万）和普通数字（如2000）
  pattern = r'(\d+\.?\d*)\s*万?'
  
  def replace_match(match):
      num_str = match.group(1)
      unit = match.group(0).strip()[-1] if '万' in match.group(0) else None
      
      # 若含“万”则乘以10000，否则直接转为整数
      num = float(num_str)
      if unit == '万':
          return str(int(num * 10000))  # 转换为整数避免小数点
      else:
          return str(int(num))  # 普通数字保持原值
  
  try:
    text = re.findall(r'\d+\.?\d*万', text)[0]
  except Exception as e:
    pass
  # 替换逻辑（保留原字符串中的非数字部分）
  converted_text = re.sub(
      pattern,
      replace_match,
      text
  )
  return converted_text

def extract_wan_fields(text):
    pattern = r'\d+\.?\d*万'  # 匹配数字+万的结构

    return re.findall(pattern, text)

if __name__ == '__main__':
  # print(extract_wan_fields('1.5万三十四'))

  print(convert_wan_to_number('1.5万三十四'))
  print(convert_wan_to_number('1500'))
  print(convert_wan_to_number('1.5万1.5亿'))
  print(convert_wan_to_number('1.5万1.5亿1.5万'))