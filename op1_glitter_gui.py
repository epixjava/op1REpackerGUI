import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os
import xml.etree.ElementTree as ET
from lxml import etree
import re
import cairosvg
from PIL import Image, ImageTk
from io import BytesIO

# Thanks to Nanobot567, creator of op1-glitter, for the inspiration and glitter functions!

# Glitter Theme Engine created by Epixjava 


class OP1GlitterGUI:
    def __init__(self, parent, firmware_path=None):
        self.THEME_IDENTIFIER = '<!-- Glitter theme applied! -->'
        self.ARROW_SYMBOL = "\u25BC"
        self.window = ctk.CTkToplevel(parent)
        self.window.title(" *   ✧ . *  ✧  . Welcome to Glitter! .  ✧  * . ✧   *")
        self.window.geometry("763x900")  

        self.firmware_path = firmware_path
        self.theme_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "themes")
        self.preview_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets", "preview.svg")
        
        self.showing_themed = True
        self.advanced_mode = None
        self.advanced_mode_var = None
        self.current_theme_data = None
        
        self.default_colors = [
            "#00ed95", "#ff3a5d", "#698eff", "#dfd9ff", "#ffffff",
            "#aeb1dc", "#9256d7", "#4d9eff", "#383572"
        ]
        
        if not self.firmware_path or not os.path.exists(os.path.join(self.firmware_path, "content", "display")):
            messagebox.showwarning("Warning", "Please select an unpacked firmware directory from File browser")
            self.window.destroy()
            return
            
        self.create_widgets()
        self.load_default_preview()


    def create_widgets(self):
        self.top_frame = ctk.CTkFrame(self.window)
        self.top_frame.pack(pady=10, padx=10, fill="x")
        
        self.main_frame = ctk.CTkFrame(self.window)
        self.main_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        ctk.CTkLabel(self.top_frame, text="Select Theme:").pack(side="left", padx=5)
        self.theme_var = tk.StringVar()
        self.theme_dropdown = ctk.CTkOptionMenu(
            self.top_frame,
            variable=self.theme_var,
            values=self.get_available_themes(),
            command=self.update_preview
        )
        self.theme_dropdown.pack(side="left", padx=5)
        
        ctk.CTkButton(
            self.top_frame,
            text="Add New Theme",
            command=self.add_new_theme
        ).pack(side="right", padx=5)
        
        ctk.CTkButton(
            self.top_frame,
            text="Apply Theme",
            command=self.apply_theme
        ).pack(side="right", padx=5)
        
        ctk.CTkButton(
            self.top_frame,
            text="How to use",
            command=self.show_theme_guide
        ).pack(side="right", padx=5)
        
        preview_frame = ctk.CTkFrame(self.main_frame)
        preview_frame.pack(pady=10, padx=10, fill="x")
        
        preview_header = ctk.CTkFrame(preview_frame)
        preview_header.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(preview_header, text="Theme Preview:", anchor="center").pack(side="left")
        
        self.toggle_button = ctk.CTkButton(
            preview_header,
            text="Theme: Off",  
            command=self.toggle_preview
        )
        self.toggle_button.pack(side="right", padx=5)
        
        self.preview_canvas = tk.Canvas(
            preview_frame,
            width=340,  
            height=170,  
            bg='black'
        )
        self.preview_canvas.pack(pady=15, padx=15)

        sparkle_frame = ctk.CTkFrame(self.main_frame)
        sparkle_frame.pack(pady=1, padx=10, fill="both", expand=True)

        ctk.CTkLabel(
            sparkle_frame,
            text=" .  ✧  *  Glitter Theme Engine  .  ✧  * ",
            font=("Helvetica", 20)
        ).pack(pady=10)

        ctk.CTkLabel(
            sparkle_frame,
            text="Common OP-1 Colors",
            font=("Helvetica", 16)
        ).pack(pady=5)

        color_grid = ctk.CTkFrame(sparkle_frame)
        color_grid.pack(expand=True, fill='both', padx=20, pady=20)

        self.top_color_frames = []
        self.bottom_color_frames = []
        self.top_color_entries = []
        self.bottom_color_entries = []

        top_container = ctk.CTkFrame(color_grid)
        top_container.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)
        top_container.grid_columnconfigure(tuple(range(9)), weight=1)

        arrow_container = ctk.CTkFrame(color_grid, height=40)
        arrow_container.grid(row=1, column=0, sticky='nsew', padx=20, pady=0)
        arrow_container.grid_columnconfigure(tuple(range(9)), weight=1)
        arrow_container.grid_propagate(False)

        bottom_container = ctk.CTkFrame(color_grid)
        bottom_container.grid(row=2, column=0, sticky='nsew', padx=20, pady=20)
        bottom_container.grid_columnconfigure(tuple(range(9)), weight=1)

        for i in range(9):
            frame = ctk.CTkFrame(top_container)
            frame.grid(row=0, column=i)
            
            color_box = tk.Canvas(
                frame,
                width=50,
                height=50,
                highlightthickness=0,
                bd=0,
                bg=self.default_colors[i]
            )
            color_box.pack(pady=2)
            
            entry = ctk.CTkEntry(
                frame,
                placeholder_text="HEX",
                width=72
            )
            entry.insert(0, self.default_colors[i])
            entry.pack(pady=2)
            
            self.top_color_frames.append(color_box)
            self.top_color_entries.append(entry)
            entry.bind('<KeyRelease>', lambda e, index=i: self.update_top_color(index))
            
            arrow = ctk.CTkLabel(
                arrow_container,
                text=self.ARROW_SYMBOL, 
                font=("Arial", 20, "bold")
            )
            arrow.grid(row=0, column=i)
            
            frame = ctk.CTkFrame(bottom_container)
            frame.grid(row=0, column=i)
            
            color_box = tk.Canvas(
                frame,
                width=50,
                height=50,
                highlightthickness=0,
                bd=0
            )
            color_box.pack(pady=2)
            
            entry = ctk.CTkEntry(
                frame,
                placeholder_text="HEX",
                width=70
            )
            entry.pack(pady=2)
            
            self.bottom_color_frames.append(color_box)
            self.bottom_color_entries.append(entry)
            
            entry.bind('<KeyRelease>', lambda e, index=i: self.update_color(index))

        save_container = ctk.CTkFrame(sparkle_frame)
        save_container.pack(pady=10)

        input_container = ctk.CTkFrame(save_container)
        input_container.pack(side=tk.LEFT, padx=10)
        
        self.theme_name_entry = ctk.CTkEntry(
            input_container,
            placeholder_text="Theme name",
            width=200
        )
        self.theme_name_entry.pack(pady=(0, 5))
        
        self.theme_description_entry = ctk.CTkEntry(
            input_container,
            placeholder_text="Theme description (optional)",
            width=200
        )
        self.theme_description_entry.pack()
        
        save_button = ctk.CTkButton(
            save_container,
            text="Save Theme",
            command=self.save_sparkle_theme
        )
        save_button.pack(side=tk.LEFT, padx=10)
        
        bottom_frame = ctk.CTkFrame(self.window)
        bottom_frame.pack(pady=5, padx=10, fill="x", side="bottom")
        
        self.advanced_mode_var = tk.BooleanVar(value=False)
        self.advanced_mode_switch = ctk.CTkSwitch(
            bottom_frame,
            text="Advanced Mode",
            command=self.toggle_advanced_mode,
            variable=self.advanced_mode_var
        )
        self.advanced_mode_switch.pack(side="left", padx=10, pady=5) 
        
    def update_top_color(self, index):
        try:
            hex_color = self.top_color_entries[index].get()
            if not hex_color:
                hex_color = self.default_colors[index]
                self.top_color_entries[index].insert(0, hex_color)
            if hex_color.startswith('#'):
                self.top_color_frames[index].configure(bg=hex_color)
            elif len(hex_color) == 6:
                self.top_color_frames[index].configure(bg=f'#{hex_color}')
        except tk.TclError:
            self.top_color_frames[index].configure(bg=self.default_colors[index])


    def update_bottom_color(self, index):
        try:
            hex_color = self.bottom_color_entries[index].get()
            if hex_color.startswith('#'):
                self.bottom_color_frames[index].configure(bg=hex_color)
            elif len(hex_color) == 6:
                self.bottom_color_frames[index].configure(bg=f'#{hex_color}')
        except tk.TclError:
            pass


    def load_theme_colors(self, theme_data):
        if not theme_data or 'global' not in theme_data:
            return
        
        for i, default_color in enumerate(self.default_colors):
            if default_color in theme_data['global']:
                new_color = theme_data['global'][default_color]
                self.bottom_color_entries[i].delete(0, 'end')
                self.bottom_color_entries[i].insert(0, new_color)
                self.bottom_color_frames[i].configure(bg=new_color)
 
    
    def render_svg(self, svg_path, theme_data=None):
        try:
            with open(svg_path, 'r', encoding='utf-8') as f:
                svg_content = f.read()
            if theme_data:
                root = ET.fromstring(svg_content)
                svg_content = ET.tostring(root, encoding='unicode')
                hex_color_regex = re.compile(r"^#(?:[0-9a-fA-F]{3}){1,2}$")
                for orig_color, new_color in theme_data['global'].items():
                    if hex_color_regex.match(orig_color) and hex_color_regex.match(new_color):
                        svg_content = svg_content.replace(orig_color.upper(), new_color.upper())
                        svg_content = svg_content.replace(orig_color.lower(), new_color.lower())
            png_data = cairosvg.svg2png(bytestring=svg_content.encode('utf-8'))
            image = Image.open(BytesIO(png_data))
            photo = ImageTk.PhotoImage(image)
            self.preview_canvas.delete("all")
            self.preview_canvas.create_image(0, 0, anchor="nw", image=photo)
            self.preview_canvas.image = photo
        except Exception as e:
            messagebox.showerror("Error", f"Failed to render SVG: {str(e)}")


    def load_default_preview(self):
        self.render_svg(self.preview_path)


    def toggle_preview(self):
        self.showing_themed = not self.showing_themed
        if not self.showing_themed:
            self.render_svg(self.preview_path)
            self.toggle_button.configure(text="Theme: Off")
        elif self.current_theme_data:
            self.render_svg(self.preview_path, self.current_theme_data)
            self.toggle_button.configure(text="Theme: On")
 
            
    def update_preview(self, *args):
        if self.theme_var.get() == "No themes available":
            return
        try:
            theme_path = os.path.join(self.theme_dir, self.theme_var.get())
            with open(theme_path, 'r') as f:
                self.current_theme_data = json.load(f)
            self.load_theme_colors(self.current_theme_data)
            if self.showing_themed and self.current_theme_data:
                self.render_svg(self.preview_path, self.current_theme_data)
            else:
                self.render_svg(self.preview_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update preview: {str(e)}")
 
    
    def update_color(self, index):
        try:
            hex_color = self.bottom_color_entries[index].get()
            if hex_color.startswith('#'):
                self.bottom_color_frames[index].configure(bg=hex_color)
            elif len(hex_color) == 6:
                self.bottom_color_frames[index].configure(bg=f'#{hex_color}')
        except tk.TclError:
            pass


    def save_sparkle_theme(self):
        theme_name = self.theme_name_entry.get().strip() or "theme"
        theme_description = self.theme_description_entry.get().strip() or "Theme created with Glitter theme engine"
    
        theme = {
            f"{theme_name}": [
                theme_description
            ],
            "global": {}
        }
    
        for i in range(len(self.default_colors)):
            top_value = self.top_color_entries[i].get().strip()
            bottom_value = self.bottom_color_entries[i].get().strip()
        
            if not top_value:
                top_value = self.default_colors[i]
            if not top_value.startswith('#'):
                top_value = f"#{top_value}"
            
            if bottom_value:
                if not bottom_value.startswith('#'):
                    bottom_value = f"#{bottom_value}"
                theme["global"][top_value] = bottom_value
    
        filename = f"{theme_name}.json"
    
        try:
            filepath = os.path.join(self.theme_dir, filename)
            with open(filepath, 'w') as f:
                json.dump(theme, f, indent=4)
            messagebox.showinfo("Success", f"Theme saved successfully as {filename}!")
            self.theme_dropdown.configure(values=self.get_available_themes())
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save theme: {str(e)}")


    def show_theme_guide(self):
        guide_window = ctk.CTkToplevel(self.window)
        guide_window.title("How to use this tool")
        guide_window.geometry("800x800")  

        text_frame = ctk.CTkFrame(guide_window)
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)

        text_widget = ctk.CTkTextbox(
            text_frame,
            wrap="none",  
            font=("Courier", 14),  
        )
        text_widget.pack(fill="both", expand=True)

        guide_path = os.path.join(self.theme_dir, "Glitter_Guide.txt")
        try:
            with open(guide_path, 'r', encoding='utf-8') as f:
                guide_content = f.read()
            text_widget.insert("1.0", guide_content)
            text_widget.configure(state="disabled")  
        except Exception as e:
            text_widget.insert("1.0", "Error loading theme guide.")
            text_widget.configure(state="disabled")


    def get_available_themes(self):
        themes = [f for f in os.listdir(self.theme_dir) if f.endswith('.json')]
        return themes if themes else ["No themes available"]


    def add_new_theme(self):
        file_path = filedialog.askopenfilename(
            initialdir=self.theme_dir,  
            filetypes=[("JSON files", "*.json")],
            title="Select Theme File"
        )
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    json.load(f)

                filename = os.path.basename(file_path)
                new_path = os.path.join(self.theme_dir, filename)
            
                if file_path != new_path:
                    with open(file_path, 'r') as src, open(new_path, 'w') as dst:
                        dst.write(src.read())
            
                self.theme_dropdown.configure(values=self.get_available_themes())
                messagebox.showinfo("Success", f"Theme {filename} added successfully!")
            except json.JSONDecodeError:
                messagebox.showerror("Error", "Invalid JSON format in theme file")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add theme: {str(e)}")
    
    
    def toggle_advanced_mode(self):
        if self.advanced_mode_var.get():
           self.advanced_window = AdvancedModeWindow(self.window, self)
           self.window.withdraw() 
        else:
            pass
    
    
    def add_theme_identifier(self, svg_content):
        return svg_content + self.THEME_IDENTIFIER
    
    
    def is_theme_applied(self, svg_content):
        return self.THEME_IDENTIFIER in svg_content
    
    
    def check_themes_applied(self, display_dir):
        for file in os.listdir(display_dir):
            if file.endswith('.svg'):
                file_path = os.path.join(display_dir, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        if self.is_theme_applied(f.read()):
                            return True
                except Exception:
                    continue
        return False
    
    
    def apply_theme(self):
        if not self.theme_var.get() or self.theme_var.get() == "No themes available":
            return  
        try:
            display_dir = os.path.join(self.firmware_path, "content", "display")
        
            if self.check_themes_applied(display_dir):
                messagebox.showwarning(
                    "Warning", 
                    "Themes have already been applied to this firmware. \nPlease use a fresh firmware directory."
                )
                return
            
            theme_path = os.path.join(self.theme_dir, self.theme_var.get())
            with open(theme_path, 'r') as f:
                theme_data = json.load(f)
                
            if self.patch_svg_files(display_dir, theme_data):
                messagebox.showinfo("Success", "Theme applied successfully!")   
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply theme: {str(e)}")
     
                   
    def patch_svg_files(self, display_dir, theme_data):
        hex_color_regex = re.compile(r"^#(?:[0-9a-fA-F]{3}){1,2}$")
        parser = etree.XMLParser(remove_blank_text=True, remove_comments=False)

        for file in os.listdir(display_dir):
            if not file.endswith('.svg'):
                continue
            file_path = os.path.join(display_dir, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    original_data = f.read()
            
                if original_data.count('<?xml') > 1:
                    original_data = re.sub(r'<\?xml[^>]*>\s*', '', original_data, count=1)
                
                tree = etree.fromstring(original_data.encode(), parser)
                colors = theme_data['global'].copy()
                fname = os.path.splitext(file)[0]
            
                if fname in theme_data:
                    for k, v in theme_data[fname].items():
                        if v != "":
                            colors[k] = v
                        
                colors_order = []
                for k, v in colors.items():
                    if not re.search(hex_color_regex, k):
                        colors_order.insert(0, k)
                    else:
                        colors_order.append(k)
                    
                for orig in colors_order:
                    repl = colors[orig]
                    if orig and repl:
                        if re.search(hex_color_regex, orig) and re.search(hex_color_regex, repl):
                            original_data = original_data.replace(orig.upper(), repl.upper())
                            original_data = original_data.replace(orig.lower(), repl.lower())
                            tree = etree.fromstring(original_data.encode(), parser)
                        else:
                            if isinstance(repl, str):
                                repl = [["stroke", repl]]
                            if not isinstance(repl[0], list):
                                repl = [repl]
                            
                            for current_repl in repl:
                                is_colors = (re.search(hex_color_regex, current_repl[0]) and 
                                        re.search(hex_color_regex, current_repl[1]))
                            
                                for element in tree.iter():
                                    if element.get("id") == orig:
                                        if is_colors:
                                            for e in element.iter():
                                                if e.get("stroke") == current_repl[0].upper():
                                                    e.set("stroke", current_repl[1].upper())
                                                if e.get("fill") == current_repl[0].upper():
                                                    e.set("fill", current_repl[1].upper())
                                        else:
                                            if element.tag.split("}")[-1] == "g":
                                                for e in element.iter():
                                                    if e.get(current_repl[0]):
                                                        e.set(current_repl[0], current_repl[1].upper())
                                            if element.get(current_repl[0]):
                                                element.set(current_repl[0], current_repl[1].upper())
                                            
                            original_data = etree.tostring(tree, pretty_print=True, encoding='unicode')
                
                final_data = self.add_theme_identifier(original_data)
                       
                with open(file_path, 'w', encoding='utf-8') as f:
                    if '<?xml' not in final_data:
                        f.write('<?xml version="1.0" encoding="utf-8"?>\n')
                    f.write(final_data)
                
            except Exception as e:
                continue
    
        return True
    
    
class AdvancedModeWindow:
    def __init__(self, parent, main_window):
        self.main_window = main_window
        self.parent = parent
        
        self.window = ctk.CTkToplevel(parent)
        self.window.title("*   ✧ . *  ✧  . Glitter Theme Engine - Advanced Mode .  ✧  * . ✧   *")
        self.window.geometry("900x1024")
        
        self.theme_data = {
            "theme_meta": [""],
            "global": {},
        }
        
        self.firmware_path = self.main_window.firmware_path
        self.theme_dir = self.main_window.theme_dir
        self.default_colors = main_window.default_colors
        self.showing_themed = True
        self.current_theme_data = None
        self.preview_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets", "preview.svg")
        self.current_svg_path = self.preview_path
        
        self.create_widgets()
        self.load_default_preview()
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.svg_cache = SVGCache()
        self.svg_parser = SVGParser()
        self.id_load_after = None
    
        
    def create_widgets(self):
        self.preview_adv()
        self.theme_controls()
        self.create_global_section()
        self.create_svg_section()
    
    
    def preview_adv(self):
        preview_frame = ctk.CTkFrame(self.window)
        preview_frame.pack(pady=10, padx=10, fill="x")

        controls_frame = ctk.CTkFrame(preview_frame)
        controls_frame.pack(side="left", pady=10, padx=10, fill="y")

        self.easy_mode_var = tk.BooleanVar(value=True)
        self.easy_mode_switch = ctk.CTkSwitch(
            controls_frame,
            text="Basic Mode",
            command=self.toggle_basic_mode,
            variable=self.easy_mode_var
        )
        self.easy_mode_switch.pack(anchor="w", padx=5, pady=(0, 10))

        svg_label = ctk.CTkLabel(controls_frame, text="Select SVG File:")
        svg_label.pack(anchor="w", padx=5, pady=(0, 2))

        self.svg_files = ["Select an SVG file"] + self.get_svg_files()
        self.svg_var = tk.StringVar(value=self.svg_files[0])

        self.svg_dropdown = ctk.CTkOptionMenu(
            controls_frame,
            variable=self.svg_var,
            values=self.svg_files,
            command=self.update_preview_adv,
            width=200
        )
        self.svg_dropdown.pack(anchor="w", padx=5, pady=(0, 10))

        theme_label = ctk.CTkLabel(controls_frame, text="Select Theme:")
        theme_label.pack(anchor="w", padx=5, pady=(0, 2))

        self.theme_var = tk.StringVar()
        self.theme_dropdown = ctk.CTkOptionMenu(
            controls_frame,
            variable=self.theme_var,
            values=self.get_available_themes(),
            command=self.update_theme,
            width=200
        )
        self.theme_dropdown.pack(anchor="w", padx=5, pady=(0, 10))
        
        apply_button = ctk.CTkButton(
            controls_frame,
            text="Apply Theme",
            command=self.apply_theme,
            width=200
        )
        apply_button.pack(anchor="w", padx=5, pady=(0, 10))

        preview_area = ctk.CTkFrame(preview_frame)
        preview_area.pack(side="right", pady=10, padx=10, fill="both", expand=True)

        preview_header = ctk.CTkFrame(preview_area)
        preview_header.pack(fill="x", padx=5, pady=5)

        preview_label = ctk.CTkLabel(preview_header, text="SVG Preview:")
        preview_label.pack(side="left", padx=5)

        self.toggle_button = ctk.CTkButton(
            preview_header,
            text="Theme: Off",  
            command=self.toggle_preview,
            width=100
        )
        self.toggle_button.pack(side="right", padx=5)

        self.preview_canvas = tk.Canvas(
            preview_area,
            width=340,
            height=170,
            bg='black'
        )
        self.preview_canvas.pack(pady=15, padx=15) 
    
              
    def load_default_preview(self):
        try:
            if not os.path.isfile(self.preview_path):
                messagebox.showerror("Error", "Could not find preview.svg in assets folder")
                return
        
            self.render_svg(self.preview_path)
        
            if hasattr(self, 'svg_dropdown'):
                self.svg_dropdown.set("Select an SVG file")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load default preview: {str(e)}")
    
    
    def create_global_section(self):
        global_frame = ctk.CTkFrame(self.window)
        global_frame.pack(fill="x", padx=10, pady=5)
    
        ctk.CTkLabel(
            global_frame,
            text="Global Color Mappings and Element IDs",
            font=("Helvetica", 16)
        ).pack(pady=5)
        
    
        split_container = ctk.CTkFrame(global_frame)
        split_container.pack(fill="both", expand=True, pady=5)
    
        colors_frame = ctk.CTkFrame(split_container)
        colors_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
    
        self.color_entries = []
        for i, color in enumerate(self.default_colors):
            row_frame = ctk.CTkFrame(colors_frame)
            row_frame.pack(pady=2)
        
            orig_canvas = tk.Canvas(
                row_frame, 
                width=20, 
                height=20, 
                bg=color
            )
            orig_canvas.pack(side="left", padx=5)
        
            orig_entry = ctk.CTkEntry(
                row_frame,
                width=100,
                placeholder_text="Original"
            )
            orig_entry.insert(0, color)
            orig_entry.pack(side="left", padx=5)
        
            ctk.CTkLabel(
                row_frame,
                text="→"
            ).pack(side="left", padx=5)
        
            new_entry = ctk.CTkEntry(
                row_frame,
                width=100,
                placeholder_text="New color"
            )
            new_entry.pack(side="left", padx=5)
        
            new_canvas = tk.Canvas(
                row_frame,
                width=20,
                height=20,
                bg="white"
            )
            new_canvas.pack(side="left", padx=5)
        
            self.color_entries.append({
                'original': orig_entry,
                'new': new_entry,
                'orig_preview': orig_canvas,
                'new_preview': new_canvas
            })
        
            new_entry.bind(
                '<KeyRelease>',
                lambda e, canvas=new_canvas: self.update_color_preview(e, canvas)
            )
    
        right_frame = ctk.CTkFrame(split_container)
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
    
    
        self.right_scroll_frame = ctk.CTkScrollableFrame(right_frame, height=200)
        self.right_scroll_frame.pack(fill="both", expand=True, pady=5)
    
      
    def create_svg_section(self):
        svg_frame = ctk.CTkFrame(self.window)
        svg_frame.pack(fill="x", padx=10, pady=5)

        header_frame = ctk.CTkFrame(svg_frame)
        header_frame.pack(fill="x", pady=5)

        left_container = ctk.CTkFrame(header_frame)
        left_container.pack(side="left", fill="x", expand=True, padx=5)

        ctk.CTkLabel(
            left_container,
            text="SVG Element ID Mappings",
            font=("Helvetica", 16)
        ).pack(side="left", pady=5, padx=5)

        add_svg_button = ctk.CTkButton(
            left_container,
            text="Add SVG Mapping",
            command=self.add_svg_section
        )
        add_svg_button.pack(side="left", padx=5)

        remove_svg_button = ctk.CTkButton(
            left_container,
            text="Remove SVG Mapping",
            command=self.remove_last_svg_section
        )
        remove_svg_button.pack(side="left", padx=5)

        self.svg_sections_frame = ctk.CTkScrollableFrame(svg_frame, height=400)
        self.svg_sections_frame.pack(fill="x", pady=5, expand=True)

        self.add_svg_section()
    
    
    def update_color_preview(self, event, canvas):
        color = event.widget.get()
        try:
            if color.startswith('#') and len(color) in [4, 7]:
                canvas.configure(bg=color)
        except tk.TclError:
            pass
    
    
    def add_svg_section(self):
        section_frame = ctk.CTkFrame(self.svg_sections_frame)
        section_frame.pack(fill="x", pady=5, padx=5)

        header_frame = ctk.CTkFrame(section_frame)
        header_frame.pack(fill="x", pady=2)

        name_frame = ctk.CTkFrame(header_frame)
        name_frame.pack(side="left", fill="x", expand=True)

        svg_name_entry = ctk.CTkEntry(
            name_frame,
            placeholder_text="SVG filename (without extension)",
            width=200
        )
        svg_name_entry.pack(side="left", padx=5)

        buttons_frame = ctk.CTkFrame(header_frame)
        buttons_frame.pack(side="right", padx=5)

        add_mapping_button = ctk.CTkButton(
            buttons_frame,
            text="Add Mapping",
            width=100,
            command=lambda: self.add_color_mapping(color_mappings_frame)
        )
        add_mapping_button.pack(side="left", padx=2)

        remove_mapping_button = ctk.CTkButton(
            buttons_frame,
            text="Remove Mapping",
            width=100,
            command=lambda: self.remove_last_mapping_from_frame(color_mappings_frame)
        )
        remove_mapping_button.pack(side="left", padx=2)

        color_mappings_frame = ctk.CTkFrame(section_frame)
        color_mappings_frame.pack(fill="x", pady=2)
    
        self.add_color_mapping(color_mappings_frame)

        return section_frame
    
    
    def get_svg_files(self):
        try:
            preview_name = "Preview Theme"  
            svg_files = [preview_name]
        
            display_dir = os.path.join(self.firmware_path, "content", "display")
            firmware_svgs = [f for f in os.listdir(display_dir) if f.endswith('.svg')]
            svg_files.extend(sorted(firmware_svgs))
           
            return svg_files if svg_files else ["No SVG files found"]
        except Exception as e:
            print(f"Error loading SVG files: {str(e)}")
            return ["Error loading SVG files"]
    
        
    def add_color_mapping(self, parent):
        row_frame = ctk.CTkFrame(parent)
        row_frame.pack(pady=1)

        orig_entry = ctk.CTkEntry(
            row_frame,
            width=150,
            height=28,
            placeholder_text="Element ID or color"
        )
        orig_entry.pack(side="left", padx=5)

        ctk.CTkLabel(
            row_frame,
            text="→",
            height=28,
        ).pack(side="left", padx=5)

        new_entry = ctk.CTkEntry(
            row_frame,
            width=100,
            height=28,
            placeholder_text="New color"
        )
        new_entry.pack(side="left", padx=5)

        new_canvas = tk.Canvas(
            row_frame,
            width=20,
            height=20,
            bg="white"
        )
        new_canvas.pack(side="left", padx=5)

        new_entry.bind(
            '<KeyRelease>',
            lambda e, canvas=new_canvas: self.update_color_preview(e, canvas)
        )

        return row_frame
    
    
    def save_theme(self):
        theme_name = self.theme_name.get().strip() or "theme"
        theme_desc = self.theme_desc.get().strip()

        self.theme_data = {
            "theme_meta": [theme_desc] if theme_desc else ["Theme created with Glitter theme engine"],
            "global": {}
        }

        for entry in self.color_entries:
            orig = entry['original'].get().strip()
            new = entry['new'].get().strip()
            if orig and new:
                self.theme_data["global"][orig] = new

        for svg_section in self.svg_sections_frame.winfo_children():
            svg_name = svg_section.winfo_children()[0].winfo_children()[0].winfo_children()[0].get().strip()
        
            if svg_name:
                self.theme_data[svg_name] = {}
            
                color_mappings_frame = svg_section.winfo_children()[1]
            
                for mapping_row in color_mappings_frame.winfo_children():
                    if isinstance(mapping_row, ctk.CTkFrame):
                        orig = mapping_row.winfo_children()[0].get().strip()
                        new = mapping_row.winfo_children()[2].get().strip()
                        if orig and new:
                            self.theme_data[svg_name][orig] = new

        file_path = os.path.join(self.theme_dir, f"{theme_name}.json")

        try:
            with open(file_path, 'w') as f:
                json.dump(self.theme_data, f, indent=2)
            messagebox.showinfo("Success", "Theme saved successfully!")
        
            if hasattr(self, 'theme_dropdown'):
                self.theme_dropdown.configure(values=self.get_available_themes())
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save theme: {str(e)}")
    
    
    def get_available_themes(self):
        themes = [f for f in os.listdir(self.theme_dir) if f.endswith('.json')]
        return themes if themes else ["No themes available"]


    def render_svg(self, svg_path, theme_data=None):
        try:
            with open(svg_path, 'r', encoding='utf-8') as f:
                svg_content = f.read()
            if theme_data:
                root = ET.fromstring(svg_content)
                svg_content = ET.tostring(root, encoding='unicode')
                hex_color_regex = re.compile(r"^#(?:[0-9a-fA-F]{3}){1,2}$")
                for orig_color, new_color in theme_data['global'].items():
                    if hex_color_regex.match(orig_color) and hex_color_regex.match(new_color):
                        svg_content = svg_content.replace(orig_color.upper(), new_color.upper())
                        svg_content = svg_content.replace(orig_color.lower(), new_color.lower())
        
            png_data = cairosvg.svg2png(bytestring=svg_content.encode('utf-8'))
            image = Image.open(BytesIO(png_data))
            photo = ImageTk.PhotoImage(image)
            self.preview_canvas.delete("all")
            self.preview_canvas.create_image(0, 0, anchor="nw", image=photo)
            self.preview_canvas.image = photo
        except Exception as e:
            messagebox.showerror("Error", f"Failed to render SVG: {str(e)}")


    def update_preview_adv(self, *args):
        selected_file = self.svg_var.get()

        if selected_file in ["No SVG files found", "Error loading SVG files", "Select an SVG file"]:
            self.current_svg_path = self.preview_path
            self.update_id_viewer(self.preview_path)  
            self.render_svg(self.preview_path, self.current_theme_data if self.showing_themed else None)
            return

        try:
            if selected_file == "Preview Theme":
                svg_path = self.preview_path
                filename = "preview"
            else:
                svg_path = os.path.join(self.firmware_path, "content", "display", selected_file)
                filename = selected_file[:-4]  

            if not os.path.isfile(svg_path):
                messagebox.showerror("Error", f"Could not find SVG file: {selected_file}")
                return

            self.current_svg_path = svg_path
        
            try:
                self.update_id_viewer(svg_path)
            except Exception as e:
                print(f"Error updating ID viewer: {str(e)}")

            name_exists = False
            for section in self.svg_sections_frame.winfo_children():
                name_entry = section.winfo_children()[0].winfo_children()[0].winfo_children()[0]
                if name_entry.get().strip() == filename:
                    name_exists = True
                    break

            if name_exists:
                self.render_svg(svg_path, self.current_theme_data if self.showing_themed else None)
                return

            first_section = self.svg_sections_frame.winfo_children()[0]
            name_entry = first_section.winfo_children()[0].winfo_children()[0].winfo_children()[0]
        
            if name_entry.get().strip():
                section = self.add_svg_section()
                new_name_entry = section.winfo_children()[0].winfo_children()[0].winfo_children()[0]
                new_name_entry.delete(0, 'end')
                new_name_entry.insert(0, filename)
                color_mappings_frame = section.winfo_children()[1]
            else:
                
                name_entry.delete(0, 'end')
                name_entry.insert(0, filename)
                color_mappings_frame = first_section.winfo_children()[1]
                
                for widget in color_mappings_frame.winfo_children():
                    widget.destroy()

            
            self.add_color_mapping(color_mappings_frame)

            
            if self.current_theme_data and filename in self.current_theme_data:
                svg_theme_data = self.current_theme_data[filename]
                for key, value in svg_theme_data.items():
                    row = self.add_color_mapping(color_mappings_frame)
                    row.winfo_children()[0].insert(0, key)  
                    row.winfo_children()[2].insert(0, value)  

            
            self.render_svg(svg_path, self.current_theme_data if self.showing_themed else None)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load SVG: {str(e)}")

    def update_id_viewer(self, svg_path):
        
        if self.id_load_after:
            self.window.after_cancel(self.id_load_after)
        
        
        for widget in self.right_scroll_frame.winfo_children():
            widget.destroy()
        
        
        loading_label = ctk.CTkLabel(
            self.right_scroll_frame,
            text="Loading element IDs...",
            text_color="gray"
        )
        loading_label.pack(pady=10)
    
        
        self.id_load_after = self.window.after(100, lambda: self.id_update(svg_path, loading_label))


    def id_update(self, svg_path, loading_label):
        try:
            ids = self.parse_svg_ids(svg_path)
        
            
            loading_label.destroy()
        
            ctk.CTkLabel(
                self.right_scroll_frame,
                text="SVG Element IDs",
                font=("Helvetica", 14, "bold")
            ).pack(pady=(0, 10))
        
            if not ids:
                ctk.CTkLabel(
                    self.right_scroll_frame,
                    text="No element IDs found in this SVG",
                    text_color="gray"
                ).pack(pady=10)
                return
            
            self._add_id_batch(sorted(ids), 0, 20)  
        
        except Exception as e:
            print(f"Error updating ID viewer: {str(e)}")
            ctk.CTkLabel(
                self.right_scroll_frame,
                text="Error loading element IDs",
                text_color="red"
            ).pack(pady=10)


    def _add_id_batch(self, ids, start, batch_size):
        end = min(start + batch_size, len(ids))
    
        for index, element_id in enumerate(ids[start:end], start + 1):
            id_label = ctk.CTkLabel(
                self.right_scroll_frame,
                text=f"{index}. {element_id}",
                anchor="w"
            )
            id_label.pack(fill="x", padx=5, pady=1)
    
        if end < len(ids):
            self.window.after(50, lambda: self._add_id_batch(ids, end, batch_size))
    
    
    def toggle_preview(self):
        self.showing_themed = not self.showing_themed

        try:
            if self.svg_var.get() in ["No SVG files found", "Error loading SVG files", "Select an SVG file"]:
                if not self.showing_themed:
                    self.render_svg(self.preview_path)
                    self.toggle_button.configure(text="Theme: Off")
                else:
                    if not self.current_theme_data:
                        theme_selection = self.theme_var.get()
                        if theme_selection and theme_selection != "No themes available":
                            self.update_theme()
                        else:
                            messagebox.showinfo("Info", "Please select a theme first")
                            self.showing_themed = False
                            return
                    self.render_svg(self.preview_path, self.current_theme_data)
                    self.toggle_button.configure(text="Theme: On")
            else:
                if not self.showing_themed:
                    self.render_svg(self.current_svg_path)
                    self.toggle_button.configure(text="Theme: Off")
                else:
                    if not self.current_theme_data:
                        theme_selection = self.theme_var.get()
                        if theme_selection and theme_selection != "No themes available":
                            self.update_theme()
                        else:
                            messagebox.showinfo("Info", "Please select a theme first")
                            self.showing_themed = False
                            return
                    self.render_svg(self.current_svg_path, self.current_theme_data)
                    self.toggle_button.configure(text="Theme: On")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to toggle preview: {str(e)}")
    
    
    def update_theme(self, *args):
        theme_selection = self.theme_var.get()

        if not theme_selection or theme_selection == "No themes available":
            self.current_theme_data = None
            return

        try:
            theme_path = os.path.join(self.theme_dir, theme_selection)
            if not os.path.exists(theme_path):
                messagebox.showerror("Error", f"Theme file not found: {theme_selection}")
                return

            with open(theme_path, 'r') as f:
                self.current_theme_data = json.load(f)

            if not isinstance(self.current_theme_data, dict):
                messagebox.showerror("Error", "Invalid theme format: Theme data must be a dictionary")
                return

            if hasattr(self, 'svg_sections_frame'):
                for widget in self.svg_sections_frame.winfo_children():
                    widget.destroy()

            if isinstance(self.current_theme_data.get('global'), dict):
                for entry in self.color_entries:
                    orig_color = entry['original'].get().strip()
                    if orig_color in self.current_theme_data['global']:
                        new_color = self.current_theme_data['global'][orig_color]
                        entry['new'].delete(0, 'end')
                        entry['new'].insert(0, new_color)
                        if new_color.startswith('#'):  
                            entry['new_preview'].configure(bg=new_color)

            has_svg_mappings = False
        
            for key, value in self.current_theme_data.items():
                if key not in ['global', 'theme_meta'] and isinstance(value, dict):
                    has_svg_mappings = True
                    section = self.add_svg_section()
                    if section is None:  
                        continue
                    
                    header_frame = section.winfo_children()[0]
                    name_frame = header_frame.winfo_children()[0]
                    name_entry = name_frame.winfo_children()[0]
                
                    name_entry.delete(0, 'end')
                    name_entry.insert(0, key)

                    color_mappings_frame = section.winfo_children()[1]
                    
                    for widget in color_mappings_frame.winfo_children():
                        widget.destroy()
                    
                    for orig, new in value.items():
                        row = self.add_color_mapping(color_mappings_frame)
                        if row is not None:
                            orig_entry = row.winfo_children()[0]  
                            new_entry = row.winfo_children()[2]   
                        
                            orig_entry.delete(0, 'end')
                            new_entry.delete(0, 'end')
                        
                            orig_entry.insert(0, orig)
                        
                            if isinstance(new, list):
                                new_entry.insert(0, new[0])
                            elif isinstance(new, dict):
                                color_value = next(iter(new.values()), '')
                                new_entry.insert(0, color_value)
                            else:
                                new_entry.insert(0, new)
                            
                            if isinstance(row.winfo_children()[-1], tk.Canvas):
                                color_preview = row.winfo_children()[-1]
                                try:
                                    if new_entry.get().startswith('#'):
                                        color_preview.configure(bg=new_entry.get())
                                except tk.TclError:
                                    pass

            if not has_svg_mappings:
                self.add_svg_section()

            if self.showing_themed:
                self.render_svg(self.current_svg_path, self.current_theme_data)

        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid theme file format")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load theme: {str(e)}")
    
    
    def theme_controls(self):
        controls_frame = ctk.CTkFrame(self.window)
        controls_frame.pack(fill="x", padx=10, pady=5)
    
        input_frame = ctk.CTkFrame(controls_frame)
        input_frame.pack(side="left", padx=10, pady=5)
    
        name_frame = ctk.CTkFrame(input_frame)
        name_frame.pack(side="left", padx=5)
    
        ctk.CTkLabel(
            name_frame,
            text="Theme Name:"
        ).pack(anchor="w")
    
        self.theme_name = ctk.CTkEntry(
            name_frame,
            placeholder_text="Theme name",
            width=200
        )
        self.theme_name.pack(pady=(0, 5))
    
        desc_frame = ctk.CTkFrame(input_frame)
        desc_frame.pack(side="left", padx=5)
    
        ctk.CTkLabel(
            desc_frame,
            text="Description:"
        ).pack(anchor="w")
    
        self.theme_desc = ctk.CTkEntry(
            desc_frame,
            placeholder_text="Enter theme description",
            width=300
        )
        self.theme_desc.pack(pady=(0, 5))
    
        save_frame = ctk.CTkFrame(controls_frame)
        save_frame.pack(side="right", padx=10, pady=5)
    
        ctk.CTkButton(
            save_frame,
            text="Save Theme",
            command=self.save_theme
        ).pack(pady=5)
    
    
    def toggle_basic_mode(self):
        self.main_window.advanced_mode_var.set(False)
        self.main_window.window.deiconify()
        self.window.destroy()
     
            
    def remove_last_svg_section(self):
        sections = self.svg_sections_frame.winfo_children()
        if len(sections) > 1:  
            sections[-1].destroy()
    
    
    def remove_last_mapping_from_frame(self, frame):
        mappings = frame.winfo_children()
        if len(mappings) > 1:  
            mappings[-1].destroy()
    
    
    def parse_svg_ids(self, svg_path):
        cached_ids = self.svg_cache.get_ids(svg_path)
        if cached_ids:
            return cached_ids
        
        try:
            with open(svg_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            potential_ids = self.svg_parser.quick_parse(content)
        
            if len(potential_ids) > 100:  # Arbitrary threshold
                valid_ids = self.svg_parser.validate_ids(content, potential_ids)
            else:
                valid_ids = potential_ids
            
          
            self.svg_cache.store_ids(svg_path, valid_ids)
            return valid_ids
        
        except Exception as e:
            print(f"Error parsing SVG IDs: {str(e)}")
            return []
    
    
    def apply_theme(self):
        if not self.theme_var.get() or self.theme_var.get() == "No themes available":
            return  
        try:
            display_dir = os.path.join(self.firmware_path, "content", "display")

            if self.main_window.check_themes_applied(display_dir):
                messagebox.showwarning(
                    "Warning", 
                    "Themes have already been applied to this firmware. \nPlease use a fresh firmware directory."
                )
                return
        
            theme_path = os.path.join(self.theme_dir, self.theme_var.get())
            with open(theme_path, 'r') as f:
                theme_data = json.load(f)
            
            if self.main_window.patch_svg_files(display_dir, theme_data):
                messagebox.showinfo("Success", "Theme applied successfully!")   
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply theme: {str(e)}")
    
    
    def on_closing(self):
        self.main_window.advanced_mode_var.set(False)
        self.main_window.window.deiconify()
        self.window.destroy() 

class SVGCache:
    def __init__(self):
        self._cache = {}
    
    
    def get_ids(self, svg_path):
        if svg_path in self._cache:
            return self._cache[svg_path]
        return None
    
        
    def store_ids(self, svg_path, ids):
        self._cache[svg_path] = ids
    
        
    def clear(self):
        self._cache.clear()
        
class SVGParser:
    def __init__(self):
        self.id_pattern = re.compile(r'id=["\'](.*?)["\']')
     
        
    def quick_parse(self, content):
        return set(self.id_pattern.findall(content))
     
        
    def validate_ids(self, content, potential_ids):
        try:
            root = ET.fromstring(content)
            valid_ids = set()
            
            for elem in root.iter():
                if 'id' in elem.attrib and elem.attrib['id'] in potential_ids:
                    valid_ids.add(elem.attrib['id'])
                    
            return valid_ids
        except ET.ParseError:
            return potential_ids          
        
#GlitterTE -v1.0