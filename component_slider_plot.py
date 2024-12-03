import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import argparse  # For command-line arguments
from matplotlib.dates import DateFormatter  # To format timestamps

def create_dataframes():
    """
    Create two sample DataFrames with timestamps, volumes, and components.
    """
    timestamps = pd.date_range(start="2023-01-01 00:00", periods=120, freq="30T")

    # Generate random volumes and components
    components = ['ComponentA', 'ComponentB', 'ComponentC', 'ComponentD', 'ComponentE']
    
    dev_volume = np.random.randint(50, 500, size=len(timestamps))
    dev_components = [random.choice(components) if random.random() > 0.2 else None for _ in timestamps]
    
    prod_volume = np.random.randint(50, 500, size=len(timestamps))
    prod_components = [random.choice(components) if random.random() > 0.2 else None for _ in timestamps]

    # Create DataFrames
    dev_df = pd.DataFrame({"timestamp": timestamps, "volume": dev_volume, "component": dev_components})
    prod_df = pd.DataFrame({"timestamp": timestamps, "volume": prod_volume, "component": prod_components})
    
    return dev_df, prod_df

def plot_filtered_components_with_scroll(dev_df, prod_df, component_name):
    """
    Plots dev and prod volumes for the specified component with a slider for horizontal scrolling.
    """
    # Filter DataFrames by component name
    dev_filtered = dev_df[dev_df['component'] == component_name]
    prod_filtered = prod_df[prod_df['component'] == component_name]

    # If no data exists for this component, skip plotting
    if dev_filtered.empty and prod_filtered.empty:
        print(f"No data available for component: {component_name}")
        return

    # Combine filtered timestamps for proper slider bounds
    all_timestamps = pd.concat([dev_filtered["timestamp"], prod_filtered["timestamp"]]).drop_duplicates().sort_values()
    if all_timestamps.empty:
        print(f"No valid timestamps for component: {component_name}")
        return

    # Initial setup
    fig, ax = plt.subplots(figsize=(14, 6))  # Adjust the size for better fit
    plt.subplots_adjust(bottom=0.25)  # Leave space for the slider

    # Plot Dev Volume
    if not dev_filtered.empty:
        dev_line, = ax.plot(dev_filtered['timestamp'], dev_filtered['volume'], label='Dev Volume', color='blue', marker='o')
        ax.scatter(dev_filtered['timestamp'], dev_filtered['volume'], color='blue')

    # Plot Prod Volume
    if not prod_filtered.empty:
        prod_line, = ax.plot(prod_filtered['timestamp'], prod_filtered['volume'], label='Prod Volume', color='green', marker='o')
        ax.scatter(prod_filtered['timestamp'], prod_filtered['volume'], color='green')

    # Add axis labels and legend
    ax.set_title(f"Volume Comparison for Component: {component_name}")
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Volume")
    ax.legend()
    ax.grid()

    # Format the x-axis to display full timestamps
    date_format = DateFormatter("%Y-%m-%d %H:%M")  # Full date + time format
    ax.xaxis.set_major_formatter(date_format)
    plt.xticks(rotation=45)  # Rotate labels for better readability

    # Initial x-axis limits
    window_size = 20  # Number of points to show at a time
    start_idx = 0
    end_idx = min(start_idx + window_size, len(all_timestamps))  # Adjust end_idx based on available data
    ax.set_xlim(all_timestamps.iloc[start_idx], all_timestamps.iloc[end_idx - 1])

    # Add a slider for scrolling
    ax_slider = plt.axes([0.2, 0.1, 0.6, 0.03])  # Slider position
    slider = Slider(ax_slider, "Scroll", 0, max(0, len(all_timestamps) - window_size), valinit=0, valstep=1)

    # Update function for the slider
    def update(val):
        start_idx = int(slider.val)
        end_idx = start_idx + window_size
        ax.set_xlim(all_timestamps.iloc[start_idx], all_timestamps.iloc[min(end_idx, len(all_timestamps)) - 1])
        fig.canvas.draw_idle()

    slider.on_changed(update)

    # Show the plot
    plt.tight_layout()
    plt.show()

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Plot Dev and Prod Volumes for a Specific Component.")
    parser.add_argument("component", type=str, help="Component name to filter and plot (e.g., ComponentA).")
    args = parser.parse_args()
    
    # Create sample data
    dev_df, prod_df = create_dataframes()

    # Call the plotting function with the component name
    plot_filtered_components_with_scroll(dev_df, prod_df, args.component)

if __name__ == "__main__":
    main()
