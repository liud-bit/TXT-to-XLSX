import matplotlib.pyplot as plt
import sys

def get_user_inputs():
    """
    Creates a console interface to collect parameters from the user.
    """
    print("--- LINEAR FUNCTION PLOTTER INTERFACE ---")
    print("Please enter the following parameters:\n")
    
    try:
        m1 = float(input("1. Slope of the first function (starts at origin): "))
        m2 = float(input("2. Slope of the second function: "))
        c2 = float(input("3. Y-intercept of the second function: "))
        
        print("\n--- GRAPH SETTINGS ---")
        x_limit = float(input("4. Max display range for X-axis: "))
        y_limit = float(input("5. Max display range for Y-axis: "))
        
        return m1, m2, c2, x_limit, y_limit

    except ValueError:
        print("\n[!] Error: Please enter valid numeric values.")
        sys.exit()

def plot_graph(m1, m2, c2, x_limit, y_limit):
    
    # --- 1. MATHEMATICAL CALCULATIONS ---
    
    # Check for parallel lines
    if m1 == m2:
        print("\n[!] Error: Slopes are identical. The lines will never intersect.")
        return

    # Calculate Intersection Point: m1*x = m2*x + c2
    x_intersect = c2 / (m1 - m2)
    y_intersect = m1 * x_intersect

    # Check for X-intercept (End point of second line)
    if m2 == 0:
        print("\n[!] Error: Second slope is 0, line will never intersect the x-axis.")
        return
    
    x_end = -c2 / m2

    # --- 2. TERMINAL OUTPUT ---
    print("\n" + "="*40)
    print("           CALCULATED POINTS           ")
    print("="*40)
    print(f"Intersection of Function 1 & 2: ({x_intersect:.4f}, {y_intersect:.4f})")
    print(f"Function 2 X-Axis Intercept:    ({x_end:.4f}, 0.0000)")
    print("="*40 + "\n")

    # --- 3. GENERATE COORDINATES ---
    
    # Segment 1: Origin (0,0) -> Intersection
    line1_x = [0, x_intersect]
    line1_y = [0, y_intersect]
    
    # Segment 2: Intersection -> X-axis intercept
    line2_x = [x_intersect, x_end]
    line2_y = [y_intersect, 0]

    # --- 4. PLOTTING AND STYLING ---
    
    # Set explicit white figure background
    fig = plt.figure(figsize=(10, 6), facecolor='white')
    ax = plt.axes()
    ax.set_facecolor('white')
    
    # Standardize Line Thickness
    graph_linewidth = 1.5
    
    # Plot Segment 1 (Solid Black)
    plt.plot(line1_x, line1_y, color='black', linewidth=graph_linewidth, linestyle='-')
    
    # Plot Segment 2 (Solid Black)
    plt.plot(line2_x, line2_y, color='black', linewidth=graph_linewidth, linestyle='-')
    
    # Draw vertical dashed line (Intersection -> X-axis)
    plt.vlines(x=x_intersect, ymin=0, ymax=y_intersect, 
               colors='black', linestyles='dashed', linewidth=1)
               
    # Draw horizontal dashed line (Intersection -> Y-axis)
    plt.hlines(y=y_intersect, xmin=0, xmax=x_intersect, 
               colors='black', linestyles='dashed', linewidth=1)

    # --- AXIS CUSTOMIZATION ---
    # Hide the Top and Right borders (spines)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Make the Bottom (X) and Left (Y) spines black and MATCH THICKNESS
    ax.spines['bottom'].set_color('black')
    ax.spines['bottom'].set_linewidth(graph_linewidth)
    
    ax.spines['left'].set_color('black')
    ax.spines['left'].set_linewidth(graph_linewidth)
    
    # Set tick colors to black
    ax.tick_params(axis='x', colors='black')
    ax.tick_params(axis='y', colors='black')
    
    # Set User Defined Ranges
    plt.xlim(0, x_limit)
    plt.ylim(0, y_limit)
    
    # Ensure no labels are printed
    plt.title("")
    plt.xlabel("")
    plt.ylabel("")

    plt.show()

if __name__ == "__main__":
    params = get_user_inputs()
    plot_graph(*params)