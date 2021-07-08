from projmag.directory import ListCommand
from projmag.directory import DupeCommand
from projmag.directory import NextCommand
from cleo import Application

application = Application()
application.add(ListCommand())
application.add(DupeCommand())
application.add(NextCommand())

if __name__ == '__main__':
    application.run()
