import turtle
import random

WORDS = [
    "python", "turtle", "programming", "hangman", "keyboard",
    "computer", "algorithm", "variable", "function", "library",
    "elephant", "dolphin", "volcano", "gravity", "mystery",
    "journey", "crystal", "lantern", "sunrise", "thunder",
    "blanket", "fashion", "diamond", "cabinet", "network",
]

#  Colours & Fonts

BG_COLOR       = "#1a1a2e"
GALLOWS_COLOR  = "#e0e0e0"
MAN_COLOR      = "#ff6b6b"
LETTER_COLOR   = "#4ecdc4"
GUESSED_COLOR  = "#a8dadc"
WIN_COLOR      = "#06d6a0"
LOSE_COLOR     = "#ef476f"
HINT_COLOR     = "#ffd166"

TITLE_FONT  = ("Courier New", 26, "bold")
WORD_FONT   = ("Courier New", 28, "bold")
INFO_FONT   = ("Courier New", 14, "normal")
ALPHA_FONT  = ("Courier New", 18, "bold")
MSG_FONT    = ("Courier New", 22, "bold")

MAX_WRONG   = 6          # head, body, left arm, right arm, left leg, right leg

#  Helper – invisible turtle writer

def make_writer():
    t = turtle.Turtle()
    t.hideturtle()
    t.penup()
    t.speed(0)
    return t

#  Drawing: gallows

def draw_gallows(draw):
    draw.pensize(4)
    draw.color(GALLOWS_COLOR)
    # Base  (shifted -220 in total)
    draw.penup();  draw.goto(-600, -220); draw.pendown()
    draw.goto(-360, -220)
    # Pole
    draw.goto(-480, -220); draw.goto(-480,  180)
    # Top bar
    draw.goto(-360,  180)
    # Rope
    draw.goto(-360,  130)

#  Drawing: hangman parts

def draw_head(draw):
    draw.penup(); draw.goto(-360, 70); draw.pendown()
    draw.color(MAN_COLOR); draw.pensize(3)
    draw.circle(40, steps=40)           # head

def draw_body(draw):
    draw.penup(); draw.goto(-360, 70); draw.pendown()
    draw.color(MAN_COLOR); draw.pensize(3)
    draw.goto(-360, -60)

def draw_left_arm(draw):
    draw.penup(); draw.goto(-360, 30); draw.pendown()
    draw.color(MAN_COLOR); draw.pensize(3)
    draw.goto(-430, -30)

def draw_right_arm(draw):
    draw.penup(); draw.goto(-360, 30); draw.pendown()
    draw.color(MAN_COLOR); draw.pensize(3)
    draw.goto(-290, -30)

def draw_left_leg(draw):
    draw.penup(); draw.goto(-360, -60); draw.pendown()
    draw.color(MAN_COLOR); draw.pensize(3)
    draw.goto(-430, -150)

def draw_right_leg(draw):
    draw.penup(); draw.goto(-360, -60); draw.pendown()
    draw.color(MAN_COLOR); draw.pensize(3)
    draw.goto(-290, -150)

# Adjusted head so it sits on the rope properly
def draw_head_fixed(draw):
    draw.penup()
    draw.goto(-360, 130)         # top of rope
    draw.pendown()
    draw.color(MAN_COLOR); draw.pensize(3)
    # draw circle: go to centre then draw
    draw.penup()
    draw.goto(-360, 70)          # centre
    draw.pendown()
    draw.circle(30, steps=36)   # r=30 → head sits nicely

BODY_PARTS = [
    draw_head_fixed,
    draw_body,
    draw_left_arm,
    draw_right_arm,
    draw_left_leg,
    draw_right_leg,
]

# ─────────────────────────────────────────
#  Game State
# ─────────────────────────────────────────
class HangmanGame:
    def __init__(self):
        self.word           = random.choice(WORDS).upper()
        self.guessed        = set()
        self.wrong_count    = 0
        self.game_over      = False

    @property
    def revealed(self):
        return [ch if ch in self.guessed else "_" for ch in self.word]

    @property
    def word_complete(self):
        return all(ch in self.guessed for ch in self.word)

# ─────────────────────────────────────────
#  Main Application
# ─────────────────────────────────────────
class HangmanApp:
    def __init__(self):
        # ── Screen ──────────────────────────────
        self.screen = turtle.Screen()
        self.screen.title("🎮  Hangman  •  Python Turtle Edition")
        self.screen.bgcolor(BG_COLOR)
        self.screen.setup(width=820, height=620)
        self.screen.tracer(0)

        # ── Turtles ─────────────────────────────
        self.draw       = turtle.Turtle()   # gallows + man
        self.draw.hideturtle()
        self.draw.speed(0)
        self.draw.penup()

        self.title_t    = make_writer()
        self.word_t     = make_writer()
        self.alpha_t    = make_writer()
        self.info_t     = make_writer()
        self.msg_t      = make_writer()

        # ── Game ────────────────────────────────
        self.game = HangmanGame()
        self._setup_ui()
        self._bind_keys()
        self.screen.update()

        self.screen.mainloop()

    # ── Initial UI ──────────────────────────────────────────────────────────
    def _setup_ui(self):
        self._draw_title()
        draw_gallows(self.draw)
        self._draw_word()
        self._draw_alphabet()
        self._draw_info()
        self.screen.update()

    def _draw_title(self):
        self.title_t.clear()
        self.title_t.color(HINT_COLOR)
        self.title_t.goto(0, 270)
        self.title_t.write("✦  H A N G M A N  ✦", align="center", font=TITLE_FONT)

    def _draw_word(self):
        self.word_t.clear()
        self.word_t.color(LETTER_COLOR)
        self.word_t.goto(265, -100)
        display = "  ".join(self.game.revealed)
        self.word_t.write(display, align="center", font=WORD_FONT)

    def _draw_alphabet(self):
        self.alpha_t.clear()
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        start_x, start_y = 100, 200
        col_w, row_h     = 55, 45
        cols             = 7

        for i, ch in enumerate(letters):
            col = i % cols
            row = i // cols
            x   = start_x + col * col_w
            y   = start_y - row * row_h

            if ch in self.game.guessed:
                color = GUESSED_COLOR if ch in self.game.word else "#555577"
            else:
                color = "#cccccc"

            self.alpha_t.color(color)
            self.alpha_t.goto(x, y)
            self.alpha_t.write(ch, align="center", font=ALPHA_FONT)

    def _draw_info(self):
        self.info_t.clear()
        remaining = MAX_WRONG - self.game.wrong_count
        self.info_t.color(HINT_COLOR)
        self.info_t.goto(265, -160)
        self.info_t.write(
            f"Wrong: {self.game.wrong_count}/{MAX_WRONG}   |   Remaining Attempts: {remaining}",
            align="center", font=INFO_FONT
        )
        # Category hint
        self.info_t.goto(265, 230)
        self.info_t.color("#888888")
        self.info_t.write("Press a letter key to guess  •  Press Space to restart",
                          align="center", font=("Courier New", 11, "normal"))

    # ── Key Bindings ────────────────────────────────────────────────────────
    def _bind_keys(self):
        self.screen.listen()
        for ch in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
            self.screen.onkey(lambda c=ch.upper(): self._guess(c), ch)
        self.screen.onkey(self._restart, "space")

    # ── Guess Logic ─────────────────────────────────────────────────────────
    def _guess(self, letter):
        if self.game.game_over:
            return
        if letter in self.game.guessed:
            return

        self.game.guessed.add(letter)

        if letter not in self.game.word:
            self.game.wrong_count += 1
            # Draw corresponding body part
            part_fn = BODY_PARTS[self.game.wrong_count - 1]
            part_fn(self.draw)

        self._draw_word()
        self._draw_alphabet()
        self._draw_info()

        if self.game.word_complete:
            self._end_game(won=True)
        elif self.game.wrong_count >= MAX_WRONG:
            self._end_game(won=False)

        self.screen.update()

    # ── End State ───────────────────────────────────────────────────────────
    def _end_game(self, won):
        self.game.game_over = True
        self.msg_t.clear()

        if won:
            self.msg_t.color(WIN_COLOR)
            self.msg_t.goto(265, -210)
            self.msg_t.write("🎉  YOU WON!  Great job!", align="center", font=MSG_FONT)
        else:
            # Reveal word
            self.word_t.clear()
            self.word_t.color(LOSE_COLOR)
            self.word_t.goto(265, -100)
            self.word_t.write("  ".join(self.game.word), align="center", font=WORD_FONT)

            self.msg_t.color(LOSE_COLOR)
            self.msg_t.goto(265, -210)
            self.msg_t.write(f"💀  GAME OVER  •  Word: {self.game.word}", align="center", font=MSG_FONT)

        # Restart prompt
        self.msg_t.color("#aaaaaa")
        self.msg_t.goto(265, -250)
        self.msg_t.write("Press SPACE to play again", align="center",
                         font=("Courier New", 13, "italic"))
        self.screen.update()

    # ── Restart ─────────────────────────────────────────────────────────────
    def _restart(self):
        # Clear all drawings
        self.draw.clear()
        self.title_t.clear()
        self.word_t.clear()
        self.alpha_t.clear()
        self.info_t.clear()
        self.msg_t.clear()

        # New game
        self.game = HangmanGame()
        self._setup_ui()


# ─────────────────────────────────────────
#  Entry Point
# ─────────────────────────────────────────
if __name__ == "__main__":
    HangmanApp()