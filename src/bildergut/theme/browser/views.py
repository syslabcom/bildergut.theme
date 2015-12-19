# -*- coding: utf-8 -*-
from Products.Five import BrowserView
from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from random import shuffle
from plone import api
from smtplib import SMTPRecipientsRefused


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
                img = None
                for img in imgs:
                    imgobs.append(img)

                if not img:
                    continue

                width, height = img.getObject().image.getImageSize()
                width = int(160.0 / height * width)
                if height == -1:
                    print img.getPath()
                projects.append(
                    dict(id=folder.getId,
                         title=folder.Title,
                         description=folder.Description,
                         imgs=imgobs,
                         width=width))

        shuffle(projects)
        return projects


class ContactsView(BrowserView):

    mailtext = ViewPageTemplateFile("templates/mailtext.pt")
    index = ViewPageTemplateFile("templates/contacts.pt")

    def __call__(self):
        if self.request.REQUEST_METHOD == 'POST':
            try:
                mail_host = api.portal.get_tool(name='MailHost')
                mail_host.send(self.mailtext(request=self.request,
                                             charset='utf-8'),
                               immediate=True)
            except SMTPRecipientsRefused:
                # Don't disclose email address on failure
                raise SMTPRecipientsRefused('Recipient address rejected')
            return self.request.RESPONSE.redirect("feedback")
        else:
            return self.index()


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
