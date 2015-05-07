__author__ = 'ads'
from cement.core import foundation, controller, handler
from cement.core.controller import CementBaseController, expose
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    Content = Column(String(5000))
    category_id = Column(Integer, ForeignKey('category.id'),
                         nullable=True)  # When a new post will be created category-id will not be available
    category = relationship(Category)


class BlogBaseController(CementBaseController):
    class Meta:
        label = 'base'
        description = 'This app provides a command-line blog handling facility'
        arguments = [
            (['--base-opt'], dict(help="option under base controller")),
        ]

    @expose(help="This creates the database", hide=True)
    def default(self):
        print "base Default---->>> Creating DATABASE"
        # Create DB here
        engine = create_engine('sqlite:///blogapp.db')
        Base.metadata.create_all(engine)


class PostController(CementBaseController):
    class Meta:
        label = 'post'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'This is post controller'
        arguments = [
            (['--2nd-opt'], dict(help="another option under base controller")),
            (['extra_arguments'], dict(action='store', nargs='*')),
        ]

    @expose(help="Add a new post", hide=True)
    def add(self):
        print "In add post"

        # implement adding a post functionality title and category
        if self.app.pargs.extra_arguments:
            title = self.app.pargs.extra_arguments[0]
            content = self.app.pargs.extra_arguments[1]
        engine = create_engine('sqlite:///blogapp.db')
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()

        new_post = Post(title=title, Content=content)
        session.add(new_post)
        session.commit()
        print "Added Post"

    @expose(help="List all post", hide=False)
    def list(self):
        print "In list all posts"

    # implement listing of all posts
    # with post-id and title

    @expose(help="Search in all posts", hide=True)
    def search(self):
        print "In post Search"


# implement Searching a keyword in all posts

class CategoryController(CementBaseController):
    class Meta:
        label = 'category'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'This is category controller'
        arguments = [
            (['--2nd-opt'], dict(help="yet another option under base controller")),
        ]

    @expose(help="Add a new category", hide=True)
    def add(self):
        print "add a new category"

    # implement adding a category

    @expose(help="List all categories", hide=True)
    def list(self):
        print "list all category"

    #       implement listing a category

    @expose(help="Assigning category to a post", hide=True)
    def assign(self):
        print "Assign a category to post"


# check if post has cat-id,if it has ask user if he wants to change
#       if user confirms do it

def main():
    app = foundation.CementApp('blog')
    try:
        handler.register(BlogBaseController)
        handler.register(PostController)
        handler.register(CategoryController)
        app.setup()
        app.run()
    #        print "HI"
    finally:
        app.close()


if __name__ == '__main__':
    main()