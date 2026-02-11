def forecast_attendance(current_present, total_classes, future_classes):
    if total_classes == 0:
        return 0

    projected_total = total_classes + future_classes
    projected_present = current_present  # assuming no improvement

    return (projected_present / projected_total) * 100
