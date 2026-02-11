def calculate_risk(attendance_percentage):
    if attendance_percentage >= 75:
        return "Low"
    elif attendance_percentage >= 60:
        return "Medium"
    else:
        return "High"
