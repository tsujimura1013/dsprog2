import flet as ft
import math


# -----------------------------
# ボタンクラス
# -----------------------------
class CalcButton(ft.ElevatedButton):
    def __init__(self, text, button_clicked, expand=1):
        super().__init__()
        self.text = text
        self.expand = expand
        self.on_click = button_clicked
        self.data = text


class DigitButton(CalcButton):
    def __init__(self, text, button_clicked, expand=1):
        super().__init__(text, button_clicked, expand)
        self.bgcolor = ft.Colors.WHITE24
        self.color = ft.Colors.WHITE


class ActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        super().__init__(text, button_clicked)
        self.bgcolor = ft.Colors.ORANGE
        self.color = ft.Colors.WHITE


class ExtraActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        super().__init__(text, button_clicked)
        self.bgcolor = ft.Colors.BLUE_GREY_100
        self.color = ft.Colors.BLACK


class SciButton(CalcButton):
    def __init__(self, text, button_clicked):
        super().__init__(text, button_clicked)
        self.bgcolor = ft.Colors.BLUE_400
        self.color = ft.Colors.WHITE


# -----------------------------
# 電卓本体
# -----------------------------
class CalculatorApp(ft.Container):
    def __init__(self):
        super().__init__()
        self.reset()

        self.result = ft.Text(value="0", color=ft.Colors.WHITE, size=24)

        self.width = 360
        self.bgcolor = ft.Colors.BLACK
        self.border_radius = ft.border_radius.all(20)
        self.padding = 20

        self.content = ft.Column(
            controls=[
                ft.Row(controls=[self.result], alignment="end"),

                # 科学計算ボタン
                ft.Row(
                    controls=[
                        SciButton("sin", self.button_clicked),
                        SciButton("cos", self.button_clicked),
                        SciButton("tan", self.button_clicked),
                        SciButton("√", self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        SciButton("x²", self.button_clicked),
                        SciButton("log", self.button_clicked),
                        SciButton("π", self.button_clicked),
                    ]
                ),

                # 通常電卓
                ft.Row(
                    controls=[
                        ExtraActionButton("AC", self.button_clicked),
                        ExtraActionButton("+/-", self.button_clicked),
                        ExtraActionButton("%", self.button_clicked),
                        ActionButton("/", self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton("7", self.button_clicked),
                        DigitButton("8", self.button_clicked),
                        DigitButton("9", self.button_clicked),
                        ActionButton("*", self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton("4", self.button_clicked),
                        DigitButton("5", self.button_clicked),
                        DigitButton("6", self.button_clicked),
                        ActionButton("-", self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton("1", self.button_clicked),
                        DigitButton("2", self.button_clicked),
                        DigitButton("3", self.button_clicked),
                        ActionButton("+", self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton("0", self.button_clicked, expand=2),
                        DigitButton(".", self.button_clicked),
                        ActionButton("=", self.button_clicked),
                    ]
                ),
            ]
        )

    # -----------------------------
    # ボタン処理
    # -----------------------------
    def button_clicked(self, e):
        data = e.control.data

        if self.result.value == "Error" or data == "AC":
            self.result.value = "0"
            self.reset()

        elif data.isdigit() or data == ".":
            if self.result.value == "0" or self.new_operand:
                self.result.value = data
                self.new_operand = False
            else:
                self.result.value += data

        elif data in ("+", "-", "*", "/"):
            self.result.value = self.calculate(
                self.operand1, float(self.result.value), self.operator
            )
            self.operator = data
            self.operand1 = 0 if self.result.value == "Error" else float(self.result.value)
            self.new_operand = True

        elif data == "=":
            self.result.value = self.calculate(
                self.operand1, float(self.result.value), self.operator
            )
            self.reset()

        elif data == "%":
            self.result.value = self.format_number(float(self.result.value) / 100)
            self.reset()

        elif data == "+/-":
            val = float(self.result.value)
            self.result.value = self.format_number(-val)

        # ---- 科学計算 ----
        elif data == "sin":
            self.result.value = self.format_number(
                math.sin(math.radians(float(self.result.value)))
            )
            self.reset()

        elif data == "cos":
            self.result.value = self.format_number(
                math.cos(math.radians(float(self.result.value)))
            )
            self.reset()

        elif data == "tan":
            self.result.value = self.format_number(
                math.tan(math.radians(float(self.result.value)))
            )
            self.reset()

        elif data == "√":
            v = float(self.result.value)
            self.result.value = "Error" if v < 0 else self.format_number(math.sqrt(v))
            self.reset()

        elif data == "x²":
            self.result.value = self.format_number(float(self.result.value) ** 2)
            self.reset()

        elif data == "log":
            v = float(self.result.value)
            self.result.value = "Error" if v <= 0 else self.format_number(math.log10(v))
            self.reset()

        elif data == "π":
            self.result.value = str(math.pi)
            self.new_operand = True

        self.update()

    # -----------------------------
    # 計算処理
    # -----------------------------
    def calculate(self, op1, op2, operator):
        try:
            if operator == "+":
                return self.format_number(op1 + op2)
            if operator == "-":
                return self.format_number(op1 - op2)
            if operator == "*":
                return self.format_number(op1 * op2)
            if operator == "/":
                return "Error" if op2 == 0 else self.format_number(op1 / op2)
        except:
            return "Error"

    def format_number(self, num):
        return int(num) if num % 1 == 0 else num

    def reset(self):
        self.operator = "+"
        self.operand1 = 0
        self.new_operand = True


# -----------------------------
# 起動
# -----------------------------
def main(page: ft.Page):
    page.title = "Scientific Calculator"
    page.add(CalculatorApp())


ft.app(main)
