import sqlite3
import requests

# function to parse a single line of the decklist file
def parse_card_line(card_line):
    card_line = card_line.strip()  # remove leading/trailing whitespace
    amount, name = card_line.split('x ', 1)  # split line into amount and name
    return name, int(amount)

# function to add cards to a deck in the database
def add_cards(conn, deck, card_list):
    print(f'{deck}{card_list}')
    x = 0
    cardamount = 0
    cursor = conn.cursor()
    for card_name, card_amount in card_list:
        x = x + 1
        try:
            response = requests.get('https://api.scryfall.com/cards/named', params={'exact': card_name})
            if response.ok:
                card_data = response.json()
                card_image_url = card_data['image_uris']['normal']
                card_type = card_data['type_line']
            if(card_image_url != '' and len(card_image_url) > 0):
                cursor.execute("""
                INSERT INTO cards (name, img, deck, type)
                VALUES (?, ?, ?, ?)
            """, (card_name, card_image_url, deck, card_type))
        except:
            try:
                response = requests.get('https://api.scryfall.com/cards/named', params={'exact': card_name})
                if response.ok:
                    card_data = response.json()
                    card_image_url = card_data['card_faces'][0]['image_uris']['normal']
                    
                    print(card_image_url)
                if(card_image_url != '' and len(card_image_url) > 0):
                    cursor.execute("""
                    INSERT INTO cards (name, img, deck, type)
                    VALUES (?, ?, ?, ?,)
                """, (card_name, card_image_url, deck, card_type))
            except:
                print("idk")
                # cursor.execute("""
                #     INSERT INTO cards (name, deck, type)
                #     VALUES (?, ?, ?)
                # """, (card_name, deck, card_type))
        cardamount += card_amount
        if(x % 10 == 0): print(f'{cardamount} cards imported; last card {card_name}')

    conn.commit()
    print(f'{cardamount} cards imported; last card {card_name}')
    print("Finished")
# function to add a new deck to the database
def add_deck(conn, deck_name):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO decks (name)
        VALUES (?)
    """, (deck_name,))
    deck_id = cursor.lastrowid
    conn.commit()
    return deck_id

# function to import a deck from a file
def import_deck(file_path, deck_name):
    conn = sqlite3.connect('storage.db')
    card_list = []

    # read each line from the file and add the cards to the list
    with open(file_path, 'r') as f:
        for line in f:
            card_name, card_amount = parse_card_line(line)
            card_list.append((card_name, card_amount))

    add_cards(conn, deck_name, card_list)
    cursor = conn.cursor()
    cursor.execute("select * from cards")
    conn.commit()
    conn.close()
deckname = ''
if __name__ == '__main__':
    # deckname = input("Whats your Deckname? ")
    deckname = "Phyrexian"
    if(deckname == '' or len(deckname) == 0):
        print("Invalid deck")
    else:
        import_deck(f'{deckname}.txt', f'{deckname}')
