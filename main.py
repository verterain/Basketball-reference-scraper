import argparse
from insertplayer import insert_player

def main():
    parser = argparse.ArgumentParser(description='Insert player into db')
    parser.add_argument('player_name', type=str, help='Name of the player to insert data for')
    args = parser.parse_args()

    insert_player(args.player_name)


if __name__ == '__main__':
    main()