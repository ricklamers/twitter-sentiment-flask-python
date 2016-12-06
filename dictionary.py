class Dictionary:
    def __init__(self, file):

        self.list = [line.rstrip('\n') for line in open(file)]

        print("Words in list "+ file +": "+str(len(self.list)))

    def check(self, word):

        if word.lower() in self.list:
            return 1
        else:
            return 0
