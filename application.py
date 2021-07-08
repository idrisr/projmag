from projmag.directory import ListCommand
from projmag.directory import DupeCommand
from projmag.directory import NextCommand
from projmag.directory import RenameCommand
from cleo import Application

application = Application()
application.add(ListCommand())
application.add(DupeCommand())
application.add(NextCommand())
application.add(RenameCommand())

if __name__ == '__main__':
    application.run()
