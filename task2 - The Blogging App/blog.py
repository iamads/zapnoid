__author__ = 'ads'
from cement.core import foundation, controller, handler
from cement.core.controller import CementBaseController, expose
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class BlogBaseController(CementBaseController):
    class Meta:
        label = 'base'
        description = 'This app provides a command-line blog handling facility'
        arguments = [
            (['--base-opt'], dict(help="option under base controller")),
        ]

    @expose(help="base controller default option", hide=True)
    def default(self):
        print "base Default"


# Create DB here


class PostController(CementBaseController):
    class Meta:
        label = 'post'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'This is post controller'
        arguments = [
            (['--2nd-opt'], dict(help="another option under base controller")),
        ]

    @expose(help="Add a new post", hide=True)
    def add(self):
        print "In add post"

    #       implement adding a post functionality

    @expose(help="List all post", hide=False)
    def list(self):
        print "In list all posts"

    #       implement listing of all posts
    #       with post-id and title

    @expose(help="Search in all posts", hide=True)
    def search(self):
        print "In post Search"


#           implement Searching a keyword in all posts

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

    #       implement adding a category

    @expose(help="List all categories", hide=True)
    def list(self):
        print "list all category"

    #       implement listing a category

    @expose(help="Assigning category to a post", hide=True)
    def assign(self):
        print "Assign a category to post"


#       check if post has cat-id,if it has ask user if he wants to change
#       if user confirms do it

def main():
    app = foundation.CementApp('blog')
    try:
        handler.register(BlogBaseController)
        handler.register(PostController)
        handler.register(CategoryController)
        app.setup()
        app.run()
        print "HI"
    finally:
        app.close()

if __name__ == '__main__':
    main()