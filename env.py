import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import Tk, Label, Canvas, Frame
from PIL import Image, ImageTk

import human as hm
import robot as rb
import config as cfg


class TrustTransition:
    def __init__(self) -> None:
        # Memory for trust history
        self.cumulative_error_history = [] # recording all the errors in a session
        self.cumulative_trust_history = []



class TkImageViewer:
    """
    Tkinter-based image viewer
    """
    def __init__(self, window_size=(1200, 800), 
                 base_path = '/Users/mahta/Documents/Trust in Human-Robot Interaction/codes/sim/Exps img/',
                 image_ratio=0.6  # Ratio of window width for image (rest for plot)
):
        """
        Initialize a persistent Tkinter window for dynamic updates with embedded plot.
        
        Args:
            window_size: Tuple of (width, height) for the window size
            base_path: Base path for image files
            image_ratio: Ratio of window width allocated to image (0-1)
        """
        self.root = Tk()
        self.root.title("Image Viewer with Trust Plot")
        self.root.geometry(f"{window_size[0]}x{window_size[1]}")
        self.window_size = window_size
        self.image_ratio = image_ratio
        
        # Create main container frame
        main_frame = Frame(self.root)
        main_frame.pack(fill="both", expand=True)
        
        # Left frame for image
        image_frame = Frame(main_frame)
        image_frame.pack(side="left", fill="both", expand=True)
        
        # Create canvas for image display with white background
        image_width = int(window_size[0] * image_ratio)
        self.canvas = Canvas(image_frame, width=image_width, height=window_size[1], bg='white')
        self.canvas.pack(fill="both", expand=True)
        
        # Right frame for plot
        plot_frame = Frame(main_frame)
        plot_frame.pack(side="right", fill="both", expand=True)
        
        # Create matplotlib figure for the plot
        self.fig = Figure(figsize=(window_size[0] * (1-image_ratio) / 100, window_size[1] / 100), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlabel('Index')
        self.ax.set_ylabel('Trust Level')
        self.ax.set_title('Trust Level Over Time')
        self.ax.grid(True, alpha=0.3)
        
        # Embed matplotlib figure in tkinter
        self.plot_canvas = FigureCanvasTkAgg(self.fig, plot_frame)
        self.plot_canvas.draw()
        self.plot_canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Data storage for plot
        self.trust_history = []  # List of trust levels
        self.index_history = []  # List of indices
        
        self.image_item = None  # Canvas image item ID
        self.photo = None
        self.text_elements = {}  # Store text element IDs
        self.shape_elements = {}  # Store shape element IDs
        self.image_center_x = None  # Store image center for relative positioning
        self.image_center_y = None
        self.image_width = None
        self.image_height = None
        
        self.base_path = base_path
        self.current_index = 0  # Track current index
        
        # Start Tkinter event loop
        self.root.update()  # Initial update to show window
        
    def show_image(self, image_path, clear_other=True):
        """
        Update the window with a new image.
        
        Args:
            image_path: Path to the PNG/image file
            clear_other: If True, clear other elements (text/shapes) before showing image
        """
        try:
            # Load and resize image FIRST (before clearing anything)
            img = Image.open(image_path)
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            # If canvas not yet rendered, use default size
            if canvas_width <= 1:
                canvas_width = self.root.winfo_width() or 800
            if canvas_height <= 1:
                canvas_height = self.root.winfo_height() or 600
            
            # Resize image maintaining aspect ratio
            img.thumbnail((canvas_width, canvas_height), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage BEFORE updating display (prevents black blink)
            new_photo = ImageTk.PhotoImage(img)
            
            # Calculate center position for image
            # Use already calculated canvas dimensions
            x_center = canvas_width // 2
            y_center = canvas_height // 2
            
            # Store image position and size for relative text positioning
            self.image_center_x = x_center
            self.image_center_y = y_center
            self.image_width = new_photo.width()
            self.image_height = new_photo.height()
            
            # Clear text/shapes if requested (but keep image visible)
            if clear_other:
                # Only clear text and shapes, NOT the image
                for text_id in self.text_elements.values():
                    self.canvas.delete(text_id)
                self.text_elements.clear()
                
                for shape_id in self.shape_elements.values():
                    self.canvas.delete(shape_id)
                self.shape_elements.clear()
            
            # Update image atomically using canvas (no gap = no black blink)
            if self.image_item is None:
                # Create image on canvas
                self.image_item = self.canvas.create_image(x_center, y_center, image=new_photo, anchor='center')
            else:
                # Update existing image - this is atomic, no black blink
                self.canvas.itemconfig(self.image_item, image=new_photo)
            
            # Keep reference to prevent garbage collection
            self.photo = new_photo
            
            self._update_display()
        except Exception as e:
            print(f"Error loading image: {e}")
    
    def add_text(self, text, x, y, name=None, **kwargs):
        """
        Add or update text in the window.
        
        Args:
            text: Text string to display
            x, y: Position coordinates (in pixels, relative to canvas)
            name: Optional name identifier for updating this text later
            **kwargs: Text properties (color, fontsize, font, fill, etc.)
                      Use 'color' for text color (will be converted to 'fill')
        """
        if name is None:
            name = f"text_{len(self.text_elements)}"
        
        # Remove old text if exists
        if name in self.text_elements:
            self.canvas.delete(self.text_elements[name])
        
        # Handle color parameter - convert 'color' to 'fill' for tkinter canvas
        fill_color = kwargs.pop('color', kwargs.get('fill', 'black'))  # Default to black for visibility
        
        # Default text properties
        default_kwargs = {
            'fill': fill_color,
            'font': kwargs.get('font', ('Arial', kwargs.get('fontsize', 12), 'bold'))
        }
        # Add remaining kwargs (excluding fontsize which is handled above)
        if 'fontsize' in kwargs:
            default_kwargs['font'] = ('Arial', kwargs['fontsize'], 'bold')
        default_kwargs.update({k: v for k, v in kwargs.items() if k not in ['fontsize']})
        
        # Create text on canvas
        text_id = self.canvas.create_text(x, y, text=text, **default_kwargs)
        self.text_elements[name] = text_id
        
        self._update_display()
    
    def add_shape(self, shape_type, coords, name=None, **kwargs):
        """
        Add shapes like rectangles, ovals, lines, etc.
        
        Args:
            shape_type: 'rectangle', 'oval', 'line', 'polygon'
            coords: List/tuple of coordinates [x1, y1, x2, y2] for rectangle/oval/line
            name: Optional name identifier
            **kwargs: Shape properties (fill, outline, width, etc.)
        """
        if name is None:
            name = f"shape_{len(self.shape_elements)}"
        
        # Remove old shape if exists
        if name in self.shape_elements:
            self.canvas.delete(self.shape_elements[name])
        
        # Create shape based on type
        if shape_type == 'rectangle':
            shape_id = self.canvas.create_rectangle(coords, **kwargs)
        elif shape_type == 'oval':
            shape_id = self.canvas.create_oval(coords, **kwargs)
        elif shape_type == 'line':
            shape_id = self.canvas.create_line(coords, **kwargs)
        elif shape_type == 'polygon':
            shape_id = self.canvas.create_polygon(coords, **kwargs)
        else:
            raise ValueError(f"Unknown shape type: {shape_type}")
        
        self.shape_elements[name] = shape_id
        self._update_display()
    
    def add_text_relative(self, text, rel_x, rel_y, name=None, **kwargs):
        """
        Add text positioned relative to the image center.
        
        Args:
            text: Text string to display
            rel_x, rel_y: Position relative to image center (-0.5 to 0.5)
                          e.g., (-0.4, -0.4) = top-left, (0, 0) = center
            name: Optional name identifier
            **kwargs: Text properties (color, fontsize, etc.)
        """
        if self.image_center_x is None:
            # Fallback to absolute positioning if image not loaded
            self.add_text(text, 100, 50, name=name, **kwargs)
            return
        
        # Calculate absolute position from relative coordinates
        abs_x = self.image_center_x + (rel_x * self.image_width)
        abs_y = self.image_center_y + (rel_y * self.image_height)
        
        self.add_text(text, abs_x, abs_y, name=name, **kwargs)
    
    def update_plot(self):
        """Update the trust level plot with current history."""
        if len(self.index_history) == 0:
            return
        
        # Clear and redraw plot
        self.ax.clear()
        self.ax.plot(self.index_history, self.trust_history, 'b-o', linewidth=2, markersize=6, label='Trust Level')
        self.ax.set_xlabel('Index')
        self.ax.set_ylabel('Trust Level')
        self.ax.set_title('Trust Level Over Time')
        self.ax.grid(True, alpha=0.3)
        self.ax.legend()
        
        # Auto-scale axes
        if len(self.index_history) > 1:
            self.ax.set_xlim(min(self.index_history) - 0.5, max(self.index_history) + 0.5)
        if len(self.trust_history) > 0:
            trust_min, trust_max = min(self.trust_history), max(self.trust_history)
            trust_range = trust_max - trust_min
            if trust_range == 0:
                trust_range = 1
            self.ax.set_ylim(trust_min - 0.1 * trust_range, trust_max + 0.1 * trust_range)
        
        # Refresh the plot canvas
        self.plot_canvas.draw()
        self._update_display()
    
    def update_viewer(self, trust_level):
        """Update both image and plot with new trust level."""
        try:
            # Convert trust_level to float for plotting
            trust_value = float(trust_level)
        except (ValueError, TypeError):
            # If not a number, use 0 or handle as needed
            trust_value = 0
        
        # Update image
        self.show_image(self.base_path+'trust'+str(trust_level)+'.png')
        
        # Position text relative to image (top-left area, clearly visible)
        self.add_text_relative(f"Trust Level = {trust_level}", -0.4, -0.4, 
                              name="status", fontsize=20, color='black')
        
        # Update plot data
        self.current_index += 1
        self.index_history.append(self.current_index)
        self.trust_history.append(trust_value)
        
        # Update the plot
        self.update_plot()

    def clear_elements(self, keep_image=True):
        """Clear all text and shapes, optionally keeping the image."""
        # Clear text elements
        for text_id in self.text_elements.values():
            self.canvas.delete(text_id)
        self.text_elements.clear()
        
        # Clear shape elements
        for shape_id in self.shape_elements.values():
            self.canvas.delete(shape_id)
        self.shape_elements.clear()
        
        if not keep_image:
            if self.image_item:
                self.canvas.delete(self.image_item)
                self.image_item = None
            self.photo = None
        
        self._update_display()
    
    def _update_display(self):
        """Internal method to refresh the display."""
        self.root.update_idletasks()
        self.root.update()
    
    def close(self):
        """Close the window."""
        self.root.quit()
        self.root.destroy()
    
    def run(self):
        """Run the Tkinter main loop (blocking). Use only if you want blocking behavior."""
        self.root.mainloop()
        
        
viewer = TkImageViewer(window_size=(1000, 800))



while True:
    x = input("Press number...")
    if x.lower() == 'q':
        viewer.close()
        break
    viewer.update_viewer(x)
