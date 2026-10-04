# Pomodoro Timer
# Manage Focused work sessions with Automatic short and long breaks.

# 1. Set Timer Durations      ===>>> 25 minutes focus, 5 minutes short break, 15 minutes long break.
# 2. Enter Number of Sessions ===>>> Specify how many focus sessions you want to complete (e.g. 3, 4, 5, etc.).
# 3. Automatic Breaks         ===>>> Runs a 5-minute short break between sessions and a 15-minute long break after every 4th session when more sessions remain.
# 4. Stay Focused             ===>>> Helps you manage time, improve productivity and maintain focus during work or study.

import time

WORK = 25 * 60 # 25 x 60 = 1500
SHORT_BREAK = 5 * 60 # 5 x 60 = 300
LONG_BREAK = 15 * 60 # 15 x 60 = 900

def countdown(seconds, label):
    print(f"\n{label}")

    while seconds > 0: # greater than 0 not less than -1
        minutes, secs = divmod(seconds, 60)
        print(f"{minutes:02d}:{secs:02d}", end=" ")
        time.sleep(1)
        seconds -= 1
    print("\n Time's Up !!! ")

def get_valid_sessions():
    while True:
        try:
            sessions = int(input("Enter number of focus sessions : "))
            if sessions <= 0:
                print("Please enter a number greater than 0.")
                continue
            return sessions
        except ValueError:
            print("Invalid input. please enter a number.")

def pomodoro_timer(sessions):
    print("\n" + "=" * 50)
    print("         POMODORO TIMER")
    print("=" * 50)

    for session in range(1, sessions + 1):
        print(f"\n Session {session}/{sessions}")
        countdown(WORK, "Focus time - stay productive !")

        if session < sessions:
            if session % 4 == 0:
                countdown(LONG_BREAK, "Long break - relax !!!")
            else:
                countdown(SHORT_BREAK, "Short break - recharge !!!")

    print("\n All sessions completed !!!")
    print("=" * 50)

if __name__ == "__main__":
    total_sessions = get_valid_sessions()
    pomodoro_timer(total_sessions)
