import tkinter as tk
from tkinter import colorchooser
import tkinter.font as tkfont
import ctypes
import webbrowser
from screeninfo import get_monitors  # 需先安裝 screeninfo 庫

class MarqueeApp:
    def __init__(self, root):
        """初始化跑馬燈主視窗"""
        self.root = root

        # -------------------------------------------------------
        # 0. 視窗基本設定 (如有需要除錯，可先改為 overrideredirect(False))
        # -------------------------------------------------------
        self.root.title("跑馬燈程式")
        self.root.attributes('-topmost', True)
        self.root.overrideredirect(True)  # 無邊框視窗
        self.root.wm_attributes('-transparentcolor', 'white')
        self.root.configure(bg='white')
        
        # -------------------------------------------------------
        # 1. 主要控制變數
        # -------------------------------------------------------
        self.texts = [
            tk.StringVar(value="阿剛老師的桌面跑馬燈程式，讚!"),
            tk.StringVar(value="阿剛老師的桌面跑馬燈程式，超讚!"),
            tk.StringVar(value="這是預設文字3")
        ]
        self.selected_text = tk.IntVar(value=0)   # 預設選第 1 段文字
        self.speed = tk.IntVar(value=10)         # 跑馬燈移動速度
        self.font_size = tk.IntVar(value=30)     # 文字大小
        self.text_color = "red"                  # 文字顏色預設紅色
        self.bg_enabled = tk.BooleanVar(value=False)
        self.bg_color = None

        # 垂直位置 (相對於所選螢幕的左上角)
        self.y_pos = tk.IntVar(value=0)

        # -------------------------------------------------------
        # 2. 字體清單設定
        # -------------------------------------------------------
        all_fonts = list(tkfont.families())
        # 過濾掉帶有 '@' 的字體，通常是直書字體
        all_fonts = [font for font in all_fonts if '@' not in font]
        # 逆序排序，讓常見字體較容易被選到
        all_fonts.sort(reverse=True)

        self.available_fonts = all_fonts
        self.selected_font = tk.StringVar()
        # 如果系統裡有「標楷體」，就預設用標楷體，否則就選第一個或Helvetica
        if "標楷體" in all_fonts:
            self.selected_font.set("標楷體")
        else:
            self.selected_font.set(all_fonts[0] if all_fonts else "Helvetica")

        # -------------------------------------------------------
        # 3. 建立 Canvas 作為跑馬燈區域 (高度固定為 450)
        # -------------------------------------------------------
        self.canvas = tk.Canvas(
            self.root, 
            bg="white", 
            height=450, 
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # -------------------------------------------------------
        # 4. 建立控制視窗 (Toplevel)
        # -------------------------------------------------------
        self.control_window = tk.Toplevel(self.root)
        self.control_window.title("阿剛老師的桌面跑馬燈程式V2")
        self.control_window.geometry("580x550")  
        self.control_window.configure(bg="#E3F2FD")

        # -------------------------------------------------------
        # 4.1 多螢幕選單
        # -------------------------------------------------------
        self.monitors = get_monitors()
        # 產生易讀名稱
        self.monitor_names = [
            f"螢幕 {i+1} ({m.width}x{m.height} @ {m.x},{m.y})" 
            for i, m in enumerate(self.monitors)
        ]
        self.selected_monitor = tk.StringVar(value=self.monitor_names[0])  # 預設第 1 個螢幕

        monitor_frame = tk.Frame(self.control_window, bg="#E3F2FD")
        monitor_frame.grid(row=0, column=0, columnspan=3, padx=20, pady=10, sticky='ew')

        tk.Label(
            monitor_frame, 
            text="選擇螢幕:", 
            bg="#E3F2FD"
        ).grid(row=0, column=0, padx=5, pady=5, sticky='e')

        monitor_menu = tk.OptionMenu(
            monitor_frame, 
            self.selected_monitor, 
            *self.monitor_names, 
            command=self.change_monitor
        )
        monitor_menu.config(width=30, bg="#E3F2FD", highlightthickness=0)
        monitor_menu.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        # -------------------------------------------------------
        # 4.2 三個文字範本 (單選 + Entry 輸入框)
        # -------------------------------------------------------
        for i in range(3):
            rb = tk.Radiobutton(
                self.control_window,
                variable=self.selected_text,
                value=i,
                command=self.update_text_selection,
                bg="#E3F2FD",
                activebackground="#E3F2FD"
            )
            rb.grid(row=i+1, column=0, padx=(20,5), pady=5, sticky='e')

            tk.Label(
                self.control_window, 
                text=f"文字 {i+1}:", 
                bg="#E3F2FD"
            ).grid(row=i+1, column=1, padx=5, pady=5, sticky='e')

            tk.Entry(
                self.control_window, 
                textvariable=self.texts[i], 
                width=40
            ).grid(row=i+1, column=2, padx=(5,20), pady=5, sticky='w')

        # -------------------------------------------------------
        # 4.3 其他設定區
        # -------------------------------------------------------
        setting_frame = tk.Frame(self.control_window, bg="#F3E5F5")
        setting_frame.grid(row=4, column=0, columnspan=3, padx=20, pady=10, sticky='ew')

        # 字型
        tk.Label(setting_frame, text="字型:", bg="#F3E5F5").grid(
            row=0, column=0, padx=5, pady=5, sticky='e'
        )
        font_menu = tk.OptionMenu(setting_frame, self.selected_font, *self.available_fonts)
        font_menu.config(width=20, bg="#F3E5F5", highlightthickness=0)
        font_menu.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        # 速度
        tk.Label(setting_frame, text="速度:", bg="#F3E5F5").grid(
            row=1, column=0, padx=5, pady=5, sticky='e'
        )
        tk.Scale(
            setting_frame, 
            from_=1, 
            to=20, 
            orient=tk.HORIZONTAL, 
            variable=self.speed,
            bg="#F3E5F5", 
            highlightthickness=0, 
            length=200
        ).grid(row=1, column=1, padx=5, pady=5, sticky='w')

        # 文字大小
        tk.Label(setting_frame, text="文字大小:", bg="#F3E5F5").grid(
            row=2, column=0, padx=5, pady=5, sticky='e'
        )
        tk.Scale(
            setting_frame, 
            from_=10, 
            to=100, 
            orient=tk.HORIZONTAL, 
            variable=self.font_size,
            bg="#F3E5F5", 
            highlightthickness=0, 
            length=200
        ).grid(row=2, column=1, padx=5, pady=5, sticky='w')

        # 選擇文字顏色
        tk.Button(
            setting_frame, 
            text="選擇文字顏色", 
            command=self.choose_color, 
            bg="#F3E5F5"
        ).grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

        # 背景色啟用 & 按鈕
        tk.Checkbutton(
            setting_frame, 
            text="啟用跑馬燈背景色", 
            variable=self.bg_enabled,
            command=self.toggle_bg_color,
            bg="#F3E5F5", 
            activebackground="#F3E5F5"
        ).grid(row=4, column=0, padx=5, pady=5, sticky='e')

        self.bg_color_button = tk.Button(
            setting_frame,
            text="選擇背景顏色",
            command=self.choose_bg_color,
            state='disabled',
            bg="#F3E5F5"
        )
        self.bg_color_button.grid(row=4, column=1, padx=5, pady=5, sticky='w')

        # -------------------------------------------------------
        # 4.4 垂直位置調整
        # -------------------------------------------------------
        pos_frame = tk.Frame(self.control_window, bg="#E3F2FD")
        pos_frame.grid(row=5, column=0, columnspan=3, padx=20, pady=10, sticky='ew')

        tk.Label(pos_frame, text="垂直位置:", bg="#E3F2FD").grid(
            row=0, column=0, padx=5, pady=5, sticky='e'
        )

        tk.Scale(
            pos_frame, 
            from_=-400, 
            to=800, 
            orient=tk.HORIZONTAL, 
            variable=self.y_pos,
            command=self.update_geometry, 
            bg="#E3F2FD", 
            length=400
        ).grid(row=0, column=1, padx=5, pady=5, sticky='w')

        # -------------------------------------------------------
        # 4.5 底部資訊 (Made by...)
        # -------------------------------------------------------
        made_frame = tk.Frame(self.control_window, bg="#E3F2FD")
        made_frame.grid(row=6, column=0, columnspan=3, pady=20, sticky='e')
        made_label = tk.Label(made_frame, text='Made by ', bg="#E3F2FD")
        made_label.pack(side='left')

        link = tk.Label(
            made_frame, 
            text="阿剛老師", 
            fg="blue", 
            cursor="hand2", 
            bg="#E3F2FD", 
            font=(self.selected_font.get(), 10, "underline")
        )
        link.pack(side='left')
        link.bind("<Button-1>", lambda e: webbrowser.open_new("https://kentxchang.blogspot.tw"))

        # -------------------------------------------------------
        # 4.6 視窗關閉時事件
        # -------------------------------------------------------
        self.control_window.protocol("WM_DELETE_WINDOW", self.close_app)

        # -------------------------------------------------------
        # 5. 初始化跑馬燈位置 & 顯示
        # -------------------------------------------------------
        # 先設定幾何位置 (放在所選螢幕上)
        self.update_geometry()

        # x_pos 用於文字跑動 x 座標
        self.x_pos = self.canvas.winfo_width()
        # 啟動跑馬燈動畫
        self.animate_text()

    # ----------------------------------------------------------------
    # A. 螢幕 & 視窗幾何位置控制
    # ----------------------------------------------------------------
    def change_monitor(self, selection):
        """當使用者改選不同螢幕時，更新視窗幾何位置。"""
        self.update_geometry()

    def update_geometry(self, event=None):
        """根據 selected_monitor 與 y_pos，更新主視窗位置。"""
        # 找到當前選擇的螢幕資訊
        index = self.monitor_names.index(self.selected_monitor.get())
        monitor = self.monitors[index]
        width = monitor.width
        height = 450  # 跑馬燈視窗固定高度

        # 垂直位置 (相對於選擇螢幕的左上角)
        y_offset = self.y_pos.get()  
        # 視窗的左上角絕對位置 (monitor.x, monitor.y)
        final_y = monitor.y + y_offset
        final_x = monitor.x

        # 設定主視窗幾何大小與位置
        self.root.geometry(f"{width}x{height}+{final_x}+{final_y}")

    # ----------------------------------------------------------------
    # B. 動畫核心: 跑馬燈移動
    # ----------------------------------------------------------------
    def animate_text(self):
        # 每次刷新都要先清空 Canvas
        self.canvas.delete("all")

        # 取得文字與字體樣式
        font_family = self.selected_font.get()
        font_size = self.font_size.get()
        font_style = (font_family, font_size, "bold")
        current_text = self.texts[self.selected_text.get()].get()

        # 先繪製一次文字 (temp) 以取得其 bbox（文字寬高）
        temp_id = self.canvas.create_text(
            self.x_pos, 225, 
            text=current_text, 
            fill=self.text_color, 
            font=font_style, 
            anchor='w'
        )
        text_bbox = self.canvas.bbox(temp_id)
        self.canvas.delete(temp_id)

        # 若有啟用背景色，先畫一個 rectangle 當底色
        if self.bg_enabled.get() and self.bg_color:
            if text_bbox:
                x1, y1, x2, y2 = text_bbox
                padding = 5
                # 在文字高度範圍內，整段填上背景
                self.canvas.create_rectangle(
                    0, 
                    y1 - padding,
                    self.canvas.winfo_width(), 
                    y2 + padding,
                    fill=self.bg_color, 
                    outline=''
                )

        # 再次繪製文字（這次是最終要顯示的）
        text_id = self.canvas.create_text(
            self.x_pos, 225,
            text=current_text, 
            fill=self.text_color, 
            font=font_style, 
            anchor='w'
        )

        # 讓文字往左移
        self.x_pos -= self.speed.get()

        # 如果文字整段左邊已經跑出畫布，就重置 x_pos 到畫布右邊
        if text_bbox:
            text_width = text_bbox[2] - text_bbox[0]
            if self.x_pos < -text_width:
                # 重置，回到畫布最右側
                self.x_pos = self.canvas.winfo_width()

        # 50 毫秒後再執行一次動畫
        self.canvas.after(50, self.animate_text)

    # ----------------------------------------------------------------
    # C. 文字 / 顏色 / 背景色 控制
    # ----------------------------------------------------------------
    def update_text_selection(self):
        """當使用者改選不同文字範本時，重置 x_pos 讓文字從右側重新開始。"""
        self.x_pos = self.canvas.winfo_width()

    def choose_color(self):
        """使用系統內建 colorchooser 選文字顏色。"""
        color_code = colorchooser.askcolor(title="選擇文字顏色")[1]
        if color_code:
            self.text_color = color_code

    def toggle_bg_color(self):
        """開/關 背景色選擇。"""
        if self.bg_enabled.get():
            self.bg_color_button.config(state='normal')
            if not self.bg_color:
                self.bg_color = "black"
        else:
            self.bg_color_button.config(state='disabled')
            self.bg_color = None

    def choose_bg_color(self):
        """使用系統內建 colorchooser 選背景顏色。"""
        color_code = colorchooser.askcolor(title="選擇背景顏色")[1]
        if color_code:
            self.bg_color = color_code

    # ----------------------------------------------------------------
    # D. 關閉程式
    # ----------------------------------------------------------------
    def close_app(self):
        self.root.destroy()

# --------------------------------------------------------------------
# 主程式入口
# --------------------------------------------------------------------
if __name__ == "__main__":
    # 1. 建立主視窗
    root = tk.Tk()
    # 2. 建立跑馬燈應用 (MarqueeApp)
    app = MarqueeApp(root)
    # 3. 進入事件循環
    root.mainloop()
