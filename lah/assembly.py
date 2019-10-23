from lah.db import Base

class Assembly(Base):
    __tablename__ = 'assemblies'

    def __str__(self):
        return "{}".format(self.directory)

#-- Assembly
