'''
Author: Leonardo Rudolf Manangka
Created: 16 March 2023
'''
from bs4 import BeautifulSoup
from time import sleep
import requests
import argparse
import sys
import curses
import subprocess
import textwrap
import webbrowser

def user_input():
    parser = argparse.ArgumentParser(prog='news', description='Web scraping\
            articles title and podcasts title from my favourite website\
            The Conversation.', epilog='Example: news.py -a')
    parser.add_argument('-l', '--limit', type=int, default=10,
                        help='Number of items display')
    group_parser = parser.add_mutually_exclusive_group(required=True)
    group_parser.add_argument('-a', '--articles', action='store_true',
                              help='Show articles title and choose one\
                                      to open it.')
    group_parser.add_argument('-p', '--podcasts', action='store_true',
                              help='Show podcasts title and choose one\
                                      to open it.')

    try:
        args = parser.parse_args()
        if args.limit > 20:
            sys.exit('The limit is 20 line.')
    except argparse.ArgumentError as error:
        sys.exit(f"Error: {str(error)}")
    return args

def get_data(limit, articles=False, podcasts=False):
    URLS = {'articles': 'https://theconversation.com/id',
            'podcasts': 'https://theconversation.com/id/podcasts/suarakademia'}
    header = {'user-agent': 'BOT'}
    data = {'title':[], 'link':[]}
    url = URLS['articles'] if articles else URLS['podcasts']

    try:
        page = requests.get(url,headers=header).text
        soup = BeautifulSoup(page, 'html.parser')
    except requests.exceptions.ConnectionError:
        sys.exit('Connection error, please try again.')

    if articles:
        articles = soup.find_all('div', class_='article--header', limit=limit)
        data['title'] = [contents.h2.text.replace(u'\xa0', ' ') for contents in articles]
        data['link'] = [f"https://theconversation.com{contents.h2.a['href']}" for contents in articles]

    elif podcasts:
        podcasts = soup.find_all('div', class_='grid-nine grid-last', limit=limit)
        data['title'] = [contents.h3.text for contents in podcasts]
        data['link'] = [contents.audio.source['src'] for contents in podcasts]

    else:
        sys.exit('Please choose between articles or podcasts!')

    return data

def menu(stdscr, index_pos, data):
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    for index, txt in enumerate(data):
        if index == index_pos:
            stdscr.addnstr(0 + index, 0, '> ' + txt[:width-3], width - 1, curses.A_REVERSE)
            stdscr.addstr(height - 1, 0, 'ctrl-c to exit', curses.A_BLINK)
        else:
            wrapped_txt = textwrap.wrap(txt, width - 2)
            for i, line in enumerate(wrapped_txt):
                stdscr.addstr(0 + index + i, 0, line[:width-3] + '...' if len(line) > width - 3 else line)
    stdscr.refresh()

def main(stdscr):
    try:
        curses.curs_set(0)
        curses.use_default_colors()
        index_pos = 0
        menu(stdscr, index_pos, data['title'])
        while True:
            if curses.is_term_resized(*stdscr.getmaxyx()):
                stdscr.clear()
                menu(stdscr, index_pos, data['title'])
            key = stdscr.getch()
            stdscr.clear()
            if key == curses.KEY_UP or key is ord('k') and index_pos > 0:
                index_pos -= 1
            elif key == curses.KEY_DOWN or key is ord ('j') and index_pos < args.limit - 1:
                index_pos += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                stdscr.clear()
                if args.podcasts:
                    try:
                        curses.endwin()
                        subprocess.call(['mpv', data['link'][index_pos]])
                        stdscr.refresh()
                        menu(stdscr, index_pos, data['title'])
                    except subprocess.CalledProcessError as error:
                        sys.exit(f"Error playing podcasts: {error}")
                else:
                    try:
                        webbrowser.open(data['link'][index_pos], new = 2)
                    except Exception as error:
                        stdscr.addnstr(0, 0, f"Error: {str(error)}")
                        stdscr.refresh()
                        sleep(2)
                stdscr.refresh()
            menu(stdscr, index_pos, data['title'])
            stdscr.refresh()
    except Exception as error:
        stdscr.addnstr(0, 0, str(error))
        stdscr.refresh()
        sleep(2)
    except KeyboardInterrupt:
        sys.exit('EXIT')

if __name__ == "__main__":
    args = user_input()
    data = get_data(args.limit, args.articles, args.podcasts)
    curses.wrapper(main)
