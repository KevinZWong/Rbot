import argparse
def main():
    parser = argparse.ArgumentParser(description = "Simple Python script to interact with the TikTok TTS API")
    parser.add_argument("-v", "--voice", help = "the code of the desired voice", nargs = "*", )
    parser.add_argument("-b", "--balls", help = "the code of the desired voice", nargs = "*", )
    args = parser.parse_args()

    #=================
    print("args.voice= ", args.voice)

    #================

if __name__ == "__main__":
    main()

