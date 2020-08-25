import json
import data

day = json.dumps(data.days, ensure_ascii=False)
with open("days.json", "w", encoding="utf-8") as days:
  days.write(day)

goal = json.dumps(data.goals, ensure_ascii=False)
with open("goals.json", "w", encoding="utf-8") as goals:
  goals.write(goal)

teacher = json.dumps(data.teachers, ensure_ascii=False)
with open("teachers.json", "w", encoding="utf-8") as teachers:
   teachers.write(teacher)
