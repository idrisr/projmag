from projmag.commands import ListCommand
from projmag.commands import DupeCommand
from projmag.commands import NextCommand
from projmag.commands import RenameCommand
from cleo import Application

application = Application()
application.add(ListCommand())
application.add(DupeCommand())
application.add(NextCommand())
application.add(RenameCommand())

if __name__ == '__main__':
    application.run()
