from .plugins.button_build import ButtonMaker
import os
from contextlib import suppress
from re import findall, IGNORECASE
from imdb import Cinemagoer
from pycountry import countries as conn
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty

imdb = Cinemagoer()

IMDB_GENRE_EMOJI = {"Action": "🚀", "Adult": "🔞", "Adventure": "🌋", "Animation": "🎠", "Biography": "📜", "Comedy": "🪗",
                    "Crime": "🔪", "Documentary": "🎞", "Drama": "🎭", "Family": "👨‍👩‍👧‍👦", "Fantasy": "🫧",
                    "Film Noir": "🎯", "Game Show": "🎮", "History": "🏛", "Horror": "🧟", "Musical": "🎻", "Music": "🎸",
                    "Mystery": "🧳", "News": "📰", "Reality-TV": "🖥", "Romance": "🥰", "Sci-Fi": "🌠", "Short": "📝",
                    "Sport": "⛳", "Talk-Show": "👨‍🍳", "Thriller": "🗡", "War": "⚔", "Western": "🪩"}
LIST_ITEMS = 4


async def imdb_search(_, message):
    print("Received message:", message.text)
    if ' ' in message.text:
        k = await message.reply_text('<code>Searching IMDB ...</code>')
        title = message.text.split(' ', 1)[1]
        user_id = message.from_user.id

        buttons = ButtonMaker()

        if title.lower().startswith("https://www.imdb.com/title/tt"):
            movieid = title.replace("https://www.imdb.com/title/tt", "")

            if movie := imdb.get_movie(movieid):
                buttons.ibutton(f"🎬 {movie.get('title')} ({movie.get('year')})", f"imdb {user_id} movie {movieid}")
            else:
                return await k.edit_text("<i>No Results Found</i>")  # Edit if no results

        else:
            movies = get_poster(title, bulk=True)
            if not movies:
                return await k.edit_text("<i>No Results Found</i>, Try Again or Use <b>Title ID</b>")

            for movie in movies:
                buttons.ibutton(f"🎬 {movie.get('title')} ({movie.get('year')})",
                                f"imdb {user_id} movie {movie.movieID}")

            buttons.ibutton("🚫 Close 🚫", f"imdb {user_id} close")
            markup = buttons.build_menu()  # Build the InlineKeyboardMarkup
            await k.edit_text('<b><i>Here What I found on IMDb.com</i></b>', reply_markup=markup)

    else:
        await message.reply_text('<i>Send Movie / TV Series Name along with /imdb Command or send IMDB URL</i>')


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
        "countries": list_to_hash(movie.get("countries"), True),
        "certificates": list_to_str(movie.get("certificates")),
        "languages": list_to_hash(movie.get("languages")),
        "director": list_to_str(movie.get("director")),
        "writer": list_to_str(movie.get("writer")),
        "producer": list_to_str(movie.get("producer")),
        "composer": list_to_str(movie.get("composer")),
        "cinematographer": list_to_str(movie.get("cinematographer")),
        "music_team": list_to_str(movie.get("music department")),
        "distributors": list_to_str(movie.get("distributors")),
        'release_date': date,
        'year': movie.get('year'),
        'genres': list_to_hash(movie.get("genres"), emoji=True),
        'poster': movie.get('full-size cover url'),
        'plot': plot,
        'rating': str(movie.get("rating")) + " / 10",
        'url': f'https://www.imdb.com/title/tt{movieid}',
        'url_cast': f'https://www.imdb.com/title/tt{movieid}/fullcredits#cast',
        'url_releaseinfo': f'https://www.imdb.com/title/tt{movieid}/releaseinfo',
    }


def list_to_str(k):
    if not k:
        return ""
    elif len(k) == 1:
        return str(k[0])
    elif LIST_ITEMS:
        k = k[:int(LIST_ITEMS)]
        return ' '.join(f'{elem},' for elem in k)[:-1] + ' ...'
    else:
        return ' '.join(f'{elem},' for elem in k)[:-1]


def list_to_hash(k, flagg=False, emoji=False):
    listing = ""
    if not k:
        return ""
    elif len(k) == 1:
        if not flagg:
            if emoji:
                return str(IMDB_GENRE_EMOJI.get(k[0], '') + " #" + k[0].replace(" ", "_").replace("-", "_"))
            return str("#" + k[0].replace(" ", "_").replace("-", "_"))
        try:
            conflag = (conn.get(name=k[0])).flag
            return str(f"{conflag} #" + k[0].replace(" ", "_").replace("-", "_"))
        except AttributeError:
            return str("#" + k[0].replace(" ", "_").replace("-", "_"))
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


@Client.on_callback_query(filters.regex(r'^imdb \d+ movie \d+$'))
async def imdb_callback(_, query):
    """Handles callbacks starting with 'imdb'."""
    query.message = query.message  # The original message
    user_id = query.from_user.id
    data = query.data.split()

    if user_id != int(data[1]):
        await query.answer("Not Yours!", show_alert=True)
        return

    if data[2] == "movie":
        await query.answer()  # Acknowledge callback
        imdb = get_poster(query=data[3], id=True)
        buttons = []

        if imdb['trailer']:
            if isinstance(imdb['trailer'], list):
                buttons.append([InlineKeyboardButton("▶️ IMDb Trailer ", url=str(imdb['trailer'][-1]))])
                imdb['trailer'] = list_to_str(imdb['trailer'])
            else:
                buttons.append([InlineKeyboardButton("▶️ IMDb Trailer ", url=str(imdb['trailer']))])

        template = ''' 
⚡𝐓𝐢𝐭𝐥𝐞: {title}    
⚡𝐈𝐌𝐃𝐁 𝐑𝐚𝐭𝐢𝐧𝐠 : {rating} 
⚡𝐐𝐮𝐚𝐥𝐢𝐭𝐲:  
⚡𝐑𝐞𝐥𝐞𝐚𝐬𝐞 𝐃𝐚𝐭𝐞: {release_date}
⚡𝐆𝐞𝐧𝐫𝐞: {genres}
⚡️𝐈𝐌𝐃𝐁: {url}
⚡𝐋𝐚𝐧𝐠𝐮𝐚𝐠𝐞: {languages}
⚡𝐂𝐨𝐮𝐧𝐭𝐫𝐲: {countries}
⚡𝐒𝐮𝐛𝐭𝐢𝐭𝐥𝐞𝐬: 

⚡𝐒𝐭𝐨𝐫𝐲 𝐋𝐢𝐧𝐞: {plot}

⚡️𝐉𝐨𝐢𝐧 𝐍𝐨𝐰 :
        '''

        cap = template.format(**imdb)  # Formatted caption

        if imdb.get('poster'):
            try:
                await query.message.reply_photo(imdb['poster'], caption=cap, reply_markup=InlineKeyboardMarkup(buttons))

            except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
                poster = imdb.get('poster').replace('.jpg', "._V1_UX360.jpg")
                await query.message.reply_photo(poster, caption=cap, reply_markup=InlineKeyboardMarkup(buttons))

        else:
            default_poster = 'https://telegra.ph/file/5af8d90a479b0d11df298.jpg'
            await query.message.reply_photo(default_poster, caption=cap, reply_markup=InlineKeyboardMarkup(buttons))
