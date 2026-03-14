"""Configure matplotlib to work without display."""
import os
import sys

# Set matplotlib backend BEFORE importing matplotlib
os.environ['MPLBACKEND'] = 'Agg'

# Configure matplotlib
try:
    import matplotlib
    matplotlib.use('Agg')
    # Build font cache on startup
    import matplotlib.pyplot as plt
    plt.figure()
    plt.close()
except Exception as e:
    print(f"Warning: Could not pre-initialize matplotlib: {e}", file=sys.stderr)
