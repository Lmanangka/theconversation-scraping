# theconversation-scraping

A Python program to web scraping articles and podcasts titles from my
favourite website [The Conversation](https://theconversation.com/id).

## Installation

1. Clone the repository:

```sh
git clone https://github.com/Lmanangka/theconversation-scraping.git
```

2. Navigate to the directory:

```sh
cd theconversation-scraping
```

3. Install the requirements:

```sh
pip install -r requirements.txt
```

4. This program use mpv player to open and play selected podcast:

    #### Linux

    - Debian/Ubuntu

    ```sh
    sudo apt install mpv
    ```

    - Fedora

    ```sh
    sudo dnf  install mpv
    ```

    - Arch

    ```sh
    sudo pacman -S mpv
    ```

    - OpenSUSE

    ```sh
    sudo zypper install mpv
    ```

    #### Windows

    - Download the Installation from the official website: https://mpv.io/installation/

## Usage

Run the program by executing the following command:

```sh
python news.py -a
```

To display the podcasts titles, use the following command:

```sh
python news.py -p
```

The program will display a menu with the articles or podcasts titles based on
your choice. You can navigate the menu using the up dan down arrow keys or the
**'j'** and **'k'** keys.  

To select an item from the menu, press **'Enter'** or **'Return'**. If you
selected a podcasts, the program will play the selected podcast using
[mpv](https://mpv.io) player. If you selected an article, the program will open
the article in your default wen browser.

You can also limit the number of items displayed in the menu by using the
**'l'** or **'--limit'** option. For example, to display only 5 items, use the
use the following command:

```sh
python news.py -a -l 5
```

