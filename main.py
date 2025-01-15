import os
import customtkinter as ctk
import tkinter as tk
import sys
import json
import subprocess
import op1_analyze
import op1_db
import op1_gfx
import op1_patches
import op1_repack
import svg_normalize
from svg_analyze import analyze_file
from shutil import copyfile
from tkinter import filedialog, messagebox
from PIL import Image


class OP1REpacker:

  
    def __init__(self, master):
        
        
        self.master = master
        self.master.title("OP-1 REpackerGUI")
        self.master.geometry("800x600")
        
        self.repacker = op1_repack.OP1Repack(debug=False)
        self.app_path = os.path.dirname(os.path.realpath(__file__))
        self.db_actions = ['iter', 'filter', 'subtle-fx', 'presets-iter']

        self.create_widgets()
        self.set_icon()
    
    
    #checks platform to use supported icon type     
    def set_icon(self):
        if sys.platform == "win32":
            icon_path = os.path.join(self.app_path, "assets", "op1re_icon.ico")
            if os.path.exists(icon_path):
                self.master.wm_iconbitmap(icon_path)
        else:
            icon_path = os.path.join(self.app_path, "assets", "op1re_icon.png")
            if os.path.exists(icon_path):
                icon = tk.PhotoImage(file=icon_path)
                self.master.iconphoto(True, icon)


    def create_widgets(self):
    
    
         main_frame = ctk.CTkFrame(self.master)
         main_frame.pack(pady=10, padx=10, fill="both", expand=True)


         left_frame = ctk.CTkFrame(main_frame)
         left_frame.pack(side="left", fill="y", padx=(0, 10))

         ctk.CTkLabel(left_frame, text="REpacker", font=("Helvetica", 16, "bold")).pack(pady=(0, 0))
         ctk.CTkLabel(left_frame, text="Firmware tools", font=("Helvetica", 16, "italic")).pack(pady=(0, 0))

         actions = ['unpack', 'modify', 'repack', 'analyze']
         for action in actions:
             button_text = action.replace('_', ' ').title()
             ctk.CTkButton(left_frame, text=button_text, command=lambda a=action: self.perform_action(a)).pack(pady=5)

     
         right_frame = ctk.CTkFrame(main_frame)
         right_frame.pack(side="right", fill="y", padx=(10, 0))

         ctk.CTkLabel(right_frame, text="SVG Tools", font=("Helvetica", 16, "bold")).pack(pady=(0, 25))

         svg_actions = ['normalize_svg', 'analyze_svg']
         for action in svg_actions:
             button_text = action.replace('_', ' ').title()
             ctk.CTkButton(right_frame, text=button_text, command=lambda a=action: self.perform_action(a)).pack(pady=5)
         
         ctk.CTkLabel(right_frame, text="Advanced Tools", font=("Helvetica", 16, "bold")).pack(pady=(120, 10))
         ctk.CTkButton(right_frame, text="Run opie toolkit", command=self.open_toolkit).pack(pady=2)
     
         ctk.CTkButton(right_frame, text="Custom GFX Tips", command=self.show_graphics_tips).pack(side="bottom")

         center_frame = ctk.CTkFrame(main_frame)
         center_frame.pack(side="left", fill="both", expand=True)

         ctk.CTkLabel(center_frame, text="Mods", font=("Helvetica", 16, "bold")).pack(pady=(0, 0))
         ctk.CTkLabel(center_frame, text="Select a mod to enable it then press Modify!", font=("Helvetica", 16, "italic")).pack(pady=(0, 0))

         # add your gfx pack to the list by putting its name under options
         self.option_vars = {}
         options = [
            ('iter', 'Enable "iter" synth'),
            ('presets-iter', 'Add community presets for "iter"'),
            ('filter', 'Enable "filter" effect'),
            ('subtle-fx', 'Make FX defaults less intensive'),
            ('gfx-iter-lab', 'Enable custom lab graphic for iter'),
            ('gfx-cwo-moose', ' Changes CWO graphic from cow to moose'),
            ('gfx-tape-invert', 'Inverts the Tape for better visability'),
            ('gfx-cwo-wizard', 'Changes CWO graphic from cow to a wizard'),
            ('gfx-iter-lostart','Changes "iter" graphic to Phytaxil custom artwork'),
         ]
         for option, description in options:
            var = tk.BooleanVar()
            self.option_vars[option] = var
            frame = ctk.CTkFrame(center_frame)
            frame.pack(fill="x", pady=2)
            ctk.CTkCheckBox(frame, text=option, variable=var).pack(side="left")
            ctk.CTkLabel(frame, text=description, anchor="w").pack(side="left", padx=(10, 0))


         path_frame = ctk.CTkFrame(self.master)
         path_frame.pack(pady=15, padx=10, fill="x")

         self.path_var = tk.StringVar()
         ctk.CTkEntry(path_frame, textvariable=self.path_var, width=630).pack(side="left", padx=(0, 10))
         ctk.CTkButton(path_frame, text="Browse", command=self.browse_path).pack(side="right")   
    
    
    def show_graphics_tips(self):
         tips_window = ctk.CTkToplevel(self.master)
         tips_window.title("SVG Formatting Tips")
         tips_window.geometry("670x870")

         frame = ctk.CTkFrame(tips_window)
         frame.pack(fill="both", expand=True, padx=10, pady=10)

         image_path = os.path.join(self.app_path, "assets", "svg_settings.png")
         if os.path.exists(image_path):
             pil_image = Image.open(image_path)
             ctk_image = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(400, 500))
             image_label = ctk.CTkLabel(frame, image=ctk_image, text="")
             image_label.pack(pady=(0, 10))   


         tips_file_path = os.path.join(self.app_path, "assets", "svg_tips.txt")
         with open(tips_file_path, "r") as file:
            tips_text = file.read()

         text_widget = ctk.CTkTextbox(frame, wrap="word")
         text_widget.pack(fill="both", expand=True)
         text_widget.insert("1.0", tips_text)
         text_widget.configure(state="disabled")     
    
    
    def browse_path(self):
        selection_type = messagebox.askquestion("Selection Type", "Are you selecting an .op-1 or .svg file? \n Select No if picking a directory")
    
        if selection_type == 'yes':
            path = filedialog.askopenfilename(filetypes=[("OP-1 Firmware", "*.op1"), ("SVG Files", "*.svg"), ("All Files", "*.*")])
        else:
            path = filedialog.askdirectory()
        if path:
            self.path_var.set(path)
    
    
    def perform_action(self, action):
        target_path = self.path_var.get()
        if not target_path:
            messagebox.showerror("Error", "Please select a file or directory.")
            return

        if not os.path.exists(target_path):
            messagebox.showerror("Error", f'The specified path "{target_path}" doesn\'t exist!')
            return

        if action == 'analyze':
            self.analyze(target_path)
        elif action == 'repack':
            self.repack(target_path)
        elif action == 'unpack':
            self.unpack(target_path)
        elif action == 'modify':
            self.modify(target_path)
        elif action == 'normalize_svg':
            self.normalize_svg(target_path)
        elif action == 'analyze_svg':
            self.analyze_svg(target_path)
    
    
    def analyze(self, target_path):
        if not os.path.isdir(target_path):
            messagebox.showerror("Error", 'The path to analyze must be a directory! Unpack the firmware file first.')
            return
        
        messagebox.showinfo("Analyzing", f'Analyzing {target_path}...')
        data = op1_analyze.analyze_unpacked_fw(target_path)
        result = ""
        for key, value in data.items():
            label = key.upper().replace('_', ' ')
            result += f'    - {label}: {value}\n'
        messagebox.showinfo("Analysis Result", result)

    
    def repack(self, target_path):
        if not os.path.isdir(target_path):
            messagebox.showerror("Error", 'The path to repack must be a directory!')
            return

        messagebox.showinfo("Repacking", f'Repacking {target_path}...')
        if self.repacker.repack(target_path):
            messagebox.showinfo("Success", 'Repacking completed successfully!')
        else:
            messagebox.showerror("Error", 'Errors occurred during repacking!')

    
    def unpack(self, target_path):
        if not os.path.isfile(target_path):
            messagebox.showerror("Error", 'The path to unpack must be a file!')
            return

        if not target_path.endswith('.op1'):
            messagebox.showerror("Error", 'That doesn\'t seem to be a firmware file. The extension must be ".op1".')
            return

        messagebox.showinfo("Unpacking", f'Unpacking {target_path}...')
        if self.repacker.unpack(target_path):
            messagebox.showinfo("Success", 'Unpacking completed successfully! \n Select the unpacked file in the file browser! \n Select mods then apply by clicking Modify!')
        else:
            messagebox.showerror("Error", 'An error occurred during unpacking!')

    
    def modify(self, target_path):
        if not os.path.isdir(target_path):
            messagebox.showerror("Error", 'Please select the fimrware directory you want to modify')
            return

        options = [opt for opt, var in self.option_vars.items() if var.get()]
        if not options:
            messagebox.showerror("Error", 'Please specify what modifications to make by selecting from the mod list \n Be carefull not to apply mods twice!')
            return

        # Database modifications
        if set(self.db_actions) - (set(self.db_actions) - set(options)):
            db_path = os.path.abspath(os.path.join(target_path, 'content', 'op1_factory.db'))
            db = op1_db.OP1DB()
            db.open(db_path)

            messagebox.showinfo("Modifying", "Running database modifications:")

            if 'iter' in options:
                if db.enable_iter():
                    messagebox.showinfo("Success", 'Enabled "iter" synth.')
                else:
                    messagebox.showwarning("Warning", 'Failed to enable "iter". Maybe it\'s already enabled?')

            if 'presets-iter' in options:
                if not db.synth_preset_folder_exists('iter'):
                    iter_preset_path = os.path.join(self.app_path, 'assets', 'presets', 'iter')
                    patches = op1_patches.load_patch_folder(iter_preset_path)

                    for patch in patches:
                        patch_data = json.dumps(patch)
                        db.insert_synth_preset(patch_data, 'iter')
                    messagebox.showinfo("Success", f'Added {len(patches)} community presets for iter.')
                else:
                    messagebox.showinfo("Info", 'Iter already has presets, not adding new ones.')

            if 'filter' in options:
                if db.enable_filter():
                    messagebox.showinfo("Success", 'Enabled "filter" effect.')
                else:
                    messagebox.showwarning("Warning", 'Failed to enable "filter". Maybe it\'s already enabled?')

            if 'subtle-fx' in options:
                if db.enable_subtle_fx_defaults():
                    messagebox.showinfo("Success", 'Modified FX defaults to be less intensive.')
                else:
                    messagebox.showwarning("Warning", 'Failed to modify default parameters for effects!')

            if not db.commit():
                messagebox.showerror("Error", 'Errors occurred while modifying database!')

        # Custom GFX
        gfx_mods = filter(lambda opt: opt.startswith('gfx-'), options)
        for mod in gfx_mods:
            if mod == 'gfx-iter-lab':
                path_from = os.path.join(self.app_path, 'assets', 'display', 'iter-lab.svg')
                path_to = os.path.abspath(os.path.join(target_path, 'content', 'display', 'iter.svg'))
                copyfile(path_from, path_to)
                messagebox.showinfo("Success", 'Enabled custom lab graphic for iter.')
            elif mod == 'gfx-iter-lostart':
                  path_from = os.path.join(self.app_path, 'assets', 'display', 'iter-lost.svg')
                  path_to = os.path.abspath(os.path.join(target_path, 'content', 'display', 'iter.svg'))
                  copyfile(path_from, path_to)
                  messagebox.showinfo("Success", 'Enabled Phytaxil custom graphic for iter.')
            else:
                patch_name = mod[4:]
                patch_path = os.path.join(self.app_path, 'assets', 'display', patch_name + '.patch.json')
                if not os.path.exists(patch_path):
                    messagebox.showerror("Error", f'GFX patch "{patch_name}" doesn\'t exist!')
                    continue

                result = op1_gfx.patch_image_file(target_path, patch_path)
                if result:
                    messagebox.showinfo("Success", f'Applied GFX patch "{patch_name}".')
                else:
                    messagebox.showwarning("Warning", f'Failed to apply patch "{patch_name}"! Maybe the patch is already applied?')

        messagebox.showinfo("Success", "All modifications completed. \n Please Repack firmware directory")
    
    def analyze_svg(self, target_path):
        if not target_path.lower().endswith('.svg'):
            target_path = filedialog.askopenfilename(filetypes=[("SVG files", "*.svg")])
            if not target_path:
                return

        try:
            result = analyze_file(target_path)
            if result is None:
                messagebox.showerror("Error", "Failed to analyze the SVG file. Check the console for details.")
                return

            analysis_text = f"Tags: {', '.join(result['tags'])}\n\n"
            analysis_text += f"Attributes: {', '.join(result['attributes'])}\n\n"
            analysis_text += f"Transforms: {', '.join(result['transforms'])}\n\n"
            analysis_text += f"Path Commands: {', '.join(result['path_commands'])}"

            messagebox.showinfo("SVG Analysis Result", analysis_text)
        except Exception as e:
            error_msg = f"An error occurred while analyzing the SVG: {str(e)}"
            messagebox.showerror("Error", error_msg)
            print(error_msg)
            import traceback
            print(traceback.format_exc())
    
    def normalize_svg(self, target_path):
        if not target_path.lower().endswith('.svg'):
            target_path = filedialog.askopenfilename(filetypes=[("SVG files", "*.svg")])
            if not target_path:
                return

        try:
            out_path = os.path.splitext(target_path)[0] + "_normalized.svg"
            result = svg_normalize.normalize_svg(target_path, out_path)
            if result:
                messagebox.showinfo("Success", f"SVG normalized successfully. Normalized file saved at: {out_path}")
            else:
                messagebox.showerror("Error", "Failed to normalize the SVG file.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while normalizing the SVG: {str(e)}")
    
    def open_toolkit(self):
        script_path = os.path.join(self.app_path, "opie.py")
        #Allows the user to manually select opie.py if the program can not find it for some reason...
        if not os.path.exists(script_path):
            selected_path = filedialog.askopenfilename(
                title="Select opie.py",
                initialdir=self.app_path,
                filetypes=[("Python files", "*.py")]
            )
        
            if not selected_path:
                messagebox.showwarning("Warning", "opie toolkit not found.\nPlease select the opie.py file.")
                return
        
            self.app_path = os.path.dirname(os.path.abspath(selected_path))
            script_path = selected_path

        try:
            python_executable = sys.executable
            subprocess.run([python_executable, script_path], check=True)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Opie failed to run. Error code: {e.returncode}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    theme_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets", "op1theme.json")
    ctk.set_default_color_theme(theme_path)

    root = ctk.CTk()
    app = OP1REpacker(root)
    root.mainloop()
