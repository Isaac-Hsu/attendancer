def split(start, end, parts):
    diff = end - start + 1
    base = diff // parts
    remainder = diff % parts
    
    ranges = []
    current = start
    
    for i in range(parts):
        extra = 1 if i < remainder else 0
        rangesize = base + extra
        rangestart = current
        rangeend = current + rangesize - 1
        ranges.append((rangestart, rangeend))
        current = rangeend + 1
    return ranges



def test_split():
    test_cases = [
        # (start, end, parts, description)
        (100, 110, 3, "11 items into 3 parts"),
        (100, 110, 6, "11 items into 6 parts"),
        (1, 10, 3, "10 items into 3 parts"),
        (0, 99, 10, "100 items into 10 parts"),
        (5, 5, 1, "Single item, single part"),
        (1, 7, 7, "7 items into 7 parts (one each)"),
    ]
    
    for start, end, parts, desc in test_cases:
        print(f"\n{desc}:")
        print(f"  split({start}, {end}, {parts})")
        result = split(start, end, parts)
        
        # Print the ranges
        for i, (s, e) in enumerate(result):
            size = e - s + 1
            print(f"    Part {i}: [{s}, {e}] (size: {size})")
        
        # Verify correctness
        total_items = end - start + 1
        covered_items = sum(e - s + 1 for s, e in result)
        all_continuous = all(result[i][1] + 1 == result[i+1][0] 
                            for i in range(len(result)-1))
        
        print(f"Total items: {total_items}, Covered: {covered_items}, " + f"Continuous: {all_continuous}, " + f"Correct: {covered_items == total_items and all_continuous}")

# Run tests
test_split()
