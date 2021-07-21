def adjustROIForOverlap(ROI_coords, bounds):
    start_bounds = bounds[0]
    end_bounds = bounds[1]
    start_coords = ROI_coords[0]
    start_overlap = [start_bounds[0]-start_coords[0], start_bounds[1]-start_coords[1]]
    end_coords = ROI_coords[1]
    end_overlap = [end_coords[0] - end_bounds[0],
                      end_coords[1] - end_bounds[1]]
    # ------Check X-----
    # X overlaps twice
    if start_overlap[0] > 0 and end_overlap[0] > 0:
        start_coords[0] = start_bounds[0]
        end_coords[0] = end_bounds[0] 
    elif start_overlap[0] > 0 or end_overlap[0] > 0:
        if start_overlap[0] > 0:
            start_coords[0] += start_overlap[0]
            end_coords[0] += start_overlap[0]
            if end_coords[0] > end_bounds[0]:
                end_coords[0] = end_bounds[0]
        elif end_overlap[0] > 0:
            start_coords[0] -= end_overlap[0]
            end_coords[0] -= end_overlap[0]
            if start_coords[0] < 0:
                start_coords[0] = start_bounds[0]

    # ------Check Y-----
    # Y overlaps twice
    if start_overlap[1] > 0 and end_overlap[1] > 0:
        start_coords[1] = start_bounds[1]
        end_coords[1] = end_bounds[1]
    elif start_overlap[1] > 0 or end_overlap[1] > 0:
        if start_overlap[1] > 0:
            start_coords[1] += start_overlap[1]
            end_coords[1] += start_overlap[1]
            if end_coords[1] > end_bounds[1]:
                end_coords[1] = end_bounds[1]
        elif end_overlap[1] > 0:
            start_coords[1] -= end_overlap[1]
            end_coords[1] -= end_overlap[1]
            if start_coords[1] < 0:
                start_coords[1] = start_bounds[1]
