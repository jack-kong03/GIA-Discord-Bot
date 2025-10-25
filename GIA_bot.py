import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
from datetime import datetime
from dotenv import load_dotenv
import os
import requests

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

# === BOT SETUP ===
intents = discord.Intents.default()
intents.message_content = True  # Needed for reading messages

bot = commands.Bot(command_prefix="!", intents=intents)
scheduler = AsyncIOScheduler()

# === CORE FUNCTIONS ===

async def send_message(channel, message):
    """Helper to send a message safely."""
    try:
        await channel.send(message)
    except Exception as e:
        print(f"Error sending message: {e}")

async def send_embed_message(channel, title, description):
    embed = discord.Embed(
        title=title,
        description=description,
        color=0x00bfff
    )
    embed.set_footer(text="Guided by GIA 🕒")
    try:
        await channel.send(embed=embed)
    except Exception as e:
        print(f"Error sending embed message: {e}")

async def send_daily_checkin(channel):
    """Morning daily goal check-in."""
    await send_message(channel, "🌅 Good morning! What **3 things** do you want to do today? (Please reply with them, one per line.)")

    def check(m):
        return m.author != bot.user and m.channel == channel

    try:
        msg = await bot.wait_for("message", check=check, timeout=600.0)
        goals = msg.content.split("\n")

        with open("daily_goals.txt", "a") as f:
            f.write(f"\n[{datetime.now().strftime('%Y-%m-%d')}] {msg.author.name}: {', '.join(goals)}")

        await send_message(channel, "✅ Got it! I’ve noted down your 3 goals for today:")
        for g in goals:
            await send_message(channel, f"• {g}")

        await send_message(channel, "💪 Let's make today productive!")

    except asyncio.TimeoutError:
        await send_message(channel, "⏰ You didn’t reply in time — you can always type `!checkin` later!")

async def send_morning_routine(channel):
    await send_embed_message(channel, "🌅 Morning Routine", "Start your day with a positive mindset and set your intentions.")

async def send_focus_session_1(channel):
    await send_embed_message(channel, "💻 Focus Session 1", "Deep work time — tackle your most important tasks.")

async def send_lunch_break(channel):
    await send_embed_message(channel, "🍽️ Lunch Break", "Take a well-deserved break and refuel.")

async def send_focus_session_2(channel):
    await send_embed_message(channel, "💻 Focus Session 2", "Continue your productive work — keep the momentum going.")

async def send_gym_prep(channel):
    await send_embed_message(channel, "🏋️‍♂️ Gym Prep", "Get ready for your workout — hydrate and warm up.")

async def send_gym_session(channel):
    await send_embed_message(channel, "💪 Gym Session", "Time to get moving and strengthen your body.")

async def send_evening_routine(channel):
    await send_embed_message(channel, "🌇 Evening Routine", "Wind down your work and prepare for the evening.")

async def send_focus_session_3(channel):
    await send_embed_message(channel, "💻 Focus Session 3", "Final focused work session — wrap up tasks or plan ahead.")

async def send_dinner_break(channel):
    await send_embed_message(channel, "🍽️ Dinner Break", "Enjoy a relaxing dinner and recharge.")

async def send_night_gym_option(channel):
    await send_embed_message(channel, "🏃‍♂️ Night Gym Option", "If you feel up to it, a light workout or stretch before bed.")

async def send_relax_session(channel):
    await send_embed_message(channel, "🎮 Relax Session", "Time to chill and unwind — enjoy your evening.")

async def send_bed_prep(channel):
    await send_embed_message(channel, "🛏️ Bed Prep", "Prepare for sleep — reduce screen time and relax.")

async def send_sleep_reminder(channel):
    await send_embed_message(channel, "😴 Sleep Reminder", "It's late — consider getting some rest for a fresh tomorrow.")

async def send_weekend_morning(channel):
    await send_embed_message(channel, "☀️ Weekend Morning", "Take it easy and enjoy a leisurely start.")

async def send_weekend_project(channel):
    await send_embed_message(channel, "📚 Weekend Project", "Spend some time on personal projects or hobbies.")

async def send_weekend_gym(channel):
    await send_embed_message(channel, "🏋️‍♀️ Weekend Gym", "Keep active with a fun workout session.")

async def send_weekend_relax(channel):
    await send_embed_message(channel, "🛋️ Weekend Relax", "Rest and recharge — enjoy your weekend downtime.")

async def send_good_morning_message(channel):
    await send_embed_message(channel, "🌞 Good morning!", "Wishing you a productive and positive day ahead!")

# === BOT EVENTS ===

@bot.event
async def on_ready():
    print(f"{bot.user} is online and scheduling tasks.")
    channel = bot.get_channel(CHANNEL_ID)
    await send_message(channel, "👋 GIA is online and ready to guide your day!")

    # Only start the scheduler once
    if not scheduler.running:
        # Weekday jobs (Monday=0 to Friday=4)
        scheduler.add_job(send_good_morning_message, "cron", day_of_week="0-4", hour=10, minute=0, args=[channel])
        scheduler.add_job(send_daily_checkin, "cron", day_of_week="0-4", hour=10, minute=30, args=[channel])
        scheduler.add_job(send_focus_session_1, "cron", day_of_week="0-4", hour=11, minute=0, args=[channel])
        scheduler.add_job(send_lunch_break, "cron", day_of_week="0-4", hour=12, minute=30, args=[channel])
        scheduler.add_job(send_focus_session_2, "cron", day_of_week="0-4", hour=13, minute=0, args=[channel])
        scheduler.add_job(send_gym_prep, "cron", day_of_week="0-4", hour=15, minute=30, args=[channel])
        scheduler.add_job(send_gym_session, "cron", day_of_week="0-4", hour=16, minute=0, args=[channel])
        scheduler.add_job(send_evening_routine, "cron", day_of_week="0-4", hour=17, minute=0, args=[channel])
        scheduler.add_job(send_focus_session_3, "cron", day_of_week="0-4", hour=18, minute=0, args=[channel])
        scheduler.add_job(send_dinner_break, "cron", day_of_week="0-4", hour=20, minute=0, args=[channel])
        scheduler.add_job(send_night_gym_option, "cron", day_of_week="0-4", hour=21, minute=0, args=[channel])
        scheduler.add_job(send_relax_session, "cron", day_of_week="0-4", hour=22, minute=30, args=[channel])
        scheduler.add_job(send_bed_prep, "cron", day_of_week="0-4", hour=0, minute=30, args=[channel])
        scheduler.add_job(send_sleep_reminder, "cron", day_of_week="0-4", hour=2, minute=0, args=[channel])

        # Weekend jobs (Saturday=5 to Sunday=6)
        scheduler.add_job(send_weekend_morning, "cron", day_of_week="5-6", hour=10, minute=0, args=[channel])
        scheduler.add_job(send_weekend_project, "cron", day_of_week="5-6", hour=13, minute=0, args=[channel])
        scheduler.add_job(send_weekend_gym, "cron", day_of_week="5-6", hour=17, minute=0, args=[channel])
        scheduler.add_job(send_weekend_relax, "cron", day_of_week="5-6", hour=19, minute=0, args=[channel])

        scheduler.start()
        print("Scheduler started.")
    else:
        print("Scheduler already running — skipping start.")

# === COMMANDS ===

@bot.command(name="checkin")
async def manual_checkin(ctx):
    """Manual trigger for daily check-in."""
    await send_daily_checkin(ctx.channel)

@bot.command(name="schedule")
async def show_schedule(ctx):
    """Shows your current daily routine."""
    schedule_text = (
        "🗓️ **Weekday Routine (Mon–Fri)**\n"
        "10:00 AM — Good Morning Message\n"
        "10:30 AM — Daily Check-In\n"
        "11:00 AM — Focus Session 1\n"
        "12:30 PM — Lunch Break\n"
        "1:00 PM — Focus Session 2\n"
        "3:30 PM — Gym Prep\n"
        "4:00 PM — Gym Session\n"
        "5:00 PM — Evening Routine\n"
        "6:00 PM — Focus Session 3\n"
        "8:00 PM — Dinner Break\n"
        "9:00 PM — Night Gym Option\n"
        "10:30 PM — Relax Session\n"
        "12:30 AM — Bed Prep\n"
        "2:00 AM — Sleep Reminder\n\n"
        "🗓️ **Weekend Routine (Sat–Sun)**\n"
        "10:00 AM — Weekend Morning\n"
        "1:00 PM — Weekend Project\n"
        "5:00 PM — Weekend Gym\n"
        "7:00 PM — Weekend Relax\n"
    )
    await ctx.send(schedule_text)

@bot.command(name="motivate")
async def motivate(ctx):
    """GIA sends a motivational quote from ZenQuotes API (with a nice embed)."""
    try:
        response = requests.get("https://zenquotes.io/api/random")
        response.raise_for_status()
        data = response.json()[0]
        quote = data["q"]
        author = data["a"]

        # Create the embed
        embed = discord.Embed(
            title="🌟 Motivation",
            description=f"\"{quote}\"",
            color=0x00ffcc
        )
        embed.set_footer(text=f"— {author}")

        await ctx.send(embed=embed)

    except Exception as e:
        print(f"Error fetching quote: {e}")
        await ctx.send("⚠️ Sorry, I couldn't fetch a motivational quote right now. Try again later!")

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send("🏓 Pong! GIA is online and responsive.")

@bot.command(name="commands")
async def commands(ctx):
    commands_text = (
        "**🧠 GIA Commands**\n"
        "`!checkin` — Start your daily check-in.\n"
        "`!schedule` — Show your full daily routine.\n"
        "`!motivate` — Get a motivational quote.\n"
        "`!ping` — Check if GIA is online.\n"
        "`!commands` — Show this help message."
    )
    await ctx.send(commands_text)

# === RUN BOT ===
bot.run(TOKEN)