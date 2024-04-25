import os
import re
import telethon
from telethon import TelegramClient, events, Button
from imdb import Cinemagoer
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from re import IGNORECASE
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram.filters import command, regex
from pyrogram.errors import MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
import os
import tgcrypto
import asyncio
from dotenv import load_dotenv


load_dotenv()
api_id = int(os.getenv("api_id"))
api_hash = os.getenv("api_hash")
bot_token = os.getenv("bot_token")

imdb = Cinemagoer()

app = TelegramClient('imdbbot', api_id, api_hash).start(bot_token=bot_token)

@app.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond(f"Hi! I Am IMDB Bot. Send movie/Series Naame After /imdb")
    raise events.StopPropagation
  
@app.on(events.NewMessage(pattern='/imdb'))  # Decorator for command handling
async def imdb_search(event: events.NewMessage.Event):
    if ' ' in event.message.message:  # Access message text
        k = await event.respond('<code>Searching IMDB ...</code>')
        title = event.message.message.split(' ', 1)[1]
        user_id = event.sender_id  
        buttons = ButtonMaker()
        if title.lower().startswith("https://www.imdb.com/title/tt"):
            movieid = title.replace("https://www.imdb.com/title/tt", "")
            if movie := imdb.get_movie(movieid):
                buttons.ibutton(f"🎬 {movie.get('title')} ({movie.get('year')})", f"imdb {user_id} movie {movieid}")
            else:
                return await editMessage(k, "<i>No Results Found</i>")
        else:
            movies = get_poster(title, bulk=True)
            if not movies:
                return editMessage("<i>No Results Found</i>, Try Again or Use <b>Title ID</b>", k)
            for movie in movies: # Refurbished Soon !!
                buttons.ibutton(f"🎬 {movie.get('title')} ({movie.get('year')})", f"imdb {user_id} movie {movie.movieID}")
        buttons.ibutton("🚫 Close 🚫", f"imdb {user_id} close")
        await editMessage(k, '<b><i>Here What I found on IMDb.com</i></b>', buttons.build_menu(1))
    else:
         await event.respond('Send Movie / TV Series Name along with /imdb Command or send IMDB URL')


IMDB_GENRE_EMOJI = {"Action": "🚀", "Adult": "🔞", "Adventure": "🌋", "Animation": "🎠", "Biography": "📜", "Comedy": "🪗", "Crime": "🔪", "Documentary": "🎞", "Drama": "🎭", "Family": "👨‍👩‍👧‍👦", "Fantasy": "🫧", "Film Noir": "🎯", "Game Show": "🎮", "History": "🏛", "Horror": "🧟", "Musical": "🎻", "Music": "🎸", "Mystery": "🧳", "News": "📰", "Reality-TV": "🖥", "Romance": "🥰", "Sci-Fi": "🌠", "Short": "📝", "Sport": "⛳", "Talk-Show": "👨‍🍳", "Thriller": "🗡", "War": "⚔", "Western": "🪩"}
                    
LIST_ITEMS = 4 

def get_poster(query, bulk=False, id=False, file=None):
  if not id:
      query = (query.strip()).lower()
      title = query
      year = findall(r'[1-2]\d{3}$', query, IGNORECASE)
      if year:
          year = list_to_str(year[:1])
          title = (query.replace(year, "")).strip()
      elif file is not None:
          year = findall(r'[1-2]\d{3}', file, IGNORECASE)
          if year:
              year = list_to_str(year[:1]) 
      else:
          year = None
      movieid = imdb.search_movie(title.lower(), results=10)
      if not movieid:
          return None
      if year:
          filtered = list(filter(lambda k: str(k.get('year')) == str(year), movieid)) or movieid
      else:
          filtered = movieid
      movieid = list(filter(lambda k: k.get('kind') in ['movie', 'tv series'], filtered)) or filtered
      if bulk:
          return movieid
      movieid = movieid[0].movieID
  else:
      movieid = query
  movie = imdb.get_movie(movieid)
  if movie.get("original air date"):
      date = movie["original air date"]
  elif movie.get("year"):
      date = movie.get("year")
  else:
      date = "N/A"
  plot = movie.get('plot')
  plot = plot[0] if plot and len(plot) > 0 else movie.get('plot outline')
  if plot and len(plot) > 300:
      plot = f"{plot[:300]}..."
  return {
      'title': movie.get('title'),
      'trailer': movie.get('videos'),
      'votes': movie.get('votes'),
      "aka": list_to_str(movie.get("akas")),
      "seasons": movie.get("number of seasons"),
      "box_office": movie.get('box office'),
      'localized_title': movie.get('localized title'),
      'kind': movie.get("kind"),
      "imdb_id": f"tt{movie.get('imdbID')}",
      "cast": list_to_str(movie.get("cast")),
      "runtime": list_to_str([get_readable_time(int(run) * 60) for run in movie.get("runtimes", "0")]),
      "countries": list_to_hash(movie.get("countries"), True),
      "certificates": list_to_str(movie.get("certificates")),
      "languages": list_to_hash(movie.get("languages")),
      "director": list_to_str(movie.get("director")),
      "writer":list_to_str(movie.get("writer")),
      "producer":list_to_str(movie.get("producer")),
      "composer":list_to_str(movie.get("composer")) ,
      "cinematographer":list_to_str(movie.get("cinematographer")),
      "music_team": list_to_str(movie.get("music department")),
      "distributors": list_to_str(movie.get("distributors")),
      'release_date': date,
      'year': movie.get('year'),
      'genres': list_to_hash(movie.get("genres"), emoji=True),
      'poster': movie.get('full-size cover url'),
      'plot': plot,
      'rating': str(movie.get("rating"))+" / 10",
      'url':f'https://www.imdb.com/title/tt{movieid}',
      'url_cast':f'https://www.imdb.com/title/tt{movieid}/fullcredits#cast',
      'url_releaseinfo':f'https://www.imdb.com/title/tt{movieid}/releaseinfo',
  }

    # ... (Implementation using Web Scraping will go here)

def list_to_str(k):
  if not k:
      return ""
  elif len(k) == 1:
      return str(k[0])
  elif LIST_ITEMS:
      k = k[:int(LIST_ITEMS)]
      return ' '.join(f'{elem},' for elem in k)[:-1]+' ...'
  else:
      return ' '.join(f'{elem},' for elem in k)[:-1]

def list_to_hash(k, flagg=False, emoji=False):
  listing = ""
  if not k:
      return ""
  elif len(k) == 1:
      if not flagg:
          if emoji:
              return str(IMDB_GENRE_EMOJI.get(k[0], '')+" #"+k[0].replace(" ", "_").replace("-", "_"))
          return str("#"+k[0].replace(" ", "_").replace("-", "_"))
      try:
          conflag = (conn.get(name=k[0])).flag
          return str(f"{conflag} #" + k[0].replace(" ", "_").replace("-", "_"))
      except AttributeError:
          return str("#"+k[0].replace(" ", "_").replace("-", "_"))
  elif LIST_ITEMS:
      k = k[:int(LIST_ITEMS)]
      for elem in k:
          ele = elem.replace(" ", "_").replace("-", "_")
          if flagg:
              with suppress(AttributeError):
                  conflag = (conn.get(name=elem)).flag
                  listing += f'{conflag} '
          if emoji:
              listing += f"{IMDB_GENRE_EMOJI.get(elem, '')} "
          listing += f'#{ele}, '
      return f'{listing[:-2]}'
  else:
      for elem in k:
          ele = elem.replace(" ", "_").replace("-", "_")
          if flagg:
              conflag = (conn.get(name=elem)).flag
              listing += f'{conflag} '
          listing += f'#{ele}, '
      return listing[:-2]

async def imdb_callback(event: events.CallbackQuery.Event):
    """Handles callbacks starting with 'imdb'."""
    message = event.original_update.message  # The original message
    user_id = event.original_update.user_id
    data = event.data.decode().split()  # Decode data for reliability

    if user_id != int(data[1]):
        await event.answer("Not Yours!", show_alert=True)
        return

    if data[2] == "movie":
        await event.answer()  # Acknowledge callback
        imdb = get_poster(query=data[3], id=True)
        buttons = []
        if imdb['trailer']:
                          if isinstance(imdb['trailer'], list):
                                                              buttons.append([InlineKeyboardButton("▶️ IMDb Trailer ", url=str(imdb['trailer'][-1]))])
                                                              imdb['trailer'] = list_to_str(imdb['trailer']) 
                          else: 
                              buttons.append([InlineKeyboardButton("▶️ IMDb Trailer ", url=str(imdb['trailer']))])
        template = '''
        
⚡𝐓𝐢𝐭𝐥𝐞:  {title}       
⚡𝐈𝐌𝐃𝐁 𝐑𝐚𝐭𝐢𝐧𝐠 : {rating} 
⚡𝐐𝐮𝐚𝐥𝐢𝐭𝐲:  
⚡𝐑𝐞𝐥𝐞𝐚𝐬𝐞 𝐃𝐚𝐭𝐞:  {release_date}
⚡𝐆𝐞𝐧𝐫𝐞: {genres}
⚡️𝐈𝐌𝐃𝐁: {url}
⚡𝐋𝐚𝐧𝐠𝐮𝐚𝐠𝐞:  {languages}
⚡𝐂𝐨𝐮𝐧𝐭𝐫𝐲:  {countries}
⚡𝐒𝐮𝐛𝐭𝐢𝐭𝐥𝐞𝐬: 

⚡𝐒𝐭𝐨𝐫𝐲 𝐋𝐢𝐧𝐞: {plot}

⚡️𝐉𝐨𝐢𝐧 𝐍𝐨𝐰 :
                  '''
        if imdb.get('poster'):
            try:
                await bot.send_photo(chat_id=query.message.reply_to_message.chat.id,  caption=cap, photo=imdb['poster'], reply_to_message_id=query.message.reply_to_message.id, reply_markup=InlineKeyboardMarkup(buttons))
            except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
              poster = imdb.get('poster').replace('.jpg', "._V1_UX360.jpg")
              await sendMessage(message.reply_to_message, cap, InlineKeyboardMarkup(buttons), poster)
        else:
            await sendMessage(message.reply_to_message, cap, InlineKeyboardMarkup(buttons), 'https://telegra.ph/file/5af8d90a479b0d11df298.jpg')
        await message.delete()
app.add_event_handler(imdb_callback, events.CallbackQuery(pattern=b'imdb'))


def main():
    """Start the bot."""
    print("\nBot started ...\n")
    app.run_until_disconnected()

if __name__ == '__main__':
    main()

