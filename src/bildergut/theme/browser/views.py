# -*- coding: utf-8 -*-
from Products.Five import BrowserView
from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from random import shuffle


class ProjectOverviewView(BrowserView):

    def categories(self, id=None):
        """List all categories in main folder"""
        query = {'portal_type': 'Folder',
                 'sort_on': 'getObjPositionInParent'}
        if id:
            query['id'] = id
        contents = self.context.main.getFolderContents(
            query,
            batch=True,
            b_size=100)
        return contents

    def get_folders_in(self, category):
        """ returns all folders within a category """
        cat_ob = category.getObject()
        contents = cat_ob.getFolderContents(
            {'portal_type': 'Folder',
             'sort_on': 'getObjPositionInParent'},
            batch=True,
            b_size=100)
        return contents

    def prepprojects(self):
        """ collect projects """
        projects = []

        categories = self.categories(id=self.request.get('cat', None))

        for category in categories:
            for folder in self.get_folders_in(category):
                imgs = folder.getObject().getFolderContents(
                    {'portal_type': 'Image',
                     'sort_on': 'getObjPositionInParent'},
                    batch=True, b_size=100)
                imgobs = []
                imgob = None
                for img in imgs:
                    imgob = img.getObject()
                    imgobs.append(imgob)

                if imgob == None:
                    continue

                width, height = imgob.image.getImageSize()
                width = int(160.0 / height * width)
                projects.append(
                    dict(id=folder.getId,
                         title=folder.Title,
                         description=folder.Description,
                         imgs=imgobs,
                         width=width))

        shuffle(projects)
        return projects


class ClientsView(BrowserView):

    def clients(self):
        query = {'portal_type': 'Image',
                 'sort_on': 'getObjPositionInParent'}
        contents = self.context.getFolderContents(
            query,
            batch=True,
            b_size=100)
        return contents


class PhotographersView(BrowserView):

    def photographers(self):
        query = {'portal_type': 'Document',
                 'sort_on': 'getObjPositionInParent'}
        contents = self.context.getFolderContents(
            query,
            batch=True,
            b_size=100)
        return contents


class SubNavViewlet(ViewletBase):
    index = ViewPageTemplateFile('templates/sub-nav.pt')
