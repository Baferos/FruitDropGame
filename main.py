from FramesClass import Frames
from GameParameters import width, height


def main():
    # Initialize Frame
    frame = Frames(width, height)
    frame.game_loop()


if __name__ == '__main__':
    main()
