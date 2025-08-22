import csv

input_file = "data/ai_ip_alarm_dynamic_history_202508121906.csv"   # file gốc
output_file = "fixed1.csv"  # file sau khi sửa

fixed_lines = []
with open(input_file, "r", encoding="utf-8", errors="ignore") as f:
    for line_num, line in enumerate(f, start=1):
        quote_count = line.count('"')
        if quote_count % 2 != 0:
            print(f"Dòng {line_num} bị lỗi dấu \" → tự đóng lại")
            line = line.strip("\n") + '"' + "\n"  # thêm dấu đóng
        fixed_lines.append(line)

with open(output_file, "w", encoding="utf-8", newline="") as f:
    f.writelines(fixed_lines)

print("✅ Đã xử lý xong. File mới:", output_file)
